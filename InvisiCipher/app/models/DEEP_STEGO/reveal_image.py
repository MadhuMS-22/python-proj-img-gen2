import os
import numpy as np
from tensorflow.keras.models import load_model
from PIL import Image
import imageio
from tkinter import filedialog
from app.models.DEEP_STEGO.Utils.preprocessing import normalize_batch, denormalize_batch


def reveal_image(stego_image_filepath):
    # Resolve paths relative to this file so cloned repos work
    current_dir = os.path.dirname(os.path.abspath(__file__))
    models_dir = os.path.join(current_dir, "models")
    app_dir = os.path.abspath(os.path.join(current_dir, "..", ".."))  # InvisiCipher/app

    model_path = os.path.join(models_dir, "reveal.h5")
    model = load_model(model_path, compile=False)

    stego_image = Image.open(stego_image_filepath).convert('RGB')

    # Resize the image to 224px*224px
    if stego_image.size != (224, 224):
        stego_image = stego_image.resize((224, 224))
        print("stego_image was resized to 224px * 224px")

    stego_image = np.array(stego_image).reshape(1, 224, 224, 3) / 255.0

    secret_image_out = model.predict([normalize_batch(stego_image)])

    secret_image_out = denormalize_batch(secret_image_out)
    secret_image_out = np.squeeze(secret_image_out) * 255.0
    secret_image_out = np.uint8(secret_image_out)

    output_path = os.path.join(app_dir, "secret_out.png")
    imageio.imsave(output_path, secret_image_out)
    print("Saved revealed image to", output_path)

    return output_path





