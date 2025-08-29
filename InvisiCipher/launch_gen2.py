#!/usr/bin/env python3
"""
InvisiCipher Gen2 Launcher
==========================

This launcher automatically handles all setup and dependency installation
to prevent common errors like missing `cv2` (OpenCV) or other import issues.

Usage:
    python launch_gen2.py
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path
import time

def get_project_root():
    """Get the project root directory"""
    return Path(__file__).parent

def get_python_executable():
    """Get the appropriate Python executable"""
    if platform.system() == "Windows":
        return "python"
    return "python3"

def get_venv_python():
    """Get Python executable from virtual environment"""
    project_root = get_project_root()
    venv_path = project_root / ".venv"
    
    if platform.system() == "Windows":
        return venv_path / "Scripts" / "python.exe"
    return venv_path / "bin" / "python"

def run_command(cmd, cwd=None, check=True, capture_output=True):
    """Run a command and return the result"""
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            check=check,
            capture_output=capture_output,
            text=True,
            timeout=300  # 5 minute timeout
        )
        return result
    except subprocess.TimeoutExpired:
        print(f"Command timed out: {' '.join(cmd)}")
        return None
    except subprocess.CalledProcessError as e:
        if check:
            print(f"Command failed: {' '.join(cmd)}")
            print(f"Error: {e}")
        return e
    except FileNotFoundError:
        print(f"Command not found: {' '.join(cmd)}")
        return None

def check_python_version():
    """Check if Python version is compatible"""
    print("Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"ERROR: Python 3.8+ required. Found Python {version.major}.{version.minor}")
        return False
    print(f"OK: Python {version.major}.{version.minor}.{version.micro}")
    return True

def check_virtual_environment():
    """Check if virtual environment exists"""
    print("Checking virtual environment...")
    project_root = get_project_root()
    venv_path = project_root / ".venv"
    
    if not venv_path.exists():
        print("Virtual environment not found. Creating...")
        return create_virtual_environment()
    
    # Check if venv is valid
    python_exe = get_venv_python()
    if not python_exe.exists():
        print("Virtual environment is corrupted. Recreating...")
        shutil.rmtree(venv_path)
        return create_virtual_environment()
    
    print("OK: Virtual environment found")
    return True

def create_virtual_environment():
    """Create virtual environment"""
    print("Creating virtual environment...")
    project_root = get_project_root()
    venv_path = project_root / ".venv"
    
    python_exe = get_python_executable()
    result = run_command([python_exe, "-m", "venv", str(venv_path)], cwd=project_root)
    
    if result is None or (hasattr(result, 'returncode') and result.returncode != 0):
        print("ERROR: Failed to create virtual environment")
        return False
    
    print("OK: Virtual environment created")
    return True

def upgrade_pip():
    """Upgrade pip to latest version"""
    print("Upgrading pip...")
    python_exe = get_venv_python()
    result = run_command([str(python_exe), "-m", "pip", "install", "--upgrade", "pip"])
    
    if result is None or (hasattr(result, 'returncode') and result.returncode != 0):
        print("WARNING: Failed to upgrade pip, continuing anyway...")
        return True
    
    print("OK: pip upgraded")
    return True

def install_dependencies():
    """Install all dependencies"""
    print("Installing dependencies...")
    project_root = get_project_root()
    python_exe = get_venv_python()
    requirements_file = project_root / "requirements.txt"
    
    if not requirements_file.exists():
        print("ERROR: requirements.txt not found")
        return False
    
    # Try installing with requirements.txt first
    result = run_command([str(python_exe), "-m", "pip", "install", "-r", str(requirements_file)], cwd=project_root)
    
    if result is None or (hasattr(result, 'returncode') and result.returncode != 0):
        print("WARNING: Failed to install from requirements.txt, trying individual packages...")
        return install_dependencies_individual()
    
    print("OK: Dependencies installed")
    return True

def install_dependencies_individual():
    """Install dependencies individually to handle conflicts"""
    print("Installing dependencies individually...")
    python_exe = get_venv_python()
    
    dependencies = [
        "tensorflow-cpu==2.16.1",
        "torch==2.8.0",
        "opencv-python==4.11.0.86",
        "Pillow==11.3.0",
        "pycryptodome==3.23.0",
        "PyQt5==5.15.11",
        "numpy==1.26.4",
        "imageio==2.37.0",
        "fastapi==0.116.1",
        "uvicorn==0.35.0",
        "SQLAlchemy==2.0.43",
        "pydantic==2.11.7",
        "bcrypt==4.3.0",
        "python-jose[cryptography]==3.5.0",
        "requests==2.32.5",
        "email-validator==2.3.0",
        "python-multipart==0.0.20"
    ]
    
    failed_packages = []
    for dep in dependencies:
        print(f"Installing {dep}...")
        result = run_command([str(python_exe), "-m", "pip", "install", dep])
        if result is None or (hasattr(result, 'returncode') and result.returncode != 0):
            failed_packages.append(dep)
            print(f"WARNING: Failed to install {dep}")
    
    if failed_packages:
        print(f"WARNING: Failed to install packages: {failed_packages}")
        print("Continuing anyway...")
    
    return True

def check_dependencies():
    """Check if critical dependencies are installed"""
    print("Checking dependencies...")
    python_exe = get_venv_python()
    
    # Create a temporary test file
    test_file = get_project_root() / "test_deps.py"
    test_script = '''import sys
try:
    import cv2
    print("OK: OpenCV (cv2) is available")
except ImportError:
    print("ERROR: OpenCV (cv2) is missing")
    sys.exit(1)

try:
    import torch
    print("OK: PyTorch is available")
except ImportError:
    print("ERROR: PyTorch is missing")
    sys.exit(1)

try:
    import tensorflow as tf
    print("OK: TensorFlow is available")
except ImportError:
    print("ERROR: TensorFlow is missing")
    sys.exit(1)

try:
    from PyQt5.QtWidgets import QApplication
    print("OK: PyQt5 is available")
except ImportError:
    print("ERROR: PyQt5 is missing")
    sys.exit(1)

try:
    import fastapi
    print("OK: FastAPI is available")
except ImportError:
    print("ERROR: FastAPI is missing")
    sys.exit(1)

try:
    import numpy as np
    print("OK: NumPy is available")
except ImportError:
    print("ERROR: NumPy is missing")
    sys.exit(1)

try:
    from PIL import Image
    print("OK: Pillow is available")
except ImportError:
    print("ERROR: Pillow is missing")
    sys.exit(1)

print("All critical dependencies are available!")
'''
    
    try:
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(test_script)
        
        result = run_command([str(python_exe), str(test_file)], cwd=get_project_root(), check=False)
        success = result is not None and result.returncode == 0
        
        # Clean up test file
        if test_file.exists():
            test_file.unlink()
        
        return success
    except Exception as e:
        print(f"Error during dependency check: {e}")
        return False

def setup_database():
    """Setup the SQLite database if it doesn't exist"""
    print("Setting up database...")
    try:
        import sqlite3
        db_path = get_project_root() / "invisicipher_auth.db"
        
        if not db_path.exists():
            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    full_name TEXT NOT NULL,
                    phone TEXT,
                    password_hash TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
            conn.close()
            print("OK: Database created")
        else:
            print("OK: Database already exists")
        
        return True
    except Exception as e:
        print(f"WARNING: Database setup failed: {e}")
        return True  # Continue anyway

