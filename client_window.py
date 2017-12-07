import MySQLdb
from PyQt5 import QtCore, QtGui, QtWidgets


class UiClient(object):
    """
        This class describes client's window and shows information about clients.
    """
    def setupUi(self, MainWindow):
        """ This function contains all client's form geometry settings """
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(823, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 821, 600))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tableWidget = QtWidgets.QTableWidget(self.horizontalLayoutWidget)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setRowCount(1)
        self.horizontalLayout.addWidget(self.tableWidget)
        self.horizontalLayoutWidget.raise_()
        self.tableWidget.raise_()
        self.tableWidget.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 823, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))


class ClientWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = UiClient()
        self.ui.setupUi(self)
        self.show_clients_data()

        self.ui.tableWidget.cellChanged.connect(self.feun)
        header = self.ui.tableWidget.verticalHeader()
        header.sectionClicked.connect(self.feun)

    def feun(self):
        print(self.ui.tableWidget.currentColumn(), self.ui.tableWidget.currentRow())
        print("HELLO!")
        print(self.a.currentIndex())

    def reed_information_about_client(self):
        conn = MySQLdb.connect('localhost', 'Valera', '5342395', 'sys')
        cursor = conn.cursor()

        cursor.execute("""SELECT c.`Name and Surname`, c.`Phone`, c.`Date`, c.`Time`, c.`Doctor's name`, d.`room number`
                       FROM clients c INNER JOIN doctors d
                       ON c.`Doctor's name` = d.`Doctor's name`""")
        data = cursor.fetchall()
        cursor.close()
        return data

    def show_clients_data(self):
        row = self.reed_information_about_client()

        print(self.ui.tableWidget.columnCount())
        for i in range(1):
            for j in range(6):
                pass
                # self.ui.tableWidget.setItem(i, j, QTableWidgetItem(str(row[0][j])))
        self.a = QtWidgets.QComboBox()
        self.a.addItem("asd")
        self.a.addItem("shgdf")
        self.a.currentIndexChanged.connect(self.feun)
        print(self.a.currentText())
        self.a.setCurrentIndex(0)
        self.ui.tableWidget.setCellWidget(0, 2, self.a)
