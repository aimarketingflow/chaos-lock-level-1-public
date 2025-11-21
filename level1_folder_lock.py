#!/usr/bin/env python3
"""
Level 1 Easy Folder Lock/Unlock GUI
Simple interface for beginners
⭐⭐⭐⭐ Easy Mode - USB + Optional NFC
"""

import sys
import os
from pathlib import Path
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QTextEdit, QTabWidget,
    QGroupBox, QProgressBar, QFileDialog, QMessageBox, QComboBox
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt6.QtGui import QFont

# Import encryption modules
from folder_lock_cli import FolderLockManager
from level1_crypto import Level1Crypto
import json


class LockWorker(QThread):
    """Worker thread for locking folders"""
    log = pyqtSignal(str)
    progress = pyqtSignal(int)
    finished = pyqtSignal(bool, str)
    
    def __init__(self, folder_path, usb_path, passkey):
        super().__init__()
        self.folder_path = folder_path
        self.usb_path = usb_path
        self.passkey = passkey
    
    def run(self):
        try:
            self.log.emit(f"🔒 Locking folder: {self.folder_path}")
            self.progress.emit(10)
            
            # Verify vault exists
            vault_dir = Path(self.usb_path) / '.chaos_vault'
            if not vault_dir.exists():
                self.log.emit("❌ No vault found on USB!")
                self.finished.emit(False, "Vault not found")
                return
            
            self.log.emit("✅ Vault found")
            self.progress.emit(20)
            
            # Load chaos alphabet
            alphabet_file = vault_dir / 'chaos_alphabet.txt'
            if not alphabet_file.exists():
                self.log.emit("❌ Chaos alphabet not found!")
                self.finished.emit(False, "Run wizard first")
                return
            
            with open(alphabet_file, 'r') as f:
                chaos_alphabet = f.read().strip()
            
            self.log.emit(f"✅ Chaos alphabet loaded ({len(chaos_alphabet)} chars)")
            self.progress.emit(30)
            
            # Initialize crypto with 100k iterations (Easy Mode)
            self.log.emit("🔒 Initializing Easy encryption (100k iterations)...")
            self.log.emit(f"🔐 Using vault passkey for encryption")
            
            crypto = Level1Crypto(
                nfc_passkey=self.passkey,
                alphabet_salt=chaos_alphabet.encode()
            )
            self.progress.emit(40)
            
            # Initialize folder lock manager with Level 1 registry
            manager = FolderLockManager(Path(self.usb_path))
            manager.locked_folders_file = manager.vault_dir / 'level1_locked_folders.json'
            manager.load_locked_folders()
            
            # Lock the folder
            self.log.emit("🌪️ Encrypting and locking folder...")
            self.progress.emit(50)
            
            success = manager.lock_folder(
                Path(self.folder_path),
                crypto,
                progress_callback=lambda count, total, size, total_size, name, eta: self.log.emit(f"   Progress: {count}/{total} files")
            )
            
            if success:
                self.log.emit("✅ Folder locked successfully!")
                self.progress.emit(100)
                self.finished.emit(True, "Folder locked with Easy Mode (100k iterations)")
            else:
                self.log.emit("❌ Failed to lock folder")
                self.finished.emit(False, "Lock operation failed")
            
        except Exception as e:
            self.log.emit(f"❌ Error: {str(e)}")
            self.finished.emit(False, str(e))


