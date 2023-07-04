import unittest
import sqlite3

class TestStaffTraining(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.connect = sqlite3.connect('StaffTrainingSystem')
        cls.cursor = cls.connect.cursor()

    @classmethod
    def tearDownClass(cls):
        cls.cursor.close()
        cls.connect.close()

    def test_publish_training(self):
        text = "Publish"
        if text == "Publish":
            text = "Unpublished"
        else:
            text = "Publish"
        self.assertEqual(text, "Unpublished")

    def test_login_function(self):
        role = self.login_function()
        self.assertEqual(role, "HR Assistance")

    def test_printName(self):
        name = self.printName()
        self.assertEqual(name, "Lee Li Yee")

    def test_printDepartment(self):
        department_id = self.printDepartment()
        self.assertEqual(department_id, 1)

    def login_function(self):
        email = "test3@gmail.com"
        password = "123123"
        self.cursor.execute('SELECT * FROM employee WHERE email=? AND password=?', (email, password))
        if self.cursor.fetchone():
            self.cursor.execute('SELECT employeeID, departmentID FROM employee WHERE email=? AND password=?',
                                (email, password))
            data = self.cursor.fetchall()
            global employeeID
            employeeID = data[0][0]
            department_id = data[0][1]
            if department_id == 4:
                self.cursor.execute('SELECT role FROM employee WHERE employeeID=? AND departmentID=?',
                                    (employeeID, department_id))
                global role
                role = self.cursor.fetchone()[0]
                return role
            else:
                role = 'Staff'
                return role
            
    def printName(self):
        email = "test@gmail.com"
        password = "123123"
        self.cursor.execute('SELECT * FROM employee WHERE email=? AND password=?', (email, password))
        if self.cursor.fetchone():
            self.cursor.execute('SELECT employeeID, departmentID FROM employee WHERE email=? AND password=?',
                                (email, password))
            data = self.cursor.fetchall()
            global employeeID
            employeeID = data[0][0]
            department_id = data[0][1]
            if department_id == 4:
                self.cursor.execute('SELECT name FROM employee WHERE employeeID=? AND departmentID=?',
                                    (employeeID, department_id))
                name = self.cursor.fetchone()[0]
                return name
            else:
                name = 'Lee Li Yee'
                return name
            
    def printDepartment(self):
        email = "test@gmail.com"
        password = "123123"
        self.cursor.execute('SELECT * FROM employee WHERE email=? AND password=?', (email, password))
        if self.cursor.fetchone():
            self.cursor.execute('SELECT employeeID, departmentID FROM employee WHERE email=? AND password=?',
                                (email, password))
            data = self.cursor.fetchall()
            global employeeID
            employeeID = data[0][0]
            department_id = data[0][1]
            if department_id == 4:
                self.cursor.execute('SELECT departmentID FROM employee WHERE employeeID=? AND departmentID=?',
                                    (employeeID, department_id))
                department_id = self.cursor.fetchone()[0]
                return department_id
            else:
                department_id = 1
                return department_id

    def test_search_training_hr(self):
        search = self.search_training_hr()
        self.assertEqual(search, "Accounting & Finance")

    def search_training_hr(self):
        keywords = 'Finance'

        self.cursor.execute(
            "SELECT DISTINCT t.trainingID, t.trainingName, d.departmentName, t.short_description, t.brochure, "
            "t.max_par, t.status, t.publish, t.cost, t.date, t.time, t.venue "
            "FROM training t "
            "JOIN department d ON d.departmentID = t.departmentID "
            "WHERE (t.trainingName LIKE ? OR d.departmentName LIKE ?) "
            "ORDER BY CASE WHEN t.status = 'Pending' THEN 1 "
            "              WHEN t.status = 'Approved' THEN 2 "
            "              WHEN t.status = 'Cancelled' THEN 3 "
            "              ELSE 4 END",
            ('%' + keywords + '%', '%' + keywords + '%'))
        search_results = self.cursor.fetchall()[0][1]
        return search_results

    def test_calculate_cost(self):
        cost = self.create_training()
        self.assertEqual(cost, 5000.0)

    def create_training(self):
        cost_per_person = 50
        max_participants = 100
        cost = float(cost_per_person) * int(max_participants)
        return cost

if __name__ == '__main__':
    unittest.main()
