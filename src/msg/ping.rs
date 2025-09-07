//! Mensagem de resposta ao comando ping

use esp_hal::uart::Uart;
use esp_hal::DriverMode;
use core::fmt::Write;

/// Envia a resposta ao comando ping
pub fn send_ping_message<D>(uart: &mut Uart<D>) -> Result<(), core::fmt::Error>
where
    D: DriverMode,
{
    write!(uart, "Pong! ESP32 respondendo\r\n")?;
    Ok(())
}