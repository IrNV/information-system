import unittest
from main import *
from client_window import *
import datetime


class MyTestCase(unittest.TestCase):
    __app = QtWidgets.QApplication(sys.argv)

    def test_reed_clients_data_from_database(self):
        data = ClientWindow.reed_information_about_client()
        self.assertEquals(type(data), tuple)
        test_data = (4, "Gray Smith", "123-41-98", datetime.date(2017, 12, 14),
                     datetime.timedelta(0, 52200), "Natali Grayson", 105)
        self.assertTupleEqual(test_data, data[0])

    def test_find_max_id_in_table(self):
        window = ClientWindow()
        max_id = window.get_max_id()
        self.assertEquals(4, max_id)

    def test_select_id_from_db(self):
        selected_id = ClientWindow.select_id()

        list_of_id_from_db = []
        for i in range(len(selected_id)):
            list_of_id_from_db.append(selected_id[i][0])

        expected_list = [1, 2, 3, 4]
        self.assertListEqual(expected_list, list_of_id_from_db)

    def test_create_update_delete_data(self):
        self.add_new_data()
        self.update_data()
        self.delete_data()

    def add_new_data(self):
        test_data = [[5, "Gray Lutz", "123-41-98", datetime.date(2017, 12, 14),
                     datetime.timedelta(0, 52200), "Natali Grayson"]]
        ClientWindow.add_new_data(0, test_data)

        conn = MySQLdb.connect('localhost', 'Valera', '5342395', 'sys')
        cursor = conn.cursor()

        cursor.execute("""SELECT * FROM clients WHERE id = 5""")
        data = cursor.fetchall()
        cursor.close()

        list_of_data = []
        for i in range(len(data[0])):
            list_of_data.append(data[0][i])

        self.assertEqual(test_data[0], list_of_data)

    def update_data(self):
        test_data = [[5, "Gray Lutz", "500-41-98", datetime.date(2017, 12, 16),
                     datetime.timedelta(0, 52200), "Natali Grayson"]]
        ClientWindow.update_data(0, test_data)

        conn = MySQLdb.connect('localhost', 'Valera', '5342395', 'sys')
        cursor = conn.cursor()

        cursor.execute("""SELECT * FROM clients WHERE id = 5""")
        data = cursor.fetchall()
        cursor.close()

        list_of_data = []
        for i in range(len(data[0])):
            list_of_data.append(data[0][i])

        self.assertEquals(test_data[0], list_of_data)

    def delete_data(self):
        ClientWindow.delete_data(5)

        conn = MySQLdb.connect('localhost', 'Valera', '5342395', 'sys')
        cursor = conn.cursor()

        cursor.execute("""SELECT * FROM doctors WHERE id = 5""")
        data = cursor.fetchall()
        cursor.close()

        self.assertTupleEqual(data, ())

if __name__ == '__main__':
    unittest.main()
