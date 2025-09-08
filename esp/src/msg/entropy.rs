//! Module for entropy command messages


use core::fmt::Write;

/// Sends confirmation message for entropy command
pub fn send_entropy_message<W>(uart: &mut W, entropy: u8) -> Result<(), core::fmt::Error>
where
    W: Write,
{
    write!(uart, "ENTROPY: {} configurado para mineração\r\n", entropy)
}

/// Sends error message for invalid entropy command
pub fn send_entropy_error_message<W>(uart: &mut W, error: &str) -> Result<(), core::fmt::Error>
where
    W: Write,
{
    write!(uart, "ENTROPY_ERROR: {}\r\n", error)
}