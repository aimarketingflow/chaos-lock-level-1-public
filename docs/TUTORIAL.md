# ⚡ 5-Minute Tutorial - Chaos Lock Level 1

**Get started with Chaos Lock in 5 minutes**

---

## 🎯 What You'll Learn

In this quick tutorial, you'll:
1. ✅ Set up your USB vault (2 min)
2. 🔒 Lock your first folder (1 min)
3. 🔓 Unlock it back (1 min)
4. 🎓 Understand best practices (1 min)

**Total time: ~5 minutes**

---

## 📦 Before You Start

Make sure you have:
- ✅ Chaos Lock installed ([Installation Guide](INSTALLATION_GUIDE.md))
- ✅ USB drive connected
- ✅ Test folder ready (or we'll create one)

---

## 🚀 Part 1: Setup Your Vault (2 min)

### Step 1: Launch Setup Wizard

```bash
python3 level1_easy_wizard.py
```

### Step 2: Follow the 6 Steps

**Quick walkthrough:**

1. **Security Level** → Click "Next" (confirms Easy Mode)
2. **USB Selection** → Browse to your USB drive → "Next"
3. **Initialize** → Wait ~5 seconds → "Next"
4. **NFC/Passkey** → Choose one:
   - Type a passkey (e.g., "MySecurePass123")
   - Or skip for USB-only
5. **Chaos Capture** → Wait 30 seconds (use computer normally)
6. **Complete** → Click "Finish"

**✅ Your vault is ready!**

---

## 🔒 Part 2: Lock a Folder (1 min)

### Step 1: Create Test Folder

```bash
# Create test folder on Desktop
mkdir ~/Desktop/my_secrets

# Add a test file
echo "This is my secret data!" > ~/Desktop/my_secrets/secret.txt
```

### Step 2: Launch Folder Lock Manager

```bash
python3 level1_folder_lock.py
```

### Step 3: Lock the Folder

1. **Lock tab** (should be selected)
2. **Folder to Lock** → Browse → Select `my_secrets`
3. **USB Vault** → Browse → Select your USB drive
4. **Passkey** → Enter passkey (if you set one)
5. Click **"Lock Folder"**
6. Wait for progress bar to complete (~10 seconds)

**✅ Folder is now encrypted!**

**What happened:**
- `my_secrets` → `my_secrets.locked`
- Files inside are encrypted
- Original folder deleted (safely stored in .locked)

### Step 4: Verify Encryption

```bash
# Try to open the encrypted file
cat ~/Desktop/my_secrets.locked/secret.txt.enc

# You'll see gibberish - it's encrypted! 🔒
```

---

## 🔓 Part 3: Unlock the Folder (1 min)

### Step 1: Switch to Unlock Tab

In the same Folder Lock Manager window:
1. Click **"Unlock"** tab

### Step 2: Unlock the Folder

1. **Locked Folder** → Browse → Select `my_secrets.locked`
2. **USB Vault** → Browse → Select your USB drive
3. **Passkey** → Enter same passkey
4. Click **"Unlock Folder"**
5. Wait for progress bar (~10 seconds)

**✅ Folder is restored!**

### Step 3: Verify Decryption

```bash
# Check your file is back
cat ~/Desktop/my_secrets/secret.txt

# Should show: "This is my secret data!"
```

**Perfect! Your files are decrypted and readable again.** 🎉

---

## 🎓 Part 4: Best Practices (1 min)

### ✅ DO:

**Keep USB Safe**
- Store in secure location
- Separate from encrypted files
- Consider encrypted backup

**Use Strong Passkeys**
- 12+ characters
- Mix letters, numbers, symbols
- Unique (not used elsewhere)

**Test Before Trusting**
- Always test unlock before deleting originals
- Start with non-critical files
- Verify decryption works

**Regular Backups**
- Backup USB vault to secure location
- Keep backup encrypted
- Test restore process

### ❌ DON'T:

**Don't Store Together**
- ❌ USB + encrypted files in same place
- ❌ Defeats the purpose of two-factor security

**Don't Use Weak Passkeys**
- ❌ "password", "123456", your name
- ❌ Short passkeys (< 8 chars)

**Don't Skip Testing**
- ❌ Locking important files without testing first
- ❌ Deleting originals before verifying unlock

**Don't Share**
- ❌ Sharing USB vault
- ❌ Sharing passkey
- ❌ Both = anyone can decrypt

---

## 🎯 Real-World Workflow

### Daily Use Example:

**Morning: Lock sensitive files before leaving**
```bash
# Lock your tax documents
python3 level1_folder_lock.py
# Select: ~/Documents/Taxes_2024
# Lock with USB + passkey
# Take USB with you or store securely
```

**Evening: Unlock when needed**
```bash
# Unlock to work on taxes
python3 level1_folder_lock.py
# Select: ~/Documents/Taxes_2024.locked
# Unlock with USB + passkey
# Work on files
# Lock again when done
```

### Travel Example:

**Before trip:**
1. Lock important folders on laptop
2. Take USB vault with you (separate bag)
3. Laptop stolen? Files are encrypted ✅

**At destination:**
1. Connect USB vault
2. Unlock folders you need
3. Work normally
4. Lock before leaving hotel

---

## 🔄 Common Workflows

### Workflow 1: Daily Lock/Unlock

**Use case:** Protect files when away from computer

```
Morning:
  Lock folders → Take USB → Leave computer

Evening:
  Return → Connect USB → Unlock folders
```

**Best for:**
- Shared computers
- Office environments
- Travel

---

### Workflow 2: Long-Term Storage

**Use case:** Archive sensitive files

```
One-time:
  Lock folders → Store USB safely → Delete .locked from computer
  
When needed:
  Connect USB → Unlock → Use files → Lock again
```

**Best for:**
- Tax documents (after filing)
- Old photos/videos
- Archived projects

---

### Workflow 3: Portable Security

**Use case:** Secure files on external drive

```
Setup:
  Lock folders on external drive → USB vault separate
  
Transport:
  Carry external drive + USB vault separately
  
Use:
  Connect both → Unlock → Work → Lock
```

**Best for:**
- Client data
- Portable projects
- Backup drives

---

## 📊 Quick Reference Card

### Commands:
```bash
# Setup (one-time)
python3 level1_easy_wizard.py

# Daily use
python3 level1_folder_lock.py
```

### Keyboard Shortcuts:
- `Tab` - Switch between Lock/Unlock tabs
- `Cmd/Ctrl + O` - Browse for folder
- `Enter` - Start lock/unlock (when ready)

### File Extensions:
- `.locked` - Encrypted folder
- `.enc` - Encrypted file inside .locked folder

### USB Vault Location:
```
/Volumes/YOUR_USB/.chaos_vault/
```

---

## 🎥 Video Tutorial

**Watch the full tutorial:**

[📺 5-Minute Video Tutorial - Coming Soon]

**Chapters:**
- 0:00 - Introduction
- 0:30 - Setup wizard
- 2:30 - Locking a folder
- 3:30 - Unlocking a folder
- 4:30 - Best practices

---

## ✅ Checklist: You're Ready When...

- [ ] USB vault created successfully
- [ ] Test folder locked and unlocked
- [ ] Understand passkey importance
- [ ] Know where USB vault is stored
- [ ] Tested with non-critical files first
- [ ] Read security best practices

**All checked? You're ready to use Chaos Lock!** 🎉

---

## 🚀 Next Steps

**Now that you know the basics:**

1. 📖 Read [Security FAQ](SECURITY_FAQ.md) - Common questions
2. 🛠️ Check [Hardware Recommendations](HARDWARE.md) - NFC options
3. 🔒 Review [Security Details](SECURITY.md) - Technical specs
4. 💬 Join [Community](https://github.com/aimarketingflow/chaos-lock-level-1-public/discussions)

---

## 💡 Pro Tips

### Tip 1: Multiple Vaults
Create separate vaults for different purposes:
- Personal vault (personal files)
- Work vault (work files)
- Family vault (shared files)

### Tip 2: Backup Strategy
```bash
# Backup your USB vault
cp -r /Volumes/USB1/.chaos_vault /Volumes/USB2/.chaos_vault

# Test backup works
# Use USB2 to unlock a folder
```

### Tip 3: Folder Naming
```bash
# Clear naming helps
~/Documents/Taxes_2024/         # Clear
~/Documents/Important_Stuff/    # Vague

# After locking
~/Documents/Taxes_2024.locked/  # You know what it is
```

### Tip 4: Quick Access
```bash
# Create aliases for quick launch
echo "alias lock='python3 ~/path/to/level1_folder_lock.py'" >> ~/.zshrc
source ~/.zshrc

# Now just type:
lock
```

---

## 🆘 Stuck? Quick Troubleshooting

### "Can't find USB"
→ Check USB is mounted in Finder/Explorer
→ Try full path: `/Volumes/YOUR_USB_NAME`

### "Wrong passkey"
→ Passkeys are case-sensitive
→ Make sure you're using same USB vault

### "Encryption failed"
→ Check disk space (need 2x folder size)
→ Close apps using the folder
→ Try smaller test folder first

**More help:** [Full Troubleshooting Guide](TROUBLESHOOTING.md)

---

## 🎓 You Did It!

**Congratulations!** You've completed the 5-minute tutorial.

You now know how to:
- ✅ Set up a USB vault
- ✅ Lock folders with encryption
- ✅ Unlock folders safely
- ✅ Follow security best practices

**Your data. Your keys. Your control.** 🔐

---

**Questions? Check the [FAQ](SECURITY_FAQ.md) or [ask the community](https://github.com/aimarketingflow/chaos-lock-level-1-public/discussions)!**

*Last updated: November 21, 2024*
