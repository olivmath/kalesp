# KALE ESP32 Miner Integration Plan (kalesp)

## 🎯 Objetivo
Integrar o ESP32 como minerador KALE reutilizando a lógica dos repositórios existentes:
- **ESP32**: Executa mineração Keccak-256 para encontrar nonces
- **Python Host**: Orquestra transações Stellar (plant, work, harvest) usando stellar_sdk + Launchtube

## 📋 Análise dos Repositórios KALE

### 🥬 KALE-sc (Contrato Inteligente)
**Localização**: `/Users/olivmath/dev/esp/KALE-sc/`

**Fluxo de Mineração**:
1. **`plant(farmer, amount)`**: Stake inicial, requer auth do farmer
2. **`work(farmer, hash, nonce)`**: Submete proof-of-work, sem auth (pode ser chamado por terceiros)
3. **`harvest(farmer, index)`**: Coleta recompensas do bloco

**Parâmetros Críticos**:
- **Block Index**: Índice do bloco atual
- **Entropy**: Hash do bloco anterior (32 bytes)
- **Farmer Address**: Endereço Stellar do minerador (32 bytes)
- **Nonce**: Valor a ser testado (8 bytes)
- **Hash**: Resultado Keccak-256 (32 bytes)

**Estrutura de Dados de Entrada** (76 bytes total):
```
[0-3]   Block Index (4 bytes, big-endian)
[4-11]  Nonce (8 bytes, big-endian)
[12-43] Entropy (32 bytes)
[44-75] Farmer Address (32 bytes)
```

**Validação de Hash**:
- Suporte para SHA256 e Keccak-256 dos 76 bytes de entrada
- Contagem de zeros prefixados (nibbles)
- Mais zeros = maior contribuição para recompensa
- Algoritmo configurável via comando `hash`

### 🦀 kale-farmer (Referência Rust)
**Localização**: `/Users/olivmath/dev/esp/kale-farmer/`

**Componentes Principais**:
- **Rust Miner** (`src/main.rs`): Mineração paralela com Keccak-256
- **Bun Scripts**: Orquestração de plant/work/harvest
- **Stellar SDK**: Integração com blockchain Stellar

**Lógica de Orquestração**:
- Monitora novos blocos a cada 5 segundos
- Plant automático no início de novo bloco
- Work com delay de ~4.7 minutos para maturação
- Harvest do bloco anterior

### ⚡ kale-miner (Referência C++/GPU)
**Localização**: `/Users/olivmath/dev/esp/kale-miner/`

**Implementações Keccak-256**:
- **CPU Otimizado**: `utils/keccak_opt.h` (~49 MH/s Intel i9)
- **CPU Portável**: `utils/keccak.h` (~42 MH/s Intel i9)
- **CUDA Kernel**: `utils/keccak.cuh` (~1.9 GH/s RTX 4080)
- **OpenCL Kernel**: `utils/keccak.cl` (~1.3 GH/s RTX 4080)

### 🔧 kalesp (Projeto Atual)
**Localização**: `/Users/olivmath/dev/esp/kalesp/`

**Estado Atual**:
- **ESP32 Firmware**: Rust com comunicação serial básica
- **Python Interface**: GUI com Flet + comunicação serial
- **Comandos Implementados**: help, info, reset, zeros, entropy, hash, mine

## 🏗️ Arquitetura Proposta

### ESP32 (Firmware Rust)
**Responsabilidades**:
- Receber parâmetros de mineração via serial
- Executar loop Keccak-256 otimizado
- Retornar melhor nonce encontrado
- Reportar progresso e estatísticas

**Entrada**:
```
START_MINING <block_index> <entropy_hex> <farmer_hex> <difficulty> <batch_size>
```

**Saída**:
```
MINE_PROGRESS <nonces_tested> <best_zeros> <hashrate>
MINE_RESULT <nonce> <hash_hex> <zeros_count>
MINE_ERROR <error_message>
```

### Python Host (Orquestrador)
**Responsabilidades**:
- Monitorar blockchain Stellar para novos blocos
- Executar sequência plant → work → harvest
- Gerenciar comunicação serial com ESP32
- Assinar e submeter transações via Launchtube
- Persistir estado e recuperar de falhas

**Módulos**:
- `stellar_client.py`: Integração Stellar SDK + Launchtube
- `mining_orchestrator.py`: Lógica de ciclo de mineração
- `esp32_manager.py`: Comunicação serial com ESP32
- `state_manager.py`: Persistência de estado

## 📋 Lista de Tarefas Detalhada

### 🔴 Prioridade Alta

1. **Analisar Requisitos Funcionais KALE**
   - Estudar fluxo plant → work → harvest
   - Mapear parâmetros de entrada (block index, entropy, farmer, nonce)
   - Entender cálculo de recompensas e deadlines
   - Documentar regras do contrato

