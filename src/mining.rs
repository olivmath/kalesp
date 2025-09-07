//! Módulo de mineração para o sistema Kale ESP
//!
//! Este módulo implementa a funcionalidade de mineração seguindo os princípios KISS e SOLID:
//! - Single Responsibility: Cada struct/função tem uma responsabilidade específica
//! - Open/Closed: Extensível para novos algoritmos de hash
//! - Liskov Substitution: Interfaces bem definidas
//! - Interface Segregation: Interfaces pequenas e específicas
//! - Dependency Inversion: Depende de abstrações, não implementações

use sha2::{Digest, Sha256};

use core::fmt::Write;

/// Estado da mineração - armazena configurações atuais
#[derive(Debug, Clone, Copy)]
pub struct MiningState {
    pub zeros: u8,
    pub entropy: u8,
    pub is_configured: bool,
    pub last_nonce: Option<u32>,
}

impl Default for MiningState {
    fn default() -> Self {
        Self {
            zeros: 0,
            entropy: 0,
            is_configured: false,
            last_nonce: None,
        }
    }
}

impl MiningState {
    /// Cria um novo estado de mineração
    pub fn new() -> Self {
        Self::default()
    }
    
    /// Define o número de zeros necessários
    pub fn set_zeros(&mut self, zeros: u8) {
        self.zeros = zeros;
        self.update_configuration_status();
    }
    
    /// Define o valor de entropy
    pub fn set_entropy(&mut self, entropy: u8) {
        self.entropy = entropy;
        self.update_configuration_status();
    }
    
    /// Verifica se a mineração está configurada (zeros e entropy definidos)
    fn update_configuration_status(&mut self) {
        self.is_configured = self.zeros > 0 && self.entropy > 0;
    }
    
    /// Verifica se está pronto para minerar
    pub fn is_ready_to_mine(&self) -> bool {
        self.is_configured
    }
    
    /// Define o último nonce encontrado
    pub fn set_last_nonce(&mut self, nonce: u32) {
        self.last_nonce = Some(nonce);
    }
}

/// Trait para operações de hash - permite extensibilidade
pub trait Hasher {
    fn hash(&self, data: u8, nonce: u32) -> [u8; 32];
}

/// Implementação SHA256 do hasher
pub struct Sha256Hasher;

impl Hasher for Sha256Hasher {
    fn hash(&self, data: u8, nonce: u32) -> [u8; 32] {
        let mut hasher = Sha256::new();
        hasher.update(data.to_be_bytes());
        hasher.update(&nonce.to_le_bytes());
        hasher.finalize().into()
    }
}

/// Verificador de zeros - responsabilidade única
pub struct ZeroChecker;

impl ZeroChecker {
    /// Verifica se o hash tem o número necessário de zeros no início
    pub fn check_zeros(hash: &[u8; 32], required_zeros: u8) -> bool {
        // Verifica bytes completos (como no exemplo funcional)
        let zeros_to_check = required_zeros as usize;
        if zeros_to_check > hash.len() {
            return false;
        }
        
        hash[..zeros_to_check].iter().all(|&byte| byte == 0u8)
    }
}

/// Minerador - orquestra o processo de mineração
pub struct Miner<H: Hasher> {
    hasher: H,
    state: MiningState,
}

impl<H: Hasher> Miner<H> {
    /// Cria um novo minerador
    pub fn new(hasher: H) -> Self {
        Self {
            hasher,
            state: MiningState::new(),
        }
    }
    
    /// Atualiza o estado de mineração
    pub fn update_state(&mut self, state: MiningState) {
        self.state = state;
    }
    
    /// Executa a mineração
    pub fn mine<W, L>(&self, uart: &mut W, led: &mut L) -> Result<u32, MiningError>
    where
        W: Write,
        L: embedded_hal::digital::StatefulOutputPin,
    {
        if !self.state.is_ready_to_mine() {
            return Err(MiningError::NotConfigured);
        }
        
        let mut nonce = 0u32;
        let ping_interval = 50000u32;
        let led_toggle_interval = 10000u32; // Piscar LED a cada 10k iterações
        
        loop {
            let hash = self.hasher.hash(self.state.entropy, nonce);
            
            // Piscar LED durante mineração
            if nonce % led_toggle_interval == 0 {
                led.toggle().ok();
            }
            
            // Enviar ping periodicamente
            if nonce % ping_interval == 0 {
                let _ = write!(uart, "MINING: nonce={}, entropy={}\r\n", nonce, self.state.entropy);
            }
            
            if ZeroChecker::check_zeros(&hash, self.state.zeros) {
                let _ = write!(uart, "FOUND: nonce={}, hash={:02x?}\r\n", nonce, &hash[..8]);
                return Ok(nonce);
            }
            
            nonce = nonce.wrapping_add(1);
            
            // Proteção contra overflow infinito
            if nonce == 0 {
                return Err(MiningError::Overflow);
            }
        }
    }
}

/// Erros de mineração
#[derive(Debug, PartialEq)]
pub enum MiningError {
    NotConfigured,
    Overflow,
}

/// Factory para criar mineradores - facilita testes e extensibilidade
pub struct MinerFactory;

impl MinerFactory {
    /// Cria um minerador SHA256
    pub fn create_sha256_miner() -> Miner<Sha256Hasher> {
        Miner::new(Sha256Hasher)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_mining_state_configuration() {
        let mut state = MiningState::new();
        assert!(!state.is_ready_to_mine());
        
        state.set_zeros(2);
        assert!(!state.is_ready_to_mine());
        
        state.set_entropy(1);
        assert!(state.is_ready_to_mine());
    }
    
    #[test]
    fn test_zero_checker() {
        let hash_with_zeros = [0, 0, 0x80, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
        assert!(ZeroChecker::check_zeros(&hash_with_zeros, 16)); // 2 bytes = 16 bits
        assert!(!ZeroChecker::check_zeros(&hash_with_zeros, 17)); // Falha no 17º bit
    }
}