import MySQLdb
from PyQt5 import QtCore, QtWidgets


class UiArchive(object):
    """
        This class describes client's window and shows information about clients.
    """
    def __init__(self):
        self.centralWidget = None
        self.horizontalLayoutWidget = None
        self.horizontalLayout = None

    def setup_ui(self, main_window):
        """ This function contains all client's form geometry settings """
        main_window.setObjectName("MainWindow")
        main_window.resize(823, 600)
        main_window.setMinimumSize(QtCore.QSize(750, 500))
        main_window.setMaximumSize(QtCore.QSize(750, 500))
        self.centralWidget = QtWidgets.QWidget(main_window)
        self.centralWidget.setObjectName("centralWidget")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralWidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 821, 600))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.create_table_widget()
        main_window.setCentralWidget(self.centralWidget)

        UiArchive.re_translate_ui(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def create_table_widget(self):
        """
        Create table widget
        """
        self.tableWidget = QtWidgets.QTableWidget(self.horizontalLayoutWidget)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setRowCount(3)
        self.horizontalLayout.addWidget(self.tableWidget)
        self.horizontalLayoutWidget.raise_()
        self.tableWidget.raise_()
        self.tableWidget.raise_()

    @staticmethod
    def re_translate_ui(main_window):
        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowTitle(_translate("MainWindow", "MainWindow"))


class ArchiveWindow(QtWidgets.QMainWindow):
    __list_of_column = [0, 0, 0, 0, 0, 0]

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = UiArchive()
        self.ui.setup_ui(self)
        row = ArchiveWindow.select_data_about_client()
        self.show_clients_data(row)
        self.ui.tableWidget.setHorizontalHeaderLabels(["Id", "Name and Surname", "Phone number",
                                                       "Date", "Time", "Doctor's name", "Room number"])

        header = self.ui.tableWidget.horizontalHeader()
        header.sectionClicked.connect(self.horizontal_header_clicked)

    @staticmethod
    def set_flags(list_of_flags):
        """
        Set all flags to 0. That means that data will sort by ascending
        :param list_of_flags: show column which we use in sort
        """
        for i in range(len(list_of_flags)):
            list_of_flags[i] = 0

    def horizontal_header_clicked(self):
        """
        Sort data from table by column
        """
        current_column = self.ui.tableWidget.currentColumn()

        if self.__list_of_column[current_column] == 0:
            order_by = "ASC"
            ArchiveWindow.set_flags(self.__list_of_column)
            self.__list_of_column[current_column] = 1
        else:
            order_by = "DESC"
            ArchiveWindow.set_flags(self.__list_of_column)

        if current_column == 0:
            data = ArchiveWindow.select_data_about_client("ID " + order_by)
        elif current_column == 1:
            data = ArchiveWindow.select_data_about_client("`Name and Surname` " + order_by)
        elif current_column == 2:
            data = ArchiveWindow.select_data_about_client("Phone " + order_by)
        elif current_column == 3:
            data = ArchiveWindow.select_data_about_client("Date " + order_by + ", Time")
        elif current_column == 4:
            data = ArchiveWindow.select_data_about_client("`Time`" + order_by)
        elif current_column == 5:
            data = ArchiveWindow.select_data_about_client("`Doctor's Name`" + order_by)
        else:
            data = ArchiveWindow.select_data_about_client("`Room number`" + order_by)

        self.show_clients_data(data)

    @staticmethod
    def select_data_about_client(parameter_order="ID"):
        """
        Select data about client from db
        :param parameter_order:  data will be sorted by this parameter
        :return:
        """
        conn = MySQLdb.connect('localhost', 'Valera', '5342395', 'sys')
        cursor = conn.cursor()

        cursor.execute("""SELECT c.ID, c.`Name and Surname`, c.`Phone`, c.`Date`, c.`Time`, c.`Doctor's name`, d.`room number`
        FROM clients c INNER JOIN doctors d
        ON c.`Doctor's name` = d.`Doctor's name`
        WHERE ((Date < CURRENT_DATE()) or (Date = current_date()) and (Time < current_time()))
        ORDER BY %s""" % parameter_order)
        data = cursor.fetchall()
        cursor.close()
        return data

    def show_clients_data(self, data):
        """
        Set data into table widget
        :param data: cortege rows with data.
        """
        self.ui.tableWidget.setRowCount(len(data))
        for i in range(len(data)):
            for j in range(len(data[i])):
                item = QtWidgets.QTableWidgetItem(str(data[i][j]))
                item.setFlags(QtCore.Qt.ItemIsEnabled)
                self.ui.tableWidget.setItem(i, j, item)
