import sys
# Импортируем наш интерфейс из файла
from main_window import *
from client_window import *
from doctor_window import *
from archive_window import *
from PyQt5 import QtWidgets


class MyWin(QtWidgets.QMainWindow):
    __clients = None
    __doctors = None
    __archive = None

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = UiMainWindow()
        self.ui.setupUi(self)

        # Здесь прописываем событие нажатия на кнопку
        self.ui.pushButton.clicked.connect(self.show_client_window)
        self.ui.pushButton_2.clicked.connect(self.show_doctor_window)
        self.ui.pushButton_3.clicked.connect(self.show_archive)

    def show_client_window(self):
        self.__clients = ClientWindow()
        self.__clients.show()

    def show_doctor_window(self):
        self.__doctors = DoctorWindow()
        self.__doctors.show()

    def show_archive(self):
        self.__archive = ArchiveWindow()
        self.__archive.show()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = MyWin()
    myapp.show()
    sys.exit(app.exec_())
