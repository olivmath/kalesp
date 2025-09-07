//! Mensagem de ajuda do sistema

use esp_hal::uart::Uart;
use esp_hal::DriverMode;
use core::fmt::Write;

/// Envia a mensagem de ajuda com todos os comandos disponíveis
pub fn send_help_message<D>(uart: &mut Uart<D>) -> Result<(), core::fmt::Error> 
where
    D: DriverMode,
{
    write!(uart, "\r\n=== Comandos Disponíveis ===\r\n")?;
    write!(uart, "help   - Mostra esta ajuda\r\n")?;
    write!(uart, "status - Mostra status do sistema\r\n")?;
    write!(uart, "info   - Informações do dispositivo\r\n")?;
    write!(uart, "ping   - Teste de conectividade\r\n")?;
    write!(uart, "reset  - Reinicia contador\r\n")?;
    write!(uart, "============================\r\n\r\n")?;
    Ok(())
}