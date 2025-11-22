#!/usr/bin/env python3
"""
Chaos Folder Lock CLI
Terminal interface for folder locking/unlocking with USB + NFC
Saves last config for quick re-use
"""

import sys
import os
import json
import time
import subprocess
import getpass
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import base64

# Import enhanced crypto module
from enhanced_crypto import EnhancedCrypto


class Config:
    """Manages saved configuration"""
    
    def __init__(self):
        self.config_file = Path.home() / '.chaos_folder_lock_config.json'
        self.config = self.load()
    
    def load(self) -> dict:
        """Load saved configuration"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️  Error loading config: {e}")
        return {}
    
    def save(self):
        """Save configuration"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
            print(f"💾 Config saved to {self.config_file}")
        except Exception as e:
            print(f"❌ Error saving config: {e}")
    
    def get(self, key: str, default=None):
        """Get config value"""
        return self.config.get(key, default)
    
    def set(self, key: str, value):
        """Set config value"""
        self.config[key] = value


class FolderLockManager:
    """Manages folder encryption, hiding, and locking"""
    
    def __init__(self, vault_path: Path):
        self.vault_path = vault_path
        self.vault_dir = vault_path / '.chaos_vault'
        self.locked_folders_file = self.vault_dir / 'locked_folders.json'
        self.locked_folders: Dict[str, dict] = {}
        self.load_locked_folders()
    
    def load_locked_folders(self):
        """Load list of locked folders from vault"""
        if self.locked_folders_file.exists():
            try:
                with open(self.locked_folders_file, 'r') as f:
                    self.locked_folders = json.load(f)
                print(f"📂 Loaded {len(self.locked_folders)} locked folder(s)")
            except Exception as e:
                print(f"❌ Error loading locked folders: {e}")
                self.locked_folders = {}
        else:
            print("📂 No locked folders yet")
    
    def save_locked_folders(self):
        """Save list of locked folders to vault"""
        try:
            with open(self.locked_folders_file, 'w') as f:
                json.dump(self.locked_folders, f, indent=2)
            print(f"💾 Saved locked folders registry")
        except Exception as e:
            print(f"❌ Error saving locked folders: {e}")
    
    def hide_from_spotlight(self, folder_path: Path) -> bool:
        """Hide folder from Spotlight indexing"""
        try:
            # Create .metadata_never_index file
            metadata_file = folder_path / '.metadata_never_index'
            metadata_file.touch()
            
            # Set hidden attribute
            subprocess.run(['chflags', 'hidden', str(folder_path)], check=True)
            
            # Add to Spotlight exclusion
            subprocess.run(['mdutil', '-i', 'off', str(folder_path)], 
                         check=False, capture_output=True)
            
            print(f"   ✅ Hidden from Spotlight")
            return True
        except Exception as e:
            print(f"   ❌ Error hiding from Spotlight: {e}")
            return False
    
    def unhide_from_spotlight(self, folder_path: Path) -> bool:
        """Unhide folder from Spotlight"""
        try:
            # Remove .metadata_never_index file
            metadata_file = folder_path / '.metadata_never_index'
            if metadata_file.exists():
                metadata_file.unlink()
            
            # Remove hidden attribute
            subprocess.run(['chflags', 'nohidden', str(folder_path)], check=True)
            
            # Re-enable Spotlight indexing
            subprocess.run(['mdutil', '-i', 'on', str(folder_path)], 
                         check=False, capture_output=True)
            
            print(f"   ✅ Unhidden from Spotlight")
            return True
        except Exception as e:
            print(f"   ❌ Error unhiding from Spotlight: {e}")
            return False
    
    def encrypt_folder_name(self, folder_path: Path, cipher: Fernet) -> Path:
        """Encrypt folder name and rename"""
        try:
            original_name = folder_path.name
            encrypted_name = cipher.encrypt(original_name.encode()).decode()
            
            # Make filesystem-safe
            safe_name = encrypted_name.replace('/', '_').replace('=', '-')[:200]
            new_path = folder_path.parent / f".locked_{safe_name}"
            
            folder_path.rename(new_path)
            print(f"   ✅ Encrypted: {original_name} → {new_path.name[:50]}...")
            return new_path
        except Exception as e:
            print(f"   ❌ Error encrypting folder name: {e}")
            return folder_path
    
    def decrypt_folder_name(self, folder_path: Path, original_name: str) -> Path:
        """Decrypt folder name and restore"""
        try:
            new_path = folder_path.parent / original_name
            folder_path.rename(new_path)
            print(f"   ✅ Decrypted: {original_name}")
            return new_path
        except Exception as e:
            print(f"   ❌ Error decrypting folder name: {e}")
            return folder_path
    
    def encrypt_file_contents(self, folder_path: Path, crypto: EnhancedCrypto, progress_callback=None) -> tuple:
        """
        Hybrid encryption: Smart batching based on file characteristics with crash recovery
        
        Strategy:
        - Root files: Encrypt individually (important)
        - Large files (>10MB): Encrypt individually
        - Small files in nested folders: Batch encrypt (efficient)
        """
        encrypted_count = 0
        
        # Checkpoint file for crash recovery
        checkpoint_file = folder_path / '.encrypt_checkpoint.json'
        processed_files = set()
        processed_batches = set()
        
        # Load checkpoint if exists (crash recovery)
        if checkpoint_file.exists():
            try:
                with open(checkpoint_file, 'r') as f:
                    checkpoint = json.load(f)
                    processed_files = set(checkpoint.get('processed_files', []))
                    processed_batches = set(checkpoint.get('processed_batches', []))
                    encrypted_count = checkpoint.get('encrypted_count', 0)
                    print(f"   🔄 Resuming from checkpoint: {encrypted_count} files already processed")
            except Exception as e:
                print(f"   ⚠️  Could not load checkpoint: {e}")
        
        # Thresholds for hybrid strategy
        BATCH_SIZE_THRESHOLD = 1  # Batch all nested files (even if just 1 file in folder)
        
        # First, analyze and categorize files
        root_files = []
        batch_folders = {}  # {folder_path: [(file, size), ...]}
        
        total_files = 0
        total_size = 0
        
        try:
            for item in folder_path.rglob('*'):
                if item.is_file() and not item.name.startswith('.') and not item.name.endswith('.encrypted'):
                    try:
                        size = item.stat().st_size
                        total_files += 1
                        total_size += size
                        
                        # Categorize file
                        if item.parent == folder_path:
                            # Root file - encrypt individually
                            root_files.append((item, size))
                        else:
                            # Nested file - batch with siblings (regardless of size)
                            folder_key = str(item.parent)
                            if folder_key not in batch_folders:
                                batch_folders[folder_key] = []
                            batch_folders[folder_key].append((item, size))
                    except:
                        pass
            
            # Handle empty folder case
            if total_files == 0:
                print(f"   ⚠️  No files to encrypt")
                if progress_callback:
                    progress_callback(0, 0, 0, 0, None, 0)
                return (0, 0, 0, 0)
            
            # Show categorization summary
            print(f"\n   📊 File Categorization:")
            print(f"      • Root files (individual): {len(root_files)}")
            print(f"      • Nested folders (batched): {len(batch_folders)}")
            total_batch_files = sum(len(files) for files in batch_folders.values())
            print(f"      • Files in batches: {total_batch_files}")
            print(f"      • Grand total: {total_files} files, {total_size / (1024**2):.1f} MB\n")
            
            if progress_callback:
                progress_callback(0, total_files, 0, total_size, None, 0)
            
            processed_size = 0
            start_time = time.time()
            
            # Encrypt root files individually
            if len(root_files) > 0:
                print(f"   📄 Encrypting {len(root_files)} root files individually...")
            else:
                print(f"   ℹ️  No root files to encrypt (skipping)")
            
            checkpoint_interval = 10  # Save checkpoint every 10 files
            files_since_checkpoint = 0
            
            for item, file_size in root_files:
                file_key = f"root:{item}"
                
                # Skip if already processed
                if file_key in processed_files:
                    processed_size += file_size
                    continue
                
                try:
                    file_start = time.time()
                    original_data = item.read_bytes()
                    encrypted_data = crypto.encrypt_file(item, original_data)
                    
                    # Clear original data from memory immediately
                    del original_data
                    
                    encrypted_file = item.parent / f"{item.name}.encrypted"
                    encrypted_file.write_bytes(encrypted_data)
                    
                    # Clear encrypted data from memory
                    del encrypted_data
                    
                    item.unlink()
                    encrypted_file.rename(item)
                    
                    encrypted_count += 1
                    processed_size += file_size
                    processed_files.add(file_key)
                    files_since_checkpoint += 1
                    
                    # Save checkpoint periodically
                    if files_since_checkpoint >= checkpoint_interval:
                        checkpoint_data = {
                            'processed_files': list(processed_files),
                            'processed_batches': list(processed_batches),
                            'encrypted_count': encrypted_count,
                            'timestamp': time.time(),
                            'folder_path': str(folder_path)
                        }
                        try:
                            with open(checkpoint_file, 'w') as f:
                                json.dump(checkpoint_data, f, indent=2)
                            files_since_checkpoint = 0
                        except Exception as e:
                            print(f"   ⚠️  Could not save checkpoint: {e}")
                    
                    elapsed = time.time() - start_time
                    eta_seconds = ((total_size - processed_size) / (processed_size / elapsed)) if processed_size > 0 else 0
                    
                    if progress_callback:
                        progress_callback(encrypted_count, total_files, processed_size, total_size, item.name, eta_seconds)
                except Exception as e:
                    print(f"   ⚠️  Could not encrypt {item.name}: {e}")
            
            # Batch encrypt all nested files by folder
            batch_count = 0
            MAX_BATCH_SIZE = 500 * 1024 * 1024  # 500 MB max per batch
            print(f"   📦 Processing {len(batch_folders)} folders for batching...")
            
            for folder_key, files_list in batch_folders.items():
                # Calculate total size for this folder
                folder_total_size = sum(size for _, size in files_list)
                
                # If folder is too large, skip it entirely
                if folder_total_size > MAX_BATCH_SIZE:
                    folder_name = Path(folder_key).name
                    print(f"   ⚠️  Skipping folder '{folder_name}' - too large ({folder_total_size / (1024**2):.1f} MB)")
                    continue
                
                if len(files_list) >= BATCH_SIZE_THRESHOLD:
                    # Batch encrypt
                    batch_count += 1
                    folder_name = Path(folder_key).name
                    print(f"   📦 Batch encrypting {len(files_list)} files in '{folder_name}'...")
                    
                    try:
                        # Read all files in batch (skip files over 750MB)
                        MAX_FILE_SIZE = 750 * 1024 * 1024  # 750 MB max per file
                        batch_data = {}
                        batch_size = 0
                        skipped_files = 0
                        
                        for item, file_size in files_list:
                            try:
                                # Skip individual files that are too large
                                if file_size > MAX_FILE_SIZE:
                                    print(f"      ⚠️  Skipping {item.name} - too large ({file_size / (1024**2):.1f} MB)")
                                    skipped_files += 1
                                    continue
                                
                                relative_path = str(item.relative_to(folder_path))
                                batch_data[relative_path] = item.read_bytes()
                                batch_size += file_size
                            except Exception as e:
                                print(f"   ⚠️  Could not read {item.name}: {e}")
                        
                        # Encrypt batch
                        batch_id = folder_key
                        encrypted_batch = crypto.encrypt_batch(batch_data, batch_id)
                        
                        # Save batch file
                        batch_file = Path(folder_key) / '.batch_encrypted'
                        batch_file.write_bytes(encrypted_batch)
                        
                        # Delete original files
                        for item, _ in files_list:
                            try:
                                item.unlink()
                            except:
                                pass
                        
                        encrypted_count += len(files_list)
                        processed_size += batch_size
                        
                        elapsed = time.time() - start_time
                        eta_seconds = ((total_size - processed_size) / (processed_size / elapsed)) if processed_size > 0 else 0
                        
                        print(f"   ✅ Batch encrypted {len(files_list)} files ({batch_size / 1024:.1f} KB)")
                        if progress_callback:
                            progress_callback(encrypted_count, total_files, processed_size, total_size, f"Batch: {folder_name}", eta_seconds)
                    except Exception as e:
                        print(f"   ⚠️  Could not batch encrypt folder {folder_name}: {e}")
                else:
                    # Too few files, encrypt individually
                    for item, file_size in files_list:
                        try:
                            original_data = item.read_bytes()
                            encrypted_data = crypto.encrypt_file(item, original_data)
                            
                            encrypted_file = item.parent / f"{item.name}.encrypted"
                            encrypted_file.write_bytes(encrypted_data)
                            item.unlink()
                            encrypted_file.rename(item)
                            
                            encrypted_count += 1
                            processed_size += file_size
                            
                            elapsed = time.time() - start_time
                            eta_seconds = ((total_size - processed_size) / (processed_size / elapsed)) if processed_size > 0 else 0
                            
                            if progress_callback:
                                progress_callback(encrypted_count, total_files, processed_size, total_size, item.name, eta_seconds)
                        except Exception as e:
                            print(f"   ⚠️  Could not encrypt {item.name}: {e}")
            
            print(f"   ✅ Hybrid encryption complete: {encrypted_count} files, {batch_count} batches")
            
            # Clean up checkpoint file on successful completion
            if checkpoint_file.exists():
                try:
                    checkpoint_file.unlink()
                    print(f"   🧹 Checkpoint file removed (encryption complete)")
                except Exception:
                    pass
            
            return (encrypted_count, processed_size, total_files, total_size)
        except Exception as e:
            print(f"   ❌ Error encrypting files: {e}")
            # Keep checkpoint file for recovery
            return (encrypted_count, 0, 0, 0)
    
    def decrypt_file_contents(self, folder_path: Path, crypto: EnhancedCrypto, progress_callback=None, expected_files=None, expected_size=None, show_skip_summary=True) -> int:
        """Decrypt all files (including batches) inside the folder recursively with progress tracking and crash recovery"""
        import time
        
        decrypted_count = 0
        total_bytes_processed = 0
        start_time = time.time()
        
        # Checkpoint file for crash recovery
        checkpoint_file = folder_path / '.decrypt_checkpoint.json'
        processed_files = set()
        
        # Remove old checkpoint at start (fresh decrypt)
        if checkpoint_file.exists():
            try:
                checkpoint_file.unlink()
                print(f"   🧹 Cleared old checkpoint")
            except Exception as e:
                print(f"   ⚠️  Could not remove checkpoint: {e}")
        
        try:
            # Use stored metadata if available (from lock operation)
            if expected_files is not None and expected_size is not None:
                total_files = expected_files
                total_size = expected_size
                print(f"   📊 Using stored metadata: {total_files} files, {total_size / (1024**3):.2f} GB")
            else:
                # Scan folder to count files and calculate total size
                print(f"   🔍 Scanning folder to count files...")
                if progress_callback:
                    progress_callback(0, 1, 0, 1, "Scanning folder...", 0)
                
                total_files = 0
                total_size = 0
                
                # Count batch files
                for item in folder_path.rglob('.batch_encrypted'):
                    total_files += 1
                    total_size += item.stat().st_size
                
                # Count individual encrypted files
                for item in folder_path.rglob('*'):
                    if item.is_file() and item.suffix == '.encrypted' and item.stat().st_size >= 100:
                        total_files += 1
                        total_size += item.stat().st_size
                
                if total_files == 0:
                    total_files = 1  # Avoid division by zero
                    total_size = 1
                
                print(f"   📊 Found {total_files} files to decrypt ({total_size / (1024**2):.1f} MB total)")
                if progress_callback:
                    progress_callback(0, total_files, 0, total_size, f"Ready to decrypt {total_files} files", 0)
            
            # Collect batch files (usually small list)
            batch_files = []
            try:
                for item in folder_path.rglob('.batch_encrypted'):
                    file_key = f"batch:{item}"
                    if file_key not in processed_files:
                        batch_files.append((item, file_key))
            except Exception as e:
                print(f"   ⚠️  Error scanning batches: {e}")
            
            # Process files with progress tracking and checkpointing
            checkpoint_interval = 10  # Save checkpoint every 10 files
            files_since_checkpoint = 0
            
            # Process batch files first
            for item, file_key in batch_files:
                try:
                    # Decrypt batch file
                    print(f"   📦 Decrypting batch in {item.parent.name}...")
                    encrypted_batch = item.read_bytes()
                    batch_size = len(encrypted_batch)
                    batch_id = str(item.parent)
                    
                    # Decrypt batch
                    files_data = crypto.decrypt_batch(encrypted_batch, batch_id)
                    
                    # Clear encrypted batch from memory immediately
                    del encrypted_batch
                    
                    # Restore individual files
                    for relative_path, file_data in files_data.items():
                        file_path = folder_path / relative_path
                        file_path.parent.mkdir(parents=True, exist_ok=True)
                        file_path.write_bytes(file_data)
                        decrypted_count += 1
                        
                        # Mark each extracted file as processed so we don't try to decrypt it again
                        extracted_file_key = f"file:{file_path}"
                        processed_files.add(extracted_file_key)
                    
                    # Clear files_data from memory
                    del files_data
                    
                    # Remove batch file
                    item.unlink()
                    total_bytes_processed += batch_size
                    print(f"   ✅ Decrypted batch")
                    
                    # Mark file as processed
                    processed_files.add(file_key)
                    files_since_checkpoint += 1
                    
                    # Save checkpoint periodically
                    if files_since_checkpoint >= checkpoint_interval:
                        checkpoint_data = {
                            'processed_files': list(processed_files),
                            'decrypted_count': decrypted_count,
                            'total_bytes_processed': total_bytes_processed,
                            'timestamp': time.time(),
                            'folder_path': str(folder_path)
                        }
                        try:
                            with open(checkpoint_file, 'w') as f:
                                json.dump(checkpoint_data, f, indent=2)
                            files_since_checkpoint = 0
                        except Exception as e:
                            print(f"   ⚠️  Could not save checkpoint: {e}")
                    
                    # Report progress (batch files)
                    if progress_callback:
                        try:
                            # Calculate ETA
                            elapsed = time.time() - start_time
                            if decrypted_count > 0 and elapsed > 0:
                                files_per_sec = decrypted_count / elapsed
                                remaining_files = total_files - decrypted_count
                                eta = remaining_files / files_per_sec if files_per_sec > 0 else 0
                            else:
                                eta = 0
                            
                            progress_callback(
                                decrypted_count,
                                total_files,  # Use actual total from metadata
                                total_bytes_processed,
                                total_size,  # Use actual total size from metadata
                                item.name,
                                eta
                            )
                        except Exception:
                            pass  # Ignore callback errors
                    
                    # Force garbage collection every 10 files
                    if decrypted_count % 10 == 0:
                        import gc
                        gc.collect()
                        
                except Exception as e:
                    print(f"   ⚠️  Could not decrypt batch: {e}")
            
            # Clear batch_files list from memory
            del batch_files
            import gc
            gc.collect()
            
            # Now process individual files using generator
            for item in folder_path.rglob('*'):
                if not item.is_file():
                    continue
                
                # Skip checkpoint file specifically
                if item.name == '.decrypt_checkpoint.json':
                    continue
                
                # Skip hidden files that start with . (silently)
                if item.name.startswith('.'):
                    continue
                    
                file_key = f"file:{item}"
                if file_key in processed_files:
                    # File was already processed (likely from a batch)
                    continue
                    
                try:
                    # Decrypt individual file
                    encrypted_data = item.read_bytes()
                    encrypted_size = len(encrypted_data)
                    
                    # Skip if file is too small to be encrypted (< 100 bytes)
                    if encrypted_size < 100:
                        del encrypted_data
                        continue
                    
                    # Try to decrypt with AES
                    try:
                        decrypted_data = crypto.decrypt_file(item, encrypted_data)
                        
                        # Clear encrypted data from memory immediately
                        del encrypted_data
                        
                        decrypted_size = len(decrypted_data)
                        
                        # Write decrypted content back
                        item.write_bytes(decrypted_data)
                        
                        # Clear decrypted data from memory
                        del decrypted_data
                        
                        decrypted_count += 1
                        total_bytes_processed += encrypted_size
                        
                        # Report progress immediately after each file
                        if progress_callback:
                            try:
                                elapsed = time.time() - start_time
                                if decrypted_count > 0 and elapsed > 0:
                                    files_per_sec = decrypted_count / elapsed
                                    remaining_files = max(total_files - decrypted_count, 0)
                                    eta = remaining_files / files_per_sec if files_per_sec > 0 else 0
                                else:
                                    eta = 0
                                
                                progress_callback(
                                    decrypted_count,
                                    total_files,
                                    total_bytes_processed,
                                    total_size,
                                    item.name,
                                    eta
                                )
                            except Exception as e:
                                print(f"   ⚠️  Progress callback error: {e}")
                    except Exception as decrypt_err:
                        # File might not be encrypted, skip it (already decrypted from batch)
                        # Don't print - this is normal for files extracted from batches
                        total_bytes_processed += encrypted_size
                        del encrypted_data
                    
                    # Force garbage collection every 20 files
                    if decrypted_count % 20 == 0:
                        import gc
                        gc.collect()
                    
                    # Mark file as processed
                    processed_files.add(file_key)
                    files_since_checkpoint += 1
                    
                    # Save checkpoint periodically
                    if files_since_checkpoint >= checkpoint_interval:
                        checkpoint_data = {
                            'processed_files': list(processed_files),
                            'decrypted_count': decrypted_count,
                            'total_bytes_processed': total_bytes_processed,
                            'timestamp': time.time(),
                            'folder_path': str(folder_path)
                        }
                        try:
                            with open(checkpoint_file, 'w') as f:
                                json.dump(checkpoint_data, f, indent=2)
                            files_since_checkpoint = 0
                        except Exception as e:
                            print(f"   ⚠️  Could not save checkpoint: {e}")
                    
                    # Report progress (individual files)
                    if progress_callback:
                        try:
                            # Calculate ETA
                            elapsed = time.time() - start_time
                            if decrypted_count > 0 and elapsed > 0:
                                files_per_sec = decrypted_count / elapsed
                                remaining_files = total_files - decrypted_count
                                eta = remaining_files / files_per_sec if files_per_sec > 0 else 0
                            else:
                                eta = 0
                            
                            progress_callback(
                                decrypted_count,
                                total_files,  # Use actual total from metadata
                                total_bytes_processed,
                                total_size,  # Use actual total size from metadata
                                item.name,
                                eta
                            )
                        except Exception:
                            pass  # Ignore callback errors
                        
                except Exception as e:
                    print(f"   ⚠️  Could not decrypt {item.name}: {e}")
            
            # Clean up checkpoint file
            if checkpoint_file.exists():
                try:
                    checkpoint_file.unlink()
                except Exception:
                    pass
            
            # Send final completion progress update
            if progress_callback:
                try:
                    progress_callback(
                        total_files,  # Report as complete
                        total_files,
                        total_size,
                        total_size,
                        "Decryption complete",
                        0
                    )
                except Exception:
                    pass
            
            print(f"   ✅ Decryption complete!")
            
            return decrypted_count
        except Exception as e:
            print(f"   ❌ Error decrypting files: {e}")
            return decrypted_count
    
    def lock_folder(self, folder_path: Path, crypto: EnhancedCrypto, progress_callback=None) -> bool:
        """Lock folder: encrypt files with AES-128, hide, encrypt name, add to vault"""
        try:
            print(f"\n🔒 Locking: {folder_path}")
            print(f"\n   ⚡ Using AES-128 encryption with 500k PBKDF2 iterations (optimized for speed)...")
            
            # Encrypt file contents first with AES-128
            print(f"\n   📄 Encrypting file contents...")
            encrypted_count, processed_size, total_files, total_size = self.encrypt_file_contents(folder_path, crypto, progress_callback)
            print(f"   ✅ Encrypted {encrypted_count} file(s) with AES-128\n")
            
            # Hide from Spotlight
            self.hide_from_spotlight(folder_path)
            
            # Encrypt folder name
            cipher = crypto.get_fernet_cipher()
            encrypted_path = self.encrypt_folder_name(folder_path, cipher)
            
            # Add to locked folders registry with metadata for accurate unlock progress
            folder_id = str(time.time())
            self.locked_folders[folder_id] = {
                'original_path': str(folder_path),
                'original_name': folder_path.name,
                'encrypted_path': str(encrypted_path),
                'locked_date': datetime.now().isoformat(),
                'status': 'locked',
                'files_encrypted': encrypted_count,
                'total_files': total_files,  # For accurate unlock progress
                'total_size': total_size      # For accurate unlock progress
            }
            
            self.save_locked_folders()
            print(f"✅ Folder locked successfully!\n")
            return True
        except Exception as e:
            print(f"❌ Error locking folder: {e}\n")
            return False
    
    def unlock_folder(self, folder_id: str, crypto: EnhancedCrypto = None, progress_callback=None) -> bool:
        """Unlock folder: restore name, unhide, decrypt files with AES-256"""
        try:
            if folder_id not in self.locked_folders:
                print(f"❌ Folder ID not found: {folder_id}")
                return False
            
            folder_info = self.locked_folders[folder_id]
            encrypted_path = Path(folder_info['encrypted_path'])
            original_name = folder_info['original_name']
            
            print(f"\n🔓 Unlocking: {original_name}")
            print(f"\n   🔐 Using AES-256 decryption...")
            
            if not encrypted_path.exists():
                print(f"   ❌ Encrypted folder not found: {encrypted_path}")
                return False
            
            # Decrypt folder name
            decrypted_path = self.decrypt_folder_name(encrypted_path, original_name)
            
            # Remove any old checkpoint files before starting
            checkpoint_file = decrypted_path / '.decrypt_checkpoint.json'
            if checkpoint_file.exists():
                try:
                    checkpoint_file.unlink()
                    print(f"   🧹 Removed old checkpoint file")
                except Exception as e:
                    print(f"   ⚠️  Could not remove checkpoint: {e}")
            
            # Decrypt file contents if crypto provided
            if crypto:
                print(f"\n   📄 Decrypting file contents...")
                # Pass stored metadata for accurate progress tracking
                expected_files = folder_info.get('total_files')
                expected_size = folder_info.get('total_size')
                decrypted_count = self.decrypt_file_contents(
                    decrypted_path, 
                    crypto, 
                    progress_callback,
                    expected_files=expected_files,
                    expected_size=expected_size
                )
                print(f"   ✅ Decrypted {decrypted_count} file(s) with AES-256\n")
            
            # Unhide from Spotlight
            self.unhide_from_spotlight(decrypted_path)
            
            # Update registry
            self.locked_folders[folder_id]['status'] = 'unlocked'
            self.locked_folders[folder_id]['unlocked_date'] = datetime.now().isoformat()
            self.save_locked_folders()
            
            print(f"✅ Folder unlocked successfully!\n")
            return True
        except Exception as e:
            print(f"❌ Error unlocking folder: {e}\n")
            return False
    
    def list_locked_folders(self):
        """List all locked folders"""
        locked = {k: v for k, v in self.locked_folders.items() if v['status'] == 'locked'}
        
        if not locked:
            print("\n📂 No locked folders")
            return
        
        print(f"\n📂 Locked Folders ({len(locked)}):")
        print("=" * 80)
        for i, (folder_id, info) in enumerate(locked.items(), 1):
            print(f"{i}. {info['original_name']}")
            print(f"   ID: {folder_id}")
            print(f"   Locked: {info['locked_date'][:19]}")
            print(f"   Path: {info['encrypted_path'][:70]}...")
            print()


