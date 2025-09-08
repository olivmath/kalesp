# Contribuindo para o KALESP

🎉 Obrigado por considerar contribuir para o KALESP! Este projeto é parte do ecossistema KALE e visa democratizar a mineração através de dispositivos ESP32.

## 📋 Índice

- [Código de Conduta](#código-de-conduta)
- [Como Posso Contribuir?](#como-posso-contribuir)
- [Configuração do Ambiente](#configuração-do-ambiente)
- [Processo de Desenvolvimento](#processo-de-desenvolvimento)
- [Padrões de Código](#padrões-de-código)
- [Testes](#testes)
- [Documentação](#documentação)

## 📜 Código de Conduta

Este projeto adere aos princípios de **Proof-of-Teamwork** do ecossistema KALE. Esperamos que todos os participantes:

- 🤝 Sejam respeitosos e inclusivos
- 🌱 Foquem na colaboração e crescimento mútuo
- 🔧 Priorizem soluções técnicas sólidas
- 🌍 Mantenham a visão de descentralização e acessibilidade

## 🚀 Como Posso Contribuir?

### 🐛 Reportando Bugs

Antes de reportar um bug:
1. Verifique se já não existe uma issue similar
2. Teste com a versão mais recente
3. Colete informações do sistema (OS, versão Python, modelo ESP32)

**Template para Bug Report:**
```markdown
**Descrição do Bug**
Descrição clara e concisa do problema.

**Passos para Reproduzir**
1. Vá para '...'
2. Clique em '...'
3. Execute '...'
4. Veja o erro

**Comportamento Esperado**
O que deveria acontecer.

**Screenshots/Logs**
Se aplicável, adicione screenshots ou logs.

**Ambiente:**
- OS: [e.g. macOS 14.0]
- Python: [e.g. 3.11.0]
- ESP32: [e.g. DevKit v1]
- Versão KALESP: [e.g. 0.1.0]
```

### 💡 Sugerindo Melhorias

**Template para Feature Request:**
```markdown
**Problema Relacionado**
Descreva o problema que esta feature resolveria.

**Solução Proposta**
Descreva a solução que você gostaria de ver.

**Alternativas Consideradas**
Descreva alternativas que você considerou.

**Contexto Adicional**
Qualquer outro contexto sobre a feature.
```

### 🔧 Contribuindo com Código

Áreas onde contribuições são especialmente bem-vindas:

#### ESP32 Firmware (Rust)
- Otimizações de algoritmos de hash
- Melhorias no protocolo de comunicação serial
- Implementações de novos comandos
- Otimizações de performance e memória

#### Interface Python
- Melhorias na GUI com Flet
- Novos recursos de monitoramento
- Integração com APIs externas
- Testes automatizados

#### Integração KALE
- Implementação do protocolo Stellar
- Integração com smart contracts KALE
- Sistema de orquestração de transações
- Rede distribuída de ESP32s

## 🛠️ Configuração do Ambiente

### Pré-requisitos
```bash
# Rust e ferramentas ESP32
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
cargo install espup
espup install
source $HOME/export-esp.sh
cargo install espflash

# Python e dependências
python3 -m pip install --upgrade pip
cd interface
pip install -r requirements.txt
```

### Fork e Clone
```bash
# Fork o repositório no GitHub
# Clone seu fork
git clone https://github.com/SEU_USERNAME/kalesp.git
cd kalesp

# Adicione o repositório original como upstream
git remote add upstream https://github.com/ORIGINAL_OWNER/kalesp.git
```

## 🔄 Processo de Desenvolvimento

### 1. Crie uma Branch
```bash
git checkout -b feature/nome-da-feature
# ou
git checkout -b fix/nome-do-bug
# ou
git checkout -b docs/melhoria-documentacao
```

### 2. Faça suas Mudanças
- Mantenha commits pequenos e focados
- Use mensagens de commit descritivas
- Teste suas mudanças localmente

### 3. Teste
```bash
# Teste o firmware ESP32
cd esp
cargo check
cargo build --release

# Teste a interface Python
cd ../interface
python -m pytest  # se houver testes
python esp32_gui.py  # teste manual
```

### 4. Commit e Push
```bash
git add .
git commit -m "feat: adiciona nova funcionalidade X"
git push origin feature/nome-da-feature
```

### 5. Abra um Pull Request
- Use o template de PR
- Descreva claramente as mudanças
- Referencie issues relacionadas
- Aguarde review e feedback

## 📝 Padrões de Código

### Rust (ESP32)
```rust
// Use snake_case para funções e variáveis
fn calculate_hash_rate() -> u32 {
    // Código aqui
}

// Use PascalCase para structs e enums
struct MiningConfig {
    difficulty: u8,
    algorithm: HashAlgorithm,
}

// Documente funções públicas
/// Calcula o hash Keccak-256 dos dados fornecidos
/// 
/// # Arguments
/// * `data` - Os dados para fazer hash
/// 
/// # Returns
/// * `[u8; 32]` - O hash resultante
pub fn keccak256(data: &[u8]) -> [u8; 32] {
    // Implementação
}
```

### Python (Interface)
```python
# Use snake_case para funções e variáveis
def connect_to_esp32(port: str) -> bool:
    """Conecta à porta serial do ESP32.
    
    Args:
        port: Caminho da porta serial (e.g., '/dev/ttyUSB0')
        
    Returns:
        True se conectado com sucesso, False caso contrário
    """
    pass

# Use PascalCase para classes
class ESP32Manager:
    """Gerencia comunicação com dispositivos ESP32."""
    
    def __init__(self, port: str, baudrate: int = 115200):
        self.port = port
        self.baudrate = baudrate
```

### Mensagens de Commit
Use o padrão [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: adiciona suporte a algoritmo Keccak-256
fix: corrige bug na comunicação serial
docs: atualiza README com instruções de instalação
style: formata código Rust com rustfmt
refactor: reorganiza estrutura de módulos
test: adiciona testes para função de hash
chore: atualiza dependências do Cargo.toml
```

## 🧪 Testes

### Testes Unitários (Rust)
```bash
cd esp
cargo test
```

### Testes de Integração (Python)
```bash
cd interface
python -m pytest tests/
```

### Testes Manuais
1. Compile e flash o firmware no ESP32
2. Execute a interface Python
3. Teste todos os comandos disponíveis
4. Verifique logs e comportamento esperado

## 📚 Documentação

### Atualizando Documentação
- **README.md**: Instruções gerais e overview
- **ROADMAP.md**: Planos futuros e integração KALE
- **LORE.md**: Contexto narrativo do projeto
- **Código**: Documente funções públicas e módulos

### Padrões de Documentação
- Use Markdown para documentos
- Inclua exemplos de código quando relevante
- Mantenha linguagem clara e acessível
- Atualize CHANGELOG.md para mudanças significativas

## 🎯 Áreas Prioritárias

### Alta Prioridade
1. **Otimização Keccak-256** para ESP32
2. **Protocolo de comunicação** robusto
3. **Integração Stellar** básica
4. **Testes automatizados** abrangentes

### Média Prioridade
1. **Interface gráfica** melhorada
2. **Sistema de logs** avançado
3. **Documentação** técnica detalhada
4. **Performance** benchmarks

### Baixa Prioridade
1. **Recursos experimentais**
2. **Integrações opcionais**
3. **Melhorias cosméticas**

## 🤔 Dúvidas?

Se você tem dúvidas sobre como contribuir:

1. 📖 Leia a documentação existente
2. 🔍 Procure por issues similares
3. 💬 Abra uma issue para discussão
4. 📧 Entre em contato com os mantenedores

---

**Lembre-se**: Toda contribuição, por menor que seja, é valiosa! Desde correções de typos até implementações de features complexas, tudo ajuda a fortalecer o espírito de **Proof-of-Teamwork** do KALESP.

🚀 **Vamos construir o futuro da mineração descentralizada juntos!**