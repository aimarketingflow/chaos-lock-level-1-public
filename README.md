# 🔐 Chaos Lock - Level 1

**Simple, Secure File Encryption with Physical Key Storage**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![PyQt6](https://img.shields.io/badge/GUI-PyQt6-green.svg)](https://www.riverbankcomputing.com/software/pyqt/)

🔗 **[Official Website](https://aimarketingflow.com/chaos-lock/)** | 🎥 **[Watch Demo Video](https://www.youtube.com/watch?v=GCxGdX1ROZI)** | 📚 **[Full Documentation](docs/)**

---

## 🎯 What is Chaos Lock?

Chaos Lock is a **beginner-friendly file encryption system** that stores your encryption keys on a physical USB drive instead of relying on passwords alone. 

**Key Innovation:** Each USB vault generates a unique 64-character "chaos alphabet" from system entropy, creating encryption keys that are physically isolated and impossible to recreate without your USB drive.

### Why Chaos Lock?

❌ **Traditional encryption problems:**
- Passwords you forget
- Passwords that can be cracked
- Cloud services you have to trust
- Complex setup processes

✅ **Chaos Lock solutions:**
- Physical USB vault (something you have)
- Optional NFC tag or passkey (something you know)
- No cloud, no backdoors, no subscriptions
- 6-step wizard setup in 2 minutes
- You own your keys—literally

---

## ⭐ Features

### 🔒 Security
- **AES-256 encryption** with PBKDF2 key derivation (100,000 iterations)
- **Unique chaos alphabet** per vault (64 characters from system entropy)
- **Per-file unique keys** derived from master key + chaos alphabet
- **HMAC integrity verification** to detect tampering
- **Two-factor security:** USB vault + optional NFC/passkey

### 🎨 User Experience
- **6-step setup wizard** with intuitive PyQt6 GUI
- **Folder lock/unlock manager** with progress tracking
- **Beginner-friendly** - no technical knowledge required
- **Cross-platform** - works on macOS, Linux, Windows

### 🛡️ Privacy
- **Zero cloud dependencies** - everything stays local
- **No telemetry** - we don't track anything
- **Open source** - audit the code yourself
- **Air-gapped keys** - stored only on your USB drive

---

## ⚡ Quick Links

- 📦 **[Installation Guide](docs/INSTALLATION_GUIDE.md)** - Step-by-step setup with screenshots
- ⚡ **[5-Minute Tutorial](docs/TUTORIAL.md)** - Get started fast
- 🔒 **[Security FAQ](docs/SECURITY_FAQ.md)** - Common security questions answered
- 🛠️ **[Hardware Recommendations](docs/HARDWARE.md)** - USB drives, NFC readers, tags

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+**
- **USB drive** (any size, will store vault ~1-10 MB)
- **Optional:** NFC reader + ISO15693 NFC tag

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/aimarketingflow/chaos-lock-level-1-public.git
cd chaos-lock-level-1-public
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Run the setup wizard:**
```bash
python3 level1_easy_wizard.py
```

---

## 📖 Usage

### Step 1: Setup Your Vault (One-Time)

Run the **6-step setup wizard:**

```bash
python3 level1_easy_wizard.py
```

**The wizard will:**
1. ✅ Confirm security level (Easy Mode)
2. 📁 Select your USB drive location
3. 🔧 Initialize the vault on USB
4. 🏷️ Setup NFC tag or passkey (optional)
5. 🎲 Capture system entropy (30 seconds)
6. ✨ Complete! Your vault is ready

**What gets created:**
- `.chaos_vault/` directory on your USB
- `chaos_alphabet.txt` - Your unique 64-char alphabet
- `vault_config.json` - Vault settings (100k iterations)
- `master_key.bin` - Encrypted master key

---

### Step 2: Lock Your Files

Run the **folder lock manager:**

```bash
python3 level1_folder_lock.py
```

**To lock a folder:**
1. Click **"Lock"** tab
2. Select folder to encrypt
3. Select your USB vault
4. Enter passkey or scan NFC (if you set one up)
5. Click **"Lock Folder"**
6. Wait for encryption to complete

**Result:** Your folder becomes `folder_name.locked/` with encrypted contents

---

### Step 3: Unlock Your Files

**To unlock a folder:**
1. Click **"Unlock"** tab
2. Select `.locked` folder
3. Select your USB vault
4. Enter passkey or scan NFC
5. Click **"Unlock Folder"**
6. Wait for decryption to complete

**Result:** Your original folder is restored with all files decrypted

---

## 🏗️ Architecture

### How It Works

```
┌─────────────────────────────────────────────────────────┐
│                    YOUR COMPUTER                        │
│                                                         │
│  [Your Files] ──┐                                      │
│                 │                                       │
│                 ▼                                       │
│         ┌───────────────┐                              │
│         │  Chaos Lock   │                              │
│         │   Level 1     │                              │
│         └───────┬───────┘                              │
│                 │                                       │
│                 ▼                                       │
│         ┌───────────────┐                              │
│         │  AES-256 +    │                              │
│         │  Chaos Alpha  │                              │
│         └───────┬───────┘                              │
│                 │                                       │
│                 ▼                                       │
│         [Encrypted Files]                              │
│                                                         │
└─────────────────────────────────────────────────────────┘
                          │
                          │ Keys stored on
                          ▼
                  ┌───────────────┐
                  │   USB VAULT   │
                  │               │
                  │ • Master Key  │
                  │ • Chaos Alpha │
                  │ • Config      │
                  └───────────────┘
```

### Security Layers

**Layer 1: AES-256 Encryption**
- Industry-standard symmetric encryption
- 256-bit keys derived via PBKDF2
- 100,000 iterations for key derivation

**Layer 2: Chaos Alphabet**
- Unique 64-character alphabet per vault
- Generated from system entropy
- Used for additional substitution cipher
- Stored only on USB (air-gapped)

**Layer 3: Per-File Keys**
- Each file gets unique encryption key
- Derived from: master key + chaos alphabet + file metadata
- Prevents pattern analysis across files

**Layer 4: HMAC Verification**
- SHA-256 HMAC for integrity checking
- Detects any tampering or corruption
- Verifies before decryption

**Layer 5: Physical Security**
- Keys stored on USB only (not on computer)
- Optional NFC tag authentication
- Two-factor: something you have + something you know

---

## 🔐 Security Details

### Encryption Specification

| Component | Specification |
|-----------|--------------|
| **Symmetric Cipher** | AES-256-CBC |
| **Key Derivation** | PBKDF2-HMAC-SHA256 |
| **Iterations** | 100,000 |
| **Salt** | 32 bytes (random per vault) |
| **IV** | 16 bytes (random per file) |
| **HMAC** | SHA-256 |
| **Chaos Alphabet** | 64 characters (system entropy) |

### Threat Model

**What Chaos Lock protects against:**
- ✅ Password cracking (keys not password-based)
- ✅ Stolen laptop (files encrypted, keys on USB)
- ✅ Cloud breaches (no cloud storage)
- ✅ Rubber-hose cryptanalysis (USB can be hidden separately)
- ✅ File tampering (HMAC verification)

**What Chaos Lock does NOT protect against:**
- ❌ Stolen USB + known passkey (physical security required)
- ❌ Keyloggers capturing passkey (use NFC instead)
- ❌ Compromised computer during encryption/decryption
- ❌ Quantum computers (Level 1 uses classical crypto)

### Best Practices

**DO:**
- ✅ Store USB vault in a safe place
- ✅ Use a strong passkey (if not using NFC)
- ✅ Keep backup of USB vault (encrypted backup)
- ✅ Test unlock before deleting original files
- ✅ Update Python and dependencies regularly

**DON'T:**
- ❌ Store USB vault and files in same location
- ❌ Use weak/common passkeys
- ❌ Share your USB vault
- ❌ Encrypt files on the same USB as vault
- ❌ Delete original files before verifying unlock works

---

## 📁 File Structure

```
chaos-lock-level-1/
├── level1_easy_wizard.py          # 6-step setup wizard (GUI)
├── level1_folder_lock.py          # Lock/unlock manager (GUI)
├── chaos_entropy.py               # Entropy collection system
├── enhanced_crypto.py             # Encryption engine
├── folder_lock_cli.py             # CLI backend
├── requirements.txt               # Python dependencies
├── README.md                      # This file
├── LICENSE                        # MIT License
└── docs/
    ├── SETUP_GUIDE.md            # Detailed setup instructions
    ├── SECURITY.md               # Security documentation
    └── TROUBLESHOOTING.md        # Common issues & solutions
```

### USB Vault Structure

```
/Volumes/YOUR_USB/
└── .chaos_vault/
    ├── chaos_alphabet.txt        # Your unique 64-char alphabet
    ├── vault_config.json         # Vault configuration
    ├── master_key.bin            # Encrypted master key
    └── vault_metadata.json       # Vault creation info
```

---

## 🛠️ Requirements

### Python Dependencies

```
PyQt6>=6.4.0              # GUI framework
cryptography>=41.0.0      # Encryption primitives
appdirs>=1.4.4           # Cross-platform paths
```

Install all at once:
```bash
pip install -r requirements.txt
```

### System Requirements

- **OS:** macOS 10.14+, Linux (Ubuntu 20.04+), Windows 10+
- **Python:** 3.8 or higher
- **RAM:** 512 MB minimum
- **Disk:** 50 MB for application
- **USB:** Any USB drive (1 MB+ free space for vault)

### Optional Hardware

- **NFC Reader:** Any ISO15693 compatible reader
- **NFC Tags:** ISO15693 tags (ICODE SLIX, etc.)

---

## 🎓 Use Cases

### Perfect For:

✅ **Personal Documents**
- Tax returns, financial records
- Medical documents, insurance
- Personal photos and videos
- Scanned IDs and passports

✅ **Small Business**
- Client data and contracts
- Financial spreadsheets
- Business plans and strategies
- Employee records

✅ **Students & Academics**
- Research data and notes
- Thesis and dissertation drafts
- Academic credentials
- Personal projects

✅ **Privacy-Conscious Users**
- Anyone who values data ownership
- Users tired of cloud services
- People who want simple security
- Those learning about encryption

### Not Ideal For:

❌ **Enterprise/Corporate** (use Level 4 instead)
❌ **High-security government** (use Level 5 + quantum-resistant)
❌ **Large teams** (no multi-user support in Level 1)
❌ **Cloud sync** (intentionally offline-only)

---

## 🆚 Comparison with Other Tools

| Feature | Chaos Lock L1 | VeraCrypt | BitLocker | Cloud Encryption |
|---------|--------------|-----------|-----------|------------------|
| **Ease of Use** | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Physical Keys** | ✅ USB | ❌ | ❌ | ❌ |
| **No Cloud** | ✅ | ✅ | ✅ | ❌ |
| **Open Source** | ✅ | ✅ | ❌ | Varies |
| **Cross-Platform** | ✅ | ✅ | ❌ (Windows) | ✅ |
| **Setup Time** | 2 min | 15 min | 5 min | 10 min |
| **Unique Per-Vault Keys** | ✅ | ❌ | ❌ | ❌ |
| **NFC Support** | ✅ | ❌ | ❌ | ❌ |
| **Cost** | Free | Free | Included | $5-15/mo |

---

## 🔄 Upgrade Path

Chaos Lock has 5 security levels. Level 1 is the entry point:

### Level 1 (⭐⭐⭐⭐) - **You Are Here**
- USB vault + optional NFC
- 100k PBKDF2 iterations
- Perfect for personal use

### Level 2-3 (⭐⭐⭐⭐⭐)
- Enhanced entropy collection
- Audio chaos capture
- 500k PBKDF2 iterations
- Visualizer for chaos patterns

### Level 4 (⭐⭐⭐⭐⭐⭐)
- Portable enterprise deployment
- Multi-device support
- Advanced key management
- Team collaboration features

### Level 5 (⭐⭐⭐⭐⭐⭐⭐)
- NFC + DMZ isolation
- Raspberry Pi air-gapped server
- Quantum-resistant research
- Physical layer encryption (EMF)

**Want more security?** Each level builds on the previous one. Start with Level 1, upgrade when needed.

---

## 🐛 Troubleshooting

### USB Drive Not Found

**Problem:** Wizard can't find your USB drive

**Solutions:**
1. Make sure USB is connected and mounted
2. Check it appears in Finder/File Explorer
3. Try path: `/Volumes/YOUR_USB_NAME` (macOS)
4. Ensure USB is not read-only

---

### Can't Write to USB

**Problem:** "Permission denied" error

**Solutions:**
1. Check USB is not write-protected (physical switch)
2. Verify permissions: Right-click → Get Info → Sharing & Permissions
3. Try reformatting USB as:
   - macOS: Mac OS Extended (Journaled)
   - Windows: NTFS or exFAT
   - Linux: ext4 or exFAT

---

### NFC Not Working

**Problem:** NFC tag not detected

**Solutions:**
1. **No NFC reader?** Just skip NFC step or type passkey manually
2. Check NFC reader is connected (USB)
3. Verify tag is ISO15693 compatible
4. Try holding tag closer to reader
5. System entropy alone is still secure!

---

### Encryption Failed

**Problem:** Folder lock fails midway

**Solutions:**
1. Ensure enough disk space (2x folder size)
2. Close other applications using the folder
3. Check USB vault is still connected
4. Verify vault was initialized correctly
5. Try with a smaller test folder first

---

### Can't Unlock Folder

**Problem:** Decryption fails or wrong passkey

**Solutions:**
1. **Double-check passkey** (case-sensitive!)
2. Ensure USB vault is the correct one
3. Verify `.locked` folder is not corrupted
4. Check vault files exist: `chaos_alphabet.txt`, `master_key.bin`
5. Try on original computer (if moved)

---

## 🤝 Contributing

Contributions are welcome! Here's how:

### Reporting Bugs
1. Check existing issues first
2. Provide detailed description
3. Include Python version, OS, error messages
4. Steps to reproduce

### Suggesting Features
1. Open an issue with `[Feature Request]` tag
2. Explain use case and benefits
3. Consider security implications

### Pull Requests
1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

### Code Style
- Follow PEP 8
- Add docstrings to functions
- Include type hints where possible
- Write tests for new features

---

## 📜 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

**TL;DR:** You can use, modify, and distribute this software freely. Just keep the copyright notice.

---

## 🙏 Acknowledgments

- **Cryptography:** Uses the excellent [cryptography](https://cryptography.io/) library
- **GUI:** Built with [PyQt6](https://www.riverbankcomputing.com/software/pyqt/)
- **Inspiration:** Combining physical security with digital encryption
- **Community:** Thanks to all testers and contributors!

---

## 📞 Support & Contact

### Documentation
- 📖 [Setup Guide](docs/SETUP_GUIDE.md)
- 🔒 [Security Details](docs/SECURITY.md)
- 🐛 [Troubleshooting](docs/TROUBLESHOOTING.md)

### Community
- 💬 [GitHub Discussions](https://github.com/aimarketingflow/chaos-lock-level-1-public/discussions)
- 🐛 [Issue Tracker](https://github.com/aimarketingflow/chaos-lock-level-1-public/issues)
- 📧 Email: [your-email@example.com]

### Social
- 🔗 LinkedIn: [Your LinkedIn Profile]
- 🐦 Twitter: [@YourHandle]
- 🌐 Website: [your-website.com]

---

## ⚠️ Disclaimer

**Important:** This software is provided "as is" without warranty. While we've implemented strong encryption:

- ⚠️ Always keep backups of important files
- ⚠️ Test unlock before deleting originals
- ⚠️ Store USB vault securely
- ⚠️ Use strong passkeys
- ⚠️ This is Level 1 (beginner security)

For maximum security needs, consider Level 4-5 or enterprise solutions.

---

## 🚀 Getting Started

Ready to take control of your data?

1. **Clone the repo**
2. **Install dependencies**
3. **Run the wizard**
4. **Lock your first folder**

```bash
git clone https://github.com/aimarketingflow/chaos-lock-level-1-public.git
cd chaos-lock-level-1-public
pip install -r requirements.txt
python3 level1_easy_wizard.py
```

**Your data. Your keys. Your control.** 🔐

---

## 🔗 Links & Resources

### Official Resources
- 🌐 **[Official Website](https://aimarketingflow.com/chaos-lock/)** - Project homepage and updates
- 🎥 **[Demo Video](https://www.youtube.com/watch?v=GCxGdX1ROZI)** - Watch Chaos Lock in action
- 💻 **[GitHub Repository](https://github.com/aimarketingflow/chaos-lock-level-1-public)** - Source code and releases

### Documentation
- 📦 **[Installation Guide](docs/INSTALLATION_GUIDE.md)** - Complete setup instructions
- ⚡ **[Quick Tutorial](docs/TUTORIAL.md)** - Get started in 5 minutes
- 🔒 **[Security FAQ](docs/SECURITY_FAQ.md)** - Security questions answered
- 🛠️ **[Hardware Guide](docs/HARDWARE.md)** - USB drives and NFC recommendations

### Community & Support
- 🐛 **[Report Issues](https://github.com/aimarketingflow/chaos-lock-level-1-public/issues)** - Bug reports and feature requests
- 💬 **[Discussions](https://github.com/aimarketingflow/chaos-lock-level-1-public/discussions)** - Ask questions and share ideas
- 🔐 **[Security Policy](SECURITY.md)** - Responsible disclosure

### Follow AI Marketing Flow
- 🌐 **Website:** [aimarketingflow.com](https://www.aimarketingflow.com)
- 💼 **LinkedIn:** [AI Marketing Flow](https://www.linkedin.com/company/aimarketingflow)
- 💻 **GitHub:** [@aimarketingflow](https://github.com/aimarketingflow)

---

<div align="center">

**Made with ❤️ for privacy and security**

⭐ Star this repo if you find it useful!

[Official Website](https://aimarketingflow.com/chaos-lock/) · [Watch Demo](https://www.youtube.com/watch?v=GCxGdX1ROZI) · [Documentation](docs/) · [Report Bug](https://github.com/aimarketingflow/chaos-lock-level-1-public/issues)

</div>
