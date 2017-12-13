import MySQLdb
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import QSize, Qt


class UiDoctor(object):
    """
        This class describes client's window and shows information about clients.
    """
    def setup_ui(self, main_window):
        """ This function contains all client's form geometry settings """
        main_window.setObjectName("MainWindow")
        main_window.resize(600, 500)
        self.centralwidget = QtWidgets.QWidget(main_window)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 821, 600))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.create_table_widget()
        main_window.setCentralWidget(self.centralwidget)#
        self.set_menu_bar(main_window)
        main_window.setMenuBar(self.menubar)

        UiDoctor.re_translate_ui(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def create_table_widget(self):
        """
        This method creates table widget and sets options
        """
        self.tableWidget = QtWidgets.QTableWidget(self.horizontalLayoutWidget)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setRowCount(0)
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
    def re_translate_ui(main_window):
        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowTitle(_translate("MainWindow", "MainWindow"))


class DoctorWindow(QtWidgets.QMainWindow):
    __selected_doctor = None

    def __init__(self, parent=None):
        """
        Initialize doctor's window
        """
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = UiDoctor()
        self.ui.setup_ui(self)
        self.ui.tableWidget.setHorizontalHeaderLabels(["Id", "Name", "Room number", "Phone number", "Email"])

        self.set_table_with_doctors_data()
        self.set_signals_and_slots()

    def set_signals_and_slots(self):
        """
        Set signals and slots to buttons and headers
        """
        self.ui.menubar.actions()[0].triggered.connect(self.add_new_doctor)
        self.ui.menubar.actions()[1].triggered.connect(self.delete_doctor)
        self.ui.menubar.actions()[2].triggered.connect(self.revert)
        self.ui.menubar.actions()[3].triggered.connect(self.save_changes)
        self.ui.tableWidget.cellClicked.connect(self.cell_clicked)
        header = self.ui.tableWidget.verticalHeader()
        header.sectionClicked.connect(self.header_clicked)

    def cell_clicked(self):
        """
        Set selected_doctor None if user click on cell.
        :return:
        """
        self.__selected_doctor = None

    def header_clicked(self):
        """
        this function set the number of raw which have been clicked and this number is set to __selected_doctor value.
        """
        self.__selected_doctor = self.ui.tableWidget.currentRow()

    @staticmethod
    def reed_information_about_doctor():
        """
        Reed data from a database about doctors.
        :return: cortege rows with data.
        """
        conn = MySQLdb.connect('localhost', 'Valera', '5342395', 'sys')
        cursor = conn.cursor()

        cursor.execute("""SELECT * FROM doctors""")
        data = cursor.fetchall()
        cursor.close()
        return data

    def set_table_with_doctors_data(self):
        row = DoctorWindow.reed_information_about_doctor()

        self.ui.tableWidget.setRowCount(len(row))

        for i in range(len(row)):
            for j in range(5):
                self.ui.tableWidget.setItem(i, j, QTableWidgetItem(str(row[i][j])))

    def get_max_id(self):
        """
        Find max id in table.
        :return: max id in current table.
        """
        list_of_id = []
        for i in range(self.ui.tableWidget.rowCount()):
            list_of_id.append(int(self.ui.tableWidget.item(i, 0).text()))
        return max(list_of_id)

    def add_new_doctor(self):
        """
        Add new doctor.
        """
        max_index = self.get_max_id()
        self.ui.tableWidget.setRowCount(self.ui.tableWidget.rowCount() + 1)
        self.ui.tableWidget.setItem(self.ui.tableWidget.rowCount() - 1, 0,  QTableWidgetItem(str(max_index + 1)))

    def delete_doctor(self):
        """
        Delete selected row.
        """
        if self.__selected_doctor is not None:
            self.ui.tableWidget.removeRow(self.__selected_doctor)

    def revert(self):
        """
        Cancel changes and revert previous data
        """
        self.set_table_with_doctors_data()

    def select_data_from_table(self):
        """
        Select data from doctor's table widget
        :return: return list where each element is list which includes data from row
        """
        data = []
        for i in range(self.ui.tableWidget.rowCount()):
            data.append([])
            for j in range(5):
                cell_data = self.ui.tableWidget.item(i, j).text()
                if (j == 0) or (j == 2):
                    data[i].append(int(cell_data))
                else:
                    data[i].append(cell_data)

        return data

    @staticmethod
    def select_id():
        """
        Select doctor's id from db
        :return: cortege of ids
        """
        conn = MySQLdb.connect('localhost', 'Valera', '5342395', 'sys')
        cursor = conn.cursor()

        cursor.execute("""SELECT ID FROM doctors ORDER BY ID""")
        data = cursor.fetchall()
        cursor.close()

        return data

    @staticmethod
    def update_data(row, data):
        """
        Update data in db b id
        """
        conn = MySQLdb.connect('localhost', 'Valera', '5342395', 'sys')
        cursor = conn.cursor()

        cursor.execute("""UPDATE doctors
        SET `Doctor's name` = %s, `Room number` = %s, Phone = %s, Email = %s
        WHERE id = %s """, (data[row][1], data[row][2], data[row][3], data[row][4], data[row][0]))

        conn.commit()
        cursor.close()

    @staticmethod
    def add_new_data(row, data):
        """
        Add new data to db from doctor's table widget
        """
        conn = MySQLdb.connect('localhost', 'Valera', '5342395', 'sys')
        cursor = conn.cursor()

        cursor.execute("""INSERT INTO doctors
        (ID, `Doctor's name`, `Room number`, Phone, Email)
        VALUES (%s, %s, %s, %s, %s)
        """, (data[row][0], data[row][1], data[row][2], data[row][3], data[row][4]))

        conn.commit()
        cursor.close()

    @staticmethod
    def delete_data(id_row):
        """
        Delete row in db by id
        """
        conn = MySQLdb.connect('localhost', 'Valera', '5342395', 'sys')
        cursor = conn.cursor()
        cursor.execute("""DELETE FROM doctors
        WHERE ID = %s
        """, (id_row,))
        conn.commit()
        cursor.close()

    def save_changes(self):
        """
        Save all changes was done
        """
        selected_id = DoctorWindow.select_id()
        list_of_id_from_db = []
        list_of_id_from_table = []

        for i in range(len(selected_id)):
            list_of_id_from_db.append(selected_id[i][0])

        data_from_table = self.select_data_from_table()
        for i in range(len(data_from_table)):
            list_of_id_from_table.append(data_from_table[i][0])

        for i in range(len(list_of_id_from_table)):
            if data_from_table[i][0] in list_of_id_from_db:
                DoctorWindow.update_data(i, data_from_table)
            else:
                DoctorWindow.add_new_data(i, data_from_table)

        for i in range(len(list_of_id_from_db)):
            if list_of_id_from_db[i] not in list_of_id_from_table:
                DoctorWindow.delete_data(list_of_id_from_db[i])
