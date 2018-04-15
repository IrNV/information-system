import MySQLdb


class DataBaseMySQL:

    def __init__(self):
        self.connect = MySQLdb.connect('localhost', 'user', 'password', 'db')

    def reed_information_about_client(self):
        """
        Reed data from a database about clients.
        :return: cortege rows with data.
        """
        conn = self.connect
        cursor = conn.cursor()

        cursor.execute("""SELECT c.ID, c.`Name and Surname`, c.`Phone`, c.`Date`, c.`Time`, c.`Doctor's name`, d.`room number`
             FROM clients c INNER JOIN doctors d
             ON c.`Doctor's name` = d.`Doctor's name`
             WHERE ((Date > CURRENT_DATE()) or (Date = current_date()) and (Time > current_time()))
             """)
        data = cursor.fetchall()
        cursor.close()
        return data

    def select_doctors(self):
        """
        Reed data from a database about doctors.
        :return: cortege rows with data.
        """
        conn = self.connect
        cursor = conn.cursor()

        cursor.execute("""SELECT  * FROM doctors """)
        data = cursor.fetchall()
        cursor.close()
        return data

    def select_id(self):
        """
        Select client's id from db
        :return: cortege of ids
        """
        conn = self.connect
        cursor = conn.cursor()

        cursor.execute("""SELECT ID FROM clients ORDER BY ID""")
        data = cursor.fetchall()
        cursor.close()

        return data

    def update_data(self, row, data):
        """
        Update data in db by id
        """
        conn = self.connect
        cursor = conn.cursor()

        cursor.execute("""UPDATE clients
            SET `Name and Surname` = %s, `Phone` = %s, `Date` = %s, `Time` = %s, `Doctor's name` = %s
            WHERE ID = %s """, (data[row][1], data[row][2], data[row][3], data[row][4], data[row][5], data[row][0]))

        conn.commit()
        cursor.close()

    def add_new_data(self, row, data):
        """
        Add new data to db from client's table widget
        """
        conn = self.connect
        cursor = conn.cursor()

        cursor.execute("""INSERT INTO clients
            (ID, `Name and Surname`, `Phone`, `Date`, `Time`, `Doctor's name`)
            VALUES (%s, %s, %s, %s, %s, %s)
            """, (data[row][0], data[row][1], data[row][2], data[row][3], data[row][4], data[row][5]))

        conn.commit()
        cursor.close()

    def delete_data(self, id_row):
        """
        Delete row in db by id
        """
        conn = self.connect
        cursor = conn.cursor()
        cursor.execute("""DELETE FROM clients
            WHERE ID = %s
            """, (id_row,))
        conn.commit()
        cursor.close()

    def select_archive_data(self, parameter_order="ID"):
        """
        Select data about client from db
        :param parameter_order:  data will be sorted by this parameter
        :return:
        """

        conn = self.connect
        cursor = conn.cursor()
        cursor.execute("""SELECT c.ID, c.`Name and Surname`, c.`Phone`, c.`Date`, c.`Time`, c.`Doctor's name`, d.`room number`
        FROM clients c INNER JOIN doctors d
        ON c.`Doctor's name` = d.`Doctor's name`
        WHERE ((Date < CURRENT_DATE()) or (Date = current_date()) and (Time < current_time()))
        ORDER BY %s""" % parameter_order)
        data = cursor.fetchall()
        cursor.close()

        return data

    def reed_information_about_doctor(self):
        """
        Reed data from a database about doctors.
        :return: cortege rows with data.
        """
        conn = self.connect
        cursor = conn.cursor()

        cursor.execute("""SELECT * FROM doctors""")
        data = cursor.fetchall()
        cursor.close()
        return data

    def select_doctors_id(self):
        """
        Select doctor's id from db
        :return: cortege of ids
        """
        conn = self.connect
        cursor = conn.cursor()

        cursor.execute("""SELECT ID FROM doctors ORDER BY ID""")
        data = cursor.fetchall()
        cursor.close()

        return data

    def update_doctor_data(self, row, data):
        """
        Update data in db b id
        """
        conn = self.connect
        cursor = conn.cursor()

        cursor.execute("""UPDATE doctors
        SET `Doctor's name` = %s, `Room number` = %s, Phone = %s, Email = %s
        WHERE id = %s """, (data[row][1], data[row][2], data[row][3], data[row][4], data[row][0]))

        conn.commit()
        cursor.close()

    def add_new_doctor_data(self, row, data):
        """
        Add new data to db from doctor's table widget
        """
        conn = self.connect
        cursor = conn.cursor()

        cursor.execute("""INSERT INTO doctors
        (ID, `Doctor's name`, `Room number`, Phone, Email)
        VALUES (%s, %s, %s, %s, %s)
        """, (data[row][0], data[row][1], data[row][2], data[row][3], data[row][4]))

        conn.commit()
        cursor.close()

    def delete_doctor_data(self, id_row):
        """
        Delete row in db by id
        """
        conn = self.connect
        cursor = conn.cursor()
        cursor.execute("""DELETE FROM doctors
        WHERE ID = %s
        """, (id_row,))
        conn.commit()
        cursor.close()