from PyQt5 import QtCore, QtWidgets
from Data_Base import DataBaseMySQL


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
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = UiArchive()
        self.ui.setup_ui(self)

        self.ui.tableWidget.setHorizontalHeaderLabels(["Id", "Name and Surname", "Phone number",
                                                       "Date", "Time", "Doctor's name", "Room number"])

    def set_horizontal_signal(self, horizontal):
        """
        What to do when the horizontal header is clicked
        """
        header = self.ui.tableWidget.horizontalHeader()
        header.sectionClicked.connect(horizontal)

    def set_row_count(self, count):
        """
        To set the count of rows
        """
        self.ui.tableWidget.setRowCount(count)

    @staticmethod
    def get_item(data):
        """
        get data from table cell
        """
        return QtWidgets.QTableWidgetItem(data)

    @staticmethod
    def set_enabled(item):
        """
        Deny the ability to modify data in cell
        """
        item.setFlags(QtCore.Qt.ItemIsEnabled)

    def set_item(self, i, j, item):
        """
        set item into table cell
        """
        self.ui.tableWidget.setItem(i, j, item)

    def get_current_column(self):
        """
        :return: a number of columns
        """
        return self.ui.tableWidget.currentColumn()


class ArchiveLogic:
    __list_of_column = [0, 0, 0, 0, 0, 0, 0]

    def __init__(self):
        self.interface = ArchiveWindow()
        self.interface.set_horizontal_signal(self.horizontal_header_clicked)
        self.DataBase = DataBaseMySQL()
        row = self.DataBase.select_archive_data()
        self.show_clients_data(row)

    def horizontal_header_clicked(self):
        """
        Sort data from table by column
        """

        current_column = self.interface.get_current_column()
        if self.__list_of_column[current_column] == 0:
            order_by = "ASC"
            self.set_flags(self.__list_of_column)
            self.__list_of_column[current_column] = 1
        else:
            order_by = "DESC"
            self.set_flags(self.__list_of_column)

        if current_column == 0:
            data = self.DataBase.select_archive_data("ID " + order_by)
        elif current_column == 1:
            data = self.DataBase.select_archive_data("`Name and Surname` " + order_by)
        elif current_column == 2:
            data = self.DataBase.select_archive_data("Phone " + order_by)
        elif current_column == 3:
            data = self.DataBase.select_archive_data("Date " + order_by + ", Time")
        elif current_column == 4:
            data = self.DataBase.select_archive_data("`Time`" + order_by)
        elif current_column == 5:
            data = self.DataBase.select_archive_data("`Doctor's Name`" + order_by)
        else:
            data = self.DataBase.select_archive_data("`Room number`" + order_by)
        self.show_clients_data(data)

    @staticmethod
    def set_flags(list_of_flags):
        """
        Set all flags to 0. That means that data will sort by ascending
        :param list_of_flags: show column which we use in sort
        """
        for i in range(len(list_of_flags)):
            list_of_flags[i] = 0

    def show(self):
        self.interface.show()

    def show_clients_data(self, data):
        """
        Set data into table widget
        :param data: cortege rows with data.
        """
        self.interface.set_row_count(len(data))
        for i in range(len(data)):
            for j in range(len(data[i])):
                item = self.interface.get_item(str(data[i][j]))
                self.interface.set_enabled(item)
                self.interface.set_item(i, j, item)