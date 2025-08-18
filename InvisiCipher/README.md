<h1 align="center">
  InvisiCipher : Deep Learning-Based image Steganography with Chaotic Encryption and
Enhanced Super Resolution
</h1>

<p align="center">
  <img src="app/ui/logo.png" alt="Project Logo" width="100">
</p>

<p align="center">
  <strong>Hide secrets, enhance images!</strong>
</p>

## Overview

Welcome to our Steganography and Super Resolution project! This project combines the power of steganography techniques and super-resolution using deep learning models. Our goal is to hide a secret image within a cover image using advanced convolutional neural networks (CNNs) and then enhance the quality of the hidden image using an Enhanced Super Resolution Generative Adversarial Network (ESRGAN). We also provide an option to encrypt the steg image using various chaos encryption algorithms for added security.

## Features

✨ **Interactive Hiding**: Utilize our intuitive hide network powered by CNNs to embed secret images within cover images effortlessly.

🔒 **Secure Encryption**: Choose from multiple chaos encryption algorithms such as AES, Blowfish to encrypt your steg image and protect your secrets.

🌟 **Enhanced Super Resolution**: Witness the magic of our ESRGAN model as it enhances the resolution and quality of the hidden image, revealing every detail.

🎨 **Easy-to-Use**: Our project provides a user-friendly interface and simple scripts to perform hiding, encryption, decryption, and image enhancement with just a few lines of code.

## Project Architecture

The project architecture consists of the following components:

1. **Prepare Network**: A CNN-based network that prepares the secret image for hiding by extracting essential features and encoding it.

2. **Hide Network**: Another CNN-based network that embeds the prepared secret image within the cover image, producing the steg image.

3. **Chaos Encryption**: Choose between AES encryption, Blowfish encryption to secure your steg image.

4. **Chaos Decryption**: Decrypt the encrypted steg image using the corresponding decryption algorithm to retrieve the steg image.

5. **Reveal Network**: A CNN-based network that extracts the secret image from the steg image by decoding the hidden information.

6. **ESRGAN**: Our Enhanced Super Resolution Generative Adversarial Network (ESRGAN) model enhances the quality and resolution of the extracted secret image.

## One-command setup

Python 3.9–3.10 recommended. This creates `.venv`, installs deps, and launches the GUI.

```bash
# From the InvisiCipher/ folder
python bootstrap.py
```

## Using the app

In the GUI:
- Hide: Image Hide → select cover and secret → Hide → Download
- Reveal: Image Reveal → select steg → Reveal → Download
- Encrypt/Decrypt: Encryption/Decryption → select algorithm (AES/Blowfish) → enter key → Encrypt/Decrypt
- Super-resolution: Super Resolution → choose LR image → UP-SCALE → Download

CLI alternative: `python app/main_CLI_v1.py`

## Welcome screen

<p align="center">
  <img src="app/ui/assets/readme_assets/main_window.png" alt="Welcome" width="1000">
</p>

## Image hide

<p align="center">
  <img src="app/ui/assets/readme_assets/hide.png" alt="Image hide" width="1000">
</p>

## Image reveal

<p align="center">
  <img src="app/ui/assets/readme_assets/reveal.png" alt="Image reveal" width="1000">
</p>

## Super resolution

<p align="center">
  <img src="app/ui/assets/readme_assets/superres.png" alt="Super resolution" width="1000">
</p>

## Notes

- Text-to-image generation has been removed to keep the project lightweight and dependency-stable.
- ESRGAN/Stego models are included; ensure your system has enough RAM/VRAM or it will fall back to CPU.

## Troubleshooting

If you encounter TensorFlow compatibility issues (like `TypeError: unhashable type: 'list'`), run:

```bash
python fix_tensorflow.py
```

This script will:
- Check Python version compatibility (3.7-3.10 recommended)
- Uninstall conflicting TensorFlow versions
- Install TensorFlow 2.10.0 (stable version)
- Provide manual troubleshooting steps if needed

**Common issues:**
- **Python version**: Use Python 3.7-3.10 for best TensorFlow compatibility
- **Virtual environment**: Always use a fresh virtual environment
- **GPU issues**: The app will automatically fall back to CPU if GPU is unavailable

## Publish to your GitHub

Reinitialize and push to your own repo (replace `<your-username>` and `<your-repo>`):

```powershell
cd InvisiCipher
if (Test-Path .git) { Remove-Item -Recurse -Force .git }
git init
git add .
git commit -m "Clean structure: removed image generation, portable paths, bootstrap launcher"
git branch -M main
git remote add origin https://github.com/<your-username>/<your-repo>.git
git push -u origin main
```

## Contributing

We welcome contributions from the open source community. If you find any issues or have suggestions for improvements, please feel free to open an issue or submit a pull request.

## Acknowledgements

We would like to acknowledge the following resources and libraries used in this project:

- <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/2/2d/Tensorflow_logo.svg/1915px-Tensorflow_logo.svg.png" alt="TensorFlow" width="26" align="center"> TensorFlow: [↗️](https://www.tensorflow.org/)
- <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/1/10/PyTorch_logo_icon.svg/1200px-PyTorch_logo_icon.svg.png"
 alt="PyTorch" width="25" align="center"> PyTorch: [↗️](https://pytorch.org/)
- <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e6/Python_and_Qt.svg/800px-Python_and_Qt.svg.png"
 alt="PyQt" width="25" align="center"> PyQt: [↗️](https://www.qt.io/qt-for-python)

## Contact

For any questions or inquiries, please contact us at [asirwadsali@gmail.com](mailto:asirwadsali@gmail.com).
