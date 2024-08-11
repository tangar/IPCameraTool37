import sys
import os
import subprocess
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.QtGui import QImageReader

class ImageFileViewer(QMainWindow):
    def __init__(self):
        super().__init__()

    def on_item_double_clicked(self, item):
        file_path = item.text()
        # Проверяем, является ли файл изображением
        if self.is_image(file_path):
            self.open_in_system_viewer(file_path)
        else:
            QMessageBox.information(self, "Not an Image", "The selected file is not an image.")

    def is_image(self, file_path):
        # Используем QImageReader для проверки формата файла
        image_reader = QImageReader(file_path)
        return image_reader.canRead()
    
    def open_in_system_viewer(self, file_path):
        # Открываем изображение в системном приложении по умолчанию
        try:
            if sys.platform.startswith('darwin'):
                subprocess.call(('open', file_path))
            elif os.name == 'nt':  # Windows
                os.startfile(file_path)
            elif os.name == 'posix':  # Linux, Unix, etc.
                subprocess.call(('xdg-open', file_path))
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to open the image: {str(e)}")