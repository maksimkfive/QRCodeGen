import io
import pyqrcode
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton,
                             QLabel, QLineEdit, QFileDialog, QCheckBox)
from PyQt5.QtGui import QPixmap, QPalette, QColor, QFont, QLinearGradient
from PyQt5.QtCore import Qt
from PIL import Image

STYLESHEET = """
QWidget {
    font-family: 'Segoe UI', sans-serif;
}

QPushButton {
    background-color: transparent;
    border: 1px solid white;
    border-radius: 10px;
    padding: 10px;
    min-height: 40px;
    color: white;
    font-size: 12pt;
}

QPushButton:hover {
    background-color: rgba(255, 255, 255, 0.2);
}

QLineEdit {
    border: 1px solid white;
    border-radius: 10px;
    padding: 10px;
    color: white;
    background-color: rgba(255, 255, 255, 0.1);
    font-size: 12pt;
}

QCheckBox {
    color: white;
    background-color: rgba(255, 255, 255, 0.1);
    padding: 5px;
    border: 1px solid white;
    border-radius: 10px;
}

QCheckBox::indicator {
    width: 15px;
    height: 15px;
    border: 1px solid white;
    border-radius: 7px;
    background-color: rgba(0, 0, 0, 0.2);
}

QCheckBox::indicator:checked {
    background-color: white;
}
"""


class QRCodeApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """ Initialize the UI components. """
        self.setup_window()
        self.create_widgets()
        self.setLayout(self.layout)

    def setup_window(self):
        """ Setup window properties """
        self.setWindowTitle("QR Code Generator")
        self.setGeometry(200, 200, 400, 400)
        self.set_background_gradient()
        font = QFont("Segoe UI", 10)
        self.setFont(font)
        self.setWindowOpacity(0.9)

    def set_background_gradient(self):
        """ Set the background gradient for the window. """
        palette = QPalette()
        gradient = QLinearGradient(0, 0, 0, 400)
        gradient.setColorAt(0.0, QColor(90, 90, 90))
        gradient.setColorAt(1.0, QColor(40, 40, 40))
        palette.setBrush(QPalette.Window, gradient)
        self.setPalette(palette)

    def create_widgets(self):
        """ Create and set the layout and widgets. """
        self.layout = QVBoxLayout()
        self.text_input = QLineEdit(self)
        self.text_input.setPlaceholderText("Enter text for QR code")
        self.layout.addWidget(self.text_input)
        self.generate_button = QPushButton("Generate QR", self)
        self.generate_button.clicked.connect(self.generate_qr)
        self.layout.addWidget(self.generate_button)
        self.qr_label = QLabel(self)
        self.layout.addWidget(self.qr_label, alignment=Qt.AlignCenter)
        self.transparent_checkbox = QCheckBox("Transparent", self)
        self.transparent_checkbox.stateChanged.connect(self.generate_qr)
        self.transparent_checkbox.setEnabled(False)
        self.layout.addWidget(self.transparent_checkbox)
        self.save_button = QPushButton("Save QR Code", self)
        self.save_button.clicked.connect(self.save_qr)
        self.save_button.setEnabled(False)
        self.layout.addWidget(self.save_button)
        self.clear_button = QPushButton("Clear", self)
        self.clear_button.clicked.connect(self.clear_content)
        self.layout.addWidget(self.clear_button)

    def generate_qr(self):
        """ Generate a QR code based on the text input. """
        text = self.text_input.text()
        if not text:
            return

        qr = pyqrcode.create(text)
        buffer = io.BytesIO()
        qr.png(buffer, scale=5)
        buffer.seek(0)
        self.update_qr_display(buffer)
        self.transparent_checkbox.setEnabled(True)

    def update_qr_display(self, buffer):
        """ Update the displayed QR code. """
        img = Image.open(buffer).convert("RGBA")
        new_data = [
            (255, 255, 255, 0) if item[:3] == (255, 255, 255) and self.transparent_checkbox.isChecked() else item for
            item in img.getdata()]
        img.putdata(new_data)

        buffer = io.BytesIO()
        img.save(buffer, "PNG")
        buffer.seek(0)

        pixmap = QPixmap()
        pixmap.loadFromData(buffer.getvalue())
        self.qr_label.setPixmap(pixmap)
        self.save_button.setEnabled(True)

    def save_qr(self):
        """ Save the QR code to a file. """
        file_path, _ = QFileDialog.getSaveFileName(self, "Save QR Code", "", "PNG files (*.png);;All files (*)")
        if file_path:
            text = self.text_input.text()
            if text:
                qr = pyqrcode.create(text)
                qr.png(file_path, scale=5)

    def clear_content(self):
        """ Clear the text input and the displayed QR code. """
        self.text_input.clear()
        self.qr_label.clear()
        self.save_button.setEnabled(False)

    def closeEvent(self, event):
        """ Handle the closing of the window. """
        event.accept()


if __name__ == '__main__':
    app = QApplication([])
    app.setStyleSheet(STYLESHEET)
    window = QRCodeApp()
    window.show()
    app.exec_()
