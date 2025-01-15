from datetime import datetime
import threading

from MyVideoCapture import MyVideoCapture

import cv2
from PyQt5 import QtWidgets
from typing import Optional

import onvif
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap

from PyQt5.QtWidgets import QApplication, QListWidget, QListWidgetItem, QVBoxLayout, QWidget, QMessageBox

from CameraController import *

import CameraGuiNew
from CameraConfig import CameraConfig
import ImageViewer as Viewer

from MyPinger import *
from MySocket import *
from endoscope import *

class App(QtWidgets.QMainWindow, CameraGuiNew.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.camONVIFSide: Optional[CameraController] = None
        self.camONVIFBott: Optional[CameraController] = None
        self.cap_main = None
        self.cap_second = None
        self.viewer = Viewer.ImageFileViewer()

        self.camera_config = CameraConfig(config_file="config.json")
        self.camera_config.load_config()
        self.camera_config.save_config()

        self.controllerOnline = False
        self.mainOnline = False
        self.secondOnline = False
        
        self.eds = None
        self.txSocket = None
        self.rxSocket = None
        
        self.eds = Endoscope()

        self.timer = QTimer(self)
        self.updateFormTimer = QTimer(self)

        self.AppConnectors()

        self.PingThread = None
        self.PingThread = threading.Thread(target=self.pingTask)
        self.PingThread.daemon = True
        self.PingThread.start()

        self.ControllerPingThread = None
        self.ControllerPingThread = threading.Thread(target=self.checkControllerTask)
        self.ControllerPingThread.daemon = True
        self.ControllerPingThread.start()

        self.ControllerHandlerThread = None
        self.ControllerHandlerThread = threading.Thread(target=self.controllerHandlerTask)
        self.ControllerHandlerThread.daemon = True
        self.ControllerHandlerThread.start()

        self.rxSocket = RxSocket(callback=self.eds.MessageProcessor)  
        self.rxSocket.Open('', self.camera_config.controller_port_rx)

        self.txSocket = TxSocket()
        self.txSocket.Open(self.camera_config.controller_ip, self.camera_config.controller_port_tx)

    def checkControllerTask(self):
        event = threading.Event()
        while(True):
            event.wait(1)
            print("Send ping packet to board")
            self.txSocket.Send(bytes([Commands.CMD_PING.value]))

    def controllerHandlerTask(self):
        event = threading.Event()
        while(True):
            event.wait(0.5)
            print("Send status request from board")
            self.txSocket.Send(bytes([Commands.CMD_GET_STATUS.value]))

    def pingTask(self):
        event = threading.Event()
        while True:
            event.wait(1)
            self.controllerOnline = MyPinger.ping(self.camera_config.controller_ip, 1,50) == 0
            self.mainOnline = MyPinger.ping(self.camera_config.main_ip, 1,50) == 0
            self.secondOnline = MyPinger.ping(self.camera_config.second_ip, 1,50) == 0

    def AppConnectors(self):
        self.timer.timeout.connect(self.updateFrame)
        self.timer.start(50)
        self.updateFormTimer.timeout.connect(self.updateForm)
        self.updateFormTimer.start(100)

        self.setPhotoPath.triggered.connect(self.configPath)
        self.saveSettings.triggered.connect(lambda: self.camera_config.save_config())
        self.loadSettings.triggered.connect(lambda: self.camera_config.load_config())
        self.loggerList.itemDoubleClicked.connect(self.viewer.on_item_double_clicked)
        self.tabWidget.currentChanged.connect(self.on_tab_changed)

        self.tabWidget.setCurrentIndex(0)

        self.connButtonIP.clicked.connect(self.connect_IP_CAM)

        self.zoomSlider.valueChanged.connect(lambda: self.set_zoom(self.zoomSlider.value()))
        self.zoomUpButton.clicked.connect(lambda: self.zoomSlider.setValue(self.zoomSlider.value() + self.zoomSlider.singleStep()))
        self.zoomDownButton.clicked.connect(lambda: self.zoomSlider.setValue(self.zoomSlider.value() - self.zoomSlider.singleStep()))

        self.FocusSlider.valueChanged.connect(lambda: self.set_focus(self.FocusSlider.value()))
        self.focusUpButton.clicked.connect(lambda: self.FocusSlider.setValue(self.FocusSlider.value() + self.FocusSlider.singleStep()))
        self.focusDownButton.clicked.connect(lambda: self.FocusSlider.setValue(self.FocusSlider.value() - self.FocusSlider.singleStep()))

        self.checkBoxAutoFocus.clicked.connect(lambda: self.auto_focus())
        self.shotButton.clicked.connect(lambda: self.make_shot())

        self.pbLightDown.clicked.connect(self.setDownLight)


    def setDownLight(self):
        cmd_pwm = self.lightBotPwm.value()
        cmd_freq = 1000

        b0, b1, b2, b3 = Endoscope.prepBotLight(cmd_pwm, cmd_freq)
        self.txSocket.Send(bytes([b0, b1, b2, b3]))

    def updateValue(self, value): 
        print(f"new value is {value}")
    
    def updateForm(self):
        self.isOnlineControllerCB.setChecked(self.controllerOnline)
        self.isOnlineMainCB.setChecked(self.mainOnline)
        self.isOnlineSecondCB.setChecked(self.secondOnline)
        str = f"UC is {self.eds.TemperatureUC} deg. Light is {self.eds.TemperatureSide} deg."
        self.statusBar().showMessage(str)

    def on_tab_changed(self, index):
        if (index == 0):
            # сделать элементы управления активными
            print(f"Switched to tab index: {index}")
        elif (index == 1):
            # сделать элементы управления пассивными
            print(f"Switched to tab index: {index}")
              
    def configPath(self):
        self.camera_config.SAVE_PATH = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Folder')
        self.camera_config.save_config()

    def connect_IP_CAM(self):
        try:
            self.cap_main = MyVideoCapture(self.camera_config.main_rtsp_url, 5000)
            self.cap_main.Open()
            if(self.cap_main.isReady):
                self.appendText("Боковая камера подключена")

            self.cap_second = MyVideoCapture(self.camera_config.second_rtsp_url, 5000)
            self.cap_second.Open()
            if(self.cap_second.isReady):
                self.appendText("Осевая камера подключена")
        
            cameraONVIFSide = CameraController(self.camera_config.CAMERA_HOST,
                                      self.camera_config.CAMERA_PORT,
                                      self.camera_config.CAMERA_USER,
                                      self.camera_config.CAMERA_PASS)
            cameraONVIFSide.connect()
            
            if (cameraONVIFSide.connected):
                self.camONVIFSide = cameraONVIFSide
                self.zoomSlider.setValue(int(self.camONVIFSide.zoom_level * 100))
                self.FocusSlider.setValue(int(self.camONVIFSide.focus_level * 100))
                self.camONVIFSide.zoom_handler(self.camONVIFSide.zoom_level)
                self.camONVIFSide.focus_handler(self.camONVIFSide.focus_level)
                self.camONVIFSide.focus_mode_auto(True)
                self.appendText('Боковая камера подключена по ONVIF')
            else:
                self.appendText('Боковая камера не подключена по ONVIF. Проверьте подключение')   
            
            cameraONVIFBott = CameraController(self.camera_config.second_ip,
                                      8080,
                                      self.camera_config.CAMERA_USER,
                                      self.camera_config.CAMERA_PASS)
            cameraONVIFBott.connect()

            if (cameraONVIFBott.connected):
                self.camONVIFBott = cameraONVIFBott
                self.appendText('Осевая камера подключена по ONVIF')
            else:
                self.appendText('Осевая камера не подключена по ONVIF. Проверьте подключение')   
            
            self.zoomSlider.setEnabled(self.camONVIFSide.connected)
            self.zoomUpButton.setEnabled(self.camONVIFSide.connected)
            self.zoomDownButton.setEnabled(self.camONVIFSide.connected)
            self.FocusSlider.setEnabled(self.camONVIFSide.connected)
            self.focusUpButton.setEnabled(self.camONVIFSide.connected)
            self.focusDownButton.setEnabled(self.camONVIFSide.connected)
            self.checkBoxAutoFocus.setEnabled(self.camONVIFSide.connected)

            if (self.cap_main.isReady and self.cap_second.isReady):
                self.appendText('Подключение выпонено')
                self.connButtonIP.setChecked(True)
            else:
                self.appendText('Подключение не выполнено')
                self.connButtonIP.setChecked(False)
        
        except onvif.exceptions.ONVIFError as e:
            self.appendText(f"Ошибка подключения к камере: {str(e)}")

    def set_zoom(self, value):
        if self.camONVIFSide and self.camONVIFSide.connected:
            pos = value / 100
            self.camONVIFSide.zoom_handler(pos)
            self.zoomSlider.setValue(value)
            self.appendText(f'Зум установлен в позицию {self.camONVIFSide.zoom_level}')
        else:
            self.appendText('Подключение к камере отсутствует')

    def set_focus(self, value):
        if self.camONVIFSide.connected:
            pos = value / 100
            print(self.camONVIFSide.focus_level)
            self.camONVIFSide.focus_handler(pos)
            print(self.camONVIFSide.focus_level)
            self.FocusSlider.setValue(value)
            self.appendText(f'Фокус установлен в позицию {self.camONVIFSide.focus_level}')
        else:
            self.appendText('Подключение к камере отсутствует')

    def auto_focus(self):
        auto = self.checkBoxAutoFocus.isChecked()
        self.camONVIFSide.focus_mode_auto(auto)
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
        id = self.tabWidget.currentIndex()
        if id == 0:
            self.savePicture(self.cap_main)
        if id == 1:
            self.savePicture(self.cap_second)
        else:
            return

    def savePicture(self, cap :MyVideoCapture):
        if cap.isReady:
            try:
                frame = cap.read()
                stamp = datetime.datetime.now()
                datetime_str = stamp.strftime("%Y-%m-%d_%H-%M-%S")
                full_file_name = "{} Frame.jpg".format(self.camera_config.SAVE_PATH + '/' + datetime_str)
                cv2.imwrite(full_file_name, frame)
                self.appendText(full_file_name)
            except Exception:
                self.appendText(f'Не удалось сделать снимок. {Exception}')
        else:
            self.appendText('Не удалось сделать снимок. Камера не подключена')

    
    def updateFrame(self):
        cap = None
        widget = None
        # определим с какой камерой работаем
        id = self.tabWidget.currentIndex()
        if id == 0:
            cap = self.cap_main
            widget = self.main_cam_widget
        elif id == 1:
            cap = self.cap_second
            widget = self.second_cam_widget
        else:
            return

        # Здесь хорошо бы проверить на то, что успешно смогли считать кадр
        try:
            if (cap == None):
                return

            frame = cap.read()
            
            var = widget.frameSize()
            target_width = var.width()
            target_height = int(var.width() / 16 * 9)

            frame = cv2.resize(frame, (target_width, target_height))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            height, width, channel = frame.shape
            step = channel * width

            qImg = QImage(frame.data, frame.shape[1], frame.shape[0], step, QImage.Format_RGB888)
            qPix = QPixmap.fromImage(qImg)
            widget.setPixmap(qPix)
        except:
            print ("Eror get frame")

    def appendText(self, text):
        now = datetime.datetime.now()
        time_string = now.strftime("%Y-%m-%d %H:%M:%S")
        text2 = time_string + ' ' + text
        self.loggerList.insertItem(0, QListWidgetItem(text))

    def show_message(self, value):
        txt = 'Slider = '+ str(value)
        print(txt)
        self.lightBotPwmLabel.setText(str(self.lightBotPwm.value()))
        self.lightSidePwmLabel.setText(str(self.lightSidePwm.value()))