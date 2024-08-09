from datetime import datetime

import cv2
from PyQt5 import QtWidgets
import sys
from typing import Optional

import onvif
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap

from CameraController import CameraController

# import MainWindow
import CameraGuiNew

class App(QtWidgets.QMainWindow, CameraGuiNew.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.camera: Optional[CameraController] = None
        self.cap = None

        self.rtsp_url_main = "rtsp://admin:6m8vw@198.0.100.108:80/cam/realmonitor?channel=1&subtype=0&unicast=true&proto=Onvif"
        self.rtsp_url_second = "rtsp://admin:6m8vw@198.0.100.108:80/cam/realmonitor?channel=1&subtype=0&unicast=true&proto=Onvif"
        
        self.savePath = './Frames'

        self.find_camera()
        self.connectButton.clicked.connect(lambda: self.connect_camera())

        self.zoomSlider.valueChanged.connect(lambda: self.set_zoom(self.zoomSlider.value()))
        self.zoomUpButton.clicked.connect(lambda: self.zoomSlider.setValue(self.zoomSlider.value() + self.zoomSlider.singleStep()))
        self.zoomDownButton.clicked.connect(lambda: self.zoomSlider.setValue(self.zoomSlider.value() - self.zoomSlider.singleStep()))

        self.FocusSlider.valueChanged.connect(lambda: self.set_focus(self.FocusSlider.value()))
        self.focusUpButton.clicked.connect(lambda: self.FocusSlider.setValue(self.FocusSlider.value() + self.FocusSlider.singleStep()))
        self.focusDownButton.clicked.connect(lambda: self.FocusSlider.setValue(self.FocusSlider.value() - self.FocusSlider.singleStep()))

        self.checkBoxAutoFocus.clicked.connect(lambda: self.auto_focus())

        self.shotButton.clicked.connect(lambda: self.make_shot())

        self.cap = cv2.VideoCapture(self.rtsp_url_main)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateFrame)
        self.timer.start(5)
        
        self.setPhotoPath.triggered.connect(lambda: self.configPath())


    def configPath(self):
        self.savePath = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Folder')
        print(self.savePath)

    def find_camera(self):
        try:
            self.camera = CameraController()
        except onvif.exceptions.ONVIFError:
            self.appendText("Отсутствует подключение к камере")

    def connect_camera(self):
        if self.camera:
            self.camera.connect()
            print(self.camera.zoom_level)
            print(self.camera.focus_level)
            self.zoomSlider.setValue(self.camera.zoom_level * 100)
            self.FocusSlider.setValue(self.camera.focus_level * 100)
            self.appendText('Камера подключена')
        else:
            self.find_camera()
        if self.camera is None:
            self.appendText('Камера не найдена. Проверьте подключение')

    def set_zoom(self, value):
        if self.camera and self.camera.connected:
            pos = value / 100
            self.camera.zoom_handler(pos)
            self.zoomSlider.setValue(value)
            self.appendText(f'Зум установлен в позицию {self.camera.zoom_level}')
        else:
            self.appendText('Подключение к камере отсутствует')

    def set_focus(self, value):
        if self.camera and self.camera.connected:
            pos = value / 100
            print(self.camera.focus_level)
            self.camera.focus_handler(pos)
            print(self.camera.focus_level)
            self.FocusSlider.setValue(value)
            self.appendText(f'Фокус установлен в позицию {self.camera.focus_level}')
        else:
            self.appendText('Подключение к камере отсутствует')

    def appendText(self, text):
        now = datetime.now()
        formatted_time = now.strftime("%Y-%m-%d %H-%M-%S")
        self.textBrowser.append(formatted_time + ' ' + text)

    def set_iris(self, value):
        if self.camera and self.camera.connected:
            pos = value / 100
            self.camera.iris_handler(pos)
            self.IrisSlider.setValue(value)
            self.appendText(f'Диафрагма установлена в позицию {self.camera.iris_level}')
        else:
            self.appendText('Подключение к камере отсутствует')

    def auto_focus(self):
        auto = self.checkBoxAutoFocus.isChecked()
        self.camera.focus_mode(auto)
        if auto:
            self.FocusSlider.setDisabled(True)
            self.focusUpButton.setDisabled(True)
            self.focusDownButton.setDisabled(True)
        else:
            self.FocusSlider.setDisabled(False)
            self.set_focus(self.FocusSlider.value())
            self.focusUpButton.setDisabled(False)
            self.focusDownButton.setDisabled(False)

    def make_shot(self):
        if self.cap:
            try:
                ret, frame = self.cap.read()
                stamp = datetime.now()
                datetime_str = stamp.strftime("%Y-%m-%d_%H-%M-%S")
                full_file_name = "{} Frame.jpg".format(self.savePath + '/' + datetime_str)
                cv2.imwrite(full_file_name, frame)
                self.textBrowser.setText(f'Файл сохранён {full_file_name}')

            except Exception:
                self.textBrowser.setText(f'Не удалось сделать снимок. {Exception}')
        else:
            self.textBrowser.setText('Не удалось сделать снимок. Камера не подключена')

    def updateFrame(self):
        ret, frame = self.cap.read()
        if ret:
            # Convert the frame to a QPixmap for display
            var = self.main_cam.frameSize()
            
            #target_width, target_height = 640, 480  # Задайте нужный размер
            target_width = var.width()
            target_height = int(var.width() / 16 * 9)

            frame = cv2.resize(frame, (target_width, target_height))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            height, width, channel = frame.shape
            step = channel * width

            qImg = QImage(frame.data, frame.shape[1], frame.shape[0], step, QImage.Format_RGB888)
            qPix = QPixmap.fromImage(qImg)
            self.main_cam.setPixmap(qPix)

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = App()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
