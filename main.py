import typing
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QDialog
from PyQt5.uic import loadUi
import sys
import sqlite3

connect = sqlite3.connect('StaffTrainingSystem')
cursor = connect.cursor()

class Login(QMainWindow):
    def __init__(self):
        super(Login,self).__init__()
        loadUi("login.ui",self)
        self.login_btn.clicked.connect(self.loginfunction)
        self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)

    def gotocreate(self):
        createacc = Create()
        widget.addWidget(createacc)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def gotoview(self):
        email = self.email_input.text()
        password = self.password_input.text()
        viewtraining = View(email,password)
        widget.addWidget(viewtraining)
        widget.setCurrentIndex(widget.currentIndex()+1)


    def loginfunction(self):
        email = self.email_input.text()
        password = self.password_input.text()
        cursor.execute('SELECT * FROM employee WHERE email=? AND password=?', (email, password))
        if cursor.fetchone():
            print("Success")
            cursor.execute('SELECT departmentID FROM employee WHERE email=? AND password=?', (email, password))
            print(cursor.fetchone()) 
            self.gotoview()
        else:
            print("Error") 

        print(f"Successfully logged in as email {email} and password as {password}")

class Create(QMainWindow):
    def __init__(self):
        super(Create,self).__init__()
        loadUi("createaccount.ui",self)
        self.registerbutton.clicked.connect(self.createaccountfunction)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirmpassword.setEchoMode(QtWidgets.QLineEdit.Password)

    def createaccountfunction(self):
        email = self.email.text()
        password = self.password.text()
        confirmpassword = self.confirmpassword.text()
        if password == confirmpassword:
            print("Account successfully created")
            mainwindow = Login()
            widget.addWidget(mainwindow)
            widget.setCurrentIndex(widget.currentIndex()+1)
        else:
            print("Error. Password different")

class View(QMainWindow):
    def __init__(self,email,password):
        super(View,self).__init__()
        self.email = email
        self.password = password
        loadUi("training_list.ui",self)
        cursor.execute('SELECT name FROM employee WHERE email=? AND password=?', (self.email,self.password))
        self.name_db.setText(cursor.fetchone()[0])
        cursor.execute('SELECT employeeID FROM employee WHERE email=? AND password=?', (self.email,self.password))
        self.id_db.setText(str(cursor.fetchone()[0]))
        cursor.execute('SELECT departmentID FROM employee WHERE email=? AND password=?', (self.email,self.password))
        UserdepartmentID = cursor.fetchone()
        cursor.execute('SELECT departmentName FROM department WHERE departmentID=?', (UserdepartmentID))
        self.department_db.setText(cursor.fetchone()[0])
        self.header.setText("Training List")
        increment = 0
        number = 1
        cursor.execute("SELECT COUNT(*) AS trainingID FROM training")


        for i in range(cursor.fetchone()[0]):
            self.printContainers(increment,number)
            increment = increment + 270
            number = number + 1

    def printContainers(self,increment, number):
            self.training = QtWidgets.QFrame(self.scrollAreaWidgetContents_2)
            new_layout = QtWidgets.QVBoxLayout(self.training)
            self.training.setGeometry(QtCore.QRect(0, 20+increment, 931, 251))
            self.training.setStyleSheet("border: 1px solid white;\nbackground: #8A8A8A;\nborder-radius: 10px;")
            self.training.setFrameShape(QtWidgets.QFrame.StyledPanel)
            self.training.setFrameShadow(QtWidgets.QFrame.Raised)
            self.training.setObjectName(f"training_{number}")
            self.training_image = QtWidgets.QLabel(self.training)
            self.training_image.setGeometry(QtCore.QRect(20, 10+increment, 200, 150))
            self.training_image.setText("")  # here to set the data from database
            self.training_image.setObjectName(f"training_image_{number}")
            new_layout.addWidget(self.training_image)
            self.department_label_2 = QtWidgets.QLabel(self.training)
            self.department_label_2.setGeometry(QtCore.QRect(230, 50+increment, 111, 31))
            font = QtGui.QFont()
            font.setBold(True)
            font.setWeight(75)
            self.department_label_2.setFont(font)
            self.department_label_2.setStyleSheet("color: white;\nfont-weight: bold;\nborder: none;")
            self.department_label_2.setObjectName(f"department_label_{number}")
            new_layout.addWidget(self.department_label_2)
            self.department_db_2 = QtWidgets.QLabel(self.training)
            self.department_db_2.setGeometry(QtCore.QRect(340, 50+increment, 581, 31))
            font = QtGui.QFont()
            font.setPointSize(8)
            font.setBold(False)
            font.setWeight(50)
            self.department_db_2.setFont(font)
            self.department_db_2.setStyleSheet("color: white;\nfont-weight: regular;\nborder: none;\nbold: none;")
            #cursor.execute('SELECT trainingname FROM training WHERE departmentID=?', (UserdepartmentID))
            self.department_db_2.setText("hello")  # here to set the data from database
            self.department_db_2.setObjectName(f"department_db__{number}")
            new_layout.addWidget(self.department_db_2)
            self.description_label = QtWidgets.QLabel(self.training)
            self.description_label.setGeometry(QtCore.QRect(230, 80+increment, 101, 21))
            font = QtGui.QFont()
            font.setBold(True)
            font.setWeight(75)
            self.description_label.setFont(font)
            self.description_label.setStyleSheet("color: white;\nfont-weight: bold;\nborder: none;")
            self.description_label.setObjectName(f"description_label_{number}")
            new_layout.addWidget(self.description_label)
            self.description_db = QtWidgets.QLabel(self.training)
            self.description_db.setGeometry(QtCore.QRect(230, 100+increment, 691, 81))
            self.description_db.setStyleSheet("color: white;\nfont-weight: regular;\nborder: none;")
            cursor.execute('SELECT description FROM training WHERE trainingID=?', str(number))
            self.description_db.setText(str(cursor.fetchone()))  # here to set the data from database
            self.description_db.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
            self.description_db.setWordWrap(True)
            self.description_db.setObjectName(f"description_db_{number}")
            new_layout.addWidget(self.description_db)
            self.view_button = QtWidgets.QPushButton(self.training)
            self.view_button.setGeometry(QtCore.QRect(810, 200+increment, 112, 34))
            self.view_button.setStyleSheet("color: white;\nfont-weight: bold;\nborder-radius: 10px;\nbackground: #008287;")
            self.view_button.setObjectName(f"view_button_{number}")
            new_layout.addWidget(self.view_button)
            self.training_name_db = QtWidgets.QPushButton(self.training)
            self.training_name_db.setGeometry(QtCore.QRect(230, 20+increment, 691, 31))
            font = QtGui.QFont()
            font.setPointSize(12)
            font.setBold(True)
            font.setWeight(75)
            self.training_name_db.setFont(font)
            self.training_name_db.setStyleSheet("color: white;\nfont-weight: bold;\nborder: none;\ntext-align: left;\n")
            self.training_name_db.setText("")  # here to set the data from database
            self.training_name_db.setObjectName(f"training_name_db_{number}")
            new_layout.addWidget(self.training_name_db)
            self.retranslateUi()


    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
      
        self.department_label_2.setText(_translate("MainWindow", "Department: "))
        self.description_label.setText(_translate("MainWindow", "Description: "))
        self.view_button.setText(_translate("MainWindow", "View More"))
       

app = QApplication(sys.argv)

mainwindow = Login()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedWidth(1280)
widget.setFixedHeight(720)
widget.show()
app.exec_()