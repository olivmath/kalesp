//! Mensagem para comandos não reconhecidos

use esp_hal::uart::Uart;
use esp_hal::DriverMode;
use heapless::String;
use core::fmt::Write;

/// Envia mensagem para comando não reconhecido
pub fn send_unknown_command_message<D>(uart: &mut Uart<D>, cmd: &str) -> Result<(), core::fmt::Error>
where
    D: DriverMode,
{
    let mut response: String<128> = String::new();
    write!(response, "Comando recebido: '{}'\r\n", cmd)?;
    write!(uart, "{}", response)?;
    write!(uart, "Digite 'help' para ver comandos disponíveis\r\n")?;
    Ok(())
}