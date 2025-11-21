#!/usr/bin/env python3
"""
Level 1 Easy Setup Wizard
Simplified 6-step wizard for basic users
⭐⭐⭐⭐ Easy Mode - USB Vault + Optional NFC
"""

import sys
import os
import json
import time
from pathlib import Path
from datetime import datetime

# Try to import appdirs, fallback to home directory
try:
    from appdirs import user_config_dir
    HAS_APPDIRS = True
except ImportError:
    HAS_APPDIRS = False

# Import shared entropy system
from chaos_entropy import ChaosEntropyCollector

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QTextEdit, QStackedWidget,
    QGroupBox, QRadioButton, QButtonGroup, QProgressBar, QFileDialog,
    QMessageBox
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt6.QtGui import QFont, QTextCursor


class EasyVaultInitializer(QThread):
    """Thread to initialize Easy Mode vault"""
    log = pyqtSignal(str)
    finished = pyqtSignal(bool)
    
    def __init__(self, vault_path):
        super().__init__()
        self.vault_path = Path(vault_path)
    
    def run(self):
        try:
            self.log.emit("📁 Creating Easy Mode vault...")
            vault_dir = self.vault_path / '.chaos_vault'
            vault_dir.mkdir(parents=True, exist_ok=True)
            
            self.log.emit("📝 Creating vault config (100k iterations)...")
            config = {
                'created': datetime.now().isoformat(),
                'version': '1.0',
                'mode': 'easy',
                'security_level': 4,
                'pbkdf2_iterations': 100000,
                'nfc_optional': True,
                'chaos_alphabet_ready': False
            }
            config_file = vault_dir / 'vault_config.json'
            with open(config_file, 'w') as f:
                json.dump(config, f, indent=2)
            
            self.log.emit("✅ Easy vault initialized!")
            self.log.emit("")
            self.log.emit("⚠️  NEXT: Chaos alphabet will be generated in Step 5")
            self.log.emit("🌪️  64-character alphabet from 30s capture")
            self.finished.emit(True)
        except Exception as e:
            self.log.emit(f"❌ Error: {str(e)}")
            self.finished.emit(False)


class SimpleCaptureWorker(QThread):
    """Enhanced 30-second chaos capture using shared entropy system"""
    log = pyqtSignal(str)
    progress = pyqtSignal(int)
    finished = pyqtSignal(str)
    
    def __init__(self, nfc_passkey=""):
        super().__init__()
        self.nfc_passkey = nfc_passkey
        # Create entropy collector with log callback
        self.collector = ChaosEntropyCollector(
            nfc_passkey=nfc_passkey,
            log_callback=self.log.emit
        )
    
    def run(self):
        try:
            import secrets
            import hashlib
            
            self.log.emit("🌪️ Starting Enhanced Chaos Capture (30 seconds)...")
            self.log.emit("📊 Collecting creative entropy sources...")
            
            # Show NFC configuration
            for line in self.collector.get_config_summary():
                self.log.emit(line)
            self.log.emit("─" * 50)
            
            self.progress.emit(10)
            
            entropy_data = []
            
            for i in range(30):
                # Base system randomness
                entropy_data.append(secrets.token_bytes(32))
                
                # Add creative entropy every 3 seconds
                if i % 3 == 0:
                    creative_entropy = self.collector.collect_creative_entropy()
                    entropy_data.append(creative_entropy)
                    self.log.emit("─" * 50)
                
                time.sleep(1)
                self.progress.emit(10 + (i * 3))
            
            self.log.emit("🔑 Generating chaos alphabet...")
            
            # Combine all entropy
            combined = b''.join(entropy_data)
            if self.nfc_passkey:
                combined += self.nfc_passkey.encode()
                self.log.emit(f"💳 NFC passkey mixed in ({len(self.nfc_passkey)} chars)")
            
            # Generate 64-character chaos alphabet
            hash_result = hashlib.sha256(combined).hexdigest()
            chaos_alphabet = hash_result[:64]
            
            self.log.emit(f"✅ Chaos alphabet: {len(chaos_alphabet)} chars")
            self.log.emit(f"🎲 Total entropy: {len(combined)} bytes")
            self.progress.emit(100)
            
            self.finished.emit(chaos_alphabet)
            
        except Exception as e:
            self.log.emit(f"❌ Error: {str(e)}")
            self.finished.emit("")


