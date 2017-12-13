import unittest
from doctor_window import *
import sys


class MyTestCase(unittest.TestCase):
    __app = QtWidgets.QApplication(sys.argv)

    def test_create_window(self):
        window = DoctorWindow()
        self.assertEquals(type(window), DoctorWindow)

    def test_reed_data_from_doctors_table(self):
        data = DoctorWindow.reed_information_about_doctor()
        self.assertEquals(type(data), tuple)
        test_data = (1, "Richard Black", 101, "+38901234", "Rich@gmail.com")
        self.assertTupleEqual(test_data, data[0])

    def test_find_max_id_in_table(self):
        window = DoctorWindow()
        max_id = window.get_max_id()
        self.assertEquals(3, max_id)

    def test_select_id_from_db(self):
        selected_id = DoctorWindow.select_id()

        list_of_id_from_db = []
        for i in range(len(selected_id)):
            list_of_id_from_db.append(selected_id[i][0])

        expected_list = [1, 2, 3]
        self.assertListEqual(expected_list, list_of_id_from_db)

    def test_create_update_delete_data(self):
        self.add_new_data()
        self.update_data()
        self.delete_data()

    def add_new_data(self):
        test_data = [[101, "Richard Richmond", 100, "+42123123", "Tom.Rich@gamil.com"]]
        DoctorWindow.add_new_data(0, test_data)

        conn = MySQLdb.connect('localhost', 'Valera', '5342395', 'sys')
        cursor = conn.cursor()

        cursor.execute("""SELECT * FROM doctors WHERE id = 101""")
        data = cursor.fetchall()
        cursor.close()

        list_of_data = []
        for i in range(len(data[0])):
            list_of_data.append(data[0][i])

        self.assertEquals(test_data[0], list_of_data)

    def update_data(self):
        test_data = [[101, "Richard Richmond", 100, "+38123123", "Tom100.Rich@gamil.com"]]
        DoctorWindow.update_data(0, test_data)

        conn = MySQLdb.connect('localhost', 'Valera', '5342395', 'sys')
        cursor = conn.cursor()

        cursor.execute("""SELECT * FROM doctors WHERE id = 101""")
        data = cursor.fetchall()
        cursor.close()

        list_of_data = []
        for i in range(len(data[0])):
            list_of_data.append(data[0][i])

        self.assertEquals(test_data[0], list_of_data)

    def delete_data(self):
        DoctorWindow.delete_data(101)

        conn = MySQLdb.connect('localhost', 'Valera', '5342395', 'sys')
        cursor = conn.cursor()

        cursor.execute("""SELECT * FROM doctors WHERE id = 101""")
        data = cursor.fetchall()
        cursor.close()

        self.assertTupleEqual(data, ())


if __name__ == '__main__':
    unittest.main()
