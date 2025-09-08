//! Mensagem de informações do dispositivo

use esp_hal::uart::Uart;
use esp_hal::DriverMode;
use core::fmt::Write;

use crate::mining::MiningState;

/// Envia mensagem de informações do dispositivo e estado de mineração
pub fn send_info_message<D>(uart: &mut Uart<D>, mining_state: &MiningState) -> Result<(), core::fmt::Error>
where
    D: DriverMode,
{
    writeln!(uart, "=== Informações do ESP32 ===")?;
    writeln!(uart, "Dispositivo: ESP32")?;
    writeln!(uart, "Firmware: Serial Echo v1.0")?;
    writeln!(uart, "UART: 115200 baud")?;
    writeln!(uart, "Pinos: TX=GPIO1, RX=GPIO3")?;
    writeln!(uart, "=== Estado de Mineração ===")?;
    writeln!(uart, "Algoritmo: {}", mining_state.get_hash_algorithm().as_str())?;
    writeln!(uart, "Zeros: {}", mining_state.zeros)?;
    writeln!(uart, "Entropy: {}", mining_state.entropy)?;
    match mining_state.last_nonce {
        Some(nonce) => writeln!(uart, "Último nonce: {}", nonce)?,
        None => writeln!(uart, "Último nonce: -1")?,
    }
    writeln!(uart, "============================")?;
    Ok(())
}