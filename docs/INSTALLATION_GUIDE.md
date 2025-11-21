# 📦 Installation Guide - Chaos Lock Level 1

**Complete step-by-step installation with screenshots**

---

## 📋 Prerequisites

Before you begin, make sure you have:

- ✅ **Python 3.8 or higher** installed
- ✅ **USB drive** (any size, at least 1 MB free space)
- ✅ **macOS 10.14+**, **Linux (Ubuntu 20.04+)**, or **Windows 10+**
- ⚪ **NFC reader + tag** (optional)

---

## 🚀 Step 1: Download & Install

### Option A: Clone from GitHub (Recommended)

```bash
# Clone the repository
git clone https://github.com/aimarketingflow/chaos-lock-level-1-public.git

# Navigate to directory
cd chaos-lock-level-1-public
```

### Option B: Download ZIP

1. Go to [GitHub Repository](https://github.com/aimarketingflow/chaos-lock-level-1-public)
2. Click green **"Code"** button
3. Select **"Download ZIP"**
4. Extract to your preferred location

---

## 📦 Step 2: Install Dependencies

Open Terminal (macOS/Linux) or Command Prompt (Windows) and run:

```bash
# Install required Python packages
pip install -r requirements.txt
```

**What gets installed:**
- `PyQt6` - GUI framework
- `cryptography` - Encryption library
- `appdirs` - Cross-platform paths

**Troubleshooting:**
- If `pip` not found, try `pip3` instead
- On Linux, you may need: `sudo apt install python3-pip`
- On macOS, install via Homebrew: `brew install python3`

---

## 🎬 Step 3: Launch Setup Wizard

### Run the Setup Wizard:

```bash
python3 level1_easy_wizard.py
```

**The wizard window will open:**

![Setup Wizard - Step 1](screenshots/wizard_step1.png)
*Screenshot: Welcome screen showing security level and requirements*

---

## 🔧 Step 4: Complete the 6-Step Setup

### Step 1: Security Level Confirmation

![Step 1 - Security Level](screenshots/wizard_step1_security.png)

- Confirms you're setting up **Level 1 (Easy Mode)**
- Shows what's included: ⭐⭐⭐⭐
- Lists requirements (USB required, NFC optional)
- Click **"Next"** to continue

---

### Step 2: Select USB Vault Location

![Step 2 - USB Selection](screenshots/wizard_step2_usb.png)

**Instructions:**
1. Connect your USB drive
2. Click **"Browse"** button
3. Navigate to your USB drive (usually `/Volumes/YOUR_USB_NAME` on macOS)
4. Select the USB drive folder
5. Click **"Next"**

**Tips:**
- USB can be any size (1 MB+ free space needed)
- Vault will be created in `.chaos_vault` hidden folder
- Don't use the same USB for storing encrypted files

---

### Step 3: Initialize Vault

![Step 3 - Vault Init](screenshots/wizard_step3_init.png)

**What happens:**
- Creates `.chaos_vault` directory on USB
- Sets up vault configuration (100k iterations)
- Prepares for chaos alphabet generation
- Takes ~5 seconds

**Progress shown:**
- ✅ Creating vault directory
- ✅ Writing configuration
- ✅ Preparing entropy collector

Click **"Next"** when complete.

---

### Step 4: NFC Tag Setup (Optional)

![Step 4 - NFC Setup](screenshots/wizard_step4_nfc.png)

**Three options:**

**Option 1: Scan NFC Tag** (Recommended if you have NFC reader)
1. Connect NFC reader to USB
2. Hold NFC tag near reader
3. Tag UID will be captured
4. Most secure option

**Option 2: Type Passkey** (No NFC reader)
1. Enter a strong passkey (8+ characters)
2. Remember it - you'll need it to unlock files
3. Case-sensitive!

**Option 3: Skip Entirely** (System entropy only)
1. Still secure with system entropy alone
2. No passkey to remember
3. USB vault is your only key

**Choose your option and click "Next"**

---

### Step 5: Chaos Capture (30 seconds)

![Step 5 - Chaos Capture](screenshots/wizard_step5_capture.png)

**What's happening:**
- Collecting system entropy for 30 seconds
- Sources: CPU timing, memory state, disk I/O, network jitter
- Generating your unique 64-character chaos alphabet
- Combining with your passkey/NFC (if provided)

**Progress bar shows:**
- Time remaining
- Entropy quality
- Real-time status

**Do NOT:**
- ❌ Disconnect USB during capture
- ❌ Close the application
- ❌ Put computer to sleep

**You CAN:**
- ✅ Use your computer normally
- ✅ Open other apps
- ✅ Type, browse, etc. (adds more entropy!)

Wait for completion (~30 seconds).

---

### Step 6: Setup Complete! 🎉

![Step 6 - Complete](screenshots/wizard_step6_complete.png)

**Success! Your vault is ready.**

**What you'll see:**
- ✅ Vault location (your USB path)
- ✅ Chaos alphabet preview (first 32 chars)
- ✅ Configuration summary
- ✅ Next steps

**Your USB now contains:**
```
/Volumes/YOUR_USB/.chaos_vault/
├── chaos_alphabet.txt      # Your unique 64-char alphabet
├── vault_config.json       # Vault settings
├── master_key.bin          # Encrypted master key
└── vault_metadata.json     # Creation info
```

**Important:**
- 🔒 Keep USB safe
- 💾 Consider making encrypted backup
- 📝 Remember your passkey (if you set one)

Click **"Finish"** to close the wizard.

---

## 🔐 Step 5: Lock Your First Folder

### Launch the Folder Lock Manager:

```bash
python3 level1_folder_lock.py
```

**The lock/unlock manager will open:**

![Folder Lock Manager](screenshots/folder_lock_main.png)
*Screenshot: Main window with Lock and Unlock tabs*

---

## 🔒 Locking a Folder

### Tab 1: Lock

![Lock Tab](screenshots/lock_tab.png)

**Instructions:**

1. **Select Folder to Lock**
   - Click **"Browse"** next to "Folder to Lock"
   - Choose folder with files you want to encrypt
   - Path will appear in text field

2. **Select USB Vault**
   - Click **"Browse"** next to "USB Vault"
   - Navigate to your USB drive
   - Select the drive (not the .chaos_vault folder)

3. **Enter Passkey/NFC**
   - If you set up NFC: Click **"Scan NFC"** and hold tag
   - If you set up passkey: Type it in the field
   - If you skipped both: Leave blank

4. **Click "Lock Folder"**
   - Progress bar will show encryption status
   - Log window shows real-time progress
   - Wait for completion

**Result:**
- Original folder becomes `folder_name.locked/`
- All files inside are encrypted
- Original folder is deleted (files are safe in .locked)

![Lock Progress](screenshots/lock_progress.png)
*Screenshot: Encryption in progress with progress bar*

![Lock Complete](screenshots/lock_complete.png)
*Screenshot: Success message after locking*

---

## 🔓 Unlocking a Folder

### Tab 2: Unlock

![Unlock Tab](screenshots/unlock_tab.png)

**Instructions:**

1. **Select Locked Folder**
   - Click **"Browse"** next to "Locked Folder"
   - Choose the `.locked` folder
   - Must end in `.locked`

2. **Select USB Vault**
   - Click **"Browse"** next to "USB Vault"
   - Navigate to your USB drive
   - Same USB you used to lock

3. **Enter Passkey/NFC**
   - Use same passkey/NFC as when locking
   - Must match exactly (case-sensitive)

4. **Click "Unlock Folder"**
   - Progress bar shows decryption status
   - Log window shows real-time progress
   - Wait for completion

**Result:**
- `.locked` folder is decrypted
- Original folder is restored with all files
- `.locked` folder is deleted

![Unlock Progress](screenshots/unlock_progress.png)
*Screenshot: Decryption in progress*

![Unlock Complete](screenshots/unlock_complete.png)
*Screenshot: Success message after unlocking*

---

## ✅ Verification

### Test Your Setup:

1. **Create a test folder:**
   ```bash
   mkdir ~/Desktop/test_folder
   echo "Hello Chaos Lock!" > ~/Desktop/test_folder/test.txt
   ```

2. **Lock it:**
   - Open `level1_folder_lock.py`
   - Select `test_folder`
   - Lock with your USB + passkey

3. **Verify encryption:**
   - Check `test_folder.locked` exists
   - Try opening files inside (should be gibberish)

4. **Unlock it:**
   - Select `test_folder.locked`
   - Unlock with same USB + passkey

5. **Verify decryption:**
   - Check `test_folder` is restored
   - Open `test.txt` (should say "Hello Chaos Lock!")

**If all steps work: ✅ Installation successful!**

---

## 🎯 Quick Reference

### Launch Commands:

```bash
# Setup wizard (one-time)
python3 level1_easy_wizard.py

# Lock/unlock manager (daily use)
python3 level1_folder_lock.py
```

### File Locations:

```
chaos-lock-level-1/
├── level1_easy_wizard.py      # Setup wizard
├── level1_folder_lock.py      # Lock/unlock GUI
├── chaos_entropy.py           # Entropy system
├── enhanced_crypto.py         # Encryption engine
└── folder_lock_cli.py         # CLI backend

USB Vault:
/Volumes/YOUR_USB/.chaos_vault/
├── chaos_alphabet.txt         # Your unique alphabet
├── vault_config.json          # Settings
├── master_key.bin             # Encrypted key
└── vault_metadata.json        # Metadata
```

---

## 🐛 Common Issues

### "Python not found"
```bash
# Try python3 instead
python3 --version

# Install Python from python.org
# Or use Homebrew (macOS): brew install python3
```

### "Module not found: PyQt6"
```bash
# Install dependencies
pip install -r requirements.txt

# Or install individually
pip install PyQt6 cryptography appdirs
```

### "USB drive not found"
- Make sure USB is connected and mounted
- Check Finder/File Explorer shows the drive
- Try full path: `/Volumes/YOUR_USB_NAME`
- Verify USB is not read-only

### "Permission denied" on USB
- Check USB is not write-protected
- Right-click USB → Get Info → Sharing & Permissions
- Try reformatting as Mac OS Extended (macOS) or exFAT

### "NFC not working"
- **No problem!** Just skip NFC or type passkey
- Check NFC reader is connected (USB)
- Verify tag is ISO15693 compatible
- System entropy alone is still secure

### "Encryption failed"
- Ensure enough disk space (2x folder size)
- Close apps using the folder
- Verify USB vault is connected
- Try with smaller test folder first

### "Wrong passkey" when unlocking
- Passkeys are case-sensitive!
- Make sure you're using correct USB vault
- Verify you're using same passkey as when locking
- Check for typos

---

## 📸 Screenshot Checklist

**For your tutorial video, capture these screens:**

### Setup Wizard:
- [ ] Step 1 - Welcome/Security Level
- [ ] Step 2 - USB Selection
- [ ] Step 3 - Vault Initialization
- [ ] Step 4 - NFC/Passkey Setup
- [ ] Step 5 - Chaos Capture (in progress)
- [ ] Step 6 - Completion screen

### Folder Lock Manager:
- [ ] Main window (both tabs visible)
- [ ] Lock tab - empty state
- [ ] Lock tab - with folder selected
- [ ] Lock in progress (progress bar)
- [ ] Lock complete (success message)
- [ ] Unlock tab - empty state
- [ ] Unlock tab - with .locked folder selected
- [ ] Unlock in progress
- [ ] Unlock complete

### File System:
- [ ] USB drive with .chaos_vault folder
- [ ] Original folder before locking
- [ ] .locked folder after encryption
- [ ] Restored folder after unlocking

---

## 🎥 Video Tutorial

**Coming soon!** Watch the 5-minute tutorial video:

[📺 YouTube Tutorial Link - Coming Soon]

**What the video covers:**
1. Installation (1 min)
2. Setup wizard walkthrough (2 min)
3. Locking a folder (1 min)
4. Unlocking a folder (1 min)

---

## 📚 Next Steps

**Now that you're installed:**

1. ✅ Read the [5-Minute Tutorial](TUTORIAL.md)
2. 🔒 Review [Security FAQ](SECURITY_FAQ.md)
3. 🛠️ Check [Hardware Recommendations](HARDWARE.md)
4. 💬 Join [GitHub Discussions](https://github.com/aimarketingflow/chaos-lock-level-1-public/discussions)

---

## 🆘 Need Help?

**Support Resources:**
- 📖 [Full Documentation](../README.md)
- 🐛 [Troubleshooting Guide](TROUBLESHOOTING.md)
- 💬 [GitHub Discussions](https://github.com/aimarketingflow/chaos-lock-level-1-public/discussions)
- 🐛 [Report Bug](https://github.com/aimarketingflow/chaos-lock-level-1-public/issues)

---

**Installation complete! Ready to secure your files.** 🔐✨

*Last updated: November 21, 2024*
