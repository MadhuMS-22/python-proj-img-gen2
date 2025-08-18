# InvisiCipher — Beginner Helper Pack (Plug‑and‑Play wrappers)

This helper pack automates setup and gives you an easy way to run the GUI for the GitHub project
**Asirwad/InvisiCipher** without training anything.

> You will still **clone the original repo** from GitHub, then drop these files into its folder.

---

## What you get
- **Single launcher** (`RUN_FIRST.py`) that:
  - Validates venv activation
  - Launches the PyQt GUI at `app/ui/main.py` or falls back to a simple demo window
- **Demo images** in `demo_images/`

---

## Quick start

### 1) Clone the original repository
```bash
git clone https://github.com/Asirwad/InvisiCipher.git
```

### 2) Copy helper pack into the repo root
- Extract this ZIP
- Copy **everything** into the cloned `InvisiCipher/` folder (same place as `requirements.txt`).

Your tree should look like:
```
InvisiCipher/
  app/
  requirements.txt
  README.md
  RUN_FIRST.py
  setup_invisicipher.bat
  setup_invisicipher.sh
  demo_images/
  ...
```

### 3) Launch

```bash
# After installing requirements and activating venv
python RUN_FIRST.py
```

---

## Notes
- This helper does **not modify** the original code; it only automates launch.
- If you have a GPU and CUDA, you can install the matching PyTorch build for CUDA.

---
