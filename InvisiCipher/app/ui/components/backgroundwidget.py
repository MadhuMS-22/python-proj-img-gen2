from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QPainter, QPaintEvent, QColor
from PyQt5.QtWidgets import QWidget


class BackgroundWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.background_image = None

    def set_background_image(self, image_path):
        self.background_image = QPixmap(image_path)
        self.update()

    def paintEvent(self, event: QPaintEvent):
        painter = QPainter(self)
        if self.background_image:
            # Cover mode scaling to fill vertically, keep aspect; center crop
            widget_w, widget_h = self.width(), self.height()
            img_w, img_h = self.background_image.width(), self.background_image.height()
            if widget_w == 0 or widget_h == 0 or img_w == 0 or img_h == 0:
                return
            scale = max(widget_w / img_w, widget_h / img_h)
            scaled_w = int(img_w * scale)
            scaled_h = int(img_h * scale)
            pixmap = self.background_image.scaled(scaled_w, scaled_h, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            x_offset = (scaled_w - widget_w) // 2
            y_offset = (scaled_h - widget_h) // 2
            painter.drawPixmap(-x_offset, -y_offset, pixmap)
            # Draw semi-transparent overlay for legibility
            painter.fillRect(self.rect(), QColor(0, 0, 0, 140))
