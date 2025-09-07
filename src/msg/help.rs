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
    write!(uart, "help     - Mostra esta ajuda\r\n")?;
    write!(uart, "info     - Informações do dispositivo\r\n")?;
    write!(uart, "reset    - Reinicia contador\r\n")?;
    write!(uart, "\r\n=== Comandos de Mineração ===\r\n")?;
    write!(uart, "zeros N  - Define número de zeros (ex: zeros 8)\r\n")?;
    write!(uart, "entropy N- Define entropy (ex: entropy 5)\r\n")?;
    write!(uart, "mine     - Inicia mineração\r\n")?;
    write!(uart, "============================\r\n\r\n")?;
    Ok(())
}