def verify_models():
    """Verify that model files exist"""
    print("Verifying model files...")
    project_root = get_project_root()
    
    required_models = [
        "app/models/DEEP_STEGO/models/hide.h5",
        "app/models/DEEP_STEGO/models/reveal.h5",
        "app/models/ESRGAN/models/RRDB_ESRGAN_x4.pth"
    ]
    
    missing_models = []
    for model_path in required_models:
        full_path = project_root / model_path
        if not full_path.exists():
            missing_models.append(model_path)
        else:
            print(f"OK: Found {model_path}")
    
    if missing_models:
        print(f"WARNING: Missing model files: {missing_models}")
        print("Some features may not work without these models")
    
    return True

def launch_ui():
    """Launch the InvisiCipher UI"""
    print("\n" + "="*60)
    print(" Setup complete! Launching UI...")
    print("="*60)
    print("Launching InvisiCipher Gen2 UI...")
    
    python_exe = get_venv_python()
    ui_script = get_project_root() / "app" / "ui" / "main.py"
    
    if not ui_script.exists():
        print("ERROR: UI script not found")
        return False
    
    try:
        # Change to project root directory
        os.chdir(get_project_root())
        
        # Launch the UI
        result = subprocess.run([str(python_exe), str(ui_script)], check=False)
        return result.returncode == 0
    except Exception as e:
        print(f"ERROR: Failed to launch UI: {e}")
        return False

def main():
    """Main launcher function"""
    print("="*60)
    print(" InvisiCipher Gen2 Launcher")
    print("="*60)
    print(f"Project root: {get_project_root()}")
    
    # Check Python version
    if not check_python_version():
        print("\nERROR: Python version check failed")
        print("Please install Python 3.8 or higher")
        input("Press Enter to exit...")
        return 1
    
    # Check/create virtual environment
    if not check_virtual_environment():
        print("\nERROR: Virtual environment setup failed")
        input("Press Enter to exit...")
        return 1
    
    # Upgrade pip
    if not upgrade_pip():
        print("\nWARNING: Failed to upgrade pip")
    
    # Install dependencies
    if not install_dependencies():
        print("\nERROR: Dependency installation failed")
        input("Press Enter to exit...")
        return 1
    
    # Check dependencies
    if not check_dependencies():
        print("\nERROR: Dependency check failed!")
        print("Trying to reinstall dependencies...")
        
        # Try reinstalling
        if not install_dependencies():
            print("ERROR: Failed to reinstall dependencies")
            input("Press Enter to exit...")
            return 1
        
        if not check_dependencies():
            print("ERROR: Dependency check still failing after reinstall")
            input("Press Enter to exit...")
            return 1
    
    # Setup database
    if not setup_database():
        print("\nWARNING: Database setup failed")
    
    # Verify models
    if not verify_models():
        print("\nWARNING: Model verification failed")
    
    # Launch UI
    if not launch_ui():
        print("\nERROR: Failed to launch UI")
        input("Press Enter to exit...")
        return 1
    
    return 0

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\nSetup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nUnexpected error: {e}")
        input("Press Enter to exit...")
        sys.exit(1)
