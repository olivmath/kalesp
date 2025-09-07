//! Módulo para mensagens do comando entropy


use core::fmt::Write;

/// Envia mensagem de confirmação para o comando entropy
pub fn send_entropy_message<W>(uart: &mut W, entropy: u8) -> Result<(), core::fmt::Error>
where
    W: Write,
{
    write!(uart, "ENTROPY: {} configurado para mineração\r\n", entropy)
}

/// Envia mensagem de erro para comando entropy inválido
pub fn send_entropy_error_message<W>(uart: &mut W, error: &str) -> Result<(), core::fmt::Error>
where
    W: Write,
{
    write!(uart, "ENTROPY_ERROR: {}\r\n", error)
}