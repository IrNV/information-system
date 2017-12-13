import MySQLdb
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QTableWidget, QTableWidgetItem


class UiClient(object):
    """
        This class describes client's window and shows information about clients.
    """
    NUMBER_OF_COLUMN = 7
    NUMBER_OF_ROW = 0

    def setupUi(self, main_window):
        """ This function contains all client's form geometry settings """
        main_window.setObjectName("MainWindow")
        main_window.resize(823, 600)
        self.centralwidget = QtWidgets.QWidget(main_window)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 821, 600))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.create_table_widget()
        main_window.setCentralWidget(self.centralwidget)
        self.set_menu_bar(main_window)
        main_window.setMenuBar(self.menubar)
        UiClient.retranslateUi(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def create_table_widget(self):
        """
        Crete table widget and sets settings
        """
        self.tableWidget = QtWidgets.QTableWidget(self.horizontalLayoutWidget)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(self.NUMBER_OF_COLUMN)
        self.tableWidget.setRowCount(self.NUMBER_OF_ROW)
        self.horizontalLayout.addWidget(self.tableWidget)
        self.horizontalLayoutWidget.raise_()
        self.tableWidget.raise_()
        self.tableWidget.raise_()

    def set_menu_bar(self, main_window):
        """
        This method creates menu bar, adds buttons and sets options
        """
        self.menubar = QtWidgets.QMenuBar(main_window)
        self.menubar.addAction("Add new doctor")
        self.menubar.addAction("Delete doctor")
        self.menubar.addAction("Revert")
        self.menubar.addAction("Save changes")
        self.menubar.setGeometry(QtCore.QRect(0, 0, 823, 21))
        self.menubar.setObjectName("menubar")

    @staticmethod
    def retranslateUi(main_window):
        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowTitle(_translate("MainWindow", "MainWindow"))


class ClientWindow(QtWidgets.QMainWindow):
    __selected_client = None
    __array_of_combo_boxes = []
    __list_of_column = [0, 0, 0, 0, 0, 0, 0]
    NUMBER_OF_COLUMN = 7

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = UiClient()
        self.ui.setupUi(self)
        self.ui.tableWidget.setHorizontalHeaderLabels(["Id", "Name and Surname", "Phone", "Date",
                                                       "Time", "Doctor's name", "Room number"])

        self.show_clients_data(ClientWindow.reed_information_about_client())
        self.set_signals_and_slots()

    def set_signals_and_slots(self):
        """
        Set signals and slots to buttons and headers
        """
        self.ui.menubar.actions()[0].triggered.connect(self.add_new_client)
        self.ui.menubar.actions()[1].triggered.connect(self.delete_client)
        self.ui.menubar.actions()[2].triggered.connect(self.revert)
        self.ui.menubar.actions()[3].triggered.connect(self.save_changes)
        self.ui.tableWidget.cellClicked.connect(self.cell_clicked)
        header = self.ui.tableWidget.verticalHeader()
        header.sectionClicked.connect(self.vertical_header_clicked)

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
        data_from_table = self.select_data_from_table()
        date_column = 3
        time_column = 4

        if self.__list_of_column[current_column] == 0:
            order = False
            ClientWindow.set_flags(self.__list_of_column)
            if current_column in [date_column, time_column]:
                self.__list_of_column[date_column] = 1
                self.__list_of_column[time_column] = 1
            else:
                self.__list_of_column[current_column] = 1
        else:
            order = True
            ClientWindow.set_flags(self.__list_of_column)

        if current_column not in [date_column, time_column]:
            sorted_data = sorted(data_from_table, key=lambda x: x[current_column],
                                 reverse=order)
        else:
            sorted_data = sorted(data_from_table, key=lambda x: (x[date_column],
                                                                 x[time_column]), reverse=order)

        self.show_clients_data(sorted_data)

    def vertical_header_clicked(self):
        """
        this function set the number of raw which have been clicked and
        this number is set to __selected_client value.
        """
        self.__selected_client = self.ui.tableWidget.currentRow()

    def cell_clicked(self):
        """
        Set selected_client None if user click on cell.
        """
        self.__selected_client = None

    def combobox_changed(self):
        doctors_data = self.select_doctors()

        for j in range(len(self.__array_of_combo_boxes)):
            for i in range(len(doctors_data)):
                if self.__array_of_combo_boxes[j].currentText() in doctors_data[i]:
                    item = QtWidgets.QTableWidgetItem(str(doctors_data[i][2]))
                    item.setFlags(QtCore.Qt.ItemIsEnabled)
                    self.ui.tableWidget.setItem(j, 6, item)

    @staticmethod
    def reed_information_about_client():
        """
        Reed data from a database about clients.
        :return: cortege rows with data.
        """
        conn = MySQLdb.connect('localhost', 'Valera', '5342395', 'sys')
        cursor = conn.cursor()

        cursor.execute("""SELECT  c.`ID`, c.`Name and Surname`, c.`Phone`, c.`Date`, c.`Time`, c.`Doctor's name`, d.`room number`
                       FROM clients c INNER JOIN doctors d
                       ON c.`Doctor's name` = d.`Doctor's name`""")
        data = cursor.fetchall()
        cursor.close()
        return data

    def show_clients_data(self, row):
        """
        Set data into table widget
        :param row: cortege rows with data.
        """
        self.ui.tableWidget.setRowCount(len(row))
        data = ClientWindow.select_doctors()
        self.__array_of_combo_boxes = []
        for i in range(len(row)):
            for j in range(self.NUMBER_OF_COLUMN):
                item = QtWidgets.QTableWidgetItem(str(row[i][j]))
                if j == 0 or j == 6:
                    item.setFlags(QtCore.Qt.ItemIsEnabled)
                elif j == 5:
                    self.create_combo_box(data, i + 1, row[i][j])
                self.ui.tableWidget.setItem(i, j, item)

    @staticmethod
    def select_doctors():
        """
        Reed data from a database about doctors.
        :return: cortege rows with data.
        """
        conn = MySQLdb.connect('localhost', 'Valera', '5342395', 'sys')
        cursor = conn.cursor()

        cursor.execute("""SELECT  * FROM doctors """)
        data = cursor.fetchall()
        cursor.close()
        return data

    def get_max_id(self):
        """
        Find max id in table.
        :return: max id in current table.
        """
        list_of_id = []
        for i in range(self.ui.tableWidget.rowCount()):
            list_of_id.append(int(self.ui.tableWidget.item(i, 0).text()))
        return max(list_of_id)

    def add_new_client(self):
        """
        Add new client.
        """
        max_id = self.get_max_id()
        data = ClientWindow.select_doctors()

        new_row = self.ui.tableWidget.rowCount() + 1
        self.ui.tableWidget.setRowCount(new_row)

        self.set_default_fields(data, max_id, new_row)
        self.create_combo_box(data, new_row)

    def set_default_fields(self, data, max_id, new_row):
        """
        Set table fields with default data
        :param data: data from db about clients
        :param max_id: max id in our table
        :param new_row: number of the current new line
        :return:
        """
        item = QtWidgets.QTableWidgetItem(str(max_id + 1))
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.ui.tableWidget.setItem(new_row - 1, 0, item)

        item = QtWidgets.QTableWidgetItem(str(data[0][2]))
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.ui.tableWidget.setItem(new_row - 1, 6, item)

        for i in range(1, 6):
            item = QtWidgets.QTableWidgetItem(None)
            self.ui.tableWidget.setItem(new_row - 1, i, item)

    def create_combo_box(self, data, row, current_doctor=None):
        """
        Create combo box for doctor's list
        :param data: data from db about doctors
        :param row: number of the current new line
        :param current_doctor: name of doctor of the client
        """
        list_of_doctors = []
        for i in range(len(data)):
            list_of_doctors.append(data[i][1])
        combo_box = QtWidgets.QComboBox()
        combo_box.addItems(list_of_doctors)
        combo_box.currentIndexChanged.connect(self.combobox_changed)
        self.__array_of_combo_boxes.append(combo_box)

        if current_doctor is not None:
            combo_box.setCurrentText(current_doctor)
        self.ui.tableWidget.setCellWidget(row - 1, 5, combo_box)

    def delete_client(self):
        """
        Delete selected row.
        """
        if self.__selected_client is not None:
            self.ui.tableWidget.removeRow(self.__selected_client)

    def revert(self):
        """
        Cancel changes and revert previous data
        """
        self.show_clients_data(ClientWindow.reed_information_about_client())

    def select_data_from_table(self):
        """
        Select data from client's table widget
        :return: return list where each element is list which includes data from row
        """
        data = []
        for i in range(self.ui.tableWidget.rowCount()):
            data.append([])
            for j in range(self.NUMBER_OF_COLUMN):
                if (j == 0) or (j == 6):
                    cell_data = self.ui.tableWidget.item(i, j).text()
                    data[i].append(int(cell_data))
                elif j == 5:
                    cell_data = self.ui.tableWidget.cellWidget(i, 5).currentText()
                    data[i].append(cell_data)
                else:
                    cell_data = self.ui.tableWidget.item(i, j).text()
                    data[i].append(cell_data)

        return data

    @staticmethod
    def select_id():
        """
        Select client's id from db
        :return: cortege of ids
        """
        conn = MySQLdb.connect('localhost', 'Valera', '5342395', 'sys')
        cursor = conn.cursor()

        cursor.execute("""SELECT ID FROM clients ORDER BY ID""")
        data = cursor.fetchall()
        cursor.close()

        return data

    @staticmethod
    def update_data(row, data):
        """
        Update data in db by id
        """
        conn = MySQLdb.connect('localhost', 'Valera', '5342395', 'sys')
        cursor = conn.cursor()

        cursor.execute("""UPDATE clients
            SET `Name and Surname` = %s, `Phone` = %s, `Date` = %s, `Time` = %s, `Doctor's name` = %s
            WHERE ID = %s """, (data[row][1], data[row][2], data[row][3], data[row][4], data[row][5], data[row][0]))

        conn.commit()
        cursor.close()

    @staticmethod
    def add_new_data(row, data):
        """
        Add new data to db from client's table widget
        """
        conn = MySQLdb.connect('localhost', 'Valera', '5342395', 'sys')
        cursor = conn.cursor()

        cursor.execute("""INSERT INTO clients
            (ID, `Name and Surname`, `Phone`, `Date`, `Time`, `Doctor's name`)
            VALUES (%s, %s, %s, %s, %s, %s)
            """, (data[row][0], data[row][1], data[row][2], data[row][3], data[row][4], data[row][5]))

        conn.commit()
        cursor.close()

    @staticmethod
    def delete_data(id_row):
        """
        Delete row in db by id
        """
        conn = MySQLdb.connect('localhost', 'Valera', '5342395', 'sys')
        cursor = conn.cursor()
        cursor.execute("""DELETE FROM clients
            WHERE ID = %s
            """, (id_row,))
        conn.commit()
        cursor.close()

    def save_changes(self):
        """
        Save all changes was done
        """
        selected_id = ClientWindow.select_id()
        list_of_id_from_db = []
        list_of_id_from_table = []

        for i in range(len(selected_id)):
            list_of_id_from_db.append(selected_id[i][0])

        data_from_table = self.select_data_from_table()

        for i in range(len(data_from_table)):
            list_of_id_from_table.append(data_from_table[i][0])

        for i in range(len(list_of_id_from_table)):
            if data_from_table[i][0] in list_of_id_from_db:
                ClientWindow.update_data(i, data_from_table)
            else:
                ClientWindow.add_new_data(i, data_from_table)

        for i in range(len(list_of_id_from_db)):
            if list_of_id_from_db[i] not in list_of_id_from_table:
                ClientWindow.delete_data(list_of_id_from_db[i])