2. **Extrair Lógica de Mineração**
   - Algoritmo Keccak-256 dos repositórios existentes
   - Preparação de dados (76 bytes: index + nonce + entropy + farmer)
   - Contagem de zeros prefixados
   - Critérios de dificuldade

3. **Definir Arquitetura Detalhada**
   - Responsabilidades ESP32 vs Python
   - Formatos de dados e protocolos
   - Pontos de integração
   - Fluxo de dados

4. **Especificar Protocolo Serial**
   - Mensagens (start/stop mining, job parameters, progress)
   - Formato binário vs texto
   - Tamanhos, checksums, timeouts
   - Tratamento de erros

5. **Portar Keccak-256 para ESP32**
   - Implementar em Rust no_std ou C otimizado
   - Avaliar performance e uso de memória
   - Garantir equivalência com referências
   - Testar endianness e layout de dados

6. **Implementar Cliente Stellar Python**
   - Módulo para transações plant/work/harvest
   - Integração com stellar_sdk
   - Suporte a Launchtube
   - Retry logic e backoff

7. **Desenvolver Orquestração de Mineração**
   - Timing de plant e maturação
   - Estratégia de submissão de work
   - Timing de harvest
   - Janelas e rate limits

8. **Garantir Segurança**
   - Chaves apenas no host (nunca no ESP)
   - Proteção de variáveis .env
   - Proteção token Launchtube
   - Logs sem informações sensíveis

### 🟡 Prioridade Média

9. **Criar Vetores de Teste**
   - Gerar casos de teste dos miners existentes
   - Validar equivalência de hashes
   - Verificar contagem de zeros
   - Testes de regressão

10. **Implementar Persistência de Estado**
    - Arquivo/DB para estado por conta
    - Último bloco, melhor nonce/hash
    - Stakes e erros recentes
    - Recuperação de falhas

### 🟢 Prioridade Baixa

11. **Melhorar Telemetria/GUI**
    - Hashrate em tempo real
    - Status de transações
    - Indicadores de conexão
    - Métricas de performance

12. **Pipeline de Build/Flash**
    - Makefile para firmware ESP32
    - Setup de ambiente Python
    - Documentação de pré-requisitos

13. **Métricas de Performance**
    - Target de hashrate ESP32
    - Latência host→tx
    - Estabilidade 24h
    - Taxa de falha de transações

14. **Testes Automatizados**
    - Testes unitários (Keccak/zeros)
    - Testes de integração (serial)
    - Testes de fluxo completo

15. **Tratamento de Erros**
    - Retry de plant/harvest
    - Ajuste de dificuldade
    - Fallback para desconexão ESP
    - Buffers de work

16. **Compatibilidade Multi-conta**
    - Queue de jobs para múltiplos farmers
    - Limites de concorrência ESP
    - Isolamento de estado

17. **Observabilidade**
    - Logs estruturados
    - Rotação de logs
    - Contadores de hashrate e sucesso
    - Export opcional (arquivo/HTTP)

18. **Integração com Repos de Suporte**
    - Bridge de equivalência com kale-miner
    - Estratégias de timing do kale-farmer
    - Manter compatibilidade sem cópia completa

## ✅ Critérios de Aceitação Mínimos

- **ESP32**: Encontra nonces com verificação de zeros idêntica às referências
- **Host**: Executa ciclo plant → work → harvest com chaves locais e Launchtube
- **Testes**: Funciona em futurenet/testnet com retries e logging
- **GUI**: Exibe hashrate e status sem travamentos
- **Estabilidade**: Operação 24h com auto-reconexão

## ⚠️ Riscos e Mitigações

| Risco | Impacto | Mitigação |
|-------|---------|----------|
| Performance limitada ESP32 | Alto | Otimizar Keccak em C/Rust, ajustar dificuldade |
| Divergência de hash | Alto | Validação precoce com vetores de teste |
| Falhas de rede/tx | Médio | Retries, backoff, alertas visuais |
| Endianness/layout | Médio | Testes de equivalência com referências |
| Overhead serial | Baixo | Protocolo binário otimizado |

## 🚀 Próximos Passos

1. **Fase 1 - Análise**: Consolidar mapeamento de dados e preparação de entrada
2. **Fase 2 - Prototipagem**: Implementar Keccak básico no ESP32
3. **Fase 3 - Integração**: Desenvolver protocolo serial e cliente Python
4. **Fase 4 - Testes**: Validar equivalência e executar testes de fluxo
5. **Fase 5 - Produção**: Deploy em testnet/mainnet com monitoramento

---

**Status**: 📋 Planejamento Completo - Pronto para Implementação
**Última Atualização**: Janeiro 2025