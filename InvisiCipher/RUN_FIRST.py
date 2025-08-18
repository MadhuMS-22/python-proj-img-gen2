#!/usr/bin/env python3
import sys, os


import os, sys, subprocess, importlib.util, pathlib, shutil, io
sys.path.append(os.path.dirname(__file__))

ROOT = pathlib.Path(__file__).resolve().parent

def in_venv():
    return (sys.prefix != sys.base_prefix) or hasattr(sys, "real_prefix")

def ensure_venv():
    if not in_venv():
        py = shutil.which("python") or shutil.which("python3")
        print("[!] Please run inside the virtual environment created by setup script.")
        print("    Windows: .venv\\Scripts\\python.exe RUN_FIRST.py")
        print("    Linux:   ./.venv/bin/python RUN_FIRST.py")
        sys.exit(1)

def try_import(mod):
    try:
        __import__(mod)
        return True
    except Exception as e:
        print(f"[miss] {mod}: {e}")
        return False

def find_gui_entry():
    # Look for a likely GUI entry file in repo (PyQt5)
    candidates = []
    for p in ROOT.rglob("*.py"):
        try:
            txt = p.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        if "PyQt5.QtWidgets" in txt or "PySide2.QtWidgets" in txt:
            if "if __name__ == \"__main__\"" in txt or "QApplication(" in txt:
                candidates.append(p)
    # common names first
    candidates.sort(key=lambda p: (p.name not in ("gui.py","main.py","app.py"), len(str(p))))
    return candidates

def launch_gui(path):
    print(f"[+] Launching GUI: {path}")
    return subprocess.call([sys.executable, str(path)])

def fallback_demo():
    # Minimal LSB + AES demo so the user can still test
    print("[*] Starting fallback demo (LSB + AES).")
    try:
        from PyQt5 import QtWidgets, QtCore, QtGui
    except Exception as e:
        print("PyQt5 missing. Install with: pip install PyQt5")
        return 1

    from Crypto.Cipher import AES
    from Crypto.Random import get_random_bytes
    from Crypto.Util.Padding import pad, unpad
    from PIL import Image
    import numpy as np
    import os

    class Demo(QtWidgets.QWidget):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("InvisiCipher - Fallback Demo (LSB + AES)")
            self.resize(500, 200)
            layout = QtWidgets.QVBoxLayout(self)
            self.info = QtWidgets.QLabel("This is a simple demo for beginners.\n"
                                         "Hide/Reveal using LSB + AES (not the DL model).")
            layout.addWidget(self.info)
            self.btn_hide = QtWidgets.QPushButton("Hide (cover.png + secret.png -> stego.png)")
            self.btn_reveal = QtWidgets.QPushButton("Reveal (stego.png -> revealed_secret.png)")
            layout.addWidget(self.btn_hide)
            layout.addWidget(self.btn_reveal)
            self.btn_hide.clicked.connect(self.do_hide)
            self.btn_reveal.clicked.connect(self.do_reveal)
            self.key = get_random_bytes(16)

        def aes_encrypt(self, data):
            iv = get_random_bytes(16)
            cipher = AES.new(self.key, AES.MODE_CBC, iv)
            return iv + cipher.encrypt(pad(data, 16))

        def aes_decrypt(self, data):
            iv, ct = data[:16], data[16:]
            cipher = AES.new(self.key, AES.MODE_CBC, iv)
            return unpad(cipher.decrypt(ct), 16)

        def do_hide(self):
            cover = Image.open(ROOT / "demo_images" / "cover.png").convert("RGB")
            secret = Image.open(ROOT / "demo_images" / "secret.png").convert("RGB").resize(cover.size)
            # encrypt raw RGB bytes
            data = self.aes_encrypt(secret.tobytes())
            # pack into pixels via LSB (truncate if too big)
            import numpy as np
            arr = np.array(cover).copy()
            bits = np.unpackbits(np.frombuffer(data, dtype=np.uint8))
            max_bits = arr.size  # 3*W*H
            bits = bits[:max_bits]
            flat = arr.reshape(-1)
            flat[:len(bits)] = (flat[:len(bits)] & 0xFE) | bits
            stego = flat.reshape(arr.shape)
            Image.fromarray(stego).save(ROOT / "stego.png")
            QtWidgets.QMessageBox.information(self, "Done", "Saved stego.png")

        def do_reveal(self):
            stego = Image.open(ROOT / "stego.png").convert("RGB")
            import numpy as np
            arr = np.array(stego)
            flat = arr.reshape(-1)
            bits = flat & 1
            # re-pack to bytes
            packed = np.packbits(bits)
            try:
                raw = self.aes_decrypt(bytes(packed))
                # try to restore image
                w, h = stego.size
                # we stored one full RGB image size, but truncated maybe
                expected = w*h*3
                raw = raw[:expected]
                from PIL import Image
                img = Image.frombytes("RGB", (w, h), raw, "raw")
                img.save(ROOT / "revealed_secret.png")
                QtWidgets.QMessageBox.information(self, "Done", "Saved revealed_secret.png")
            except Exception as e:
                QtWidgets.QMessageBox.warning(self, "Error", f"Failed: {e}")

    app = QtWidgets.QApplication(sys.argv)
    w = Demo()
    w.show()
    return app.exec_()

def main():
    ensure_venv()
    # Try to launch our known GUI first
    explicit_gui = ROOT / "app" / "ui" / "main.py"
    if explicit_gui.exists():
        rc = launch_gui(explicit_gui)
        if rc == 0:
            return 0
    # Otherwise scan for any PyQt GUI entry
    gui_files = find_gui_entry()
    if gui_files:
        for gf in gui_files:
            rc = launch_gui(gf)
            if rc == 0:
                return 0
    print("[!] Could not auto-launch the project's GUI.")
    print("    Starting fallback demo instead.")
    return fallback_demo()

if __name__ == "__main__":
    sys.exit(main())
