#!/usr/bin/env python3
"""
InvisiCipher Complete Setup Script
==================================

This script handles the complete setup process for InvisiCipher:
- Python version check
- Virtual environment creation
- Dependency installation with conflict resolution
- Database setup
- Model verification
- System compatibility checks

Usage:
    python setup_invisicipher.py
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path
import urllib.request
import zipfile
import sqlite3

class InvisiCipherSetup:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.venv_path = self.project_root / ".venv"
        self.python_exe = None
        self.pip_exe = None
        
    def print_header(self, title):
        print("\n" + "="*60)
        print(f" {title}")
        print("="*60)
        
    def print_step(self, step):
        print(f"\n🔧 {step}")
        print("-" * 40)
        
    def print_success(self, message):
        print(f"✅ {message}")
        
    def print_error(self, message):
        print(f"❌ {message}")
        
    def print_warning(self, message):
        print(f"⚠️  {message}")
        
    def check_python_version(self):
        """Check if Python version is compatible"""
        self.print_step("Checking Python Version")
        
        version = sys.version_info
        if version.major < 3 or (version.major == 3 and version.minor < 8):
            self.print_error(f"Python 3.8+ required. Found Python {version.major}.{version.minor}")
            return False
            
        self.print_success(f"Python {version.major}.{version.minor}.{version.micro} - Compatible")
        return True
        
    def get_python_executable(self):
        """Get the appropriate Python executable"""
        if platform.system() == "Windows":
            return "python"
        return "python3"
        
    def get_pip_executable(self):
        """Get the appropriate pip executable"""
        if platform.system() == "Windows":
            return "pip"
        return "pip3"
        
    def create_virtual_environment(self):
        """Create virtual environment"""
        self.print_step("Creating Virtual Environment")
        
        if self.venv_path.exists():
            self.print_warning("Virtual environment already exists. Removing...")
            shutil.rmtree(self.venv_path)
            
        try:
            python_exe = self.get_python_executable()
            result = subprocess.run([python_exe, "-m", "venv", str(self.venv_path)], 
                                  capture_output=True, text=True, check=True)
            self.print_success("Virtual environment created successfully")
            return True
        except subprocess.CalledProcessError as e:
            self.print_error(f"Failed to create virtual environment: {e}")
            return False
            
    def get_venv_python(self):
        """Get Python executable from virtual environment"""
        if platform.system() == "Windows":
            return self.venv_path / "Scripts" / "python.exe"
        return self.venv_path / "bin" / "python"
        
    def get_venv_pip(self):
        """Get pip executable from virtual environment"""
        if platform.system() == "Windows":
            return self.venv_path / "Scripts" / "pip.exe"
        return self.venv_path / "bin" / "pip"
        
    def upgrade_pip(self):
        """Upgrade pip to latest version"""
        self.print_step("Upgrading pip")
        
        try:
            pip_exe = self.get_venv_pip()
            result = subprocess.run([str(pip_exe), "install", "--upgrade", "pip"], 
                                  capture_output=True, text=True, check=True)
            self.print_success("pip upgraded successfully")
            return True
        except subprocess.CalledProcessError as e:
            self.print_error(f"Failed to upgrade pip: {e}")
            return False
            
    def install_dependencies(self):
        """Install all dependencies with conflict resolution"""
        self.print_step("Installing Dependencies")
        
        try:
            pip_exe = self.get_venv_pip()
            requirements_file = self.project_root / "requirements.txt"
            
            # Install dependencies with verbose output
            result = subprocess.run([str(pip_exe), "install", "-r", str(requirements_file), "--verbose"], 
                                  capture_output=True, text=True, check=True)
            
            self.print_success("All dependencies installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            self.print_error(f"Failed to install dependencies: {e}")
            self.print_warning("Attempting to install dependencies individually...")
            return self.install_dependencies_individual()
            
    def install_dependencies_individual(self):
        """Install dependencies individually to handle conflicts"""
        self.print_step("Installing Dependencies Individually")
        
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
        
        pip_exe = self.get_venv_pip()
        
        for dep in dependencies:
            try:
                print(f"Installing {dep}...")
                result = subprocess.run([str(pip_exe), "install", dep], 
                                      capture_output=True, text=True, check=True)
                self.print_success(f"Installed {dep}")
            except subprocess.CalledProcessError as e:
                self.print_error(f"Failed to install {dep}: {e}")
                return False
                
        return True
        
    def verify_dependencies(self):
        """Verify that all critical dependencies are installed"""
        self.print_step("Verifying Dependencies")
        
        python_exe = self.get_venv_python()
        test_script = """
