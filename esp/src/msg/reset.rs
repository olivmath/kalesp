//! Mensagem de confirmação do reset do contador

use esp_hal::uart::Uart;
use esp_hal::DriverMode;
use core::fmt::Write;

use crate::mining::MiningState;


/// Envia a mensagem de confirmação do reset do contador
pub fn send_reset_message<D>(uart: &mut Uart<D>, mining_state: &mut MiningState) -> Result<(), core::fmt::Error>
where
    D: DriverMode,
{
    // Reset do estado de mineração usando o método específico
    mining_state.reset();
    
    writeln!(uart, "=== Reset Executado ===")?;
    writeln!(uart, "Estado de mineração reiniciado:")?;
    writeln!(uart, "Zeros: {}", mining_state.zeros)?;
    writeln!(uart, "Entropy: {}", mining_state.entropy)?;
    writeln!(uart, "Configurado: {}", mining_state.is_configured)?;
    match mining_state.last_nonce {
        Some(nonce) => writeln!(uart, "Último nonce: {}", nonce)?,
        None => writeln!(uart, "Último nonce: Nenhum")?,
    }
    write!(uart, "Reset concluído com sucesso!\r\n")?;
    Ok(())
}