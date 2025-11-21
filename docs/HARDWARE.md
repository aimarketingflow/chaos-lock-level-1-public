# 🛠️ Hardware Recommendations - Chaos Lock Level 1

**Recommended hardware for optimal security**

---

## 📋 Required Hardware

### USB Drive (Required)

**Purpose:** Store your encryption vault

**Minimum specs:**
- **Capacity:** 1 MB+ free space (vault is tiny)
- **Type:** Any USB 2.0/3.0 drive
- **Format:** Any (FAT32, exFAT, NTFS, HFS+)

**Recommended:**
- **Capacity:** 4-32 GB (room for backups)
- **Speed:** USB 3.0+ (faster encryption)
- **Brand:** SanDisk, Samsung, Kingston (reliable)
- **Durability:** Metal casing (vs plastic)

**Budget options:**
- 💰 **$5-10:** Generic 8GB USB 2.0
- 💰💰 **$10-20:** SanDisk 16GB USB 3.0
- 💰💰💰 **$20-40:** Samsung 32GB USB 3.1 (metal)

**Pro tip:** Buy 2 identical drives (one for backup)

---

## 🏷️ NFC Hardware (Optional but Recommended)

### NFC Reader

**Purpose:** Read NFC tags for authentication (no typing passkeys)

**Recommended models:**

#### Budget: ACR122U (~$40)
- ✅ Most popular NFC reader
- ✅ Works with macOS, Linux, Windows
- ✅ Supports ISO15693 tags
- ✅ USB powered
- ✅ Widely available
- ❌ Bulky design

**Where to buy:**
- Amazon: ~$40
- eBay: ~$30-35
- AliExpress: ~$25-30

---

#### Mid-Range: ACR1252U (~$60)
- ✅ Compact design
- ✅ Better build quality
- ✅ Faster read speeds
- ✅ LED indicators
- ✅ Professional look

**Where to buy:**
- Amazon: ~$60
- Official ACS store

---

#### Premium: ACR1255U-J1 (~$80)
- ✅ Bluetooth + USB
- ✅ Portable (battery powered)
- ✅ Works with mobile devices
- ✅ Sleek design
- ✅ Best for travel

**Where to buy:**
- Amazon: ~$80-90
- Official ACS store

---

#### Budget Alternative: PN532 Module (~$10)
- ✅ Very cheap
- ✅ Works with Raspberry Pi
- ✅ DIY-friendly
- ❌ Requires technical setup
- ❌ No official drivers

**Where to buy:**
- Amazon: ~$10-15
- AliExpress: ~$5-8

**Note:** Requires Python NFC library setup

---

### NFC Tags

**Purpose:** Physical authentication token (like a key)

**Recommended type:** ISO15693 (ICODE SLIX)

**Why ISO15693:**
- ✅ Longer read range (~10cm vs 4cm)
- ✅ More secure than MIFARE
- ✅ Better for desktop readers
- ✅ Supported by ACR readers

**Form factors:**

#### Card (Credit card size)
- 💰 **Price:** $2-5 per card
- ✅ Fits in wallet
- ✅ Professional look
- ✅ Durable
- ❌ Can't attach to keychain

---

#### Keyfob (Keychain)
- 💰 **Price:** $3-6 per fob
- ✅ Attach to keys
- ✅ Always with you
- ✅ Waterproof (usually)
- ❌ Bulkier than card

---

#### Sticker (Adhesive)
- 💰 **Price:** $1-3 per sticker
- ✅ Cheapest option
- ✅ Stick anywhere
- ✅ Very thin
- ❌ Less durable
- ❌ Can't remove easily

---

**Where to buy NFC tags:**
- Amazon: Search "ISO15693 NFC tag"
- eBay: Bulk packs (10-50 tags)
- AliExpress: Cheapest (slow shipping)
- TagsForDroid.com: Specialized NFC store

**Recommended pack:**
- 5x ISO15693 cards (~$10-15)
- Use 1, backup 4

---

## 💻 Computer Requirements

### Minimum Specs

**Operating System:**
- macOS 10.14+ (Mojave or later)
- Linux: Ubuntu 20.04+, Debian 10+, Fedora 33+
- Windows 10+ (64-bit)

**Hardware:**
- **CPU:** Any modern processor (Intel/AMD/ARM)
- **RAM:** 512 MB available
- **Disk:** 50 MB for application
- **USB Port:** USB 2.0+ (for vault + NFC reader)

**Software:**
- Python 3.8 or higher
- pip (Python package manager)

---

### Recommended Specs

**For best performance:**
- **CPU:** Intel i5/AMD Ryzen 5 or better
- **RAM:** 2 GB+ available
- **Disk:** SSD (faster encryption)
- **USB:** USB 3.0+ ports (faster transfers)

**Why it matters:**
- Faster CPU = faster encryption
- More RAM = handle larger folders
- SSD = much faster file operations
- USB 3.0 = 10x faster than USB 2.0

