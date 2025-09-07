//! Mensagem de confirmação do reset do contador

use esp_hal::uart::Uart;
use esp_hal::DriverMode;
use core::fmt::Write;

/// Envia a mensagem de confirmação do reset do contador
pub fn send_reset_message<D>(uart: &mut Uart<D>) -> Result<(), core::fmt::Error>
where
    D: DriverMode,
{
    write!(uart, "Contador reiniciado!\r\n")?;
    Ok(())
}