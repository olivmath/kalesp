#!/usr/bin/env python3
"""
Graphical interface for ESP32 communication using Flet
Terminal/Assembler style
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
        self.is_mining = False

        # Mining configurations
        self.zeros_value = 0
        self.entropy_value = 0

        # Device state
        self.device_info = {
            "device": "ESP32",
            "firmware": "Serial Echo v1.0",
            "uart": "115200 baud",
            "pins": "TX=GPIO1, RX=GPIO3",
            "zeros": 0,
            "entropy": 0,
            "last_nonce": -1,
        }

        # Interface controls
        self.status_text = None
        self.port_dropdown = None
        self.connect_button = None
        self.log_column = None
        self.zeros_field = None
        self.entropy_field = None
        self.device_info_column = None
        self.mining_status = None

    def get_available_ports(self):
        """Search for available serial ports"""
        ports = []
        # macOS/Linux
        ports.extend(glob.glob("/dev/cu.*"))
        ports.extend(glob.glob("/dev/ttyUSB*"))
        ports.extend(glob.glob("/dev/ttyACM*"))

        if not ports:
            ports = ["/dev/cu.usbserial-0001"]  # Default port

        return ports

    def log_message(self, message, msg_type="info"):
        """Add message to log"""
        if self.log_column:
            timestamp = time.strftime("%H:%M:%S")

            # Define colors based on type
            color = ft.Colors.WHITE
            prefix = ""

            if msg_type == "sent":
                color = ft.Colors.CYAN_400
                prefix = ">"
            elif msg_type == "received":
                color = ft.Colors.WHITE
            elif msg_type == "error":
                color = ft.Colors.RED_400
            elif msg_type == "success":
                color = ft.Colors.GREEN_400
            elif msg_type == "warning":
                color = ft.Colors.YELLOW_400

            log_entry = ft.Row(
                [
                    ft.Text(
                        f"{timestamp}",
                        size=10,
                        color=ft.Colors.GREY_600,
                        font_family="Courier New",
                        width=80,
                    ),
                    ft.Text(
                        f"{prefix}",
                        size=10,
                        color=ft.Colors.GREY_600,
                        font_family="Courier New",
                        width=20,
                    ),
                    ft.Text(
                        message,
                        size=10,
                        color=color,
                        font_family="Courier New",
                        selectable=True,
                    ),
                ],
                spacing=5,
            )

            self.log_column.controls.append(log_entry)

            # Keep only the last 100 messages
            if len(self.log_column.controls) > 100:
                self.log_column.controls.pop(0)

            self.log_column.update()

            # Auto-scroll to end
            if hasattr(self.log_column.parent, "scroll_to"):
                self.log_column.parent.scroll_to(offset=-1, duration=100)

    def update_device_info(self):
        """Updates device information display"""
        if self.device_info_column:
            self.device_info_column.controls.clear()

            info_items = [
                f"Device: {self.device_info['device']}",
                f"Firmware: {self.device_info['firmware']}",
                f"UART: {self.device_info['uart']}",
                f"{self.device_info['pins']}",
                "",
                "MINING STATE:",
                f"Zeros: {self.device_info['zeros']}",
                f"Entropy: {self.device_info['entropy']}",
                f"Last Nonce: {self.device_info['last_nonce']}",
            ]

            for item in info_items:
                if item == "":
                    continue

                color = ft.Colors.WHITE
                if "MINING STATE:" in item:
                    color = ft.Colors.GREY_400
                elif any(x in item for x in ["Zeros:", "Entropy:", "Last Nonce:"]):
                    color = ft.Colors.YELLOW_400

                self.device_info_column.controls.append(
                    ft.Text(item, size=10, color=color, font_family="Courier New")
                )

            self.device_info_column.update()

    def connect_esp32(self, e):
        """Connect or disconnect from ESP32"""
        if not self.connected:
            port = self.port_dropdown.value
            if not port:
                self.log_message("ERRO: Selecione uma porta serial", "error")
                return

            self.log_message(f"Conectando em {port}...", "info")
            self.esp32 = ESP32Serial(port=port)

            if self.esp32.connect():
                self.connected = True
                self.connect_button.text = "DISCONNECT"
                self.connect_button.bgcolor = ft.Colors.RED_900
                self.status_text.value = "Conectado"
                self.status_text.color = ft.Colors.GREEN_400

                # Start custom monitoring
                self.start_custom_monitoring()

                self.log_message(f"Connected to ESP32 on {port}", "success")
                self.log_message(
                    "Communication started! Commands: help, info, reset", "info"
                )
            else:
                self.log_message(f"Erro ao conectar em {port}", "error")
        else:
            if self.esp32:
                self.esp32.disconnect()
            self.connected = False
            self.is_mining = False
            self.connect_button.text = "CONNECT"
            self.connect_button.bgcolor = ft.Colors.GREEN_900
            self.status_text.value = "Desconectado"
            self.status_text.color = ft.Colors.RED_400
            self.log_message("Disconnected from ESP32", "warning")
            self.update_mining_status()

        self.connect_button.update()
        self.status_text.update()

    def start_custom_monitoring(self):
        """Start custom message monitoring"""

        def monitor():
            while (
                self.connected
                and self.esp32
                and self.esp32.serial_conn
                and self.esp32.serial_conn.is_open
            ):
                try:
                    if self.esp32.serial_conn.in_waiting > 0:
                        message = (
                            self.esp32.serial_conn.readline().decode("utf-8").strip()
                        )
                        if message:
                            self.process_esp32_message(message)
                    time.sleep(0.1)
                except Exception as e:
                    self.log_message(f"Monitoring error: {e}", "error")
                    break

        self.monitoring_thread = threading.Thread(target=monitor, daemon=True)
        self.monitoring_thread.start()

    def process_esp32_message(self, message):
        """Process ESP32 messages and update state"""
        self.log_message(message, "received")

        # Update state based on messages
        if message.startswith("ZEROS:"):
            try:
                zeros = int(message.split()[1])
                self.device_info["zeros"] = zeros
                self.zeros_field.value = str(zeros)
                self.zeros_field.update()
                self.update_device_info()
            except:
                pass

        elif message.startswith("ENTROPY:"):
            try:
                entropy = int(message.split()[1])
                self.device_info["entropy"] = entropy
                self.entropy_field.value = str(entropy)
                self.entropy_field.update()
                self.update_device_info()
            except:
                pass

        elif "MINE_START:" in message:
            self.is_mining = True
            self.update_mining_status()

        elif "MINE_RESULT:" in message or "FOUND:" in message:
            self.is_mining = False
            self.update_mining_status()
            # Extract nonce if possible
            if "encontrado:" in message:
                try:
                    nonce = int(message.split("encontrado:")[-1].strip())
                    self.device_info["last_nonce"] = nonce
                    self.update_device_info()
                except:
                    pass

        elif message.startswith("=== Reset Executado ==="):
            self.device_info.update({"zeros": 0, "entropy": 0, "last_nonce": -1})
            self.zeros_field.value = "0"
            self.entropy_field.value = "0"
            self.zeros_field.update()
            self.entropy_field.update()
            self.update_device_info()

    def update_mining_status(self):
        """Updates mining status"""
        if self.mining_status:
            if self.is_mining:
                self.mining_status.value = "MINING..."
                self.mining_status.color = ft.Colors.YELLOW_400
            else:
                self.mining_status.value = "IDLE"
                self.mining_status.color = ft.Colors.GREY_500
            self.mining_status.update()

    def send_command(self, command):
        """Send command to ESP32"""
        if not self.connected or not self.esp32:
            self.log_message("ERRO: ESP32 nao conectado", "error")
            return

        if self.esp32.send_message(command):
            self.log_message(command, "sent")
        else:
            self.log_message(f"Erro ao enviar: {command}", "error")

    def on_help_click(self, e):
        self.send_command("help")

    def on_info_click(self, e):
        self.send_command("info")

    def on_reset_click(self, e):
        self.send_command("reset")

    def on_mine_click(self, e):
        if self.is_mining:
            self.is_mining = False
            self.update_mining_status()
            self.log_message("MINE_STOP: Mining interrupted by user", "sent")
        else:
            self.send_command("mine")

    def on_set_zeros_click(self, e):
        try:
            zeros = int(self.zeros_field.value)
            self.send_command(f"zeros {zeros}")
        except ValueError:
            self.log_message("ERRO: Valor de zeros invalido", "error")

    def on_set_entropy_click(self, e):
        try:
            entropy = int(self.entropy_field.value)
            self.send_command(f"entropy {entropy}")
        except ValueError:
            self.log_message("ERRO: Valor de entropy invalido", "error")

    def clear_log(self, e):
        """Clear message log"""
        if self.log_column:
            self.log_column.controls.clear()
            self.log_column.update()
            self.log_message(
                "Terminal ready. Connect to ESP32 to start communication.", "info"
            )

    def build_ui(self, page: ft.Page):
        """Builds the user interface"""
        page.title = "ESP32 Serial Mining Interface"
        page.theme_mode = ft.ThemeMode.DARK
        page.bgcolor = ft.Colors.BLACK
        page.window_width = 1400
        page.window_height = 900
        page.padding = 15

        # Header
        header = ft.Container(
            content=ft.Row(
                [
                    ft.Text(
                        "ESP32",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.GREEN_400,
                        font_family="Courier New",
                    ),
                    ft.Text(
                        "|",
                        size=24,
                        color=ft.Colors.GREY_600,
                        font_family="Courier New",
                    ),
                    ft.Text(
                        "Serial Mining Interface",
                        size=16,
                        color=ft.Colors.WHITE,
                        font_family="Courier New",
                    ),
                    ft.Container(expand=True),
                    ft.Text(
                        time.strftime("%Y-%m-%d %H:%M:%S"),
                        size=12,
                        color=ft.Colors.GREY_600,
                        font_family="Courier New",
                    ),
                ]
            ),
            padding=ft.padding.all(10),
            border=ft.border.only(bottom=ft.border.BorderSide(1, ft.Colors.GREY_700)),
        )

        # Connection area
        available_ports = self.get_available_ports()
        self.port_dropdown = ft.Dropdown(
            label="PORTA",
            options=[ft.dropdown.Option(port) for port in available_ports],
            value=available_ports[0] if available_ports else None,
            width=200,
            bgcolor=ft.Colors.GREY_900,
            color=ft.Colors.WHITE,
            label_style=ft.TextStyle(size=10, font_family="Courier New"),
        )

        self.connect_button = ft.ElevatedButton(
            text="CONNECT",
            on_click=self.connect_esp32,
            bgcolor=ft.Colors.GREEN_900,
            color=ft.Colors.WHITE,
            style=ft.ButtonStyle(
                text_style=ft.TextStyle(size=10, font_family="Courier New")
            ),
        )

        self.status_text = ft.Text(
            "Desconectado",
            size=12,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.RED_400,
            font_family="Courier New",
        )

        connection_card = ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "CONEXAO",
                        size=12,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.WHITE,
                        font_family="Courier New",
                    ),
                    ft.Row(
                        [self.port_dropdown, self.connect_button, self.status_text],
                        spacing=10,
                    ),
                ],
                spacing=5,
            ),
            bgcolor=ft.Colors.GREY_900,
            padding=ft.padding.all(10),
            border=ft.border.all(1, ft.Colors.GREY_700),
            border_radius=5,
            width=450,
        )

        # Device Info
        self.device_info_column = ft.Column(spacing=2)

        device_info_card = ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "DEVICE INFO",
                        size=12,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.WHITE,
                        font_family="Courier New",
                    ),
                    self.device_info_column,
                ],
                spacing=5,
            ),
            bgcolor=ft.Colors.GREY_900,
            padding=ft.padding.all(10),
            border=ft.border.all(1, ft.Colors.GREY_700),
            border_radius=5,
            width=450,
            height=250,
        )

        # Mining Controls
        self.zeros_field = ft.TextField(
            label="ZEROS",
            value="0",
            width=100,
            bgcolor=ft.Colors.GREY_800,
            color=ft.Colors.WHITE,
            label_style=ft.TextStyle(size=10, font_family="Courier New"),
            text_style=ft.TextStyle(size=10, font_family="Courier New"),
        )

        self.entropy_field = ft.TextField(
            label="ENTROPY",
            value="0",
            width=100,
            bgcolor=ft.Colors.GREY_800,
            color=ft.Colors.WHITE,
            label_style=ft.TextStyle(size=10, font_family="Courier New"),
            text_style=ft.TextStyle(size=10, font_family="Courier New"),
        )

        self.mining_status = ft.Text(
            "IDLE", size=10, color=ft.Colors.GREY_500, font_family="Courier New"
        )

        mining_controls = ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "MINING CTRL",
                        size=12,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.WHITE,
                        font_family="Courier New",
                    ),
                    ft.Row(
                        [
                            self.zeros_field,
                            ft.ElevatedButton(
                                "SET Z",
                                on_click=self.on_set_zeros_click,
                                bgcolor=ft.Colors.GREY_700,
                                color=ft.Colors.WHITE,
                                style=ft.ButtonStyle(
                                    text_style=ft.TextStyle(
                                        size=9, font_family="Courier New"
                                    )
                                ),
                            ),
                        ],
                        spacing=5,
                    ),
                    ft.Row(
                        [
                            self.entropy_field,
                            ft.ElevatedButton(
                                "SET E",
                                on_click=self.on_set_entropy_click,
                                bgcolor=ft.Colors.GREY_700,
                                color=ft.Colors.WHITE,
                                style=ft.ButtonStyle(
                                    text_style=ft.TextStyle(
                                        size=9, font_family="Courier New"
                                    )
                                ),
                            ),
                        ],
                        spacing=5,
                    ),
                    ft.Row(
                        [
                            ft.ElevatedButton(
                                "MINE",
                                on_click=self.on_mine_click,
                                bgcolor=ft.Colors.GREEN_900,
                                color=ft.Colors.WHITE,
                                style=ft.ButtonStyle(
                                    text_style=ft.TextStyle(
                                        size=10, font_family="Courier New"
                                    )
                                ),
                            ),
                            ft.ElevatedButton(
                                "RESET",
                                on_click=self.on_reset_click,
                                bgcolor=ft.Colors.GREY_700,
                                color=ft.Colors.WHITE,
                                style=ft.ButtonStyle(
                                    text_style=ft.TextStyle(
                                        size=10, font_family="Courier New"
                                    )
                                ),
                            ),
                        ],
                        spacing=5,
                    ),
                    ft.Row(
                        [
                            ft.Text(
                                "Status:",
                                size=10,
                                color=ft.Colors.GREY_400,
                                font_family="Courier New",
                            ),
                            self.mining_status,
                        ]
                    ),
                ],
                spacing=8,
            ),
            bgcolor=ft.Colors.GREY_900,
            padding=ft.padding.all(10),
            border=ft.border.all(1, ft.Colors.GREY_700),
            border_radius=5,
            width=450,
            height=180,
        )

        # Left column: Connection + Device Info + Mining Controls
        left_column = ft.Column(
            [connection_card, device_info_card, mining_controls], 
            spacing=15,
            width=470
        )

        # Coluna da direita: Terminal Log
        self.log_column = ft.Column(spacing=2, scroll=ft.ScrollMode.AUTO)

        log_container = ft.Container(
            content=self.log_column,
            bgcolor=ft.Colors.BLACK,
            padding=ft.padding.all(10),
            border=ft.border.all(1, ft.Colors.GREY_700),
            border_radius=5,
            expand=True,
        )

        clear_button = ft.ElevatedButton(
            "CLEAR LOG",
            on_click=self.clear_log,
            bgcolor=ft.Colors.RED_900,
            color=ft.Colors.WHITE,
            style=ft.ButtonStyle(
                text_style=ft.TextStyle(size=10, font_family="Courier New")
            ),
        )

        right_column = ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Text(
                                "TERMINAL LOG",
                                size=12,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.WHITE,
                                font_family="Courier New",
                            ),
                            ft.Container(expand=True),
                            clear_button,
                        ]
                    ),
                    log_container,
                ],
                spacing=5,
            ),
            bgcolor=ft.Colors.GREY_900,
            padding=ft.padding.all(10),
            border=ft.border.all(1, ft.Colors.GREY_700),
            border_radius=0,
            expand=True,
        )

        # Layout principal com 2 colunas
        main_content = ft.Row(
            [left_column, right_column], 
            spacing=20, 
            expand=True,
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.START
        )

        page.add(ft.Column([header, main_content], spacing=15, expand=True))

        # Inicializar log e device info
        self.log_message(
            "Terminal ready. Connect to ESP32 to start communication.", "info"
        )
        self.update_device_info()


def main(page: ft.Page):
    app = ESP32GUI()
    app.build_ui(page)


if __name__ == "__main__":
    ft.app(target=main)