def find_usb_drives() -> List[Path]:
    """Find mounted USB drives"""
    volumes = Path('/Volumes')
    if not volumes.exists():
        return []
    
    usb_drives = []
    for volume in volumes.iterdir():
        if volume.is_dir() and volume.name != 'Macintosh HD':
            # Check if it has a .chaos_vault
            if (volume / '.chaos_vault').exists():
                usb_drives.append(volume)
    
    return usb_drives


def unlock_vault(vault_path: Path, nfc_passkey: str) -> Optional[Fernet]:
    """Unlock vault with NFC passkey"""
    try:
        print("\n🔓 Unlocking vault...")
        
        vault_dir = vault_path / '.chaos_vault'
        
        # Load vault config
        config_path = vault_dir / 'vault_config.json'
        if not config_path.exists():
            print("❌ Vault config not found")
            return None
        
        with open(config_path, 'r') as f:
            vault_config = json.load(f)
        
        print(f"   📊 Vault version: {vault_config.get('vault_version', 'unknown')}")
        print(f"   🔒 Hardware locked: {vault_config.get('hardware_locked', False)}")
        print(f"   📅 Created: {vault_config.get('initialized_date', 'unknown')[:19]}")
        
        # Load sealed alphabet
        sealed_path = vault_dir / 'chaos_alphabet_sealed.enc'
        if not sealed_path.exists():
            print("❌ Sealed alphabet not found")
            return None
        
        with open(sealed_path, 'rb') as f:
            encrypted_alphabet = f.read()
        
        # Get salt from vault config (chaos alphabet hash)
        # The wizard should have saved this during sealing
        salt = vault_config.get('alphabet_salt', b'chaos_vault_salt')
        if isinstance(salt, str):
            salt = salt.encode()
        
        # Derive decryption key from NFC passkey
        print("   🔑 Deriving decryption key...")
        print(f"   🧂 Using salt: {salt[:16] if isinstance(salt, bytes) else salt}")
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt if isinstance(salt, bytes) else salt.encode(),
            iterations=100000,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(nfc_passkey.encode()))
        cipher = Fernet(key)
        
        # Decrypt alphabet
        print("   🔓 Decrypting vault...")
        decrypted_data = cipher.decrypt(encrypted_alphabet)
        alphabet_data = json.loads(decrypted_data)
        
        print(f"   ✅ Vault unlocked!")
        print(f"   📝 Sealed with: {alphabet_data.get('sealed_with', 'unknown')}")
        
        return cipher
        
    except Exception as e:
        print(f"❌ Unlock failed: {str(e)}")
        return None


