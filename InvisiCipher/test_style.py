#!/usr/bin/env python3
import os
import sys
from PyQt5.QtCore import QFile, QTextStream
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget

# Get the base directory for assets
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) + "/app/ui"

class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Style Test")
        self.setGeometry(100, 100, 400, 300)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create layout
        layout = QVBoxLayout(central_widget)
        
        # Create test button
        test_button = QPushButton("Test Button")
        layout.addWidget(test_button)
        
        # Load stylesheet
        self.load_stylesheet()
    
    def load_stylesheet(self):
        stylesheet_path = os.path.join(BASE_DIR, "styles/style.qss")
        print(f"Loading stylesheet from: {stylesheet_path}")
        print(f"File exists: {os.path.exists(stylesheet_path)}")
        
        stylesheet = QFile(stylesheet_path)
        if stylesheet.open(QFile.ReadOnly | QFile.Text):
            stream = QTextStream(stylesheet)
            style_content = stream.readAll()
            print(f"Stylesheet content length: {len(style_content)}")
            self.setStyleSheet(style_content)
        else:
            print("Failed to open stylesheet file")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TestWindow()
    window.show()
    sys.exit(app.exec_())

