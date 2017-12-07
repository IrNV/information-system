import unittest
from test import *


class MyTestCase(unittest.TestCase):
    __app = QtWidgets.QApplication(sys.argv)

    def test_reed_clients_data_from_database(self):
        client_window = ClientWindow()
        data = client_window.reed_information_about_client()
        first_client = (('Ben Josef', '111-11-11', '2017-11-30', '12:00:00',
                        'Richard Black', 101),)
        self.assertTrue(type(data) == tuple)
        self.assertTupleEqual(first_client, data)

if __name__ == '__main__':
    unittest.main()