class UnlockWorker(QThread):
    """Worker thread for unlocking folders"""
    log = pyqtSignal(str)
    progress = pyqtSignal(int)
    finished = pyqtSignal(bool, str)
    
    def __init__(self, folder_path, usb_path, folder_id, passkey=None):
        super().__init__()
        self.folder_path = folder_path
        self.usb_path = usb_path
        self.folder_id = folder_id
        self.passkey = passkey
    
    def run(self):
        try:
            self.log.emit(f"🔓 Unlocking folder: {self.folder_path}")
            self.progress.emit(10)
            
            # Verify vault
            vault_dir = Path(self.usb_path) / '.chaos_vault'
            if not vault_dir.exists():
                self.log.emit("❌ No vault found!")
                self.finished.emit(False, "Vault not found")
                return
            
            self.log.emit("✅ Vault found")
            self.progress.emit(20)
            
            # Load chaos alphabet
            alphabet_file = vault_dir / 'chaos_alphabet.txt'
            if not alphabet_file.exists():
                self.log.emit("❌ Chaos alphabet missing!")
                self.finished.emit(False, "Alphabet not found")
                return
            
            with open(alphabet_file, 'r') as f:
                chaos_alphabet = f.read().strip()
            
            self.log.emit(f"✅ Chaos alphabet loaded ({len(chaos_alphabet)} chars)")
            self.progress.emit(30)
            
            # Initialize crypto with 100k iterations
            self.log.emit("🔓 Initializing Easy decryption (100k iterations)...")
            self.log.emit(f"🔐 Using vault passkey for decryption")
            
            crypto = Level1Crypto(
                nfc_passkey=self.passkey,
                alphabet_salt=chaos_alphabet.encode()
            )
            self.progress.emit(40)
            
            # Initialize folder lock manager with Level 1 registry
            manager = FolderLockManager(Path(self.usb_path))
            manager.locked_folders_file = manager.vault_dir / 'level1_locked_folders.json'
            manager.load_locked_folders()
            
            self.log.emit(f"✅ Using folder ID: {self.folder_id}")
            self.progress.emit(50)
            
            # Unlock the folder
            self.log.emit("🌪️ Decrypting and unlocking folder...")
            success = manager.unlock_folder(
                self.folder_id, 
                crypto,
                progress_callback=lambda count, total, size, total_size, name, eta: self.log.emit(f"   Progress: {count}/{total} files - {name}")
            )
            
            if success:
                self.log.emit("✅ Folder unlocked successfully!")
                self.progress.emit(100)
                self.finished.emit(True, "Folder unlocked with Easy Mode")
            else:
                self.log.emit("❌ Failed to unlock folder")
                self.finished.emit(False, "Unlock operation failed")
            
        except Exception as e:
            self.log.emit(f"❌ Error: {str(e)}")
            self.finished.emit(False, str(e))


