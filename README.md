# KALESP - ESP32 Mining Development Platform

🚀 **KALESP** é uma plataforma de desenvolvimento para mineração usando ESP32 com interface Python para comunicação serial. Este projeto serve como base para futuras integrações com o ecossistema KALE blockchain.

## 📋 Visão Geral

O projeto é composto por dois componentes principais:

### 🔧 **ESP32 Firmware (Rust)**
- Implementação de algoritmos de hash (SHA-256, Keccak-256)
- Comunicação serial otimizada
- Comandos de mineração e configuração
- Suporte a diferentes níveis de dificuldade

### 🖥️ **Interface Python**
- **GUI moderna** com Flet para controle visual
- **Comunicação serial** robusta com o ESP32
- **Monitoramento em tempo real** de hashrate e status
- **Comandos disponíveis**: help, info, reset, mine, zeros, entropy, hash

## 🎯 Funcionalidades Atuais

- ✅ Comunicação serial bidirecional ESP32 ↔ Python
- ✅ Interface gráfica intuitiva estilo terminal
- ✅ Algoritmos de hash SHA-256 e Keccak-256
- ✅ Configuração de dificuldade (zeros prefixados)
- ✅ Monitoramento de performance em tempo real
- ✅ Sistema de logs estruturado
- ✅ Auto-detecção de portas seriais

## 🛠️ Pré-requisitos

### Sistema Operacional
- macOS, Linux ou Windows
- Python 3.8+ instalado
- Rust instalado via [rustup](https://rustup.rs/)

### Hardware
- **ESP32 DevKit** (qualquer variante)
- **Cabo USB** para conexão
- **Porta serial** disponível

## 🚀 Instalação

### 1. Configuração do Ambiente ESP32

#### Instalar ferramentas ESP32
```bash
# Instalar espup (gerenciador de toolchain ESP32)
cargo install espup
espup install

# Configurar variáveis de ambiente
source $HOME/export-esp.sh
```

#### Instalar espflash para upload do firmware
```bash
cargo install espflash
```

### 2. Configuração do Ambiente Python

```bash
# Navegar para o diretório do projeto
cd /caminho/para/kalesp

# Instalar dependências Python
cd interface
pip install -r requirements.txt
```

### 3. Compilar e Fazer Upload do Firmware

```bash
# Navegar para o diretório ESP32
cd esp

# Compilar o firmware
cargo build --release

# Fazer upload para o ESP32 (substitua /dev/ttyUSB0 pela sua porta)
espflash flash --monitor target/xtensa-esp32-espidf/release/kalesp
```

## 🎮 Como Usar

### Interface Gráfica (Recomendado)

1. **Iniciar a GUI**:
```bash
cd interface
python esp32_gui.py
```

2. **Conectar ao ESP32**:
   - Selecione a porta serial na dropdown
   - Clique em "Connect"
   - Aguarde a confirmação de conexão

3. **Comandos Disponíveis**:
   - **Help**: Mostra lista de comandos disponíveis
   - **Info**: Exibe informações do dispositivo
   - **Reset**: Reinicia o ESP32
   - **Mine**: Inicia processo de mineração
   - **Zeros**: Define dificuldade (número de zeros prefixados)
   - **Entropy**: Define valor de entropia para mineração

### Interface de Linha de Comando

```bash
cd interface
python python_serial.py
```

## 📊 Monitoramento

A interface gráfica fornece:
- **Status de conexão** em tempo real
- **Log de comandos** e respostas
- **Informações do dispositivo** (firmware, UART, configurações)
- **Status de mineração** (hashrate, nonces testados)
- **Configurações atuais** (zeros, entropy)

## 🔧 Comandos ESP32

| Comando | Descrição | Exemplo |
|---------|-----------|----------|
| `help` | Lista todos os comandos | `help` |
| `info` | Informações do sistema | `info` |
| `reset` | Reinicia o dispositivo | `reset` |
| `mine` | Inicia mineração | `mine` |
| `zeros <n>` | Define dificuldade | `zeros 4` |
| `entropy <hex>` | Define entropia | `entropy deadbeef` |
| `hash <algo>` | Seleciona algoritmo | `hash keccak256` |

## 🚀 Roadmap - Integração KALE

### 🎯 **Objetivo Futuro**
Integrar o KALESP com o ecossistema **KALE blockchain** para mineração real na rede Stellar:

### 📋 **Funcionalidades Planejadas**

#### 🔗 **Integração com kale-farmer**
- **Orquestração automática** de transações Stellar (plant → work → harvest)
- **Monitoramento de blocos** em tempo real
- **Submissão automática** de proof-of-work
- **Gerenciamento de recompensas** e stakes

#### ⚡ **Mineração KALE Real**
- **Algoritmo Keccak-256** otimizado para ESP32
- **Estrutura de dados** compatível (76 bytes: block_index + nonce + entropy + farmer_address)
- **Validação de zeros** prefixados para dificuldade
- **Integração com Stellar SDK** via Python host

#### 🏗️ **Arquitetura Distribuída**
- **ESP32**: Execução de mineração Keccak-256
- **Python Host**: Orquestração de transações Stellar
- **Stellar Network**: Submissão via Launchtube
- **KALE Smart Contracts**: Validação e recompensas

#### 🔐 **Recursos de Segurança**
- **Chaves privadas** apenas no host Python
- **Comunicação segura** ESP32 ↔ Host
- **Retry logic** para transações falhadas
- **Backup de estado** para recuperação

### 📅 **Fases de Desenvolvimento**

1. **Fase 1** - Análise e Mapeamento *(Em Progresso)*
2. **Fase 2** - Implementação Keccak-256 no ESP32
3. **Fase 3** - Integração com Stellar SDK
4. **Fase 4** - Testes em Testnet
5. **Fase 5** - Deploy em Mainnet

### 🎯 **Meta de Performance**
- **Hashrate alvo**: ~100 KH/s no ESP32
- **Latência**: <1s para submissão de work
- **Uptime**: 24/7 com auto-reconexão
- **Eficiência**: Otimização de consumo energético

---

> 💡 **Nota**: O KALESP atual é uma versão de desenvolvimento. A integração completa com KALE blockchain está planejada para futuras versões.

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor:

1. Faça fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 🔗 Links Relacionados

- [KALE Smart Contracts](../KALE-sc/) - Contratos inteligentes KALE
- [kale-farmer](../kale-farmer/) - Minerador de referência em Rust
- [kale-miner](../kale-miner/) - Minerador GPU/CPU otimizado
- [Stellar Network](https://stellar.org/) - Blockchain Stellar
- [Soroban](https://soroban.stellar.org/) - Plataforma de smart contracts

---

**Status do Projeto**: 🚧 Em Desenvolvimento Ativo  
**Versão Atual**: v0.1.0 - Prototipo de Desenvolvimento  
**Próxima Release**: v0.2.0 - Integração KALE Básica