---

## 🎯 Complete Setup Recommendations

### Budget Setup (~$15)

**What you get:**
- Generic 8GB USB drive ($8)
- Skip NFC (type passkey instead)
- Total: ~$8-15

**Good for:**
- Testing Chaos Lock
- Personal use
- Low-security needs
- Budget-conscious users

---

### Standard Setup (~$60)

**What you get:**
- SanDisk 16GB USB 3.0 ($15)
- ACR122U NFC reader ($40)
- 5x ISO15693 NFC cards ($10)
- Total: ~$65

**Good for:**
- Daily use
- Personal + work files
- Convenient authentication
- Most users (recommended)

---

### Premium Setup (~$150)

**What you get:**
- Samsung 32GB USB 3.1 metal ($30)
- ACR1255U-J1 Bluetooth reader ($80)
- 10x ISO15693 NFC keyfobs ($30)
- Backup USB drive ($30)
- Total: ~$170

**Good for:**
- Maximum convenience
- Travel-friendly
- Multiple vaults
- Professional use

---

### Pro Setup (~$300+)

**What you get:**
- 2x Samsung T7 portable SSD ($150 each)
- ACR1255U-J1 reader ($80)
- 20x ISO15693 tags (mixed) ($40)
- Raspberry Pi for Level 5 ($100)
- Total: ~$520

**Good for:**
- Large file encryption
- Maximum speed
- Future Level 5 upgrade
- Enterprise use

---

## 🔍 Buying Guide

### USB Drive Selection

**What to look for:**

✅ **Reliability:**
- Stick with known brands
- Check reviews (4+ stars)
- Avoid ultra-cheap no-name drives

✅ **Speed:**
- USB 3.0 minimum (blue port)
- USB 3.1/3.2 even better
- Check MB/s ratings (100+ MB/s)

