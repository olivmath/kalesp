# Comunicação Serial com ESP32

Exemplos de como se comunicar com o ESP32 via USB usando Python e JavaScript/Node.js.

## 📋 Pré-requisitos

1. **ESP32 conectado via USB** com o programa `serial_echo` rodando
2. **Porta serial identificada** (ex: `/dev/cu.usbserial-0001`)

### 🔍 Encontrar a porta serial

```bash
# No macOS/Linux
ls /dev/cu.*

# Procure por:
# /dev/cu.usbserial-XXXX
# /dev/cu.SLAB_USBtoUART
# /dev/cu.wchusbserial-XXXX
```

## 🐍 Python

### Instalação

```bash
cd examples
pip install -r requirements.txt
```

### Uso

```bash
# Execute o script
python3 python_serial.py

# Ou torne executável
chmod +x python_serial.py
./python_serial.py
```

### Funcionalidades Python

- ✅ Conexão automática com ESP32
- ✅ Envio de mensagens
- ✅ Recepção em tempo real (threading)
- ✅ Interface de linha de comando
- ✅ Tratamento de erros
- ✅ **Comunicação bidirecional completa**

### Exemplo de uso Python

```python
from python_serial import ESP32Serial

# Conecta ao ESP32
esp32 = ESP32Serial(port='/dev/cu.usbserial-0001')
if esp32.connect():
    esp32.start_monitoring()
    
    # Envia comandos
    esp32.send_message('help')
    esp32.send_message('status')
    
    # Desconecta
    esp32.disconnect()
```

## 🟨 JavaScript/Node.js

### Instalação

```bash
cd examples
npm install
```

### Uso

```bash
# Execute o script
node js_serial.js

# Ou use npm
npm start

# Listar portas disponíveis
npm run list-ports
```

### Funcionalidades JavaScript

- ✅ Conexão automática com ESP32
- ✅ Envio de mensagens
- ✅ Recepção em tempo real (eventos)
- ✅ Interface de linha de comando
- ✅ Listagem de portas seriais
- ✅ Tratamento de erros
- ✅ **Comunicação bidirecional completa**

### Exemplo de uso JavaScript

```javascript
const ESP32Serial = require('./js_serial.js');

// Conecta ao ESP32
const esp32 = new ESP32Serial('/dev/cu.usbserial-0001');
esp32.connect().then(connected => {
    if (connected) {
        // Envia comandos
        esp32.sendMessage('help');
        esp32.sendMessage('status');
        
        // Desconecta após 5 segundos
        setTimeout(() => esp32.disconnect(), 5000);
    }
});
```

## 🚀 Testando a Comunicação

### 1. Prepare o ESP32

```bash
# No diretório do projeto ESP32
cd /Users/olivmath/dev/esp/kalesp
cargo run --bin serial_echo --release
```

### 2. Execute o cliente Python ou JavaScript

**Python:**
```bash
cd examples
python3 python_serial.py
```

**JavaScript:**
```bash
cd examples
node js_serial.js
```

### 3. Teste os comandos

```
> help
> status
> info
> Olá ESP32!
> quit  # Para sair
```

## 📡 Protocolo de Comunicação

O ESP32 agora processa comandos em tempo real e responde adequadamente:

### Comandos Disponíveis
- `help` - Mostra lista completa de comandos
- `status` - Retorna status atual do sistema
- `info` - Informações detalhadas do dispositivo
- `ping` - Teste de conectividade (responde "Pong!")
- `reset` - Reinicia o contador do sistema
- Qualquer outro texto será ecoado com confirmação

### Exemplo de Interação
```
> help
=== Comandos Disponíveis ===
help   - Mostra esta ajuda
status - Mostra status do sistema
info   - Informações do dispositivo
ping   - Teste de conectividade
reset  - Reinicia contador
============================

> ping
Pong! ESP32 respondendo

> status
[Status] Sistema ativo - Uptime: 5 ciclos
```

### Mensagens do ESP32 → Computador

- `=== ESP32 Serial Demo ===` - Mensagem de boas-vindas
- `Comandos: 'help', 'status', 'info'` - Lista de comandos
- `[Status] Sistema ativo - Uptime: X ciclos` - Status periódico

### Comandos Computador → ESP32

- `help` - Mostra ajuda (quando implementado)
- `status` - Mostra status do sistema
- `info` - Informações do dispositivo
- Qualquer texto - Será ecoado de volta

## 🔧 Configurações

### Parâmetros da Comunicação Serial

- **Velocidade (Baud Rate):** 115200
- **Data Bits:** 8
- **Stop Bits:** 1
- **Parity:** None
- **Flow Control:** None

### Personalizando a Porta

**Python:**
```python
esp32 = ESP32Serial(port='/sua/porta/aqui', baudrate=115200)
```

**JavaScript:**
```javascript
const esp32 = new ESP32Serial('/sua/porta/aqui', 115200);
```

## 🐛 Solução de Problemas

### Erro: "Porta não encontrada"

1. Verifique se o ESP32 está conectado
2. Liste as portas disponíveis:
   ```bash
   ls /dev/cu.*
   ```
3. Ajuste o caminho da porta no código

### Erro: "Permissão negada"

```bash
# Adicione seu usuário ao grupo dialout (Linux)
sudo usermod -a -G dialout $USER

# No macOS, geralmente não é necessário
```

### Erro: "Porta em uso"

1. Feche outros programas que usam a porta serial
2. Desconecte e reconecte o ESP32
3. Reinicie o terminal

### ESP32 não responde

1. Verifique se o programa `serial_echo` está rodando
2. Pressione o botão RESET no ESP32
3. Reflashe o programa:
   ```bash
   cargo run --bin serial_echo --release
   ```

## 📚 Próximos Passos

- [ ] Implementar recepção de dados no ESP32
- [ ] Adicionar protocolo de comandos estruturado
- [ ] Criar interface gráfica (GUI)
- [ ] Adicionar logging de mensagens
- [ ] Implementar controle de GPIO via serial

## 🤝 Contribuindo

Sinta-se à vontade para melhorar os exemplos:

1. Adicione tratamento de erros mais robusto
2. Implemente novos comandos
3. Crie interfaces gráficas
4. Adicione testes automatizados