def get_nfc_input() -> str:
    """Get NFC input from keyboard (hidden)"""
    print("\n📱 NFC Scan")
    print("=" * 80)
    print("Place NFC tag on reader and scan now...")
    print("(Passkey will be hidden for security)")
    print()
    
    # Get passkey without showing it
    import getpass
    nfc_passkey = getpass.getpass("⌨️  NFC Passkey (hidden): ").strip()
    
    if not nfc_passkey:
        print("❌ No passkey entered")
        return ""
    
    print(f"✅ Captured {len(nfc_passkey)} characters (hidden)")
    
    return nfc_passkey


def main_menu():
    """Main menu"""
    print("\n" + "=" * 80)
    print("🔐 CHAOS FOLDER LOCK - CLI")
    print("=" * 80)
    print("\n1. 🔓 Unlock Vault & Lock New Folder")
    print("2. 🔓 Unlock Vault & Unlock Folder")
    print("3. 📂 List Locked Folders")
    print("4. ⚙️  Show Config")
    print("5. 🚪 Exit")
    print()
    
    choice = input("Select option (1-5): ").strip()
    return choice


def lock_new_folder(config: Config):
    """Lock a new folder"""
    print("\n" + "=" * 80)
    print("🔒 LOCK NEW FOLDER")
    print("=" * 80)
    
    # Find USB drives
    print("\n📂 Scanning for USB vaults...")
    usb_drives = find_usb_drives()
    
    if not usb_drives:
        print("❌ No USB vaults found!")
        print("   Make sure USB drive with .chaos_vault is connected")
        return
    
    # Select USB drive
    if len(usb_drives) == 1:
        vault_path = usb_drives[0]
        print(f"✅ Found vault: {vault_path}")
    else:
        print(f"\n📂 Found {len(usb_drives)} vaults:")
        for i, drive in enumerate(usb_drives, 1):
            print(f"{i}. {drive}")
        
        choice = input(f"\nSelect vault (1-{len(usb_drives)}): ").strip()
        try:
            vault_path = usb_drives[int(choice) - 1]
        except (ValueError, IndexError):
            print("❌ Invalid selection")
            return
    
    # Save to config
    config.set('last_vault_path', str(vault_path))
    config.save()
    
    # Get NFC passkey
    nfc_passkey = get_nfc_input()
    if not nfc_passkey:
        return
    
    # Save to config (encrypted would be better!)
    config.set('last_nfc_passkey', nfc_passkey)
    config.save()
    
    # Unlock vault
    cipher = unlock_vault(vault_path, nfc_passkey)
    if not cipher:
        return
    
    # Initialize folder manager
    folder_manager = FolderLockManager(vault_path)
    
    # Get folder to lock
    print("\n📂 Select Folder to Lock")
    print("=" * 80)
    folder_path_str = input("Enter folder path: ").strip()
    
    if not folder_path_str:
        print("❌ No folder path entered")
        return
    
    folder_path = Path(folder_path_str).expanduser()
    
    if not folder_path.exists():
        print(f"❌ Folder not found: {folder_path}")
        return
    
    if not folder_path.is_dir():
        print(f"❌ Not a directory: {folder_path}")
        return
    
    # Confirm
    print(f"\n⚠️  About to lock: {folder_path}")
    print("   This will:")
    print("   - Hide folder from Spotlight")
    print("   - Set hidden flag")
    print("   - Encrypt folder name")
    print("   - Require USB + NFC to unlock")
    print()
    
    confirm = input("Continue? (yes/no): ").strip().lower()
    if confirm != 'yes':
        print("❌ Cancelled")
        return
    
    # Lock folder
    folder_manager.lock_folder(folder_path, cipher)


