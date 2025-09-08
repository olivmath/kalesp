#![no_std]
#![no_main]
#![deny(
    clippy::mem_forget,
    reason = "mem::forget is generally not safe to do with esp_hal types, especially those \
    holding buffers for the duration of a data transfer."
)]

use esp_hal::clock::CpuClock;
use esp_hal::gpio::{Level, Output, OutputConfig};
use esp_hal::main;
use esp_hal::time::{Duration, Instant};
use esp_hal::uart::{Config, Uart};
use rtt_target::rprintln;
use heapless::String;
use core::fmt::Write;
use kalesp::msg::{
    Command, send_help_message, send_info_message, 
    send_reset_message, send_unknown_command_message,
    send_zeros_message, send_entropy_message, send_mine_start_message,
    send_mine_result_message, send_mine_error_message, send_hash_message,
    send_current_hash_message
};
use kalesp::mining::{MiningState, MinerFactory};

#[panic_handler]
fn panic(_: &core::panic::PanicInfo) -> ! {
    loop {}
}

// This creates a default app-descriptor required by the esp-idf bootloader.
esp_bootloader_esp_idf::esp_app_desc!();

#[main]
fn main() -> ! {
    rtt_target::rtt_init_print!();

    let config = esp_hal::Config::default().with_cpu_clock(CpuClock::max());
    let peripherals = esp_hal::init(config);

    // Configurar LED para indicar atividade
    let mut led = Output::new(peripherals.GPIO2, Level::Low, OutputConfig::default());

    // Configure UART0 (uses ESP32 default pins: TX=GPIO1, RX=GPIO3)
    let uart_config = Config::default();
    let mut uart = Uart::new(peripherals.UART0, uart_config).unwrap();

    rprintln!("Iniciando comunicação serial simples!");
    write!(uart, "ESP32 Serial Comunicação iniciada!\r\n").ok();
    write!(uart, "Digite 'help' para ver comandos disponíveis\r\n").ok();
    

    let mut last_led_toggle = Instant::now();
    let mut buffer: String<128> = String::new();
    
    // Mining state
    let mut mining_state = MiningState::new();
    let mut current_miner = MinerFactory::create_miner_for_algorithm(mining_state.get_hash_algorithm());

    loop {
        // Blink LED every 500ms to indicate it's working
        if last_led_toggle.elapsed() >= Duration::from_millis(500) {
            led.toggle();
            last_led_toggle = Instant::now();
        }

        // Ler dados recebidos via UART
        let mut temp_buffer = [0u8; 32];
        if let Ok(bytes_read) = uart.read(&mut temp_buffer) {
            if bytes_read > 0 {
                for &byte in &temp_buffer[..bytes_read] {
                    if byte == b'\n' || byte == b'\r' {
                        // Processar comando completo
                        if !buffer.is_empty() {
                            let cmd_str = buffer.as_str().trim();
                            let command = Command::from_str(cmd_str);
                            
                            match command {
                                Command::Help => {
                                    send_help_message(&mut uart).ok();
                                }
                                Command::Info => {
                                    send_info_message(&mut uart, &mining_state).ok();
                                }
                                Command::Reset => {
                                    send_reset_message(&mut uart, &mut mining_state).ok();
                                }
                                Command::Zeros(zeros) => {
                                    mining_state.set_zeros(zeros);
                                    send_zeros_message(&mut uart, zeros).ok();
                                    rprintln!("Zeros configurado: {}", zeros);
                                }
                                Command::Entropy(entropy) => {
                                    mining_state.set_entropy(entropy);
                                    send_entropy_message(&mut uart, entropy).ok();
                                    rprintln!("Entropy configurado: {}", entropy);
                                }
                                Command::Mine => {
                                    if mining_state.is_ready_to_mine() {
                                        send_mine_start_message(&mut uart, mining_state.zeros, mining_state.entropy).ok();
                                        rprintln!("Iniciando mineração com {}...", mining_state.get_hash_algorithm().as_str());
                                        
                                        // Atualizar o estado do minerador atual
                                        current_miner.update_state(mining_state);
                                        
                                        match current_miner.mine(&mut uart, &mut led) {
                                            Ok(nonce) => {
                                                mining_state.set_last_nonce(nonce);
                                                send_mine_result_message(&mut uart, nonce).ok();
                                                rprintln!("Mineração concluída! Nonce: {}", nonce);
                                            }
                                            Err(_) => {
                                                send_mine_error_message(&mut uart, "Erro durante mineração").ok();
                                                rprintln!("Erro na mineração");
                                            }
                                        }
                                    } else {
                                        send_mine_error_message(&mut uart, "Configure zeros e entropy primeiro").ok();
                                        rprintln!("Mineração não configurada");
                                    }
                                }
                                Command::Hash(algorithm) => {
                                    mining_state.set_hash_algorithm(algorithm);
                                    current_miner = MinerFactory::create_miner_for_algorithm(algorithm);
                                    send_hash_message(&mut uart, algorithm).ok();
                                    rprintln!("Algoritmo alterado para: {}", algorithm.as_str());
                                }
                                Command::HashInfo => {
                                    send_current_hash_message(&mut uart, mining_state.get_hash_algorithm()).ok();
                                    rprintln!("Algoritmo atual: {}", mining_state.get_hash_algorithm().as_str());
                                }
                                Command::Unknown(_) => {
                                    send_unknown_command_message(&mut uart, cmd_str).ok();
                                }
                            }
                            
                            rprintln!("Comando processado: {}", cmd_str);
                            buffer.clear();
                        }
                    } else if byte >= 32 && byte <= 126 { // Printable characters
                        if buffer.push(byte as char).is_err() {
                            // Buffer cheio, limpar e continuar
                            buffer.clear();
                        }
                    }
                }
            }
        }



        // Small delay to not overload the system
        let delay_start = Instant::now();
        while delay_start.elapsed() < Duration::from_millis(50) {}
    }
}