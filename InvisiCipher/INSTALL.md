# InvisiCipher Installation Guide

## Quick Start (Recommended)

### For Windows Users:
1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd InvisiCipher
   ```

2. **Run the setup script:**
   ```bash
   python setup_invisicipher.py
   ```

3. **Launch the application:**
   - Double-click `launch_invisicipher.bat`
   - OR run: `python launch_gen2.py`

### For Unix/Linux/macOS Users:
1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd InvisiCipher
   ```

2. **Run the setup script:**
   ```bash
   python3 setup_invisicipher.py
   ```

3. **Launch the application:**
   ```bash
   chmod +x launch_invisicipher.sh
   ./launch_invisicipher.sh
   ```

## Prerequisites

- **Python 3.8 or higher**
- **4GB RAM minimum** (8GB recommended)
- **2GB free disk space**
- **Internet connection** (for downloading dependencies)

## What the Setup Script Does

The `setup_invisicipher.py` script automatically:

1. ✅ **Checks Python version** (requires 3.8+)
2. ✅ **Creates virtual environment** (isolated Python environment)
3. ✅ **Upgrades pip** to latest version
4. ✅ **Installs all dependencies** with proper versions
5. ✅ **Handles dependency conflicts** automatically
6. ✅ **Sets up SQLite database** for user authentication
7. ✅ **Verifies model files** are present
8. ✅ **Creates launcher scripts** for easy startup
9. ✅ **Generates comprehensive README** with troubleshooting

## Troubleshooting

### Common Issues:

#### 1. "Python not found" Error
- **Solution:** Install Python 3.8+ from [python.org](https://python.org)
- **Windows:** Make sure to check "Add Python to PATH" during installation

#### 2. "Permission denied" Error (Linux/macOS)
- **Solution:** Run with sudo or fix permissions:
  ```bash
  sudo python3 setup_invisicipher.py
  ```

#### 3. "No module named 'cv2'" Error
- **Solution:** Run the setup script again:
  ```bash
  python setup_invisicipher.py
  ```

#### 4. "Virtual environment creation failed"
- **Solution:** Install venv module:
  ```bash
  # Ubuntu/Debian
  sudo apt-get install python3-venv
  
  # macOS
  brew install python3
  
  # Windows
  # Usually included with Python installation
  ```

#### 5. "PyQt5 installation failed" (Linux)
- **Solution:** Install system dependencies:
  ```bash
  # Ubuntu/Debian
  sudo apt-get install python3-pyqt5
  
  # Fedora
  sudo dnf install python3-qt5
  ```

#### 6. "TensorFlow installation failed"
- **Solution:** The setup script uses `tensorflow-cpu` which is more compatible
- If you need GPU support, modify `requirements.txt` after first run

### Manual Installation (If Setup Script Fails)

If the automatic setup fails, you can install manually:

```bash
# 1. Create virtual environment
python -m venv .venv

# 2. Activate virtual environment
# Windows:
.venv\Scripts\activate
# Unix/Linux/macOS:
source .venv/bin/activate

# 3. Upgrade pip
pip install --upgrade pip

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run the application
python launch_gen2.py
```

## System Requirements

### Minimum Requirements:
- **OS:** Windows 10, macOS 10.14+, or Linux (Ubuntu 18.04+)
- **Python:** 3.8 or higher
- **RAM:** 4GB
- **Storage:** 2GB free space
- **CPU:** Multi-core processor

### Recommended Requirements:
- **OS:** Windows 11, macOS 12+, or Linux (Ubuntu 20.04+)
- **Python:** 3.9 or higher
- **RAM:** 8GB or more
- **Storage:** 5GB free space
- **CPU:** Modern multi-core processor
- **GPU:** NVIDIA GPU with CUDA support (optional, for faster processing)

## First Run

After successful installation:

1. **Launch the application** using one of the methods above
2. **Create a new account** or log in if you have one
3. **Explore the features:**
   - Image Steganography (Hide/Reveal)
   - Encryption/Decryption (AES/Blowfish)
   - Super Resolution (ESRGAN)

## Getting Help

If you encounter any issues:

1. **Check this troubleshooting guide**
2. **Run the setup script again:** `python setup_invisicipher.py`
3. **Check the README.md** for detailed information
4. **Create an issue** on GitHub with:
   - Your operating system
   - Python version
   - Error message
   - Steps to reproduce

## Support

For additional support:
- 📧 Email: [support email]
- 🐛 GitHub Issues: [repository issues page]
- 📖 Documentation: [documentation link]

---

**Note:** The setup process may take 10-15 minutes on first run due to downloading large ML libraries. Subsequent runs will be much faster.
