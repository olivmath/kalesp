# Interface Gráfica ESP32 KALE Miner

Interface gráfica moderna para comunicação com ESP32 usando Flet framework.

## 🎯 Funcionalidades

### ✅ Conexão Serial
- Detecção automática de portas seriais disponíveis
- Conexão/desconexão com um clique
- Status visual da conexão em tempo real

### ✅ Comandos ESP32
- **Help**: Mostra comandos disponíveis no ESP32
- **Info**: Informações do dispositivo
- **Reset**: Reinicia contador
- **Mine**: Inicia processo de mineração

### ✅ Configurações de Mineração
- **Zeros**: Slider para definir número de zeros (1-12)
- **Entropy**: Slider para definir entropy (1-10)
- Envio automático ao alterar valores

### ✅ Log de Comunicação
- Mensagens coloridas por tipo:
  - 🔴 Erros (ERROR)
  - 🔵 Mineração (MINE_*)
  - 🟢 Informações (INFO/STATUS)
  - 🟣 Ajuda (HELP)
- Timestamps automáticos
- Scroll automático
- Botão para limpar log
- Limite de 100 mensagens (performance)

### ✅ Comandos Personalizados
- Campo de texto para comandos customizados
- Histórico de comandos enviados
- Suporte a todos os comandos do ESP32

## 📦 Instalação

```bash
# Instalar dependências
pip install -r requirements.txt

# Ou instalar individualmente
pip install flet>=0.24.0 pyserial>=3.5
```

## 🚀 Como Usar

### 1. Executar a Interface

```bash
# Executar interface gráfica
python3 esp32_gui.py

# Ou tornar executável
chmod +x esp32_gui.py
./esp32_gui.py
```

### 2. Conectar ao ESP32

1. **Conecte o ESP32** via USB
2. **Selecione a porta** no dropdown (detecção automática)
3. **Clique em "Conectar"**
4. **Status muda para 🟢 Conectado**

### 3. Usar Comandos

#### Comandos Rápidos
- Clique nos botões: **Help**, **Info**, **Reset**, **Mine**

#### Configurar Mineração
- Ajuste o slider **Zeros** (1-12)
- Ajuste o slider **Entropy** (1-10)
- Comandos são enviados automaticamente

#### Comandos Personalizados
- Digite no campo "Comando personalizado"
- Pressione **Enter** ou clique **Enviar**

### 4. Monitorar Comunicação

- **Log em tempo real** de todas as mensagens
- **Cores diferentes** para tipos de mensagem
- **Timestamps** para cada entrada
- **Scroll automático** para mensagens mais recentes

## 🎨 Interface

### Layout Principal

```
┌─────────────────────────────────────────┐
│ 🔌 Conexão Serial                       │
│ [Porta] [Conectar] 🟢 Conectado         │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ ⚡ Comandos                              │
│ [Help] [Info] [Reset] [Mine]            │
│                                         │
│ 🔧 Configurações de Mineração           │
│ Zeros:   [====●====] 4                 │
│ Entropy: [===●=====] 5                 │
│                                         │
│ 💬 Comando personalizado                │
│ [_________________] [Enviar]            │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ 📋 Log de Comunicação        [Limpar]   │
│ ┌─────────────────────────────────────┐ │
│ │ [12:34:56] 📤 help                  │ │
│ │ [12:34:57] 📥 === Comandos ===      │ │
│ │ [12:34:57] 📥 help - Mostra ajuda  │ │
│ │ [12:34:58] 📤 mine                  │ │
│ │ [12:34:59] 📥 MINE_START: zeros=4   │ │
│ └─────────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

## 🔧 Comandos Suportados

### Comandos Básicos
- `help` - Lista todos os comandos
- `info` - Informações do dispositivo
- `reset` - Reinicia contador

### Comandos de Mineração
- `zeros N` - Define número de zeros (ex: `zeros 8`)
- `entropy N` - Define entropy (ex: `entropy 5`)
- `mine` - Inicia mineração

### Exemplos de Uso
```
help           # Mostra ajuda
info           # Info do dispositivo
zeros 6        # Define 6 zeros
entropy 3      # Define entropy 3
mine           # Inicia mineração
reset          # Reinicia contador
```

## 🎯 Vantagens da Interface Gráfica

### ✅ Facilidade de Uso
- **Interface intuitiva** sem necessidade de linha de comando
- **Botões visuais** para comandos frequentes
- **Sliders** para configurações numéricas
- **Status visual** da conexão

### ✅ Monitoramento Avançado
- **Log colorido** por tipo de mensagem
- **Timestamps** para rastreamento temporal
- **Scroll automático** para acompanhar em tempo real
- **Histórico persistente** durante a sessão

### ✅ Produtividade
- **Comandos rápidos** com um clique
- **Configuração visual** de parâmetros
- **Feedback imediato** de comandos enviados
- **Interface responsiva** e moderna

### ✅ Flexibilidade
- **Comandos personalizados** para casos especiais
- **Detecção automática** de portas seriais
- **Reconexão fácil** em caso de desconexão
- **Compatível** com todos os comandos do ESP32

## 🔍 Troubleshooting

### Porta não encontrada
```bash
# Verificar portas disponíveis
ls /dev/cu.*

# Procurar por:
# /dev/cu.usbserial-XXXX
# /dev/cu.SLAB_USBtoUART
# /dev/cu.wchusbserial-XXXX
```

### Erro de conexão
1. Verificar se ESP32 está conectado
2. Verificar se porta está correta
3. Verificar se outro programa não está usando a porta
4. Tentar desconectar e reconectar

### Interface não abre
```bash
# Verificar instalação do Flet
pip list | grep flet

# Reinstalar se necessário
pip install --upgrade flet
```

## 🚀 Próximas Melhorias

- [ ] **Gráficos em tempo real** de hash rate
- [ ] **Salvamento de configurações** entre sessões
- [ ] **Múltiplas conexões** ESP32 simultâneas
- [ ] **Export de logs** para arquivo
- [ ] **Temas escuro/claro** personalizáveis
- [ ] **Notificações** para eventos importantes
- [ ] **Estatísticas** de mineração
- [ ] **Auto-reconexão** em caso de desconexão

---

**Desenvolvido com ❤️ usando Flet Framework**