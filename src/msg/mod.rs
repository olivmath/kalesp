//! Módulo de mensagens para comunicação serial
//! 
//! Este módulo contém todas as mensagens e comandos suportados
//! pelo sistema de comunicação serial do ESP32.

pub mod help;
pub mod status;
pub mod info;
pub mod ping;
pub mod reset;
pub mod unknown;

// Re-exportar as funções principais
pub use help::send_help_message;
pub use status::send_status_message;
pub use info::send_info_message;
pub use ping::send_ping_message;
pub use reset::send_reset_message;
pub use unknown::send_unknown_command_message;

/// Enum para representar os diferentes tipos de comando
#[derive(Debug, PartialEq)]
pub enum Command {
    Help,
    Status,
    Info,
    Ping,
    Reset,
    Unknown(heapless::String<64>),
}

impl Command {
    /// Parse um comando a partir de uma string
    pub fn from_str(cmd: &str) -> Self {
        let cmd = cmd.trim();
        
        if cmd.eq_ignore_ascii_case("help") {
            Command::Help
        } else if cmd.eq_ignore_ascii_case("status") {
            Command::Status
        } else if cmd.eq_ignore_ascii_case("info") {
            Command::Info
        } else if cmd.eq_ignore_ascii_case("ping") {
            Command::Ping
        } else if cmd.eq_ignore_ascii_case("reset") {
            Command::Reset
        } else {
            let mut unknown_cmd = heapless::String::new();
            let _ = unknown_cmd.push_str(cmd);
            Command::Unknown(unknown_cmd)
        }
    }
}