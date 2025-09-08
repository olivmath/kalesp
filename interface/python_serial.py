#!/usr/bin/env python3
"""
Exemplo de comunicação serial com ESP32 usando Python
Instale: pip install pyserial
"""

try:
    import serial
except ImportError:
    print("❌ Módulo 'pyserial' não encontrado!")
    print("📦 Instale com: pip install pyserial")
    print("🔧 Ou: pip3 install pyserial")
    exit(1)

import time
import threading

class ESP32Serial:
    def __init__(self, port='/dev/cu.usbserial-0001', baudrate=115200):
        """
        Inicializa a comunicação serial com ESP32
        
        Args:
            port: Porta serial (encontre com: ls /dev/cu.*)
            baudrate: Velocidade de comunicação (115200 é padrão)
        """
        self.port = port
        self.baudrate = baudrate
        self.serial_conn = None
        self.running = False
        
    def connect(self):
        """Conecta ao ESP32"""
        try:
            self.serial_conn = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=1
            )
            print(f"✅ Conectado ao ESP32 em {self.port}")
            return True
        except Exception as e:
            print(f"❌ Erro ao conectar: {e}")
            return False
    
    def disconnect(self):
        """Desconecta do ESP32"""
        self.running = False
        if self.serial_conn and self.serial_conn.is_open:
            self.serial_conn.close()
            print("🔌 Desconectado do ESP32")
    
    def send_message(self, message):
        """Envia mensagem para o ESP32"""
        if self.serial_conn and self.serial_conn.is_open:
            try:
                self.serial_conn.write(f"{message}\n".encode('utf-8'))
                print(f"📤 Enviado: {message}")
                return True
            except Exception as e:
                print(f"❌ Erro ao enviar: {e}")
                return False
        return False
    
    def read_messages(self):
        """Reads messages from ESP32 continuously"""
        while self.running and self.serial_conn and self.serial_conn.is_open:
            try:
                if self.serial_conn.in_waiting > 0:
                    message = self.serial_conn.readline().decode('utf-8').strip()
                    if message:
                        print(f"📥 Recebido: {message}")
                time.sleep(0.1)
            except Exception as e:
                print(f"❌ Erro ao ler: {e}")
                break
    
    def start_monitoring(self):
        """Inicia monitoramento em thread separada"""
        self.running = True
        monitor_thread = threading.Thread(target=self.read_messages)
        monitor_thread.daemon = True
        monitor_thread.start()
        return monitor_thread

def main():
    """Exemplo de uso"""
    # Encontre sua porta com: ls /dev/cu.*
    esp32 = ESP32Serial(port='/dev/cu.usbserial-0001')
    
    if not esp32.connect():
        print("Verifique se o ESP32 está conectado e a porta está correta")
        return
    
    # Inicia monitoramento
    monitor_thread = esp32.start_monitoring()
    
    try:
        print("\n🚀 Comunicação iniciada! Digite 'quit' para sair")
        print("Comandos disponíveis: help, status, info")
        
        while True:
            user_input = input("\n> ")
            
            if user_input.lower() == 'quit':
                break
            
            if user_input.strip():
                esp32.send_message(user_input)
            
            time.sleep(0.1)
    
    except KeyboardInterrupt:
        print("\n⏹️  Interrompido pelo usuário")
    
    finally:
        esp32.disconnect()

if __name__ == "__main__":
    main()