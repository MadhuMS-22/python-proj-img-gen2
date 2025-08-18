import os
import os
import sys

import cv2
import shutil
import numpy as np
import torch
from PyQt5.QtCore import QFile, QTextStream
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap, QFont, QPainter, QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, \
    QMessageBox, QFileDialog, QDialog, QRadioButton, QButtonGroup, QLineEdit, QScrollArea, QSizePolicy


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app.models.DEEP_STEGO.hide_image import hide_image
from app.models.DEEP_STEGO.reveal_image import reveal_image
from app.models.ESRGAN import RRDBNet_arch as arch
from app.models.encryption import aes, blowfish
from app.ui.components.backgroundwidget import BackgroundWidget
from app.ui.components.customtextbox import CustomTextBox

# Get the base directory for assets
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Project root (InvisiCipher/) two levels up from ui/
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, "..", ".."))

class MainAppWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # vars
        self.last_download_path = None
        self.main_content = None
        self.blowfish_radio_dec = None
        self.aes_radio_dec = None
        self.key_text_box_of_dec = None
        self.enc_filepath = None
        self.dec_display_label = None
        self.download_dec_button = None
        self.dec_img_text_label = None
        self.enc_img_text_label = None
        self.key_text_box = None
        self.blowfish_radio = None
        self.aes_radio = None
        self.image_tobe_enc_filepath = None
        self.download_enc_button = None
        self.enc_display_label = None
        self.container_image_filepath = None
        self.secret_out_display_label = None
        self.container_display_label = None
        self.download_revealed_secret_image_button = None
        self.download_steg_button = None
        self.secret_image_filepath = None
        self.cover_image_filepath = None
        self.steg_display_label = None
        self.secret_display_label = None
        self.cover_display_label = None
        self.low_res_image_text_label = None
        self.image_label = None
        self.low_res_image_filepath = None
        self.download_HR_button = None

        # Set window properties
        self.setWindowTitle("ImageSteganography")
        self.setGeometry(200, 200, 1400, 800)
        self.setWindowIcon(QIcon(os.path.join(PROJECT_ROOT, "logo.png")))
        self.setStyleSheet("background-color: #2b2b2b;")
        # self.setWindowFlags(Qt.FramelessWindowHint)

        # Set up the main window layout
        main_layout = QHBoxLayout()

        # Create the side navigation bar
        side_navigation = BackgroundWidget()
        # Set sidebar background image from project root (vertical menu background)
        menubg_path = os.path.join(PROJECT_ROOT, "menubg.jpg")
        if os.path.exists(menubg_path):
            side_navigation.set_background_image(menubg_path)
        side_navigation.setObjectName("side_navigation")
        side_navigation.setFixedWidth(200)
        side_layout = QVBoxLayout()

        # label for logo
        logo_label = QLabel()
        logo_pixmap = QPixmap(os.path.join(PROJECT_ROOT, "logo.png")).scaled(50, 50, Qt.KeepAspectRatio)
        logo_label.setPixmap(logo_pixmap)
        logo_label.setAlignment(Qt.AlignCenter)

        # label for app name (avoid overflow in narrow sidebar)
        name_label = QLabel()
        name_label.setText("ImageSteganography")
        name_label.setWordWrap(True)
        name_label.setStyleSheet("color: #ffffff; font-size: 14px; font-weight: 800;")
        name_label.setAlignment(Qt.AlignCenter)

        # Create buttons for each option
        encryption_button = QPushButton("Encryption")
        decryption_button = QPushButton("Decryption")
        image_hiding_button = QPushButton("Image Hide")
        image_reveal_button = QPushButton("Image Reveal")
        super_resolution_button = QPushButton("Super Resolution")

        # Connect button signals to their corresponding slots
        encryption_button.clicked.connect(self.show_encryption_page)
        decryption_button.clicked.connect(self.show_decryption_page)
        image_hiding_button.clicked.connect(self.show_image_hiding_page)
        image_reveal_button.clicked.connect(self.show_reveal_page)
        super_resolution_button.clicked.connect(self.show_super_resolution_page)

        # Add buttons to the side navigation layout
        side_layout.addWidget(logo_label)
        side_layout.addWidget(name_label)
        side_layout.addSpacing(8)
        side_layout.addWidget(image_hiding_button)
        side_layout.addWidget(encryption_button)
        side_layout.addWidget(decryption_button)
        side_layout.addWidget(image_reveal_button)
        side_layout.addWidget(super_resolution_button)
        # Auth buttons below navigation
        login_button = QPushButton("Log in")
        signup_button = QPushButton("Sign up")
        login_button.clicked.connect(self.show_login_dialog)
        signup_button.clicked.connect(self.show_signup_dialog)
        side_layout.addWidget(login_button)
        side_layout.addWidget(signup_button)

        # Add a logout button
        logout_button = QPushButton("Exit")
        logout_button.setObjectName("logout_button")
        logout_button.clicked.connect(self.logout)
        side_layout.addStretch()
        side_layout.addWidget(logout_button)

        # Set the layout for the side navigation widget
        side_navigation.setLayout(side_layout)

        # Create the main content area
        self.main_content = BackgroundWidget()
        self.main_content.setObjectName("main_content")
        # Set background image from project root bg.jpg
        bg_path = os.path.join(PROJECT_ROOT, "bg.jpg")
        if os.path.exists(bg_path):
            self.main_content.set_background_image(bg_path)
        self.main_layout = QVBoxLayout()
        self.main_content.setLayout(self.main_layout)

        # Add the side navigation and main content to the main window layout (scrollable)
        main_layout.addWidget(side_navigation)
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QScrollArea.NoFrame)
        scroll_area.setWidget(self.main_content)
        main_layout.addWidget(scroll_area)

        # Set the main window layout
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Populate home page content
        self.show_home_page()

    def show_encryption_page(self):
        # ensure bg applied
        bg_path = os.path.join(PROJECT_ROOT, "bg.jpg")
        if os.path.exists(bg_path):
            self.main_content.set_background_image(bg_path)
        self.image_tobe_enc_filepath = None
        self.key_text_box = None
        self.enc_img_text_label = None
        # Clear the main window layout
        self.clear_main_layout()

        # Add content to the super resolution page
        title_label = QLabel("<H2>Image Encryption</H2>")
        title_label.setStyleSheet("font-size: 24px; color: #ffffff;")
        title_label.setAlignment(Qt.AlignTop)
        self.main_layout.addWidget(title_label)

        # label layout
        label_layout = QHBoxLayout()

        method_text_label = QLabel("Select encryption method:")
        method_text_label.setAlignment(Qt.AlignVCenter)
        method_text_label.setStyleSheet("font-size: 16px; color: #c6c6c6; margin-bottom: 10px; font-weight: bold;")
        label_layout.addWidget(method_text_label)

        self.enc_img_text_label = QLabel("Select Image to be Encrypted:")
        self.enc_img_text_label.setAlignment(Qt.AlignCenter)
        self.enc_img_text_label.setStyleSheet("font-size: 16px; color: #c6c6c6; margin-bottom: 10px; font-weight: bold;")
        label_layout.addWidget(self.enc_img_text_label)

        label_layout_widget = QWidget()
        label_layout_widget.setLayout(label_layout)
        self.main_layout.addWidget(label_layout_widget)

        # Image  display layout
        image_display_layout = QHBoxLayout()

        radio_layout = QVBoxLayout()
        radio_layout.setAlignment(Qt.AlignLeft)
        self.aes_radio = QRadioButton("AES Encryption")
        self.aes_radio.setToolTip("Widely adopted symmetric-key block cipher with strong security and flexibility")

        self.blowfish_radio = QRadioButton("Blowfish Encryption")
        self.blowfish_radio.setToolTip("Fast, efficient symmetric-key block cipher with versatile key lengths")

        self.encryption_group = QButtonGroup(self)
        self.encryption_group.addButton(self.aes_radio)
        self.encryption_group.addButton(self.blowfish_radio)
        radio_layout.addWidget(self.blowfish_radio)
        radio_layout.addWidget(self.aes_radio)

        key_text_label = QLabel("<br><br><br>Enter the secret key")
        key_text_label.setStyleSheet("font-size: 18px; color: #ffffff; font-weight: bold;")
        radio_layout.addWidget(key_text_label)

        self.key_text_box = CustomTextBox()
        self.key_text_box.setFixedWidth(300)
        radio_layout.addWidget(self.key_text_box)

        radio_layout_widget = QWidget()
        radio_layout_widget.setLayout(radio_layout)
        image_display_layout.addWidget(radio_layout_widget)

        self.enc_display_label = QLabel()
        self.set_label_placeholder(self.enc_display_label, 256, 256, "Select the image")
        image_display_layout.addWidget(self.enc_display_label)

        image_display_layout_widget = QWidget()
        image_display_layout_widget.setLayout(image_display_layout)
        self.main_layout.addWidget(image_display_layout_widget)

        # button layout
        button_layout = QHBoxLayout()
        clear_button = QPushButton("Clear")
        clear_button.clicked.connect(lambda: self.show_encryption_page())
        button_layout.addWidget(clear_button)

        browse_enc_button = QPushButton("Browse image")
        browse_enc_button.clicked.connect(lambda: self.select_enc_image(self.enc_display_label))
        button_layout.addWidget(browse_enc_button)

        encrypt_button = QPushButton("Encrypt")
        encrypt_button.clicked.connect(lambda: self.perform_encryption(self.image_tobe_enc_filepath))
        button_layout.addWidget(encrypt_button)

        self.download_enc_button = QPushButton("Download🔽")
        self.download_enc_button.setEnabled(False)
        self.download_enc_button.clicked.connect(lambda: self.download_image())
        button_layout.addWidget(self.download_enc_button)

        button_layout_widget = QWidget()
        button_layout_widget.setLayout(button_layout)
        self.main_layout.addWidget(button_layout_widget)

    def show_decryption_page(self):
        bg_path = os.path.join(PROJECT_ROOT, "bg.jpg")
        if os.path.exists(bg_path):
            self.main_content.set_background_image(bg_path)
        self.key_text_box_of_dec = None
        # Clear the main window layout
        self.clear_main_layout()

        # Add content to the super resolution page
        title_label = QLabel("<H2>Image Decryption</H2>")
        title_label.setStyleSheet("font-size: 24px; color: #ffffff;")
        title_label.setAlignment(Qt.AlignTop)
        self.main_layout.addWidget(title_label)

        # label layout
        label_layout = QHBoxLayout()

        method_text_label = QLabel("Select Decryption method:")
        method_text_label.setAlignment(Qt.AlignVCenter)
        method_text_label.setStyleSheet("font-size: 16px; color: #c6c6c6; margin-bottom: 10px; font-weight: bold;")
        label_layout.addWidget(method_text_label)

        self.dec_img_text_label = QLabel("Select the file to be decrypted:")
        self.dec_img_text_label.setAlignment(Qt.AlignCenter)
        self.dec_img_text_label.setStyleSheet("font-size: 16px; color: #c6c6c6; margin-bottom: 10px; font-weight: bold;")
        label_layout.addWidget(self.dec_img_text_label)

        label_layout_widget = QWidget()
        label_layout_widget.setLayout(label_layout)
        self.main_layout.addWidget(label_layout_widget)

        # Image  display layout
        image_display_layout = QHBoxLayout()

        radio_layout = QVBoxLayout()
        radio_layout.setAlignment(Qt.AlignLeft)
        self.aes_radio_dec = QRadioButton("AES Decryption")
        self.aes_radio_dec.setToolTip("Widely adopted symmetric-key block cipher with strong security and flexibility")

        self.blowfish_radio_dec = QRadioButton("Blowfish Decryption")
        self.blowfish_radio_dec.setToolTip("Fast, efficient symmetric-key block cipher with versatile key lengths")

        self.decryption_group = QButtonGroup(self)
        self.decryption_group.addButton(self.aes_radio_dec)
        self.decryption_group.addButton(self.blowfish_radio_dec)
        radio_layout.addWidget(self.blowfish_radio_dec)
        radio_layout.addWidget(self.aes_radio_dec)

        key_text_label = QLabel("<br><br><br>Enter the secret key")
        key_text_label.setStyleSheet("font-size: 18px; color: #ffffff; font-weight: bold;")
        radio_layout.addWidget(key_text_label)

        self.key_text_box_of_dec = CustomTextBox()
        self.key_text_box_of_dec.setFixedWidth(300)
        radio_layout.addWidget(self.key_text_box_of_dec)

        radio_layout_widget = QWidget()
        radio_layout_widget.setLayout(radio_layout)
        image_display_layout.addWidget(radio_layout_widget)

        self.dec_display_label = QLabel()
        self.dec_display_label.setAlignment(Qt.AlignLeft)
        self.set_label_placeholder(self.dec_display_label, 256, 256, "Select the image")
        image_display_layout.addWidget(self.dec_display_label)

        image_display_layout_widget = QWidget()
        image_display_layout_widget.setLayout(image_display_layout)
        self.main_layout.addWidget(image_display_layout_widget)

        # button layout
        button_layout = QHBoxLayout()
        clear_button = QPushButton("Clear")
        clear_button.clicked.connect(lambda: self.show_decryption_page())
        button_layout.addWidget(clear_button)

        browse_enc_button = QPushButton("Browse encrypted file")
        browse_enc_button.clicked.connect(lambda: self.select_dec_image(self.dec_display_label))
        button_layout.addWidget(browse_enc_button)

        decrypt_button = QPushButton("Decrypt")
        decrypt_button.clicked.connect(lambda: self.perform_decryption(self.enc_filepath))
        button_layout.addWidget(decrypt_button)

        self.download_dec_button = QPushButton("Download🔽")
        self.download_dec_button.setEnabled(False)
        self.download_dec_button.clicked.connect(lambda: self.download_image())
        button_layout.addWidget(self.download_dec_button)

        button_layout_widget = QWidget()
        button_layout_widget.setLayout(button_layout)
        self.main_layout.addWidget(button_layout_widget)

    def show_image_hiding_page(self):
        bg_path = os.path.join(PROJECT_ROOT, "bg.jpg")
        if os.path.exists(bg_path):
            self.main_content.set_background_image(bg_path)
        self.secret_image_filepath = None
        self.cover_image_filepath = None
        # Clear the main window layout
        self.clear_main_layout()

        # Add content to the super resolution page
        title_label = QLabel("<H2>STEGO CNN : Steganography Hide</H2>")
        title_label.setStyleSheet("font-size: 24px; color: #ffffff;")
        title_label.setAlignment(Qt.AlignTop)
        self.main_layout.addWidget(title_label)

        # STEGO CNN model path label
        model_path_label = QLabel("<h5>Model Path: InvisiCipher/app/models/DEEP_STEGO/models/hide.h5</h5>")
        model_path_label.setStyleSheet("font-size: 16px; color: #c6c6c6;")
        model_path_label.setAlignment(Qt.AlignTop)
        self.main_layout.addWidget(model_path_label)

        # GPU Info
        gpu_info_label = QLabel("<b><ul><li>Device info will appear if available</li></ul></b>")
        gpu_info_label.setStyleSheet("font-size: 13px; color: #fae69e;")
        gpu_info_label.setAlignment(Qt.AlignTop)
        self.main_layout.addWidget(gpu_info_label)

        # label layout
        label_layout = QHBoxLayout()
        cover_text_label = QLabel("Select cover image:")
        cover_text_label.setAlignment(Qt.AlignCenter)
        cover_text_label.setStyleSheet("font-size: 16px; color: #c6c6c6; margin-bottom: 10px; font-weight: bold;")
        label_layout.addWidget(cover_text_label)

        secret_text_label = QLabel("Select secret image:")
        secret_text_label.setAlignment(Qt.AlignCenter)
        secret_text_label.setStyleSheet("font-size: 16px; color: #c6c6c6; margin-bottom: 10px; font-weight: bold;")
        label_layout.addWidget(secret_text_label)

        steg_text_label = QLabel("Generated steg image:")
        steg_text_label.setAlignment(Qt.AlignCenter)
        steg_text_label.setStyleSheet("font-size: 16px; color: #00ff00; margin-bottom: 10px; font-weight: bold;")
        label_layout.addWidget(steg_text_label)
        # keep a reference for status updates after hide
        self.steg_text_label = steg_text_label

        label_layout_widget = QWidget()
        label_layout_widget.setLayout(label_layout)
        self.main_layout.addWidget(label_layout_widget)

        # Image  display layout
        image_display_layout = QHBoxLayout()
        self.cover_display_label = QLabel()
        self.cover_display_label.setAlignment(Qt.AlignCenter)
        self.set_label_placeholder(self.cover_display_label, 256, 256, "Select the image")
        image_display_layout.addWidget(self.cover_display_label)

        self.secret_display_label = QLabel()
        self.secret_display_label.setAlignment(Qt.AlignCenter)
        self.set_label_placeholder(self.secret_display_label, 256, 256, "Select the image")
        image_display_layout.addWidget(self.secret_display_label)

        self.steg_display_label = QLabel()
        self.steg_display_label.setAlignment(Qt.AlignCenter)
        self.set_label_placeholder(self.steg_display_label, 256, 256, "Select the image")
        image_display_layout.addWidget(self.steg_display_label)

        image_display_layout_widget = QWidget()
        image_display_layout_widget.setLayout(image_display_layout)
        self.main_layout.addWidget(image_display_layout_widget)

        # button layout
        button_layout = QHBoxLayout()
        clear_button = QPushButton("Clear")
        clear_button.clicked.connect(lambda: self.show_image_hiding_page())
        button_layout.addWidget(clear_button)

        browse_cover_button = QPushButton("Browse cover image")
        browse_cover_button.clicked.connect(lambda: self.select_cover_image(self.cover_display_label))
        button_layout.addWidget(browse_cover_button)

        browse_secret_button = QPushButton("Browse secret image")
        browse_secret_button.clicked.connect(lambda: self.select_secret_image(self.secret_display_label))
        button_layout.addWidget(browse_secret_button)

        hide_button = QPushButton("Hide")
        hide_button.clicked.connect(lambda: self.perform_hide(self.cover_image_filepath, self.secret_image_filepath))
        button_layout.addWidget(hide_button)

        self.download_steg_button = QPushButton("Download steg image🔽")
        self.download_steg_button.setEnabled(False)
        self.download_steg_button.clicked.connect(lambda: self.download_image())
        button_layout.addWidget(self.download_steg_button)

        button_layout_widget = QWidget()
        button_layout_widget.setLayout(button_layout)
        self.main_layout.addWidget(button_layout_widget)

    def show_reveal_page(self):
        bg_path = os.path.join(PROJECT_ROOT, "bg.jpg")
        if os.path.exists(bg_path):
            self.main_content.set_background_image(bg_path)
        self.clear_main_layout()

        # Add content to the super resolution page
        title_label = QLabel("<H2>STEGO CNN : Steganography Reveal</H2>")
        title_label.setStyleSheet("font-size: 24px; color: #ffffff;")
        title_label.setAlignment(Qt.AlignTop)
        self.main_layout.addWidget(title_label)

        # STEGO CNN model path label
        model_path_label = QLabel("<h5>Model Path: InvisiCipher/app/models/DEEP_STEGO/models/reveal.h5</h5>")
        model_path_label.setStyleSheet("font-size: 16px; color: #c6c6c6;")
        model_path_label.setAlignment(Qt.AlignTop)
        self.main_layout.addWidget(model_path_label)

        # GPU Info
        gpu_info_label = QLabel("<b><ul><li>Device info will appear if available</li></ul></b>")
        gpu_info_label.setStyleSheet("font-size: 13px; color: #fae69e;")
        gpu_info_label.setAlignment(Qt.AlignTop)
        self.main_layout.addWidget(gpu_info_label)

        # image text layout
        image_text_layout = QHBoxLayout()
        container_text_label = QLabel("Select steg image:")
        container_text_label.setAlignment(Qt.AlignCenter)
        container_text_label.setStyleSheet("font-size: 16px; color: #c6c6c6; margin-bottom: 10px; font-weight: bold;")
        image_text_layout.addWidget(container_text_label)

        secret_out_text_label = QLabel("Revealed secret image:")
        secret_out_text_label.setAlignment(Qt.AlignCenter)
        secret_out_text_label.setStyleSheet("font-size: 16px; color: #00ff00; margin-bottom: 10px; font-weight: bold;")
        image_text_layout.addWidget(secret_out_text_label)
        # keep a reference for status updates after reveal
        self.secret_out_text_label = secret_out_text_label

        image_text_layout_widget = QWidget()
        image_text_layout_widget.setLayout(image_text_layout)
        self.main_layout.addWidget(image_text_layout_widget)
        
        # Image display layout
        image_layout = QHBoxLayout()
        self.container_display_label = QLabel()
        self.container_display_label.setAlignment(Qt.AlignCenter)
        self.set_label_placeholder(self.container_display_label, 256, 256, "Select the image")
        image_layout.addWidget(self.container_display_label)
        
        self.secret_out_display_label = QLabel()
        self.secret_out_display_label.setAlignment(Qt.AlignCenter)
        self.set_label_placeholder(self.secret_out_display_label, 256, 256, "Select the image")
        image_layout.addWidget(self.secret_out_display_label)

        image_layout_widget = QWidget()
        image_layout_widget.setLayout(image_layout)
        self.main_layout.addWidget(image_layout_widget)

        # button layout
        button_layout = QHBoxLayout()
        clear_button = QPushButton("Clear")
        clear_button.clicked.connect(lambda: self.show_reveal_page())
        button_layout.addWidget(clear_button)

        browse_cover_button = QPushButton("Browse steg image")
        browse_cover_button.clicked.connect(lambda: self.select_container_image(self.container_display_label))
        button_layout.addWidget(browse_cover_button)

        reveal_button = QPushButton("Reveal")
        reveal_button.clicked.connect(lambda: self.perform_reveal(self.container_image_filepath))
        button_layout.addWidget(reveal_button)

        self.download_revealed_secret_image_button = QPushButton("Download🔽")
        self.download_revealed_secret_image_button.setEnabled(False)
        self.download_revealed_secret_image_button.clicked.connect(lambda: self.download_image())
        button_layout.addWidget(self.download_revealed_secret_image_button)

        button_layout_widget = QWidget()
        button_layout_widget.setLayout(button_layout)
        self.main_layout.addWidget(button_layout_widget)

    def show_super_resolution_page(self):
        bg_path = os.path.join(PROJECT_ROOT, "bg.jpg")
        if os.path.exists(bg_path):
            self.main_content.set_background_image(bg_path)
        self.low_res_image_filepath = None
        # Clear the main window layout
        self.clear_main_layout()

        # Add content to the super resolution page
        title_label = QLabel("<H2>Enhanced Super Resolution using ESRGAN</H2>")
        title_label.setAlignment(Qt.AlignTop)
        title_label.setStyleSheet("font-size: 24px; color: #ffffff; margin-bottom: 20px;")
        self.main_layout.addWidget(title_label)

        # ESRGAN model path label
        model_path_label = QLabel("<h5>Model Path: InvisiCipher/app/models/ESRGAN/models/RRDB_ESRGAN_x4.pth</h5>")
        model_path_label.setStyleSheet("font-size: 16px; color: #c6c6c6; margin-bottom: 20px;")
        model_path_label.setAlignment(Qt.AlignTop)
        self.main_layout.addWidget(model_path_label)

        # GPU Info
        gpu_info_label = QLabel(
            "<b><ul><li>Device info will appear if available</li></ul></b>")
        gpu_info_label.setStyleSheet("font-size: 13px; color: #fae69e;")
        gpu_info_label.setAlignment(Qt.AlignTop)
        self.main_layout.addWidget(gpu_info_label)

        # Low resolution image selection
        low_res_label = QLabel("Select Low Resolution Image:")
        low_res_label.setAlignment(Qt.AlignCenter)
        low_res_label.setStyleSheet("font-size: 16px; color: #c6c6c6; margin-bottom: 10px; font-weight: bold;")
        self.main_layout.addWidget(low_res_label)

        # image display
        image_label = QLabel()
        image_label.setAlignment(Qt.AlignCenter)
        self.set_label_placeholder(image_label, 384, 384, "Select the image")
        self.main_layout.addWidget(image_label)

        # defining button layout
        button_layout = QHBoxLayout()

        # Browse button
        clear_button = QPushButton("Clear")
        clear_button.clicked.connect(lambda: self.show_super_resolution_page())
        button_layout.addWidget(clear_button)

        browse_button = QPushButton("Browse")
        browse_button.clicked.connect(lambda: self.select_low_resolution_image(image_label))
        button_layout.addWidget(browse_button)

        # Up-scale button
        upscale_button = QPushButton("UP-SCALE")
        upscale_button.clicked.connect(lambda: self.upscaleImage(image_label))
        button_layout.addWidget(upscale_button)

        # Download button
        download_button = QPushButton("Download🔽")
        download_button.setObjectName("download_button")
        download_button.setEnabled(False)
        download_button.clicked.connect(self.download_image)
        button_layout.addWidget(download_button)

        # add the button layout to the main layout
        button_widget = QWidget()
        button_widget.setLayout(button_layout)
        self.main_layout.addWidget(button_widget)

        # Set the image labels as attributes
        self.low_res_image_text_label = low_res_label
        self.image_label = image_label
        self.download_HR_button = download_button

    def select_low_resolution_image(self, label):
        file_dialog = QFileDialog()
        low_res_image_filepath, _ = file_dialog.getOpenFileName(self, "Select Low Resolution Image")
        if low_res_image_filepath:
            self.low_res_image_filepath = low_res_image_filepath
            self.set_label_image_box(label, low_res_image_filepath, 384, 384)
            self.style_image_box(label)

    def upscaleImage(self, label):
        if self.low_res_image_filepath is None:
            QMessageBox.information(self, "Upscaling Error", "Please select the low-resolution image first.")
            return
        os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "max_split_size_mb:400"
        model_path = os.path.join(os.path.dirname(BASE_DIR), "models/ESRGAN/models/RRDB_ESRGAN_x4.pth")
        if not os.path.exists(model_path):
            QMessageBox.critical(self, "Upscaling Error", f"ESRGAN model not found at:\n{model_path}")
            return
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        model = arch.RRDBNet(3, 3, 64, 23, gc=32)
        state_dict = torch.load(model_path, map_location=device)
        model.load_state_dict(state_dict, strict=True)
        model.eval()
        model = model.to(device)

        print('Model path {:s}. \nUp-scaling...'.format(model_path))

        image = cv2.imread(self.low_res_image_filepath, cv2.IMREAD_COLOR)
        image = image * 1.0 / 255
        image = torch.from_numpy(np.transpose(image[:, :, [2, 1, 0]], (2, 0, 1))).float()
        image_low_res = image.unsqueeze(0)
        image_low_res = image_low_res.to(device)

        with torch.no_grad():
            image_high_res = model(image_low_res).data.squeeze().float().cpu().clamp_(0, 1).numpy()
        image_high_res = np.transpose(image_high_res[[2, 1, 0], :, :], (1, 2, 0))
        image_high_res = (image_high_res * 255.0).round().astype(np.uint8)

        high_res_image_path = os.path.abspath(os.path.join(os.path.dirname(BASE_DIR), "upscaled.png"))
        cv2.imwrite(high_res_image_path, image_high_res)

        # Display the high resolution image
        if os.path.exists(high_res_image_path):
            print("image saved as: ", high_res_image_path)
            self.set_label_image_box(label, high_res_image_path, 384, 384)
            self.low_res_image_text_label.setText("High Res Image:")
            self.low_res_image_text_label.setStyleSheet(
                "font-size: 16px; color: #00ff00; margin-bottom: 10px; font-weight: bold;")
            self.download_HR_button.setEnabled(True)
            self.last_download_path = high_res_image_path
        else:
            QMessageBox.critical(self, "Upscaling Error", "Failed to upscale the image.")

    def download_image(self):
        if not self.last_download_path or not os.path.exists(self.last_download_path):
            QMessageBox.information(self, "Download", "Nothing to download yet.")
            return
        target, _ = QFileDialog.getSaveFileName(self, "Save File As", os.path.basename(self.last_download_path))
        if not target:
            return
        try:
            shutil.copyfile(self.last_download_path, target)
            QMessageBox.information(self, "Download", f"Saved to {target}")
        except Exception as e:
            QMessageBox.critical(self, "Download Error", f"Failed to save: {e}")

    def clear_main_layout(self):
        # Remove all widgets from the main layout
        while self.main_layout.count():
            child = self.main_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def select_cover_image(self, label):
        file_dialog = QFileDialog()
        filepath, _ = file_dialog.getOpenFileName(self, "Select cover Image")
        if filepath:
            self.cover_image_filepath = filepath
            self.set_label_image_box(label, filepath, 256, 256)
            self.style_image_box(label)

    def select_secret_image(self, label):
        file_dialog = QFileDialog()
        filepath, _ = file_dialog.getOpenFileName(self, "Select secret Image")
        if filepath:
            self.secret_image_filepath = filepath
            self.set_label_image_box(label, filepath, 256, 256)
            self.style_image_box(label)

    def select_container_image(self, label):
        file_dialog = QFileDialog()
        filepath, _ = file_dialog.getOpenFileName(self, "Select secret Image")
        if filepath:
            self.container_image_filepath = filepath
            self.set_label_image_box(label, filepath, 256, 256)
            self.style_image_box(label)

    def select_enc_image(self, label):
        file_dialog = QFileDialog()
        filepath, _ = file_dialog.getOpenFileName(self, "Select Image")
        if filepath:
            self.image_tobe_enc_filepath = filepath
            self.set_label_image_box(label, filepath, 256, 256)
            self.style_image_box(label)

    def select_dec_image(self, label):
        file_dialog = QFileDialog()
        filepath, _ = file_dialog.getOpenFileName(self, "Select enc file")
        if filepath:
            self.enc_filepath = filepath
            self.set_label_placeholder(label, 256, 256, "Select the image")

    def _placeholder_pixmap(self, width, height, text="Select the image"):
        bg_path = os.path.join(PROJECT_ROOT, "imgbg.jpg")
        if os.path.exists(bg_path):
            bg = QPixmap(bg_path)
            scaled = bg.scaled(width, height, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
            x = (scaled.width() - width) // 2
            y = (scaled.height() - height) // 2
            canvas = scaled.copy(x, y, width, height)
        else:
            canvas = QPixmap(width, height)
            canvas.fill(QColor(50, 50, 50))
        painter = QPainter(canvas)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QColor(255, 255, 255))
        f = QFont()
        f.setPointSize(12)
        f.setBold(True)
        painter.setFont(f)
        painter.drawText(canvas.rect(), Qt.AlignCenter, text)
        painter.end()
        return canvas

    def set_label_placeholder(self, label: QLabel, width: int, height: int, text: str):
        label.setAlignment(Qt.AlignCenter)
        label.setPixmap(self._placeholder_pixmap(width, height, text))
        self.style_image_box(label)

    def style_image_box(self, label: QLabel):
        label.setStyleSheet(
            "border: 2px solid #d62828; border-radius: 8px; background-color: rgba(0,0,0,80);"
        )
        pm = label.pixmap()
        if pm is not None:
            label.setFixedSize(pm.width(), pm.height())

    def set_label_image_box(self, label: QLabel, image_path: str, box_width: int, box_height: int):
        try:
            src = QPixmap(image_path)
            if src.isNull():
                self.set_label_placeholder(label, box_width, box_height, "Select the image")
                return
            scaled = src.scaled(box_width, box_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            canvas = QPixmap(box_width, box_height)
            canvas.fill(QColor(0, 0, 0, 0))
            painter = QPainter(canvas)
            x = (box_width - scaled.width()) // 2
            y = (box_height - scaled.height()) // 2
            painter.drawPixmap(x, y, scaled)
            painter.end()
            label.setPixmap(canvas)
            label.setFixedSize(box_width, box_height)
        except Exception:
            self.set_label_placeholder(label, box_width, box_height, "Select the image")

    def logout(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Exit")
        dialog.setMinimumSize(450, 100)

        layout = QVBoxLayout(dialog)
        msg_box = QMessageBox()
        msg_box.setText("<h3>Are you sure you want to Exit?</h3>")

        # Set custom font and size
        font = QFont("Arial", 12)  # Adjust the font and size as desired
        msg_box.setFont(font)

        button_layout = QHBoxLayout()
        layout.addWidget(msg_box)
        layout.addLayout(button_layout)

        # Remove the standard buttons
        msg_box.setStandardButtons(QMessageBox.NoButton)

        yes_button = QPushButton("Yes")
        yes_button.setStyleSheet("color: #000000;")
        yes_button.clicked.connect(lambda: QApplication.quit())

        no_button = QPushButton("No")
        no_button.setStyleSheet("color: #000000;")
        no_button.clicked.connect(dialog.reject)

        button_layout.addWidget(yes_button)
        button_layout.addWidget(no_button)

        dialog.exec_()

    def load_stylesheet(self):
        stylesheet = QFile(os.path.join(BASE_DIR, "styles/style.qss"))
        if stylesheet.open(QFile.ReadOnly | QFile.Text):
            stream = QTextStream(stylesheet)
            self.setStyleSheet(stream.readAll())

    def show_home_page(self):
        self.clear_main_layout()
        # Apply page margins for full-width blocks
        self.main_layout.setContentsMargins(16, 16, 16, 16)
        # Logo on home page
        logo_home = QLabel()
        lp = QPixmap(os.path.join(PROJECT_ROOT, "logo.png"))
        if not lp.isNull():
            logo_home.setPixmap(lp.scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        logo_home.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(logo_home)
        # Title
        title_label = QLabel("<h1>ImageSteganography</h1>")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 42px; color: #d62828; font-weight: 800; letter-spacing: 1px;")
        self.main_layout.addWidget(title_label)

        # Overview info (full paragraph)
        info = QLabel(
            "<div style='color:#f0f0f0; font-size:20px; text-align:center; line-height:1.9'>"
            "ImageSteganography is a desktop application that lets you seamlessly embed a secret image inside a cover image "
            "using a convolutional neural network. You can optionally secure files with AES or Blowfish encryption, recover the "
            "hidden content later with the paired reveal model, and improve clarity of low‑resolution images using ESRGAN super‑resolution. "
            "All workflows are available through an elegant, offline‑friendly PyQt interface."
            "</div>"
        )
        info.setAlignment(Qt.AlignCenter)
        info.setWordWrap(True)
        info.setStyleSheet(
            "background-color: transparent; padding: 16px 22px; border-radius: 10px;"
        )
        info.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        self.main_layout.addWidget(info)

        # Technologies section
        tech_header = QLabel("<h3>Technologies Used</h3>")
        tech_header.setAlignment(Qt.AlignCenter)
        tech_header.setStyleSheet("color:#ffd1d1; font-size:26px; font-weight: 800;")
        self.main_layout.addWidget(tech_header, alignment=Qt.AlignCenter)

        def make_chip(text: str) -> QWidget:
            chip = QLabel(text)
            chip.setAlignment(Qt.AlignCenter)
            chip.setStyleSheet(
                "color:#ffffff; background-color: transparent;"
                "padding: 10px 14px; border-radius: 12px; font-size: 16px; font-weight: 800;"
            )
            w = QWidget()
            l = QVBoxLayout(w)
            l.setContentsMargins(0,0,0,0)
            l.addWidget(chip)
            return w

        tech_row_container = QWidget()
        tech_row = QHBoxLayout(tech_row_container)
        tech_row.setContentsMargins(0,0,0,0)
        tech_row.setSpacing(10)
        tech_row.addWidget(make_chip("TensorFlow/Keras"))
        tech_row.addWidget(make_chip("PyTorch"))
        tech_row.addWidget(make_chip("PyQt5"))
        tech_row.addWidget(make_chip("OpenCV & NumPy"))
        tech_row.addWidget(make_chip("PyCryptodome"))

        # Put chips in a horizontal scroll to keep one row if needed
        tech_scroll = QScrollArea()
        tech_scroll.setWidgetResizable(True)
        tech_scroll.setFrameShape(QScrollArea.NoFrame)
        tech_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        tech_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # make scroll area and its viewport transparent
        tech_scroll.setStyleSheet("QScrollArea{background:transparent;} QScrollArea>Viewport{background:transparent;} QWidget{background:transparent;}")
        tech_row_container.setAttribute(Qt.WA_TranslucentBackground, True)
        tech_row_container.setAutoFillBackground(False)
        tech_scroll.setWidget(tech_row_container)
        tech_scroll.setMaximumHeight(70)
        self.main_layout.addWidget(tech_scroll)

        # Feature cards (tiny boxes) — one row with horizontal scroll if needed
        def make_card(title: str, desc: str, on_click) -> QWidget:
            card = QWidget()
            card_layout = QVBoxLayout(card)
            card_layout.setContentsMargins(12, 10, 12, 12)
            t = QLabel(title)
            t.setAlignment(Qt.AlignCenter)
            t.setStyleSheet("color:#d62828; font-size:20px; font-weight:900;")
            d = QLabel(desc)
            d.setAlignment(Qt.AlignCenter)
            d.setWordWrap(True)
            d.setStyleSheet("color:#f0f0f0; font-size:15px; font-weight:600;")
            card_layout.addWidget(t)
            card_layout.addWidget(d)
            card.setStyleSheet("background-color: transparent; border-radius: 10px;")
            card.setFixedWidth(260)
            card.setCursor(Qt.PointingHandCursor)
            # Click handler
            def _mp(_: object = None):
                try:
                    on_click()
                except Exception:
                    pass
            card.mousePressEvent = lambda e: _mp()
            return card

        features_row_container = QWidget()
        features_row_container.setAttribute(Qt.WA_TranslucentBackground, True)
        features_row_container.setAutoFillBackground(False)
        features_row = QHBoxLayout(features_row_container)
        features_row.setContentsMargins(0,0,0,0)
        features_row.setSpacing(16)
        features_row.addWidget(make_card("Hide", "Embed a secret image into a cover image using a CNN (auto‑resized to 224×224).", self.show_image_hiding_page))
        features_row.addWidget(make_card("Reveal", "Recover the hidden secret image from a stego image using the paired model.", self.show_reveal_page))
        features_row.addWidget(make_card("Encrypt", "Protect files with AES or Blowfish in CBC mode (key‑derived via SHA‑256).", self.show_encryption_page))
        features_row.addWidget(make_card("Upscale", "Enhance image quality using ESRGAN ×4 (CPU/GPU).", self.show_super_resolution_page))

        features_scroll = QScrollArea()
        features_scroll.setWidgetResizable(True)
        features_scroll.setFrameShape(QScrollArea.NoFrame)
        features_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        features_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # make features scroll area transparent
        features_scroll.setStyleSheet("QScrollArea{background:transparent;} QScrollArea>Viewport{background:transparent;} QWidget{background:transparent;}")
        features_scroll.setWidget(features_row_container)
        features_scroll.setMaximumHeight(180)
        self.main_layout.addWidget(features_scroll)

    def show_login_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Log in")
        layout = QVBoxLayout(dialog)
        layout.addWidget(QLabel("Username"))
        username = QLineEdit()
        layout.addWidget(username)
        layout.addWidget(QLabel("Password"))
        password = QLineEdit()
        password.setEchoMode(QLineEdit.Password)
        layout.addWidget(password)
        row = QHBoxLayout()
        ok = QPushButton("OK")
        cancel = QPushButton("Cancel")
        ok.clicked.connect(dialog.accept)
        cancel.clicked.connect(dialog.reject)
        row.addWidget(ok)
        row.addWidget(cancel)
        layout.addLayout(row)
        dialog.exec_()

    def show_signup_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Sign up")
        layout = QVBoxLayout(dialog)
        layout.addWidget(QLabel("Email"))
        email = QLineEdit()
        layout.addWidget(email)
        layout.addWidget(QLabel("Password"))
        password = QLineEdit()
        password.setEchoMode(QLineEdit.Password)
        layout.addWidget(password)
        layout.addWidget(QLabel("Confirm Password"))
        confirm = QLineEdit()
        confirm.setEchoMode(QLineEdit.Password)
        layout.addWidget(confirm)
        row = QHBoxLayout()
        ok = QPushButton("Create Account")
        cancel = QPushButton("Cancel")
        ok.clicked.connect(dialog.accept)
        cancel.clicked.connect(dialog.reject)
        row.addWidget(ok)
        row.addWidget(cancel)
        layout.addLayout(row)
        dialog.exec_()

    def perform_hide(self, cover_filepath: str, secret_filepath: str):
        if not cover_filepath or not secret_filepath:
            QMessageBox.information(self, "Hiding Error", "Please select the cover and secret images first.")
            return
        try:
            steg_image_path = hide_image(cover_filepath, secret_filepath)
            self.set_label_image_box(self.steg_display_label, steg_image_path, 256, 256)
            self.download_steg_button.setEnabled(True)
            self.last_download_path = steg_image_path
            if hasattr(self, 'steg_text_label') and self.steg_text_label is not None:
                self.steg_text_label.setText("Image Hidden Successfully!")
                self.steg_text_label.setStyleSheet("font-size: 16px; color: #00ff00; margin-bottom: 10px; font-weight: bold;")
        except Exception as e:
            QMessageBox.critical(self, "Hiding Error", f"Failed to hide the image.\n{e}")

    def perform_reveal(self, filepath: str):
        if not filepath:
            QMessageBox.information(self, "Revealing Error", "Please select the steg image first.")
            return
        try:
            secret_out_filepath = reveal_image(filepath)
            self.set_label_image_box(self.secret_out_display_label, secret_out_filepath, 256, 256)
            self.download_revealed_secret_image_button.setEnabled(True)
            self.last_download_path = secret_out_filepath
            if hasattr(self, 'secret_out_text_label') and self.secret_out_text_label is not None:
                self.secret_out_text_label.setText("Image Revealed Successfully!")
                self.secret_out_text_label.setStyleSheet("font-size: 16px; color: #00ff00; margin-bottom: 10px; font-weight: bold;")
        except Exception as e:
            QMessageBox.critical(self, "Revealing Error", f"Failed to reveal the image.\n{e}")

    def perform_encryption(self, filepath: str):
        if not filepath:
            QMessageBox.information(self, "Encrypting Error", "Please select the image first.")
            return
        if not (self.aes_radio.isChecked() or self.blowfish_radio.isChecked()):
            QMessageBox.information(self, "Encrypting Error", "Please select an encryption method.")
            return
        if self.key_text_box.text() == "":
            QMessageBox.information(self, "Encrypting Error", "Please enter a secret key.")
            return
        try:
            if self.aes_radio.isChecked():
                aes.encrypt(filepath, self.key_text_box.text())
            else:
                blowfish.encrypt(filepath, self.key_text_box.text())
                self.last_download_path = filepath + '.enc'
            self.download_enc_button.setEnabled(True)
            if self.enc_img_text_label is not None:
            self.enc_img_text_label.setText("Encrypted!")
                self.enc_img_text_label.setStyleSheet("font-size: 16px; color: #00ff00; margin-bottom: 10px; font-weight: bold;")
            self.key_text_box.setText("")
        except Exception as e:
            QMessageBox.critical(self, "Encrypting Error", f"Failed to encrypt the image.\n{e}")

    def perform_decryption(self, filepath: str):
        if not filepath:
            QMessageBox.information(self, "Decrypting Error", "Please select the encrypted file first.")
            return
        if not (self.aes_radio_dec.isChecked() or self.blowfish_radio_dec.isChecked()):
            QMessageBox.information(self, "Decrypting Error", "Please select a decryption method.")
            return
        if self.key_text_box_of_dec.text() == "":
            QMessageBox.information(self, "Decrypting Error", "Please enter a secret key.")
            return
        try:
            result = 0
            dec_filename = None
            if self.aes_radio_dec.isChecked():
                result, dec_filename = aes.decrypt(filepath, self.key_text_box_of_dec.text())
            else:
                result, dec_filename = blowfish.decrypt(filepath, self.key_text_box_of_dec.text())
            if result == -1 or not dec_filename:
                QMessageBox.critical(self, "Decrypting Error", "Wrong key or failed to decrypt.")
                    return
            self.download_dec_button.setEnabled(True)
            if self.dec_img_text_label is not None:
            self.dec_img_text_label.setText("Decrypted!")
                self.dec_img_text_label.setStyleSheet("font-size: 16px; color: #00ff00; margin-bottom: 10px; font-weight: bold;")
            # Show decrypted output in the box
            self.set_label_image_box(self.dec_display_label, dec_filename, 256, 256)
            self.last_download_path = dec_filename
            self.key_text_box_of_dec.setText("")
        except Exception as e:
            QMessageBox.critical(self, "Decrypting Error", f"Failed to decrypt the file.\n{e}")


# Create the application
QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
app = QApplication(sys.argv)
window = MainAppWindow()
window.load_stylesheet()
window.show()
sys.exit(app.exec_())
