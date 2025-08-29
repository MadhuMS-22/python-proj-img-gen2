# InvisiCipher Gen2 Launcher

This launcher automatically handles all setup and dependency installation to prevent common errors like missing `cv2` (OpenCV) or other import issues.

## Quick Start

### Windows
```bash
# Double-click or run:
launch_gen2.bat
```

### Unix/Linux/macOS
```bash
# Make executable and run:
chmod +x launch_gen2.sh
./launch_gen2.sh
```

### Manual (Any Platform)
```bash
python launch_gen2.py
```

## What the Launcher Does

1. **Creates Virtual Environment**: Sets up an isolated Python environment
2. **Upgrades pip**: Ensures latest package manager
3. **Installs Dependencies**: Installs all required packages from `requirements.txt`
4. **Validates Setup**: Checks that critical dependencies (cv2, torch, tensorflow, PyQt5, fastapi) are available
5. **Launches UI**: Starts the application with proper environment

## Troubleshooting

### Common Issues

**"No module named 'cv2'"**
- The launcher will automatically install OpenCV
- If it persists, run the launcher again

**"No module named 'fastapi'"**
- The launcher will automatically install FastAPI and dependencies
- If it persists, run the launcher again

**TensorFlow Version Issues**
- The launcher uses `tensorflow-cpu==2.16.1` which is compatible with Python 3.11
- If you need GPU support, modify `requirements.txt` after first run

### Manual Recovery

If the launcher fails, you can manually set up:

```bash
# Create virtual environment
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate

# Activate (Unix/Linux/macOS)
source .venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Run UI
python app/ui/main.py
```

## Features

- ✅ Automatic virtual environment creation
- ✅ Dependency validation
- ✅ Cross-platform support
- ✅ Error handling and recovery
- ✅ Clear status messages
- ✅ Backend auto-start integration

## Requirements

- Python 3.8 or higher
- Internet connection (for first-time dependency download)
- ~2GB disk space for dependencies

## Notes

- First run may take 5-10 minutes to download dependencies
- Subsequent runs will be much faster
- The launcher creates a `.venv` folder - don't delete it
- All dependencies are isolated in the virtual environment