class Level1EasyWizard(QMainWindow):
    """
    Level 1 Easy Setup Wizard
    6 Steps: Security Level → Equipment → Vault → NFC → Capture → Complete
    """
    
    def __init__(self):
        super().__init__()
        self.current_step = 0
        self.vault_path = ""
        self.nfc_passkey = ""
        self.chaos_alphabet = ""
        self.vault_worker = None
        self.capture_worker = None
        
        # Setup config directory
        if HAS_APPDIRS:
            self.config_dir = Path(user_config_dir("ChaosLock", "ChaosEncryption"))
        else:
            self.config_dir = Path.home() / ".chaoslock"
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.config_file = self.config_dir / "wizard_settings.json"
        
        self.load_saved_path()
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("⭐⭐⭐⭐ Easy Setup Wizard - Level 1")
        self.setGeometry(100, 100, 900, 650)
        
        # Styling will be added in next chunk
        self.apply_styles()
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Header
        header = QLabel("⭐ EASY SETUP WIZARD - LEVEL 1")
        header.setFont(QFont("Arial", 22, QFont.Weight.Bold))
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setStyleSheet("color: #00ff88; padding: 15px; background-color: #1a1f3a; border-radius: 10px;")
        main_layout.addWidget(header)
        
        # Progress indicator
        progress_layout = QHBoxLayout()
        self.step_labels = []
        steps = ["1️⃣ Mode", "2️⃣ USB", "3️⃣ Vault", "4️⃣ NFC", "5️⃣ Capture", "6️⃣ Done"]
        
        for i, step in enumerate(steps):
            label = QLabel(step)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setStyleSheet("color: #666666; padding: 5px; font-size: 12px;")
            self.step_labels.append(label)
            progress_layout.addWidget(label)
        
        main_layout.addLayout(progress_layout)
        
        # Stacked widget for steps
        self.stack = QStackedWidget()
        main_layout.addWidget(self.stack)
        
        # Create all 6 steps (will be added in next chunks)
        self.create_step1_security_level()
        self.create_step2_equipment()
        self.create_step3_vault()
        self.create_step4_nfc()
        self.create_step5_capture()
        self.create_step6_complete()
        
        # Navigation buttons
        nav_layout = QHBoxLayout()
        
        self.back_btn = QPushButton("⬅️ Back")
        self.back_btn.clicked.connect(self.go_back)
        self.back_btn.setEnabled(False)
        nav_layout.addWidget(self.back_btn)
        
        nav_layout.addStretch()
        
        self.next_btn = QPushButton("Next ➡️")
        self.next_btn.clicked.connect(self.go_next)
        nav_layout.addWidget(self.next_btn)
        
        main_layout.addLayout(nav_layout)
        
        # Update initial step
        self.update_step_indicator()
    
    def apply_styles(self):
        """Apply dark theme styling"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #0a0e27;
            }
            QWidget {
                background-color: #0a0e27;
                color: #ffffff;
            }
            QGroupBox {
                border: 2px solid #00ff88;
                border-radius: 5px;
                margin-top: 10px;
                padding: 15px;
                font-weight: bold;
                color: #00d4ff;
            }
            QPushButton {
                background-color: #00ff88;
                color: black;
                border: none;
                padding: 12px;
                border-radius: 5px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #00d4ff;
            }
            QPushButton:disabled {
                background-color: #444444;
                color: #888888;
            }
            QLineEdit {
                background-color: #2a2f4a;
                color: #ffffff;
                border: 2px solid #00ff88;
                padding: 8px;
                border-radius: 3px;
            }
            QTextEdit {
                background-color: #1a1f3a;
                color: #00ff88;
                border: 2px solid #00ff88;
                border-radius: 3px;
                font-family: monospace;
            }
            QRadioButton {
                color: #ffffff;
                spacing: 10px;
            }
            QRadioButton::indicator {
                width: 20px;
                height: 20px;
            }
        """)
    
    def create_step1_security_level(self):
        """Step 1: Security Level Selection"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Title
        title = QLabel("Step 1: Choose Your Security Mode")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title.setStyleSheet("color: #00ff88; padding: 10px;")
        layout.addWidget(title)
        
        # Description
        desc = QLabel("You've selected Easy Mode - the simplest setup for basic encryption")
        desc.setStyleSheet("color: #aaaaaa; padding: 5px;")
        layout.addWidget(desc)
        
        # Easy mode info box
        info_box = QGroupBox("⭐⭐⭐⭐ Easy Mode")
        info_layout = QVBoxLayout()
        
        features = [
            "✅ USB Vault Drive (required)",
            "📱 NFC Tag (optional - can type passkey instead)",
            "⏱️  30-second setup time",
            "🔒 Basic encryption (100,000 iterations)",
            "👍 Perfect for personal files"
        ]
        
        for feature in features:
            label = QLabel(feature)
            label.setStyleSheet("color: #ffffff; padding: 3px;")
            info_layout.addWidget(label)
        
        info_box.setLayout(info_layout)
        layout.addWidget(info_box)
        
        # Info about other modes
        other_modes = QLabel(
            "💡 Tip: For stronger security, use the Standard or Maximum wizards\n"
            "   (Standard = 5 stars, Maximum = 6 stars)"
        )
        other_modes.setStyleSheet("color: #888888; padding: 10px; font-style: italic;")
        layout.addWidget(other_modes)
        
        layout.addStretch()
        self.stack.addWidget(widget)
    
    def create_step2_equipment(self):
        """Step 2: Equipment Selection (USB Vault)"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Title
        title = QLabel("Step 2: Select Your USB Vault")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title.setStyleSheet("color: #00ff88; padding: 10px;")
        layout.addWidget(title)
        
        # Instructions
        instructions = QLabel(
            "Connect your USB drive and select it below.\n"
            "This will store your encryption vault."
        )
        instructions.setStyleSheet("color: #aaaaaa; padding: 5px;")
        layout.addWidget(instructions)
        
        # USB selection
        usb_group = QGroupBox("USB Vault Drive")
        usb_layout = QVBoxLayout()
        
        path_layout = QHBoxLayout()
        path_layout.addWidget(QLabel("Vault Path:"))
        
        self.vault_path_input = QLineEdit()
        self.vault_path_input.setPlaceholderText("/Volumes/YOUR_USB_NAME")
        # Set saved path if available
        if self.vault_path:
            self.vault_path_input.setText(self.vault_path)
        path_layout.addWidget(self.vault_path_input)
        
        browse_btn = QPushButton("📁 Browse...")
        browse_btn.clicked.connect(self.browse_vault_path)
        path_layout.addWidget(browse_btn)
        
        usb_layout.addLayout(path_layout)
        
        # Save path checkbox
        from PyQt6.QtWidgets import QCheckBox
        self.save_path_checkbox = QCheckBox("💾 Remember this path for next time")
        self.save_path_checkbox.setStyleSheet("color: #aaaaaa; padding: 5px;")
        self.save_path_checkbox.setChecked(True)
        usb_layout.addWidget(self.save_path_checkbox)
        
        # Verify button
        self.verify_usb_btn = QPushButton("✅ Verify USB Drive")
        self.verify_usb_btn.clicked.connect(self.verify_usb_drive)
        usb_layout.addWidget(self.verify_usb_btn)
        
        # Status
        self.usb_status = QLabel("⏳ Waiting for USB selection...")
        self.usb_status.setStyleSheet("color: #ffaa00; padding: 5px;")
        usb_layout.addWidget(self.usb_status)
        
        usb_group.setLayout(usb_layout)
        layout.addWidget(usb_group)
        
        layout.addStretch()
        self.stack.addWidget(widget)
    
    def create_step3_vault(self):
        """Step 3: Configure USB Vault"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        title = QLabel("Step 3: Initialize Vault")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title.setStyleSheet("color: #00ff88; padding: 10px;")
        layout.addWidget(title)
        
        vault_group = QGroupBox("Vault Configuration")
        vault_layout = QVBoxLayout()
        
        self.vault_info_label = QLabel("Vault Path: Not selected")
        self.vault_info_label.setStyleSheet("color: #ffffff; padding: 5px;")
        vault_layout.addWidget(self.vault_info_label)
        
        self.init_vault_btn = QPushButton("🚀 Initialize Vault")
        self.init_vault_btn.clicked.connect(self.initialize_vault)
        vault_layout.addWidget(self.init_vault_btn)
        
        self.vault_log = QTextEdit()
        self.vault_log.setReadOnly(True)
        self.vault_log.setMaximumHeight(200)
        vault_layout.addWidget(self.vault_log)
        
        vault_group.setLayout(vault_layout)
        layout.addWidget(vault_group)
        
        layout.addStretch()
        self.stack.addWidget(widget)
    
    def create_step4_nfc(self):
        """Step 4: NFC Tag Scan (Optional)"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        title = QLabel("Step 4: NFC Tag (Optional)")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title.setStyleSheet("color: #00ff88; padding: 10px;")
        layout.addWidget(title)
        
        instructions = QLabel(
            "In Easy Mode, you can:\n"
            "• Scan an NFC tag for extra security\n"
            "• Type a passkey manually\n"
            "• Skip this step entirely"
        )
        instructions.setStyleSheet("color: #aaaaaa; padding: 5px;")
        layout.addWidget(instructions)
        
        nfc_group = QGroupBox("NFC / Passkey Options")
        nfc_layout = QVBoxLayout()
        
        passkey_layout = QHBoxLayout()
        passkey_layout.addWidget(QLabel("Passkey:"))
        
        self.nfc_passkey_input = QLineEdit()
        self.nfc_passkey_input.setPlaceholderText("Optional: Type passkey or scan NFC")
        self.nfc_passkey_input.setEchoMode(QLineEdit.EchoMode.Password)
        passkey_layout.addWidget(self.nfc_passkey_input)
        
        show_btn = QPushButton("👁️")
        show_btn.setMaximumWidth(50)
        show_btn.clicked.connect(self.toggle_passkey_visibility)
        passkey_layout.addWidget(show_btn)
        
        nfc_layout.addLayout(passkey_layout)
        
        skip_btn = QPushButton("⏭️ Skip NFC")
        skip_btn.clicked.connect(self.skip_nfc)
        skip_btn.setStyleSheet("background-color: #666666;")
        nfc_layout.addWidget(skip_btn)
        
        self.nfc_status = QLabel("💡 Optional: Add passkey for extra security")
        self.nfc_status.setStyleSheet("color: #aaaaaa; padding: 5px;")
        nfc_layout.addWidget(self.nfc_status)
        
        nfc_group.setLayout(nfc_layout)
        layout.addWidget(nfc_group)
        
        layout.addStretch()
        self.stack.addWidget(widget)
    
    def create_step5_capture(self):
        """Step 5: Chaos Capture (30 seconds)"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        title = QLabel("Step 5: Chaos Capture")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title.setStyleSheet("color: #00ff88; padding: 10px;")
        layout.addWidget(title)
        
        instructions = QLabel(
            "Generating your encryption key from creative entropy sources:\n"
            "🖱️ Mouse position • 💻 System metrics • ⏱️ Timing jitter\n"
            "🌐 Network stats • 🔢 Process IDs • 🎲 Cryptographic RNG"
        )
        instructions.setStyleSheet("color: #aaaaaa; padding: 5px;")
        layout.addWidget(instructions)
        
        capture_group = QGroupBox("Capture Progress")
        capture_layout = QVBoxLayout()
        
        self.capture_progress = QProgressBar()
        self.capture_progress.setValue(0)
        capture_layout.addWidget(self.capture_progress)
        
        self.capture_log = QTextEdit()
        self.capture_log.setReadOnly(True)
        self.capture_log.setMaximumHeight(250)
        capture_layout.addWidget(self.capture_log)
        
        self.start_capture_btn = QPushButton("🌪️ Start Capture")
        self.start_capture_btn.clicked.connect(self.start_capture)
        capture_layout.addWidget(self.start_capture_btn)
        
        capture_group.setLayout(capture_layout)
        layout.addWidget(capture_group)
        
        layout.addStretch()
        self.stack.addWidget(widget)
    
    def create_step6_complete(self):
        """Step 6: Setup Complete"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        title = QLabel("✅ Setup Complete!")
        title.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        title.setStyleSheet("color: #00ff88; padding: 10px;")
        layout.addWidget(title)
        
        success_group = QGroupBox("Your Vault is Ready")
        success_layout = QVBoxLayout()
        
        self.complete_summary = QTextEdit()
        self.complete_summary.setReadOnly(True)
        self.complete_summary.setMaximumHeight(300)
        success_layout.addWidget(self.complete_summary)
        
        success_group.setLayout(success_layout)
        layout.addWidget(success_group)
        
        close_btn = QPushButton("🎉 Close Wizard")
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)
        
        layout.addStretch()
        self.stack.addWidget(widget)
    
    # Navigation methods
    def update_step_indicator(self):
        """Update the step progress indicator"""
        for i, label in enumerate(self.step_labels):
            if i == self.current_step:
                label.setStyleSheet("color: #00ff88; padding: 5px; font-size: 12px; font-weight: bold;")
            elif i < self.current_step:
                label.setStyleSheet("color: #00d4ff; padding: 5px; font-size: 12px;")
            else:
                label.setStyleSheet("color: #666666; padding: 5px; font-size: 12px;")
    
    def go_next(self):
        """Go to next step"""
        # Validate before advancing from Step 2
        if self.current_step == 1 and not self.vault_path:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.warning(
                self,
                "USB Not Verified",
                "Please select and verify your USB drive before proceeding."
            )
            return
        
        if self.current_step < self.stack.count() - 1:
            self.current_step += 1
            self.stack.setCurrentIndex(self.current_step)
            self.update_step_indicator()
            self.back_btn.setEnabled(True)
            
            if self.current_step == 2:
                if self.vault_path:
                    self.vault_info_label.setText(f"Vault Path: {self.vault_path}")
                else:
                    self.vault_info_label.setText("Vault Path: Not selected - Go back to Step 2")
    
    def go_back(self):
        """Go to previous step"""
        if self.current_step > 0:
            self.current_step -= 1
            self.stack.setCurrentIndex(self.current_step)
            self.update_step_indicator()
            if self.current_step == 0:
                self.back_btn.setEnabled(False)
    
    def load_saved_path(self):
        """Load previously saved vault path"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    self.vault_path = config.get('vault_path', '')
        except Exception as e:
            print(f"Could not load saved path: {e}")
            self.vault_path = ''
    
    def save_vault_path(self, path):
        """Save vault path to config file"""
        try:
            config = {'vault_path': path}
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
        except Exception as e:
            print(f"Could not save path: {e}")
    
    def browse_vault_path(self):
        """Browse for USB vault path"""
        path = QFileDialog.getExistingDirectory(self, "Select USB Vault Drive", "/Volumes")
        if path:
            self.vault_path_input.setText(path)
    
    def verify_usb_drive(self):
        """Verify USB drive is accessible"""
        path = self.vault_path_input.text()
        if not path:
            self.usb_status.setText("❌ Please select a path first")
            self.usb_status.setStyleSheet("color: #ff0000; padding: 5px;")
            return
        
        vault_path = Path(path)
        if not vault_path.exists():
            self.usb_status.setText("❌ Path does not exist")
            self.usb_status.setStyleSheet("color: #ff0000; padding: 5px;")
            return
        
        if not os.access(path, os.W_OK):
            self.usb_status.setText("❌ Path is not writable")
            self.usb_status.setStyleSheet("color: #ff0000; padding: 5px;")
            return
        
        self.vault_path = path
        self.usb_status.setText("✅ USB drive verified!")
        self.usb_status.setStyleSheet("color: #00ff88; padding: 5px;")
        
        # Save path if checkbox is checked
        if self.save_path_checkbox.isChecked():
            self.save_vault_path(path)
    
    def initialize_vault(self):
        """Initialize vault structure"""
        if not self.vault_path:
            self.vault_log.append("❌ No vault path selected")
            return
        
        self.init_vault_btn.setEnabled(False)
        self.vault_worker = EasyVaultInitializer(self.vault_path)
        self.vault_worker.log.connect(self.vault_log.append)
        self.vault_worker.finished.connect(self.on_vault_initialized)
        self.vault_worker.start()
    
    def on_vault_initialized(self, success):
        """Handle vault initialization completion"""
        self.init_vault_btn.setEnabled(True)
        if success:
            self.vault_log.append("\n🎉 Ready to proceed!")
    
    def toggle_passkey_visibility(self):
        """Toggle passkey visibility"""
        if self.nfc_passkey_input.echoMode() == QLineEdit.EchoMode.Password:
            self.nfc_passkey_input.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.nfc_passkey_input.setEchoMode(QLineEdit.EchoMode.Password)
    
    def skip_nfc(self):
        """Skip NFC step"""
        self.nfc_passkey = ""
        self.nfc_status.setText("⏭️ Skipped - using system entropy only")
        self.nfc_status.setStyleSheet("color: #00d4ff; padding: 5px;")
    
    def start_capture(self):
        """Start chaos capture"""
        self.nfc_passkey = self.nfc_passkey_input.text()
        self.start_capture_btn.setEnabled(False)
        self.capture_log.clear()
        self.capture_progress.setValue(0)
        
        self.capture_worker = SimpleCaptureWorker(self.nfc_passkey)
        self.capture_worker.log.connect(self.capture_log.append)
        self.capture_worker.progress.connect(self.capture_progress.setValue)
        self.capture_worker.finished.connect(self.on_capture_finished)
        self.capture_worker.start()
    
    def on_capture_finished(self, chaos_alphabet):
        """Handle capture completion"""
        self.start_capture_btn.setEnabled(True)
        if chaos_alphabet:
            self.chaos_alphabet = chaos_alphabet
            self.save_chaos_alphabet()
            self.capture_log.append("\n✅ Saved to vault!")
    
    def save_chaos_alphabet(self):
        """Save chaos alphabet to vault"""
        try:
            self.capture_log.append("")
            self.capture_log.append("=" * 50)
            self.capture_log.append("🌪️  CHAOS ALPHABET GENERATED!")
            self.capture_log.append("=" * 50)
            self.capture_log.append(f"📏 Length: {len(self.chaos_alphabet)} characters")
            self.capture_log.append(f"🔑 Preview: {self.chaos_alphabet[:32]}...")
            self.capture_log.append("")
            
            vault_dir = Path(self.vault_path) / '.chaos_vault'
            alphabet_file = vault_dir / 'chaos_alphabet.txt'
            with open(alphabet_file, 'w') as f:
                f.write(self.chaos_alphabet)
            
            # Update vault config to mark if passkey was used
            config_file = vault_dir / 'vault_config.json'
            if config_file.exists():
                with open(config_file, 'r') as f:
                    vault_config = json.load(f)
                vault_config['requires_passkey'] = bool(self.nfc_passkey)
                vault_config['chaos_alphabet_ready'] = True
                with open(config_file, 'w') as f:
                    json.dump(vault_config, f, indent=2)
            
            self.capture_log.append(f"💾 Saved to: {alphabet_file}")
            self.capture_log.append("✅ Chaos alphabet ready for encryption!")
            if self.nfc_passkey:
                self.capture_log.append("🔐 Vault requires passkey to unlock")
            else:
                self.capture_log.append("🔓 Vault has no passkey requirement")
            self.capture_log.append("=" * 50)
            
            summary = f"""🎉 Setup Complete!

📁 Vault: {self.vault_path}
🔑 Alphabet: {self.chaos_alphabet[:32]}...
📊 Level: Easy Mode (⭐⭐⭐⭐)
🔒 Iterations: 100,000

Next Steps:
1. Keep USB drive safe
2. {'Remember NFC passkey' if self.nfc_passkey else 'No NFC passkey'}
3. Use Folder Lock GUI to encrypt
4. Always backup data

Ready to use!"""
            self.complete_summary.setText(summary.strip())
        except Exception as e:
            self.capture_log.append(f"❌ Error: {str(e)}")


def main():
    app = QApplication(sys.argv)
    wizard = Level1EasyWizard()
    wizard.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
