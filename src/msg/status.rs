//! Mensagem de status do sistema

use esp_hal::uart::Uart;
use esp_hal::DriverMode;
use heapless::String;
use core::fmt::Write;

/// Envia a mensagem de status do sistema com o contador atual
pub fn send_status_message<D>(uart: &mut Uart<D>, counter: u32) -> Result<(), core::fmt::Error>
where
    D: DriverMode,
{
    let mut message: String<64> = String::new();
    write!(message, "[Status] Sistema ativo - Uptime: {} ciclos\r\n", counter)?;
    write!(uart, "{}", message)?;
    Ok(())
}