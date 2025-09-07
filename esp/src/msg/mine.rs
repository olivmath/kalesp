//! Módulo para mensagens do comando mine


use core::fmt::Write;

/// Envia mensagem de início da mineração
pub fn send_mine_start_message<W>(uart: &mut W, zeros: u8, entropy: u8) -> Result<(), core::fmt::Error>
where
    W: Write,
{
    write!(uart, "MINE_START: Iniciando mineração com {} zeros e entropy {}\r\n", zeros, entropy)
}

/// Envia mensagem de resultado da mineração
pub fn send_mine_result_message<W>(uart: &mut W, nonce: u32) -> Result<(), core::fmt::Error>
where
    W: Write,
{
    write!(uart, "MINE_RESULT: Nonce encontrado: {}\r\n", nonce)
}

/// Envia mensagem de erro para comando mine
pub fn send_mine_error_message<W>(uart: &mut W, error: &str) -> Result<(), core::fmt::Error>
where
    W: Write,
{
    write!(uart, "MINE_ERROR: {}\r\n", error)
}

/// Envia mensagem de progresso da mineração
pub fn send_mine_progress_message<W>(uart: &mut W, nonce: u32, entropy: u8) -> Result<(), core::fmt::Error>
where
    W: Write,
{
    write!(uart, "MINE_PROGRESS: nonce={}, entropy={}\r\n", nonce, entropy)
}