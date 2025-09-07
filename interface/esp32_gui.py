#!/usr/bin/env python3
"""
Interface gráfica para comunicação com ESP32 usando Flet
Autor: Sistema de Interface ESP32
"""

import flet as ft
import threading
import time
import glob
from python_serial import ESP32Serial

class ESP32GUI:
    def __init__(self):
        self.esp32 = None
        self.connected = False
        self.monitoring_thread = None
        
        # Configurações de mineração
        self.zeros_value = 4
        self.entropy_value = 5
        
        # Controles da interface
        self.status_text = None
        self.port_dropdown = None
        self.connect_button = None
        self.log_column = None
        self.zeros_slider = None
        self.entropy_slider = None
        self.custom_command_field = None
        
    def get_available_ports(self):
        """Busca portas seriais disponíveis"""
        ports = []
        # macOS/Linux
        ports.extend(glob.glob('/dev/cu.*'))
        ports.extend(glob.glob('/dev/ttyUSB*'))
        ports.extend(glob.glob('/dev/ttyACM*'))
        
        if not ports:
            ports = ['/dev/cu.usbserial-0001']  # Porta padrão
            
        return ports
    
    def log_message(self, message, color=ft.Colors.BLACK):
        """Adiciona mensagem ao log"""
        if self.log_column:
            timestamp = time.strftime("%H:%M:%S")
            log_entry = ft.Row([
                ft.Text(f"[{timestamp}]", size=12, color=ft.Colors.GREY_600),
                ft.Text(message, size=12, color=color, selectable=True)
            ])
            self.log_column.controls.append(log_entry)
            
            # Manter apenas as últimas 100 mensagens
            if len(self.log_column.controls) > 100:
                self.log_column.controls.pop(0)
                
            self.log_column.update()
    
    def connect_esp32(self, e):
        """Conecta ou desconecta do ESP32"""
        if not self.connected:
            port = self.port_dropdown.value
            if not port:
                self.log_message("❌ Selecione uma porta serial", ft.Colors.RED)
                return
                
            self.esp32 = ESP32Serial(port=port)
            if self.esp32.connect():
                self.connected = True
                self.connect_button.text = "Desconectar"
                self.connect_button.bgcolor = ft.Colors.RED_400
                self.status_text.value = "🟢 Conectado"
                self.status_text.color = ft.Colors.GREEN
                
                # Iniciar monitoramento personalizado
                self.start_custom_monitoring()
                
                self.log_message(f"✅ Conectado ao ESP32 em {port}", ft.Colors.GREEN)
            else:
                self.log_message(f"❌ Erro ao conectar em {port}", ft.Colors.RED)
        else:
            if self.esp32:
                self.esp32.disconnect()
            self.connected = False
            self.connect_button.text = "Conectar"
            self.connect_button.bgcolor = ft.Colors.BLUE_400
            self.status_text.value = "🔴 Desconectado"
            self.status_text.color = ft.Colors.RED
            self.log_message("🔌 Desconectado do ESP32", ft.Colors.ORANGE)
            
        self.connect_button.update()
        self.status_text.update()
    
    def start_custom_monitoring(self):
        """Inicia monitoramento personalizado das mensagens"""
        def monitor():
            while self.connected and self.esp32 and self.esp32.serial_conn and self.esp32.serial_conn.is_open:
                try:
                    if self.esp32.serial_conn.in_waiting > 0:
                        message = self.esp32.serial_conn.readline().decode('utf-8').strip()
                        if message:
                            # Colorir mensagens baseado no tipo
                            color = ft.Colors.BLACK
                            if "ERROR" in message:
                                color = ft.Colors.RED
                            elif "MINE_" in message:
                                color = ft.Colors.BLUE
                            elif "INFO" in message or "STATUS" in message:
                                color = ft.Colors.GREEN
                            elif "HELP" in message:
                                color = ft.Colors.PURPLE
                                
                            self.log_message(f"📥 {message}", color)
                    time.sleep(0.1)
                except Exception as e:
                    self.log_message(f"❌ Erro no monitoramento: {e}", ft.Colors.RED)
                    break
        
        self.monitoring_thread = threading.Thread(target=monitor, daemon=True)
        self.monitoring_thread.start()
    
    def send_command(self, command):
        """Envia comando para o ESP32"""
        if not self.connected or not self.esp32:
            self.log_message("❌ ESP32 não conectado", ft.Colors.RED)
            return
            
        if self.esp32.send_message(command):
            self.log_message(f"📤 {command}", ft.Colors.BLUE_600)
        else:
            self.log_message(f"❌ Erro ao enviar: {command}", ft.Colors.RED)
    
    def on_help_click(self, e):
        self.send_command("help")
    
    def on_info_click(self, e):
        self.send_command("info")
    
    def on_reset_click(self, e):
        self.send_command("reset")
    
    def on_mine_click(self, e):
        self.send_command("mine")
    
    def on_zeros_change(self, e):
        self.zeros_value = int(e.control.value)
        self.send_command(f"zeros {self.zeros_value}")
    
    def on_entropy_change(self, e):
        self.entropy_value = int(e.control.value)
        self.send_command(f"entropy {self.entropy_value}")
    
    def on_custom_command(self, e):
        command = self.custom_command_field.value.strip()
        if command:
            self.send_command(command)
            self.custom_command_field.value = ""
            self.custom_command_field.update()
    
    def clear_log(self, e):
        """Limpa o log de mensagens"""
        if self.log_column:
            self.log_column.controls.clear()
            self.log_column.update()
            self.log_message("🧹 Log limpo", ft.Colors.GREY)
    
    def build_ui(self, page: ft.Page):
        """Constrói a interface do usuário"""
        page.title = "ESP32 KALE Miner Interface"
        page.theme_mode = ft.ThemeMode.LIGHT
        page.window_width = 1000
        page.window_height = 700
        page.padding = 20
        
        # Área de conexão
        self.port_dropdown = ft.Dropdown(
            label="Porta Serial",
            options=[ft.dropdown.Option(port) for port in self.get_available_ports()],
            value=self.get_available_ports()[0] if self.get_available_ports() else None,
            width=200
        )
        
        self.connect_button = ft.ElevatedButton(
            text="Conectar",
            on_click=self.connect_esp32,
            bgcolor=ft.Colors.BLUE_400,
            color=ft.Colors.WHITE
        )
        
        self.status_text = ft.Text(
            "🔴 Desconectado",
            size=16,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.RED
        )
        
        connection_section = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text("Conexão Serial", size=18, weight=ft.FontWeight.BOLD),
                    ft.Row([
                        self.port_dropdown,
                        self.connect_button,
                        self.status_text
                    ], alignment=ft.MainAxisAlignment.START)
                ]),
                padding=15
            )
        )
        
        # Área de comandos
        command_buttons = ft.Row([
            ft.ElevatedButton("Help", on_click=self.on_help_click, bgcolor=ft.Colors.PURPLE_400, color=ft.Colors.WHITE),
            ft.ElevatedButton("Info", on_click=self.on_info_click, bgcolor=ft.Colors.GREEN_400, color=ft.Colors.WHITE),
            ft.ElevatedButton("Reset", on_click=self.on_reset_click, bgcolor=ft.Colors.ORANGE_400, color=ft.Colors.WHITE),
            ft.ElevatedButton("Mine", on_click=self.on_mine_click, bgcolor=ft.Colors.AMBER_400, color=ft.Colors.WHITE),
        ], wrap=True)
        
        # Configurações de mineração
        self.zeros_slider = ft.Slider(
            min=1, max=12, value=self.zeros_value, divisions=11,
            label="Zeros: {value}",
            on_change=self.on_zeros_change
        )
        
        self.entropy_slider = ft.Slider(
            min=1, max=10, value=self.entropy_value, divisions=9,
            label="Entropy: {value}",
            on_change=self.on_entropy_change
        )
        
        mining_config = ft.Column([
            ft.Text("Configurações de Mineração", size=16, weight=ft.FontWeight.BOLD),
            ft.Row([ft.Text("Zeros:"), self.zeros_slider]),
            ft.Row([ft.Text("Entropy:"), self.entropy_slider])
        ])
        
        # Campo de comando personalizado
        self.custom_command_field = ft.TextField(
            label="Comando personalizado",
            on_submit=self.on_custom_command,
            expand=True
        )
        
        custom_command_row = ft.Row([
            self.custom_command_field,
            ft.ElevatedButton("Enviar", on_click=self.on_custom_command)
        ])
        
        commands_section = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text("Comandos", size=18, weight=ft.FontWeight.BOLD),
                    command_buttons,
                    ft.Divider(),
                    mining_config,
                    ft.Divider(),
                    custom_command_row
                ]),
                padding=15
            )
        )
        
        # Área de log
        self.log_column = ft.Column(
            scroll=ft.ScrollMode.AUTO,
            height=300
        )
        
        log_section = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Text("Log de Comunicação", size=18, weight=ft.FontWeight.BOLD),
                        ft.ElevatedButton("Limpar", on_click=self.clear_log, bgcolor=ft.Colors.RED_300)
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Container(
                        content=self.log_column,
                        bgcolor=ft.Colors.GREY_100,
                        padding=10,
                        border_radius=5
                    )
                ]),
                padding=15
            )
        )
        
        # Layout principal
        page.add(
            connection_section,
            commands_section,
            log_section
        )
        
        # Mensagem inicial
        self.log_message("🚀 Interface ESP32 KALE Miner iniciada")
        self.log_message("💡 Selecione uma porta e clique em 'Conectar' para começar")

def main(page: ft.Page):
    app = ESP32GUI()
    app.build_ui(page)

if __name__ == "__main__":
    ft.app(target=main)