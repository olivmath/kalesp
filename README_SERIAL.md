# Comunicação Serial ESP32

Este projeto contém exemplos simples de comunicação serial para ESP32 usando Rust e esp-hal.

## Exemplos Disponíveis

### 1. `serial_comm` - Transmissão Básica
- Envia dados periodicamente via UART
- Pisca LED para indicar atividade
- Apenas transmissão (TX)

### 2. `serial_echo` - Demonstração Completa
- Envia mensagens de status periodicamente
- Interface mais amigável
- Demonstra uso básico da UART

## Como Compilar

```bash
# Compilar exemplo básico
cargo build --bin serial_comm

# Compilar exemplo completo
cargo build --bin serial_echo
```

## Como Executar

```bash
# Executar exemplo básico
cargo run --bin serial_comm --release

# Executar exemplo completo
cargo run --bin serial_echo --release
```

## Configuração da UART

- **UART0** é usado (padrão do ESP32)
- **TX**: GPIO1 (pino padrão)
- **RX**: GPIO3 (pino padrão)
- **Baud Rate**: 115200 (padrão)
- **LED**: GPIO2 (LED interno)

## Monitoramento

### Via espflash (recomendado)
O espflash já está configurado no `.cargo/config.toml` com `--monitor`:

```bash
cargo run --bin serial_echo --release
```

### Via terminal serial externo
Você também pode usar qualquer terminal serial:

```bash
# macOS/Linux
screen /dev/cu.usbserial-0001 115200

# Ou minicom
minicom -D /dev/cu.usbserial-0001 -b 115200
```

## Funcionalidades

### serial_comm
- Envia mensagens periódicas via UART
- Pisca LED para indicar atividade
- Transmite contador incrementado
- Compatível com esp-hal v1.0.0-rc.0

### serial_echo (Atualizado!)
- **Comunicação bidirecional completa**
- Processa comandos recebidos via UART
- Comandos disponíveis:
  - `help` - Mostra lista de comandos
  - `status` - Exibe status do sistema
  - `info` - Informações do dispositivo
  - `ping` - Teste de conectividade
  - `reset` - Reinicia contador
- Mensagens de status menos frequentes (15s)
- Pisca LED indicativo
- Buffer de comando robusto

## Próximos Passos

1. **✅ Implementado: RX (Recepção)**
   - ✅ Ler dados da UART
   - ✅ Processar comandos recebidos
   - ✅ Responder adequadamente

2. **Melhorias futuras**
   - Controle avançado de LED (cores, padrões)
   - Leitura de sensores (temperatura, umidade)
   - Configurações do sistema via comandos
   - Protocolo JSON para dados estruturados
   - **Usar Embassy (async)**: Para comunicação não-bloqueante
   - **Implementar interrupts**: Para recepção em tempo real
   - **Usar DMA**: Para transferências de dados maiores

## Troubleshooting

### Erro "No connected probes"
Se você ver este erro, significa que o projeto estava configurado para probe-rs. Já foi alterado para usar espflash.

### Porta serial não encontrada
Verifique a porta com:
```bash
ls /dev/cu.*
```

E ajuste no comando se necessário.

### Problemas de compilação
Certifique-se de ter o toolchain correto:
```bash
rustup target add xtensa-esp32-none-elf
```