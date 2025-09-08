//! Module for zeros command messages


use core::fmt::Write;

/// Sends confirmation message for zeros command
pub fn send_zeros_message<W>(uart: &mut W, zeros: u8) -> Result<(), core::fmt::Error>
where
    W: Write,
{
    write!(uart, "ZEROS: {} zeros configurados para mineração\r\n", zeros)
}

/// Sends error message for invalid zeros command
pub fn send_zeros_error_message<W>(uart: &mut W, error: &str) -> Result<(), core::fmt::Error>
where
    W: Write,
{
    write!(uart, "ZEROS_ERROR: {}\r\n", error)
}