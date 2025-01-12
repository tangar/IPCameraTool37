# возможное решение проблемы с видео
# https://stackoverflow.com/questions/43665208/how-to-get-the-latest-frame-from-capture-device-camera-in-opencv

from PyQt5 import QtWidgets
import sys
from Camera import App

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = App()
    window.setWindowTitle("Управление эндоскопом Э-37")
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()
