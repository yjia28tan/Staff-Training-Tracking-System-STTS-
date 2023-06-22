import typing
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QDialog
from PyQt5.uic import loadUi
import sys
import sqlite3

connect = sqlite3.connect('StaffTrainingSystem')
cursor = connect.cursor()

class Login(QDialog):
    def __init__(self):
        super(Login,self).__init__()
        loadUi("login.ui",self)
        self.loginbutton.clicked.connect(self.loginfunction)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)

    def gotocreate(self):
        createacc = Create()
        widget.addWidget(createacc)
        widget.setCurrentIndex(widget.currentIndex()+1)


    def loginfunction(self):
        email = self.email.text()
        password = self.password.text()
        cursor.execute('SELECT * FROM employee WHERE email=? AND password=?', (email, password))
        if cursor.fetchone():
            print("Success")
            cursor.execute('SELECT departmentID FROM employee WHERE email=? AND password=?', (email, password))
            print(cursor.fetchone())
            cursor.execute('SELECT name FROM employee WHERE email=? AND password=?', (email, password))
            self.usertext.triggered.connect(lambda: self.clicked("New was clicked"))
        else:
            print("Error") 

        print(f"Successfully logged in as email {email} and password as {password}")

class Create(QDialog):
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




app = QApplication(sys.argv)

mainwindow = Login()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedWidth(480)
widget.setFixedHeight(620)
widget.show()
app.exec_()