//! Módulo para mensagens do comando zeros


use core::fmt::Write;

/// Envia mensagem de confirmação para o comando zeros
pub fn send_zeros_message<W>(uart: &mut W, zeros: u8) -> Result<(), core::fmt::Error>
where
    W: Write,
{
    write!(uart, "ZEROS: {} zeros configurados para mineração\r\n", zeros)
}

/// Envia mensagem de erro para comando zeros inválido
pub fn send_zeros_error_message<W>(uart: &mut W, error: &str) -> Result<(), core::fmt::Error>
where
    W: Write,
{
    write!(uart, "ZEROS_ERROR: {}\r\n", error)
}