class Level1FolderLock(QMainWindow):
    """
    Level 1 Easy Folder Lock/Unlock GUI
    Simple interface for locking and unlocking folders
    """
    
    def __init__(self):
        super().__init__()
        self.lock_worker = None
        self.unlock_worker = None
        self.config_file = Path.home() / '.level1_folder_lock_config.json'
        self.load_settings()
        self.usb_path = ""
        self.passkey = ""
        self.init_ui()
        self.apply_saved_settings()
    
    def load_settings(self):
        """Load saved settings"""
        self.settings = {}
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    self.settings = json.load(f)
            except Exception as e:
                print(f"Error loading settings: {e}")
    
    def save_settings_to_file(self):
        """Save current USB path settings"""
        try:
            usb_path = self.lock_usb_dropdown.currentData()
            if not usb_path:
                usb_path = self.lock_usb_dropdown.currentText()
            
            if not usb_path or usb_path.startswith("--"):
                QMessageBox.warning(self, "No Path", "Please select a USB vault first!")
                return
            
            self.settings['usb_path'] = usb_path
            self.settings['saved'] = True
            
            with open(self.config_file, 'w') as f:
                json.dump(self.settings, f, indent=2)
            
            QMessageBox.information(self, "Saved", f"✅ USB path saved as default:\n{usb_path}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error saving settings: {e}")
    
    def save_folder_path(self):
        """Save current folder path as default"""
        try:
            folder_path = self.lock_folder_input.text()
            if not folder_path:
                QMessageBox.warning(self, "No Path", "Please select a folder first!")
                return
            
            # Get the parent directory (so it opens to that location)
            folder_parent = str(Path(folder_path).parent)
            
            self.settings['default_folder_path'] = folder_parent
            
            with open(self.config_file, 'w') as f:
                json.dump(self.settings, f, indent=2)
            
            QMessageBox.information(self, "Saved", f"✅ Default folder path saved:\n{folder_parent}\n\nBrowse will now open to this location.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error saving folder path: {e}")
    
    def apply_saved_settings(self):
        """Apply saved settings to UI"""
        # Dropdowns will auto-detect, no need to apply saved settings
        pass
    
    def detect_usb_vaults(self, dropdown):
        """Detect USB drives with chaos vaults"""
        try:
            dropdown.clear()
            
            # Get all volumes
            volumes_path = "/Volumes"
            if not os.path.exists(volumes_path):
                dropdown.addItem("-- No volumes found --")
                return
            
            volumes = [v for v in os.listdir(volumes_path) if not v.startswith('.')]
            excluded = ['Macintosh HD', 'Preboot', 'Recovery', 'VM', 'Data', 'Update']
            usb_volumes = [v for v in volumes if v not in excluded]
            
            if not usb_volumes:
                dropdown.addItem("-- No USB drives detected --")
                return
            
            # Check which ones have chaos vaults
            vault_count = 0
            for volume in usb_volumes:
                volume_path = Path(f"/Volumes/{volume}")
                vault_dir = volume_path / '.chaos_vault'
                
                if vault_dir.exists():
                    # Check if it has a chaos alphabet (valid vault)
                    alphabet_file = vault_dir / 'chaos_alphabet.txt'
                    if alphabet_file.exists():
                        display_text = f"✅ {volume} (has vault)"
                        dropdown.addItem(display_text, str(volume_path))
                        vault_count += 1
                    else:
                        display_text = f"⚠️  {volume} (incomplete vault)"
                        dropdown.addItem(display_text, str(volume_path))
                else:
                    display_text = f"📁 {volume} (no vault)"
                    dropdown.addItem(display_text, str(volume_path))
            
            if vault_count == 0:
                dropdown.insertItem(0, "-- No vaults found (run wizard first) --")
                dropdown.setCurrentIndex(0)
            
        except Exception as e:
            dropdown.clear()
            dropdown.addItem(f"-- Error: {str(e)[:30]} --")
    
    def load_locked_folders_list(self):
        """Load locked folders from registry into dropdown"""
        usb_path = self.unlock_usb_dropdown.currentData()
        if not usb_path:
            usb_path = self.unlock_usb_dropdown.currentText()
        
        if not usb_path or usb_path.startswith("--"):
            QMessageBox.warning(self, "No USB Vault", "Please select a USB vault from the dropdown first!")
            return
        
        try:
            vault_path = Path(usb_path)
            vault_dir = vault_path / '.chaos_vault'
            registry_file = vault_dir / 'level1_locked_folders.json'
            
            self.unlock_folder_dropdown.clear()
            
            if not registry_file.exists():
                self.unlock_folder_dropdown.addItem("-- No locked folders found --")
                self.unlock_folder_info.setText("📭 No folders in Level 1 registry")
                return
            
            with open(registry_file, 'r') as f:
                locked_folders = json.load(f)
            
            if not locked_folders:
                self.unlock_folder_dropdown.addItem("-- No locked folders found --")
                self.unlock_folder_info.setText("📭 No folders in Level 1 registry")
                return
            
            # Add locked folders to dropdown
            locked_count = 0
            for folder_id, info in locked_folders.items():
                if info.get('status') == 'locked':
                    name = info.get('original_name', 'Unknown')
                    path = info.get('encrypted_path', info.get('original_path', 'Unknown'))
                    display_text = f"🔒 {name} ({path})"
                    self.unlock_folder_dropdown.addItem(display_text, folder_id)
                    locked_count += 1
            
            if locked_count == 0:
                self.unlock_folder_dropdown.addItem("-- No locked folders (all unlocked) --")
                self.unlock_folder_info.setText("✅ All folders are unlocked")
            else:
                self.unlock_folder_info.setText(f"✅ Found {locked_count} locked folder(s)")
            
        except Exception as e:
            self.unlock_folder_dropdown.clear()
            self.unlock_folder_dropdown.addItem("-- Error loading registry --")
            self.unlock_folder_info.setText(f"❌ Error: {str(e)[:50]}")
    
    def cleanup_registry(self):
        """Remove folders from registry that no longer exist"""
        usb_path = self.registry_usb_dropdown.currentData()
        if not usb_path:
            usb_path = self.registry_usb_dropdown.currentText()
        
        if not usb_path or usb_path.startswith("--"):
            QMessageBox.warning(self, "No Vault", "Please select a USB vault from the dropdown first!")
            return
        
        try:
            vault_path = Path(usb_path)
            vault_dir = vault_path / '.chaos_vault'
            registry_file = vault_dir / 'level1_locked_folders.json'
            
            if not registry_file.exists():
                QMessageBox.information(self, "No Registry", "No registry file found.")
                return
            
            with open(registry_file, 'r') as f:
                locked_folders = json.load(f)
            
            if not locked_folders:
                QMessageBox.information(self, "Empty", "Registry is already empty.")
                return
            
            # Check which folders don't exist
            to_remove = []
            for folder_id, info in locked_folders.items():
                encrypted_path = info.get('encrypted_path', '')
                if not Path(encrypted_path).exists():
                    to_remove.append((folder_id, info.get('original_name', 'Unknown')))
            
            if not to_remove:
                QMessageBox.information(self, "All Good", "All folders in registry exist!")
                return
            
            # Confirm removal
            names = '\n'.join([f"• {name}" for _, name in to_remove])
            reply = QMessageBox.question(
                self,
                "Confirm Cleanup",
                f"Remove {len(to_remove)} missing folder(s) from registry?\n\n{names}",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                for folder_id, _ in to_remove:
                    del locked_folders[folder_id]
                
                with open(registry_file, 'w') as f:
                    json.dump(locked_folders, f, indent=2)
                
                QMessageBox.information(self, "Cleaned", f"Removed {len(to_remove)} missing folder(s) from registry.")
                self.refresh_registry()
        
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error cleaning registry: {e}")
    
    def refresh_registry(self):
        """Refresh the folder registry display"""
        usb_path = self.registry_usb_dropdown.currentData()
        if not usb_path:
            usb_path = self.registry_usb_dropdown.currentText()
        
        if not usb_path or usb_path.startswith("--"):
            self.registry_display.setText("⚠️  Please select USB vault from dropdown and click Refresh")
            return
        
        try:
            vault_path = Path(usb_path)
            vault_dir = vault_path / '.chaos_vault'
            registry_file = vault_dir / 'level1_locked_folders.json'
            
            self.registry_display.clear()
            
            # Header
            html = """
            <style>
                body { background-color: #0a0e27; color: #00ff88; font-family: monospace; }
                table { width: 100%; border-collapse: collapse; margin: 10px 0; }
                th { background-color: #1a2f1a; color: #00ff88; padding: 8px; text-align: left; border: 1px solid #00ff88; }
                td { padding: 8px; border: 1px solid #00ff88; }
                .locked { color: #ff6600; }
                .unlocked { color: #00ff88; }
                .header { color: #00ff88; font-size: 16px; font-weight: bold; margin: 10px 0; }
            </style>
            """
            
            html += f'<div class="header">📋 LEVEL 1 EASY - FOLDER REGISTRY</div>'
            html += f'<div>📁 Vault: {usb_path}</div><br>'
            
            if not registry_file.exists():
                html += '<div>📭 No folders in Level 1 registry</div>'
                self.registry_display.setHtml(html)
                return
            
            import json
            with open(registry_file, 'r') as f:
                locked_folders = json.load(f)
            
            if not locked_folders:
                html += '<div>📭 No folders in Level 1 registry</div>'
                self.registry_display.setHtml(html)
                return
            
            locked_count = 0
            unlocked_count = 0
            
            # Table
            html += '<table>'
            html += '<tr><th>Status</th><th>Name</th><th>Path</th><th>Locked Date</th><th>Files</th></tr>'
            
            for folder_id, info in locked_folders.items():
                status = info.get('status', 'unknown')
                if status == 'locked':
                    locked_count += 1
                    status_icon = '🔒 LOCKED'
                    status_class = 'locked'
                else:
                    unlocked_count += 1
                    status_icon = '🔓 UNLOCKED'
                    status_class = 'unlocked'
                
                name = info.get('original_name', 'N/A')
                path = info.get('original_path', 'N/A')
                locked_date = info.get('locked_date', 'N/A')[:19] if info.get('locked_date') else 'N/A'
                files = info.get('files_encrypted', 0)
                
                html += f'<tr class="{status_class}">'
                html += f'<td>{status_icon}</td>'
                html += f'<td>{name}</td>'
                html += f'<td>{path}</td>'
                html += f'<td>{locked_date}</td>'
                html += f'<td>{files}</td>'
                html += '</tr>'
            
            html += '</table>'
            html += f'<br><div class="header">📊 Summary: {locked_count} locked, {unlocked_count} unlocked</div>'
            
            self.registry_display.setHtml(html)
            
        except Exception as e:
            self.registry_display.setText(f"❌ Error loading registry:\n{str(e)}")
    
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("⭐ Level 1 Easy Folder Lock")
        self.setGeometry(100, 100, 800, 600)
        
        self.apply_styles()
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Header
        header = QLabel("⭐ EASY FOLDER LOCK - LEVEL 1")
        header.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setStyleSheet("color: #00ff88; padding: 15px; background-color: #1a1f3a; border-radius: 10px;")
        main_layout.addWidget(header)
        
        # Tabs for Lock, Unlock, and Registry
        self.tabs = QTabWidget()
        self.tabs.addTab(self.create_lock_tab(), "🔒 Lock Folder")
        self.tabs.addTab(self.create_unlock_tab(), "🔓 Unlock Folder")
        self.tabs.addTab(self.create_registry_tab(), "📋 Folder Registry")
        main_layout.addWidget(self.tabs)
    
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
            QTabWidget::pane {
                border: 2px solid #00ff88;
                border-radius: 5px;
            }
            QTabBar::tab {
                background-color: #2a2f4a;
                color: #ffffff;
                padding: 10px 20px;
                margin: 2px;
                border-radius: 3px;
            }
            QTabBar::tab:selected {
                background-color: #00ff88;
                color: #000000;
            }
            QComboBox {
                background-color: #2a2f4a;
                color: #ffffff;
                border: 2px solid #00ff88;
                padding: 8px;
                border-radius: 3px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                border: none;
            }
            QComboBox QAbstractItemView {
                background-color: #2a2f4a;
                color: #ffffff;
                selection-background-color: #00ff88;
                selection-color: #000000;
            }
        """)
    
    def create_lock_tab(self):
        """Create the Lock Folder tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # USB Vault section
        usb_group = QGroupBox("Step 1: USB Vault")
        usb_layout = QVBoxLayout()
        
        usb_path_layout = QHBoxLayout()
        usb_path_layout.addWidget(QLabel("USB Vault:"))
        self.lock_usb_dropdown = QComboBox()
        self.lock_usb_dropdown.setMinimumWidth(400)
        self.lock_usb_dropdown.addItem("-- Detecting USB vaults... --")
        usb_path_layout.addWidget(self.lock_usb_dropdown)
        
        refresh_usb_btn = QPushButton("🔄 Refresh")
        refresh_usb_btn.clicked.connect(lambda: self.detect_usb_vaults(self.lock_usb_dropdown))
        usb_path_layout.addWidget(refresh_usb_btn)
        usb_layout.addLayout(usb_path_layout)
        
        # Auto-detect on startup
        QTimer.singleShot(100, lambda: self.detect_usb_vaults(self.lock_usb_dropdown))
        
        # Save USB button
        save_usb_btn = QPushButton("💾 Save USB Path as Default")
        save_usb_btn.setStyleSheet("""
            QPushButton {
                background-color: #2a2f4a;
                color: #00ff88;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #3a3f5a;
            }
        """)
        save_usb_btn.clicked.connect(self.save_settings_to_file)
        usb_layout.addWidget(save_usb_btn)
        
        usb_group.setLayout(usb_layout)
        layout.addWidget(usb_group)
        
        # Folder selection
        folder_group = QGroupBox("Step 2: Select Folder to Lock")
        folder_layout = QVBoxLayout()
        
        folder_path_layout = QHBoxLayout()
        folder_path_layout.addWidget(QLabel("Folder:"))
        self.lock_folder_input = QLineEdit()
        self.lock_folder_input.setPlaceholderText("Select folder to encrypt")
        folder_path_layout.addWidget(self.lock_folder_input)
        
        browse_folder_btn = QPushButton("📁 Browse")
        browse_folder_btn.clicked.connect(lambda: self.browse_folder(self.lock_folder_input))
        folder_path_layout.addWidget(browse_folder_btn)
        folder_layout.addLayout(folder_path_layout)
        
        # Save folder path button
        save_folder_btn = QPushButton("💾 Save This Path as Default")
        save_folder_btn.setStyleSheet("""
            QPushButton {
                background-color: #2a2f4a;
                color: #00ff88;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #3a3f5a;
            }
        """)
        save_folder_btn.clicked.connect(self.save_folder_path)
        folder_layout.addWidget(save_folder_btn)
        
        folder_group.setLayout(folder_layout)
        layout.addWidget(folder_group)
        
        # Progress and log
        self.lock_progress = QProgressBar()
        layout.addWidget(self.lock_progress)
        
        self.lock_log = QTextEdit()
        self.lock_log.setReadOnly(True)
        self.lock_log.setMaximumHeight(150)
        layout.addWidget(self.lock_log)
        
        # Lock button
        self.lock_btn = QPushButton("🔒 LOCK FOLDER")
        self.lock_btn.clicked.connect(self.lock_folder)
        self.lock_btn.setStyleSheet("background-color: #ff6600; font-size: 16px; padding: 15px;")
        layout.addWidget(self.lock_btn)
        
        return widget
    
    def create_unlock_tab(self):
        """Create the Unlock Folder tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # USB Vault section
        usb_group = QGroupBox("Step 1: USB Vault")
        usb_layout = QVBoxLayout()
        
        usb_path_layout = QHBoxLayout()
        usb_path_layout.addWidget(QLabel("USB Vault:"))
        self.unlock_usb_dropdown = QComboBox()
        self.unlock_usb_dropdown.setMinimumWidth(400)
        self.unlock_usb_dropdown.addItem("-- Detecting USB vaults... --")
        usb_path_layout.addWidget(self.unlock_usb_dropdown)
        
        refresh_usb_btn = QPushButton("🔄 Refresh")
        refresh_usb_btn.clicked.connect(lambda: self.detect_usb_vaults(self.unlock_usb_dropdown))
        usb_path_layout.addWidget(refresh_usb_btn)
        usb_layout.addLayout(usb_path_layout)
        
        # Auto-detect on startup
        QTimer.singleShot(100, lambda: self.detect_usb_vaults(self.unlock_usb_dropdown))
        
        usb_group.setLayout(usb_layout)
        layout.addWidget(usb_group)
        
        # Folder selection
        folder_group = QGroupBox("Step 2: Select Locked Folder")
        folder_layout = QVBoxLayout()
        
        folder_path_layout = QHBoxLayout()
        folder_path_layout.addWidget(QLabel("Locked Folder:"))
        self.unlock_folder_dropdown = QComboBox()
        self.unlock_folder_dropdown.setMinimumWidth(400)
        self.unlock_folder_dropdown.addItem("-- Load USB vault first --")
        folder_path_layout.addWidget(self.unlock_folder_dropdown)
        
        refresh_list_btn = QPushButton("🔄 Refresh List")
        refresh_list_btn.clicked.connect(self.load_locked_folders_list)
        folder_path_layout.addWidget(refresh_list_btn)
        folder_layout.addLayout(folder_path_layout)
        
        # Info label
        self.unlock_folder_info = QLabel("💡 Select USB vault and click Refresh to see locked folders")
        self.unlock_folder_info.setStyleSheet("color: #00d4ff; padding: 5px; font-size: 11px;")
        self.unlock_folder_info.setWordWrap(True)
        folder_layout.addWidget(self.unlock_folder_info)
        
        folder_group.setLayout(folder_layout)
        layout.addWidget(folder_group)
        
        # Progress and log
        self.unlock_progress = QProgressBar()
        layout.addWidget(self.unlock_progress)
        
        self.unlock_log = QTextEdit()
        self.unlock_log.setReadOnly(True)
        self.unlock_log.setMaximumHeight(150)
        layout.addWidget(self.unlock_log)
        
        # Unlock button
        self.unlock_btn = QPushButton("🔓 UNLOCK FOLDER")
        self.unlock_btn.clicked.connect(self.unlock_folder)
        self.unlock_btn.setStyleSheet("background-color: #00ff88; font-size: 16px; padding: 15px;")
        layout.addWidget(self.unlock_btn)
        
        return widget
    
    def create_registry_tab(self):
        """Create the Folder Registry tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        title = QLabel("📋 Locked Folders Registry")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setStyleSheet("color: #00ff88; padding: 10px;")
        layout.addWidget(title)
        
        # USB path for loading registry
        usb_group = QGroupBox("USB Vault")
        usb_layout = QHBoxLayout()
        usb_layout.addWidget(QLabel("USB Vault:"))
        
        self.registry_usb_dropdown = QComboBox()
        self.registry_usb_dropdown.setMinimumWidth(400)
        self.registry_usb_dropdown.addItem("-- Detecting USB vaults... --")
        usb_layout.addWidget(self.registry_usb_dropdown)
        
        refresh_usb_btn = QPushButton("🔄 Refresh USB")
        refresh_usb_btn.clicked.connect(lambda: self.detect_usb_vaults(self.registry_usb_dropdown))
        usb_layout.addWidget(refresh_usb_btn)
        
        # Auto-detect on startup and auto-refresh registry
        QTimer.singleShot(100, lambda: self.detect_usb_vaults(self.registry_usb_dropdown))
        QTimer.singleShot(200, self.refresh_registry)
        
        refresh_btn = QPushButton("🔄 Refresh List")
        refresh_btn.clicked.connect(self.refresh_registry)
        usb_layout.addWidget(refresh_btn)
        
        cleanup_btn = QPushButton("🧹 Clean Up Missing Folders")
        cleanup_btn.setStyleSheet("""
            QPushButton {
                background-color: #ff6600;
                color: white;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #ff8800;
            }
        """)
        cleanup_btn.clicked.connect(self.cleanup_registry)
        usb_layout.addWidget(cleanup_btn)
        
        usb_group.setLayout(usb_layout)
        layout.addWidget(usb_group)
        
        # Registry display
        self.registry_display = QTextEdit()
        self.registry_display.setReadOnly(True)
        layout.addWidget(self.registry_display)
        
        return widget
    
    # Helper methods
    def browse_usb(self, input_field):
        """Browse for USB vault path"""
        path = QFileDialog.getExistingDirectory(self, "Select USB Vault", "/Volumes")
        if path:
            input_field.setText(path)
    
    def browse_folder(self, input_field):
        """Browse for folder to lock/unlock"""
        # Use saved default folder path if available
        default_path = self.settings.get('default_folder_path', str(Path.home()))
        path = QFileDialog.getExistingDirectory(self, "Select Folder", default_path)
        if path:
            input_field.setText(path)
    
    def toggle_visibility(self, input_field):
        """Toggle passkey visibility"""
        if input_field.echoMode() == QLineEdit.EchoMode.Password:
            input_field.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            input_field.setEchoMode(QLineEdit.EchoMode.Password)
    
    def lock_folder(self):
        """Lock the selected folder"""
        usb_path = self.lock_usb_dropdown.currentData()
        if not usb_path:
            usb_path = self.lock_usb_dropdown.currentText()
        
        # Validation
        if not usb_path or usb_path.startswith("--"):
            QMessageBox.warning(self, "Missing USB", "Please select a USB vault from the dropdown")
            return
        
        # Check vault config for passkey requirement
        try:
            vault_dir = Path(usb_path) / '.chaos_vault'
            config_file = vault_dir / 'vault_config.json'
            
            if not config_file.exists():
                QMessageBox.warning(self, "Invalid Vault", "Vault configuration not found. Run wizard first.")
                return
            
            with open(config_file, 'r') as f:
                vault_config = json.load(f)
            
            requires_passkey = vault_config.get('requires_passkey', False)
            
            if requires_passkey:
                # Prompt for passkey
                from PyQt6.QtWidgets import QInputDialog
                passkey, ok = QInputDialog.getText(
                    self, 
                    "Vault Passkey Required",
                    "Enter vault passkey (NFC or password):",
                    QLineEdit.EchoMode.Password
                )
                if not ok or not passkey:
                    return
                passkey_to_use = passkey
            else:
                # No passkey required, use default
                passkey_to_use = "level1_easy_default"
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error reading vault config: {e}")
            return
        
        folder_path = self.lock_folder_input.text()
        
        if not folder_path:
            QMessageBox.warning(self, "Missing Folder", "Please select a folder to lock")
            return
        
        if not Path(usb_path).exists():
            QMessageBox.warning(self, "USB Not Found", f"USB path does not exist: {usb_path}")
            return
        
        if not Path(folder_path).exists():
            QMessageBox.warning(self, "Folder Not Found", f"Folder does not exist: {folder_path}")
            return
        
        # Confirm
        reply = QMessageBox.question(
            self, 
            "Confirm Lock",
            f"Lock folder:\n{folder_path}\n\nThis will encrypt all files. Continue?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply != QMessageBox.StandardButton.Yes:
            return
        
        # Start locking
        self.lock_btn.setEnabled(False)
        self.lock_log.clear()
        self.lock_progress.setValue(0)
        
        self.worker = LockWorker(folder_path, usb_path, passkey_to_use)
        self.worker.log.connect(self.lock_log.append)
        self.worker.progress.connect(self.lock_progress.setValue)
        self.worker.finished.connect(self.on_lock_finished)
        self.worker.start()
    
    def on_lock_finished(self, success, message):
        """Handle lock completion"""
        self.lock_btn.setEnabled(True)
        if success:
            QMessageBox.information(
                self,
                "Success!",
                f"Folder locked successfully!\n\nEncrypted name: {message}"
            )
        else:
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to lock folder:\n{message}"
            )
    
    def unlock_folder(self):
        """Unlock the selected folder"""
        usb_path = self.unlock_usb_dropdown.currentData()
        if not usb_path:
            usb_path = self.unlock_usb_dropdown.currentText()
        
        # Validation
        if not usb_path or usb_path.startswith("--"):
            QMessageBox.warning(self, "Missing USB", "Please select a USB vault from the dropdown")
            return
        
        if not Path(usb_path).exists():
            QMessageBox.warning(self, "USB Not Found", f"USB path does not exist: {usb_path}")
            return
        
        # Check vault config for passkey requirement
        try:
            vault_dir = Path(usb_path) / '.chaos_vault'
            config_file = vault_dir / 'vault_config.json'
            
            if not config_file.exists():
                QMessageBox.warning(self, "Invalid Vault", "Vault configuration not found.")
                return
            
            with open(config_file, 'r') as f:
                vault_config = json.load(f)
            
            requires_passkey = vault_config.get('requires_passkey', False)
            
            if requires_passkey:
                # Prompt for passkey
                from PyQt6.QtWidgets import QInputDialog
                passkey, ok = QInputDialog.getText(
                    self, 
                    "Vault Passkey Required",
                    "Enter vault passkey (NFC or password):",
                    QLineEdit.EchoMode.Password
                )
                if not ok or not passkey:
                    return
                passkey_to_use = passkey
            else:
                # No passkey required, use default
                passkey_to_use = "level1_easy_default"
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error reading vault config: {e}")
            return
        
        # Get selected folder from dropdown
        if self.unlock_folder_dropdown.currentIndex() < 0:
            QMessageBox.warning(self, "No Selection", "Please select a locked folder from the list")
            return
        
        folder_id = self.unlock_folder_dropdown.currentData()
        if not folder_id:
            QMessageBox.warning(self, "No Selection", "Please refresh the list and select a locked folder")
            return
        
        # Load registry to get folder path
        try:
            vault_dir = Path(usb_path) / '.chaos_vault'
            registry_file = vault_dir / 'level1_locked_folders.json'
            with open(registry_file, 'r') as f:
                locked_folders = json.load(f)
            
            if folder_id not in locked_folders:
                QMessageBox.warning(self, "Not Found", "Selected folder not found in registry")
                return
            
            folder_info = locked_folders[folder_id]
            folder_path = folder_info.get('encrypted_path', folder_info.get('original_path'))
            
            if not Path(folder_path).exists():
                QMessageBox.warning(self, "Folder Not Found", f"Folder does not exist: {folder_path}")
                return
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error loading folder info: {e}")
            return
        
        # Confirm
        reply = QMessageBox.question(
            self,
            "Confirm Unlock",
            f"Unlock folder:\n{folder_path}\n\nThis will decrypt all files. Continue?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply != QMessageBox.StandardButton.Yes:
            return
        
        # Start unlocking
        self.unlock_btn.setEnabled(False)
        self.unlock_log.clear()
        self.unlock_progress.setValue(0)
        
        self.worker = UnlockWorker(folder_path, usb_path, folder_id, passkey_to_use)
        self.worker.log.connect(self.unlock_log.append)
        self.worker.progress.connect(self.unlock_progress.setValue)
        self.worker.finished.connect(self.on_unlock_finished)
        self.worker.start()
    
    def on_unlock_finished(self, success, message):
        """Handle unlock completion"""
        self.unlock_btn.setEnabled(True)
        if success:
            QMessageBox.information(
                self,
                "Success!",
                "Folder unlocked successfully!\n\nAll files have been decrypted."
            )
        else:
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to unlock folder:\n{message}"
            )
    
    def closeEvent(self, event):
        """Clean up on close"""
        if self.worker and self.worker.isRunning():
            self.worker.terminate()
            self.worker.wait()
        event.accept()


def main():
    app = QApplication(sys.argv)
    window = Level1FolderLock()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