✅ **Durability:**
- Metal casing > plastic
- Water-resistant is bonus
- Keychain loop (won't lose it)

✅ **Capacity:**
- 8-16 GB is plenty for vault
- 32 GB if storing backups
- 64+ GB overkill for vault alone

❌ **Avoid:**
- Ultra-cheap drives (<$5 for 16GB)
- No-name brands
- USB 2.0 (too slow)
- Tiny drives (easy to lose)

---

### NFC Reader Selection

**What to look for:**

✅ **Compatibility:**
- Explicitly supports ISO15693
- Works with your OS
- USB powered (no batteries)

✅ **Build quality:**
- Solid construction
- Good reviews
- Known brand (ACS, HID)

✅ **Features:**
- LED indicators (helpful)
- Compact design (desk space)
- Long cable (flexibility)

❌ **Avoid:**
- MIFARE-only readers
- Bluetooth-only (less reliable)
- No ISO15693 support
- Generic Chinese brands (hit or miss)

---

### NFC Tag Selection

**What to look for:**

✅ **Type:**
- ISO15693 (ICODE SLIX) required
- NOT MIFARE Classic (wrong type)
- NOT NTAG (wrong type)

✅ **Form factor:**
- Cards for wallet
- Keyfobs for keychain
- Stickers for laptop/desk

✅ **Quality:**
- Name-brand chips (NXP)
- Good reviews
- Bulk packs (cheaper per tag)

❌ **Avoid:**
- Wrong tag type (MIFARE, NTAG)
- Ultra-thin stickers (fragile)
- No-name chips (may not work)

---

## 🛒 Where to Buy

### USB Drives

**Amazon:**
- ✅ Fast shipping (Prime)
- ✅ Easy returns
- ✅ Good selection
- ❌ Slightly more expensive

**Best Buy / Micro Center:**
- ✅ In-store pickup
- ✅ Can see/touch before buying
- ✅ Good return policy
- ❌ Limited selection

**Newegg:**
- ✅ Tech-focused
- ✅ Good deals
- ✅ Bulk options
- ❌ Shipping can be slow

---

### NFC Readers

**Amazon:**
- ACR122U: ~$40
- ACR1252U: ~$60
- ACR1255U-J1: ~$80

**Official ACS Store:**
- Direct from manufacturer
- Sometimes cheaper
- Slower shipping

**eBay:**
- Used/refurbished options
- Can find deals
- Check seller ratings

---

### NFC Tags

**Amazon:**
- Search: "ISO15693 NFC tags"
- Filter by Prime shipping
- Read reviews carefully

**TagsForDroid.com:**
- Specialized NFC store
- Good selection
- Helpful guides

**AliExpress:**
- Cheapest option
- Bulk packs
- 2-4 week shipping

---

## 📦 Starter Kits

### DIY Starter Kit

**Build your own:**
1. USB drive from Amazon ($15)
2. NFC reader from Amazon ($40)
3. NFC tags from Amazon ($10)
4. Total: ~$65

**Advantage:** Choose exactly what you want

---

### Pre-Made Kit (Future)

**Coming soon:** Official Chaos Lock starter kit

**Would include:**
- Tested USB drive
- Compatible NFC reader
- 5x NFC tags
- Quick start guide
- All verified to work together

**Estimated price:** ~$70-80

**Interest?** Let us know in [GitHub Discussions](https://github.com/aimarketingflow/chaos-lock-level-1-public/discussions)

---

## 🔧 Setup Tips

### USB Drive Setup

**Before first use:**

1. **Format the drive:**
   ```bash
   # macOS
   Disk Utility → Erase → Mac OS Extended (Journaled)
   
   # Windows
   Format → exFAT or NTFS
   
   # Linux
   GParted → Format → ext4 or exFAT
   ```

2. **Label it clearly:**
   - "Chaos Vault 1" (not "Secret Keys"!)
   - Helps identify, doesn't reveal purpose

3. **Test write permissions:**
   ```bash
   # Create test file
   echo "test" > /Volumes/YOUR_USB/test.txt
   
   # If error: fix permissions
   ```

---

### NFC Reader Setup

**Installation:**

**macOS:**
- Plug in → should work automatically
- No drivers needed (usually)

**Windows:**
- May need ACS drivers
- Download from: acs.com.hk

**Linux:**
- Install libnfc: `sudo apt install libnfc-bin`
- May need udev rules

**Test reader:**
```bash
# Check if detected
lsusb | grep ACS

# Should show: "ACS ACR122U" or similar
```

---

### NFC Tag Setup

**First-time use:**

1. **Test tag with reader:**
   - Hold tag near reader
   - Should see LED flash
   - Tag UID should be readable

2. **Label tags:**
   - Use stickers or marker
   - "Vault 1", "Vault 2", etc.
   - Don't write actual passkeys on them!

3. **Store safely:**
   - Wallet (cards)
   - Keychain (fobs)
   - Desk drawer (stickers)
   - NOT with USB vault

---

## 🎓 Advanced Hardware

### For Level 5 (Future)

**Raspberry Pi Setup:**
- Raspberry Pi 4 (4GB RAM) - $55
- PN5180 NFC HAT - $30
- USB Ethernet adapter - $15
- MicroSD card (32GB) - $10
- Power supply - $10
- Total: ~$120

**Purpose:** Air-gapped NFC server in DMZ

---

### For Maximum Security

**Hardware Security Module (HSM):**
- YubiKey 5 NFC - $50
- Nitrokey Pro 2 - $60
- Purpose: Hardware-backed key storage

**Note:** Level 1 doesn't support HSM (yet)

---

## 💡 Pro Tips

### Tip 1: Buy Duplicates

**Always buy 2 of everything:**
- 2x USB drives (primary + backup)
- 2x NFC tags (daily + backup)
- Store backups separately

**Cost:** +50% upfront
**Benefit:** Never locked out

---

### Tip 2: Test Before Trusting

**Before using for real data:**
1. Test USB drive (read/write)
2. Test NFC reader (tag detection)
3. Test full lock/unlock cycle
4. Verify on different computer

**Time:** 10 minutes
**Benefit:** Catch issues early

---

### Tip 3: Label Everything

**Clear labeling helps:**
- USB: "Vault 1", "Vault 2"
- NFC: "Primary", "Backup"
- NOT: "Secret Keys", "Encryption"

**Why:** Identify without revealing purpose

---

### Tip 4: Protect Your Hardware

**USB drive:**
- Use keychain loop
- Store in safe place
- Avoid extreme temps
- Don't leave in computer

**NFC tags:**
- Keep in wallet/keychain
- Don't bend cards
- Avoid magnets (not affected, but good practice)
- Don't share

---

## 🆘 Troubleshooting Hardware

### USB Drive Not Detected

**Try:**
1. Different USB port
2. Restart computer
3. Check Disk Utility (macOS) / Disk Management (Windows)
4. Try on different computer
5. Reformat drive

---

### NFC Reader Not Working

**Try:**
1. Different USB port
2. Install drivers (Windows)
3. Check `lsusb` (Linux)
4. Try different NFC tag
5. Restart computer

---

### NFC Tag Not Reading

**Try:**
1. Hold tag closer to reader
2. Try different position/angle
3. Check tag type (must be ISO15693)
4. Try different tag
5. Check reader LED (should flash)

---

## 📚 Learn More

**Related documentation:**
- 📦 [Installation Guide](INSTALLATION_GUIDE.md)
- ⚡ [5-Minute Tutorial](TUTORIAL.md)
- 🔒 [Security FAQ](SECURITY_FAQ.md)
- 🛡️ [Security Details](SECURITY.md)

**Need help choosing?**
- 💬 [Ask the community](https://github.com/aimarketingflow/chaos-lock-level-1-public/discussions)

---

**Happy hardware shopping!** 🛒✨

*Last updated: November 21, 2024*
