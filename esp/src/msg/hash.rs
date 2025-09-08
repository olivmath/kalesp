//! Módulo para comando de seleção de algoritmo de hash

use core::fmt::Write;

/// Enum para representar os algoritmos de hash disponíveis
#[derive(Debug, Clone, Copy, PartialEq)]
pub enum HashAlgorithm {
    Sha256,
    Keccak256,
}

impl HashAlgorithm {
    /// Parse um algoritmo a partir de uma string
    pub fn from_str(s: &str) -> Option<Self> {
        // Comparação case-insensitive manual para no_std
        if s.eq_ignore_ascii_case("sha256") {
            Some(HashAlgorithm::Sha256)
        } else if s.eq_ignore_ascii_case("keccak256") || s.eq_ignore_ascii_case("keccak") {
            Some(HashAlgorithm::Keccak256)
        } else {
            None
        }
    }
    
    /// Converte o algoritmo para string
    pub fn as_str(&self) -> &'static str {
        match self {
            HashAlgorithm::Sha256 => "SHA256",
            HashAlgorithm::Keccak256 => "Keccak-256",
        }
    }
}

/// Envia mensagem de confirmação de mudança de algoritmo de hash
pub fn send_hash_message<W: Write>(uart: &mut W, algorithm: HashAlgorithm) -> Result<(), core::fmt::Error> {
    write!(uart, "[HASH] Algoritmo alterado para: {}\r\n", algorithm.as_str())
}

/// Envia mensagem de erro para comando hash inválido
pub fn send_hash_error_message<W: Write>(uart: &mut W, error: &str) -> Result<(), core::fmt::Error> {
    write!(uart, "[HASH_ERROR] {}\r\n", error)
}

/// Envia mensagem com algoritmo atual
pub fn send_current_hash_message<W: Write>(uart: &mut W, algorithm: HashAlgorithm) -> Result<(), core::fmt::Error> {
    write!(uart, "[HASH_INFO] Algoritmo atual: {}\r\n", algorithm.as_str())
}