def unlock_folder_menu(config: Config):
    """Unlock a folder"""
    print("\n" + "=" * 80)
    print("🔓 UNLOCK FOLDER")
    print("=" * 80)
    
    # Get vault path from config or scan
    vault_path_str = config.get('last_vault_path')
    
    if vault_path_str:
        vault_path = Path(vault_path_str)
        print(f"✅ Using saved vault: {vault_path}")
        
        use_saved = input("Use this vault? (yes/no): ").strip().lower()
        if use_saved != 'yes':
            vault_path = None
    else:
        vault_path = None
    
    if not vault_path:
        # Find USB drives
        print("\n📂 Scanning for USB vaults...")
        usb_drives = find_usb_drives()
        
        if not usb_drives:
            print("❌ No USB vaults found!")
            return
        
        if len(usb_drives) == 1:
            vault_path = usb_drives[0]
            print(f"✅ Found vault: {vault_path}")
        else:
            print(f"\n📂 Found {len(usb_drives)} vaults:")
            for i, drive in enumerate(usb_drives, 1):
                print(f"{i}. {drive}")
            
            choice = input(f"\nSelect vault (1-{len(usb_drives)}): ").strip()
            try:
                vault_path = usb_drives[int(choice) - 1]
            except (ValueError, IndexError):
                print("❌ Invalid selection")
                return
        
        config.set('last_vault_path', str(vault_path))
        config.save()
    
    # Get NFC passkey
    nfc_passkey_saved = config.get('last_nfc_passkey')
    
    if nfc_passkey_saved:
        print(f"\n📱 Saved NFC passkey found ({len(nfc_passkey_saved)} chars)")
        use_saved = input("Use saved passkey? (yes/no): ").strip().lower()
        if use_saved == 'yes':
            nfc_passkey = nfc_passkey_saved
        else:
            nfc_passkey = get_nfc_input()
    else:
        nfc_passkey = get_nfc_input()
    
    if not nfc_passkey:
        return
    
    # Unlock vault
    cipher = unlock_vault(vault_path, nfc_passkey)
    if not cipher:
        return
    
    # Initialize folder manager
    folder_manager = FolderLockManager(vault_path)
    
    # List locked folders
    folder_manager.list_locked_folders()
    
    locked = {k: v for k, v in folder_manager.locked_folders.items() 
              if v['status'] == 'locked'}
    
    if not locked:
        return
    
    # Select folder to unlock
    print("Select folder to unlock:")
    folder_ids = list(locked.keys())
    
    choice = input(f"Enter number (1-{len(folder_ids)}): ").strip()
    try:
        folder_id = folder_ids[int(choice) - 1]
    except (ValueError, IndexError):
        print("❌ Invalid selection")
        return
    
    # Unlock folder
    folder_manager.unlock_folder(folder_id)


