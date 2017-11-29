import sys
import MySQLdb
# Импортируем наш интерфейс из файла
from main_window import *
from client import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import QSize, Qt


class ClientWindow(QtWidgets.QMainWindow):
    tablemodel = None
    my_array = [['00', '01', '02'],
                ['10', '11', '12'],
                ['20', '21', '22']]

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_client()
        self.ui.setupUi(self)
        self.MyFunction()

    def MyFunction(self):
        conn = MySQLdb.connect('localhost', 'Valera', '5342395', 'sys')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users")

        # Получаем данные.
        row = cursor.fetchall()
        print(type(row))
        print(row[0])

        # Разрываем подключение.
        conn.close()

        self.ui.tableWidget.setRowCount(30000)
        self.ui.tableWidget.setColumnCount(3)
        for i in range(3):
           for j in range(3):
               self.ui.tableWidget.setItem(i, j, QTableWidgetItem("Text in column 1"))
        print(self.ui.tableWidget.item(0, 0).text())


class MyWin(QtWidgets.QMainWindow):
    __clients = None

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Здесь прописываем событие нажатия на кнопку
        self.ui.pushButton.clicked.connect(self.Function)
        #self.ui.menu.triggered.connect(self.Function())

    def Function(self):
        self.__clients = ClientWindow()
        self.__clients.show()


    # Пока пустая функция которая выполняется
    # при нажатии на кнопку



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = MyWin()
    myapp.show()
    sys.exit(app.exec_())
