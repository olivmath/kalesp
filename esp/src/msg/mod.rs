//! Message module for serial communication
//!
//! This module contains all messages and commands supported
//! by the ESP32 serial communication system.

pub mod help;
pub mod info;
pub mod reset;
pub mod unknown;
pub mod zeros;
pub mod entropy;
pub mod mine;
pub mod hash;

// Re-export main functions
pub use help::send_help_message;
pub use info::send_info_message;
pub use reset::send_reset_message;
pub use unknown::send_unknown_command_message;
pub use zeros::{send_zeros_message, send_zeros_error_message};
pub use entropy::{send_entropy_message, send_entropy_error_message};
pub use mine::{send_mine_start_message, send_mine_result_message, send_mine_error_message, send_mine_progress_message};
pub use hash::{send_hash_message, send_hash_error_message, send_current_hash_message, HashAlgorithm};

/// Enum para representar os diferentes tipos de comando
#[derive(Debug, PartialEq)]
pub enum Command {
    Help,
    Info,
    Reset,
    Zeros(u8),
    Entropy(u8),
    Mine,
    Hash(HashAlgorithm),
    HashInfo,
    Unknown(heapless::String<64>),
}

impl Command {
    /// Parse um comando a partir de uma string
    pub fn from_str(cmd: &str) -> Self {
        let cmd = cmd.trim();
        let parts: heapless::Vec<&str, 3> = cmd.split_whitespace().collect();
        
        if parts.is_empty() {
            return Command::Unknown(heapless::String::new());
        }
        
        let command = parts[0];
        
        if command.eq_ignore_ascii_case("help") {
            Command::Help
        } else if command.eq_ignore_ascii_case("info") {
            Command::Info
        } else if command.eq_ignore_ascii_case("reset") {
            Command::Reset
        } else if command.eq_ignore_ascii_case("zeros") {
            if parts.len() >= 2 {
                if let Ok(value) = parts[1].parse::<u8>() {
                    Command::Zeros(value)
                } else {
                    let mut unknown_cmd = heapless::String::new();
                    let _ = unknown_cmd.push_str(cmd);
                    Command::Unknown(unknown_cmd)
                }
            } else {
                let mut unknown_cmd = heapless::String::new();
                let _ = unknown_cmd.push_str(cmd);
                Command::Unknown(unknown_cmd)
            }
        } else if command.eq_ignore_ascii_case("entropy") {
            if parts.len() >= 2 {
                if let Ok(value) = parts[1].parse::<u8>() {
                    Command::Entropy(value)
                } else {
                    let mut unknown_cmd = heapless::String::new();
                    let _ = unknown_cmd.push_str(cmd);
                    Command::Unknown(unknown_cmd)
                }
            } else {
                let mut unknown_cmd = heapless::String::new();
                let _ = unknown_cmd.push_str(cmd);
                Command::Unknown(unknown_cmd)
            }
        } else if command.eq_ignore_ascii_case("mine") {
            Command::Mine
        } else if command.eq_ignore_ascii_case("hash") {
            if parts.len() >= 2 {
                if let Some(algorithm) = HashAlgorithm::from_str(parts[1]) {
                    Command::Hash(algorithm)
                } else {
                    let mut unknown_cmd = heapless::String::new();
                    let _ = unknown_cmd.push_str(cmd);
                    Command::Unknown(unknown_cmd)
                }
            } else {
                Command::HashInfo
            }
        } else {
            let mut unknown_cmd = heapless::String::new();
            let _ = unknown_cmd.push_str(cmd);
            Command::Unknown(unknown_cmd)
        }
    }
}