import sys
try:
    import cv2
    print("OK: OpenCV")
except ImportError:
    print("ERROR: OpenCV")
    sys.exit(1)

try:
    import torch
    print("OK: PyTorch")
except ImportError:
    print("ERROR: PyTorch")
    sys.exit(1)

try:
    import tensorflow as tf
    print("OK: TensorFlow")
except ImportError:
    print("ERROR: TensorFlow")
    sys.exit(1)

try:
    from PyQt5.QtWidgets import QApplication
    print("OK: PyQt5")
except ImportError:
    print("ERROR: PyQt5")
    sys.exit(1)

try:
    import fastapi
    print("OK: FastAPI")
except ImportError:
    print("ERROR: FastAPI")
    sys.exit(1)

try:
    import numpy as np
    print("OK: NumPy")
except ImportError:
    print("ERROR: NumPy")
    sys.exit(1)

try:
    from PIL import Image
    print("OK: Pillow")
except ImportError:
    print("ERROR: Pillow")
    sys.exit(1)

print("All critical dependencies verified!")
"""
        
        try:
            result = subprocess.run([str(python_exe), "-c", test_script], 
                                  capture_output=True, text=True, check=True)
            print(result.stdout)
            self.print_success("All dependencies verified successfully")
            return True
        except subprocess.CalledProcessError as e:
            self.print_error(f"Dependency verification failed: {e}")
            print(e.stdout)
            print(e.stderr)
            return False
            
    def setup_database(self):
        """Setup the SQLite database"""
        self.print_step("Setting up Database")
        
        try:
            db_path = self.project_root / "invisicipher_auth.db"
            
            # Create database connection
            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()
            
            # Create users table
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
            
            self.print_success("Database setup completed")
            return True
        except Exception as e:
            self.print_error(f"Database setup failed: {e}")
            return False
            
    def verify_models(self):
        """Verify that all required model files exist"""
        self.print_step("Verifying Model Files")
        
        required_models = [
            "app/models/DEEP_STEGO/models/hide.h5",
            "app/models/DEEP_STEGO/models/reveal.h5",
            "app/models/ESRGAN/models/RRDB_ESRGAN_x4.pth"
        ]
        
        missing_models = []
        for model_path in required_models:
            full_path = self.project_root / model_path
            if not full_path.exists():
                missing_models.append(model_path)
            else:
                self.print_success(f"Found: {model_path}")
                
        if missing_models:
            self.print_warning(f"Missing model files: {missing_models}")
            self.print_warning("Some features may not work without these models")
        else:
            self.print_success("All model files verified")
            
        return len(missing_models) == 0
        
    def create_launcher_scripts(self):
        """Create launcher scripts for different platforms"""
        self.print_step("Creating Launcher Scripts")
        
        # Windows batch file
        bat_content = '''@echo off
echo ================================================
echo InvisiCipher Launcher (Windows)
echo ================================================
echo.

cd /d "%~dp0"
if not exist ".venv" (
    echo Virtual environment not found. Running setup...
    python setup_invisicipher.py
)

echo Starting InvisiCipher...
.venv\\Scripts\\python.exe launch_gen2.py
pause
'''
        
        # Unix shell script
        sh_content = '''#!/bin/bash
echo "================================================"
echo "InvisiCipher Launcher (Unix/Linux/macOS)"
echo "================================================"
echo

cd "$(dirname "$0")"
if [ ! -d ".venv" ]; then
    echo "Virtual environment not found. Running setup..."
    python3 setup_invisicipher.py
fi

echo "Starting InvisiCipher..."
source .venv/bin/activate
python launch_gen2.py
'''
        
        try:
            # Create Windows launcher
            with open(self.project_root / "launch_invisicipher.bat", "w") as f:
                f.write(bat_content)
                
            # Create Unix launcher
            with open(self.project_root / "launch_invisicipher.sh", "w") as f:
                f.write(sh_content)
                
            # Make Unix script executable
            if platform.system() != "Windows":
                os.chmod(self.project_root / "launch_invisicipher.sh", 0o755)
                
            self.print_success("Launcher scripts created")
            return True
        except Exception as e:
            self.print_error(f"Failed to create launcher scripts: {e}")
            return False
            
    def create_readme(self):
        """Create comprehensive README file"""
        self.print_step("Creating README")
        
        readme_content = '''# InvisiCipher - Secure Image Steganography Platform

## Overview
InvisiCipher is a powerful desktop application that enables secure image steganography using advanced convolutional neural networks. You can hide secret images within cover images, encrypt files with AES or Blowfish algorithms, reveal hidden content, and enhance image quality using ESRGAN super-resolution.

## Features
- **Image Steganography**: Hide secret images within cover images using CNN
- **Encryption**: AES and Blowfish encryption algorithms
- **Image Enhancement**: ESRGAN super-resolution for image quality improvement
- **Local Processing**: All operations performed locally for data privacy
- **User Authentication**: Secure login/signup system with database storage

## Quick Start

### Prerequisites
- Python 3.8 or higher
- 4GB RAM minimum (8GB recommended)
- 2GB free disk space

### Installation

#### Option 1: Automatic Setup (Recommended)
```bash
# Clone the repository
git clone <repository-url>
cd InvisiCipher

# Run the setup script
python setup_invisicipher.py
```

#### Option 2: Manual Setup
```bash
# Clone the repository
git clone <repository-url>
cd InvisiCipher

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\\Scripts\\activate
# Unix/Linux/macOS:
source .venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### Running the Application

#### Option 1: Using Launcher Scripts
```bash
# Windows
launch_invisicipher.bat

# Unix/Linux/macOS
./launch_invisicipher.sh
```

#### Option 2: Manual Launch
```bash
# Activate virtual environment
# Windows:
.venv\\Scripts\\activate
# Unix/Linux/macOS:
source .venv/bin/activate

# Run the application
python launch_gen2.py
```

## Troubleshooting

### Common Issues

#### 1. "No module named 'cv2'" Error
- Run the setup script again: `python setup_invisicipher.py`
- This will reinstall OpenCV and other dependencies

#### 2. TensorFlow Version Conflicts
- The setup script uses `tensorflow-cpu==2.16.1` which is compatible with Python 3.11
- If you need GPU support, modify `requirements.txt` after first run

#### 3. PyQt5 Installation Issues
- On some Linux systems, you may need to install system dependencies:
  ```bash
  sudo apt-get install python3-pyqt5  # Ubuntu/Debian
  sudo dnf install python3-qt5        # Fedora
  ```

#### 4. Database Connection Issues
- The application creates a SQLite database automatically
- Ensure the application has write permissions in the project directory

#### 5. Model Files Missing
- Some features require pre-trained models
- Download models from the releases page or contact the maintainers

### System Requirements

#### Minimum Requirements
- **OS**: Windows 10, macOS 10.14+, or Linux (Ubuntu 18.04+)
- **Python**: 3.8 or higher
- **RAM**: 4GB
- **Storage**: 2GB free space
- **CPU**: Multi-core processor

#### Recommended Requirements
- **OS**: Windows 11, macOS 12+, or Linux (Ubuntu 20.04+)
- **Python**: 3.9 or higher
- **RAM**: 8GB or more
- **Storage**: 5GB free space
- **CPU**: Modern multi-core processor
- **GPU**: NVIDIA GPU with CUDA support (optional, for faster processing)

## Project Structure
```
InvisiCipher/
├── app/
│   ├── models/
│   │   ├── DEEP_STEGO/          # Steganography models
│   │   ├── ESRGAN/              # Super-resolution models
│   │   └── encryption/          # Encryption algorithms
│   ├── ui/                      # PyQt5 user interface
│   └── backend/                 # FastAPI backend
├── .venv/                       # Virtual environment
├── requirements.txt             # Python dependencies
├── setup_invisicipher.py        # Setup script
├── launch_gen2.py              # Main launcher
├── launch_invisicipher.bat     # Windows launcher
├── launch_invisicipher.sh      # Unix launcher
└── README.md                   # This file
```

## Development

### Setting up Development Environment
```bash
# Clone the repository
git clone <repository-url>
cd InvisiCipher

# Create virtual environment
python -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # Unix/Linux/macOS
# or
.venv\\Scripts\\activate   # Windows

# Install development dependencies
pip install -r requirements.txt
pip install pytest black flake8  # Optional: for testing and code formatting
```

### Running Tests
```bash
# Activate virtual environment first
pytest tests/
```

## Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Support
If you encounter any issues:
1. Check the troubleshooting section above
2. Search existing issues on GitHub
3. Create a new issue with detailed information about your problem

## Acknowledgments
- TensorFlow/Keras for deep learning models
- PyTorch for ESRGAN implementation
- PyQt5 for the user interface
- FastAPI for the backend API
- OpenCV for image processing
'''
        
        try:
            with open(self.project_root / "README.md", "w") as f:
                f.write(readme_content)
            self.print_success("README.md created")
            return True
        except Exception as e:
            self.print_error(f"Failed to create README: {e}")
            return False
            
    def run_system_checks(self):
        """Run comprehensive system compatibility checks"""
        self.print_step("Running System Compatibility Checks")
        
        checks_passed = True
        
        # Check Python version
        if not self.check_python_version():
            checks_passed = False
            
        # Check available disk space
        try:
            free_space = shutil.disk_usage(self.project_root).free
            free_space_gb = free_space / (1024**3)
            if free_space_gb < 2:
                self.print_warning(f"Low disk space: {free_space_gb:.1f}GB available (2GB recommended)")
            else:
                self.print_success(f"Disk space: {free_space_gb:.1f}GB available")
        except Exception as e:
            self.print_warning(f"Could not check disk space: {e}")
            
        # Check memory
        try:
            import psutil
            memory = psutil.virtual_memory()
            memory_gb = memory.total / (1024**3)
            if memory_gb < 4:
                self.print_warning(f"Low memory: {memory_gb:.1f}GB available (4GB recommended)")
            else:
                self.print_success(f"Memory: {memory_gb:.1f}GB available")
        except ImportError:
            self.print_warning("psutil not available - could not check memory")
        except Exception as e:
            self.print_warning(f"Could not check memory: {e}")
            
        # Check platform compatibility
        platform_name = platform.system()
        if platform_name in ["Windows", "Darwin", "Linux"]:
            self.print_success(f"Platform: {platform_name} - Supported")
        else:
            self.print_warning(f"Platform: {platform_name} - May have compatibility issues")
            
        return checks_passed
        
    def setup_complete(self):
        """Final setup completion"""
        self.print_header("Setup Complete!")
        
        print("\n🎉 InvisiCipher has been successfully installed!")
        print("\n📋 Next Steps:")
        print("1. Run the application using one of these methods:")
        print("   - Windows: Double-click 'launch_invisicipher.bat'")
        print("   - Unix/Linux/macOS: Run './launch_invisicipher.sh'")
        print("   - Manual: Activate virtual environment and run 'python launch_gen2.py'")
        print("\n2. The application will start with a login screen")
        print("3. Create a new account or log in to access features")
        print("\n📚 For more information, see README.md")
        print("\n🔧 If you encounter any issues, run 'python setup_invisicipher.py' again")
        
    def run(self):
        """Run the complete setup process"""
        self.print_header("InvisiCipher Setup")
        
        print("This script will set up InvisiCipher with all necessary dependencies.")
        print("The process may take 10-15 minutes depending on your internet connection.")
        
        # Run system checks
        if not self.run_system_checks():
            self.print_error("System compatibility check failed")
            return False
            
        # Create virtual environment
        if not self.create_virtual_environment():
            return False
            
        # Upgrade pip
        if not self.upgrade_pip():
            return False
            
        # Install dependencies
        if not self.install_dependencies():
            return False
            
        # Verify dependencies
        if not self.verify_dependencies():
            return False
            
        # Setup database
        if not self.setup_database():
            return False
            
        # Verify models
        self.verify_models()
        
        # Create launcher scripts
        if not self.create_launcher_scripts():
            return False
            
        # Create README
        if not self.create_readme():
            return False
            
        # Setup complete
        self.setup_complete()
        return True

def main():
    """Main entry point"""
    setup = InvisiCipherSetup()
    success = setup.run()
    
    if success:
        print("\n✅ Setup completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Setup failed. Please check the error messages above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
