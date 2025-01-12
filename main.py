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
