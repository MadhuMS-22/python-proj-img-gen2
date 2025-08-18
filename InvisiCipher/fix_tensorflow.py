#!/usr/bin/env python3
"""
TensorFlow Compatibility Fix Script
This script helps resolve TensorFlow installation and compatibility issues.
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def run_cmd(cmd, check=True):
    """Run a command and return the result"""
    print(f"Running: {' '.join(cmd)}")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=check)
        if result.stdout:
            print("Output:", result.stdout)
        return result
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        if e.stderr:
            print("Error output:", e.stderr)
        return e

def check_python_version():
    """Check if Python version is compatible with TensorFlow"""
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major != 3:
        print("❌ Python 3 is required")
        return False
    
    if version.minor < 7 or version.minor > 10:
        print("❌ Python 3.7-3.10 is recommended for TensorFlow 2.10.0")
        return False
    
    print("✅ Python version is compatible")
    return True

def check_tensorflow_installation():
    """Check TensorFlow installation"""
    try:
        import tensorflow as tf
        print(f"✅ TensorFlow version: {tf.__version__}")
        return True
    except ImportError:
        print("❌ TensorFlow not installed")
        return False
    except Exception as e:
        print(f"❌ TensorFlow import error: {e}")
        return False

def fix_tensorflow():
    """Attempt to fix TensorFlow installation"""
    print("\n🔧 Attempting to fix TensorFlow installation...")
    
    # Get Python executable
    python_exe = sys.executable
    
    # Uninstall existing TensorFlow
    print("1. Uninstalling existing TensorFlow...")
    run_cmd([python_exe, "-m", "pip", "uninstall", "tensorflow", "-y"], check=False)
    
    # Clear pip cache
    print("2. Clearing pip cache...")
    run_cmd([python_exe, "-m", "pip", "cache", "purge"], check=False)
    
    # Upgrade pip
    print("3. Upgrading pip...")
    run_cmd([python_exe, "-m", "pip", "install", "--upgrade", "pip"])
    
    # Install specific TensorFlow version
    print("4. Installing TensorFlow 2.10.0...")
    result = run_cmd([python_exe, "-m", "pip", "install", "tensorflow==2.10.0"])
    
    if result.returncode == 0:
        print("✅ TensorFlow installation successful")
        return True
    else:
        print("❌ TensorFlow installation failed, trying alternative...")
        
        # Try installing without version constraint
        result = run_cmd([python_exe, "-m", "pip", "install", "tensorflow"])
        if result.returncode == 0:
            print("✅ TensorFlow installation successful (alternative version)")
            return True
        else:
            print("❌ TensorFlow installation failed completely")
            return False

def main():
    print("🔍 TensorFlow Compatibility Checker")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        print("\n💡 Recommendation: Use Python 3.7-3.10 for best compatibility")
        return
    
    # Check current TensorFlow installation
    if check_tensorflow_installation():
        print("✅ TensorFlow appears to be working correctly")
        return
    
    # Try to fix TensorFlow
    if fix_tensorflow():
        print("\n✅ TensorFlow has been fixed!")
        print("Try running your application again.")
    else:
        print("\n❌ Could not fix TensorFlow automatically")
        print("\n💡 Manual troubleshooting steps:")
        print("1. Create a fresh virtual environment")
        print("2. Install Python 3.9 or 3.10")
        print("3. Run: pip install tensorflow==2.10.0")
        print("4. If still having issues, try: pip install tensorflow-cpu==2.10.0")

if __name__ == "__main__":
    main()
