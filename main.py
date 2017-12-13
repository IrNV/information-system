import sys
# Импортируем наш интерфейс из файла
from main_window import *
from client_window import *
from doctor_window import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import QSize, Qt


class MyWin(QtWidgets.QMainWindow):
    __clients = None
    __doctors = None

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = UiMainWindow()
        self.ui.setupUi(self)

        # Здесь прописываем событие нажатия на кнопку
        self.ui.pushButton.clicked.connect(self.function)
        self.ui.pushButton_2.clicked.connect(self.f2)

    def function(self):
        self.__clients = ClientWindow()
        self.__clients.show()

    def f2(self):
        self.__doctors = DoctorWindow()
        self.__doctors.show()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = MyWin()
    myapp.show()
    sys.exit(app.exec_())