def list_locked_folders(config: Config):
    """List all locked folders"""
    vault_path_str = config.get('last_vault_path')
    
    if not vault_path_str:
        print("❌ No vault configured. Run option 1 or 2 first.")
        return
    
    vault_path = Path(vault_path_str)
    if not vault_path.exists():
        print(f"❌ Vault not found: {vault_path}")
        return
    
    folder_manager = FolderLockManager(vault_path)
    folder_manager.list_locked_folders()


def show_config(config: Config):
    """Show current configuration"""
    print("\n" + "=" * 80)
    print("⚙️  CONFIGURATION")
    print("=" * 80)
    print(f"\nConfig file: {config.config_file}")
    print()
    
    if config.config:
        for key, value in config.config.items():
            if 'passkey' in key.lower():
                print(f"{key}: {'*' * len(str(value))} ({len(str(value))} chars)")
            else:
                print(f"{key}: {value}")
    else:
        print("No configuration saved yet")
    print()


def main():
    """Main CLI loop"""
    config = Config()
    
    print("\n🔐 Chaos Folder Lock - CLI")
    print("Terminal interface for folder locking/unlocking")
    print()
    
    while True:
        choice = main_menu()
        
        if choice == '1':
            lock_new_folder(config)
        elif choice == '2':
            unlock_folder_menu(config)
        elif choice == '3':
            list_locked_folders(config)
        elif choice == '4':
            show_config(config)
        elif choice == '5':
            print("\n👋 Goodbye!")
            break
        else:
            print("❌ Invalid option")
        
        input("\nPress Enter to continue...")


if __name__ == '__main__':
    main()
