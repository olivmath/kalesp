//! Mensagem de informações do dispositivo

use esp_hal::uart::Uart;
use esp_hal::DriverMode;
use core::fmt::Write;

/// Envia as informações detalhadas do dispositivo ESP32
pub fn send_info_message<D>(uart: &mut Uart<D>) -> Result<(), core::fmt::Error>
where
    D: DriverMode,
{
    write!(uart, "\r\n=== Informações do ESP32 ===\r\n")?;
    write!(uart, "Dispositivo: ESP32\r\n")?;
    write!(uart, "Firmware: Serial Echo v1.0\r\n")?;
    write!(uart, "UART: 115200 baud\r\n")?;
    write!(uart, "Pinos: TX=GPIO1, RX=GPIO3\r\n")?;
    write!(uart, "============================\r\n\r\n")?;
    Ok(())
}