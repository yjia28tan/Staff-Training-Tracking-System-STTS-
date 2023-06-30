from datetime import datetime
from tkinter import messagebox
import logging
import typing
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QDialog
from PyQt5.uic import loadUi
import sys
import sqlite3
from PIL import Image
from io import BytesIO
import logging
from PyQt5 import Qt, uic
from PyQt5.QtCore import QSize, QRect, QMetaObject, QCoreApplication, Qt
from PyQt5.QtGui import QPixmap, QIcon, QFont
from PyQt5.QtWidgets import QApplication, QWidget, QFrame, QHBoxLayout, QSizePolicy, QPushButton, QLabel, QScrollArea, QLineEdit, QMessageBox, QMainWindow
from PyQt5.uic import loadUi
import sys
import sqlite3
from PyQt5 import QtWidgets


connect = sqlite3.connect('StaffTrainingSystem')
cursor = connect.cursor()
global employeeID

def connectDatabase():
        try:
            global connect
            global cursor
            # connect to database
            connect = sqlite3.connect("StaffTrainingSystem")
            cursor = connect.cursor()
        except ConnectionError:
            # Show error message box
            messagebox.critical(None, "Error", "Cannot connect to database!", QMessageBox.Ok)

class ClickableGraphicsView(QtWidgets.QGraphicsView):
    def __init__(self, parent=None):
        super(ClickableGraphicsView, self).__init__(parent)
        self.clicked = False
        self.zoomed_in = False

        self.setRenderHint(QtGui.QPainter.Antialiasing)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setResizeAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.clicked = True

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton and self.clicked:
            self.clicked = False
            self.toggleZoom()

    def toggleZoom(self):
        if self.zoomed_in:
            self.resetTransform()
            self.zoomed_in = False
        else:
            self.scale(2, 2)
            self.zoomed_in = True

class ImagePopup(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(ImagePopup, self).__init__(parent)

        self.view = ClickableGraphicsView()
        self.scene = QtWidgets.QGraphicsScene()
        self.view.setScene(self.scene)

        self.setCentralWidget(self.view)

        # Set window size to match screen size
        screen = QtWidgets.QApplication.instance().primaryScreen()
        screen_rect = screen.availableGeometry()
        self.resize(screen_rect.width(), screen_rect.height())

    def setImage(self, image):
        self.scene.clear()
        self.image_item = QtWidgets.QGraphicsPixmapItem(image)
        self.scene.addItem(self.image_item)
        self.view.fitInView(self.image_item, QtCore.Qt.KeepAspectRatio)

class Login(QMainWindow):
    def __init__(self):
        super(Login,self).__init__()
        loadUi("login.ui",self)
        self.login_btn.clicked.connect(self.loginfunction)
        self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)


    def loginfunction(self):
        email = self.email_input.text()
        password = self.password_input.text()
        cursor.execute('SELECT * FROM employee WHERE email=? AND password=?', (email, password))
        if cursor.fetchone():
            print("Success")
            cursor.execute('SELECT employeeID, departmentID FROM employee WHERE email=? AND password=?', (email, password))
            data = cursor.fetchall()
            global employeeID
            employeeID = data[0][0]
            departmentID = data[0][1]
            if departmentID == 4:
                gotoHrView()
            else: 
                gotoview()
        else:
            print("Error") 

        print(f"Successfully logged in as email {email} and password as {password}")

class HrView(QMainWindow):
    def __init__(self):
        super(HrView, self).__init__()
        loadUi("hr_training_list(no_box_template).ui", self)

        # Define the size and position of each frame
        frame_width = 931
        frame_height = 251
        frame_spacing = 20

        # self.profile_button.clicked.connect()
        self.name_db.setText("")
        self.id_db.setText("")
        self.department_db.setText("")
        # Connect the button's clicked signal to the reset function
        self.list_button.clicked.connect(self.reset)
        # self.logout_button.clicked.connect()
        
        cursor.execute('SELECT name, employeeID, departmentID FROM employee WHERE employeeID = ?', (employeeID, )) 
        display = cursor.fetchall()
        self.employeeID = display[0][1]
        self.name_db.setText(display[0][0])  
        self.id_db.setText(str(display[0][1]))
        cursor.execute('SELECT departmentName FROM department WHERE departmentID=?', (display[0][2],))
        self.department_db.setText(cursor.fetchone()[0])
        self.profile_button.setIcon(QtGui.QIcon("pictures/profile.png"))
        self.profile_button.clicked.connect(self.gotoProfile)
        self.logout_button.setIcon(QtGui.QIcon("pictures/logout.png"))
        self.logout_button.clicked.connect(gotologin)

        self.header.setText("Training Lists")

        self.create_button.clicked.connect(self.create_new_training)

        self.search_button.clicked.connect(self.search_training_hr)

        connectDatabase()
        self.cursor = connect.cursor()
        self.cursor.execute(
            "SELECT t.trainingID, t.trainingName, d.departmentName, t.short_description, t.brochure, t.max_par, "
            "t.status, t.publish, " 
            "CASE WHEN t.date >= DATE('now') THEN t.date ELSE NULL END AS happening_soon_date "
            "FROM training t "
            "JOIN department d ON d.departmentID = t.departmentID "
            "ORDER BY happening_soon_date DESC, t.status")
        row_data = self.cursor.fetchall()
        rows = len(row_data)

        self.app_status = "approved"

        for item in range(rows):
            training_id = row_data[item][0]
            self.cursor.execute("SELECT COUNT(a.applicationID) "
                                "FROM application a "
                                "JOIN training t ON t.trainingID = a.trainingID "
                                "WHERE t.trainingID = ? AND a.applicationStatus = ?",
                                (training_id, self.app_status,))
            application_count = str(self.cursor.fetchone()[0])

            self.training = QFrame(self.scrollAreaWidgetContents_2)
            self.training.setObjectName(u"training")
            self.training.setGeometry(QRect(0, 50 + (item * (frame_height + frame_spacing)), frame_width, frame_height))
            self.training.setStyleSheet(u"border: 1px solid white;\n"
                                        "background: #8A8A8A;\n"
                                        "border-radius: 10px;")
            self.training.setFrameShape(QFrame.StyledPanel)
            self.training.setFrameShadow(QFrame.Raised)

            blob_data = row_data[item][4]

            image = Image.open(BytesIO(blob_data))
            image.save(f"pictures/image{item}.png", "PNG")

            self.training_image = QLabel(self.training)

            self.training_image.setGeometry(QtCore.QRect(20, 10, 200, 150))
            self.training_image.setScaledContents(True)
            self.training_image.setPixmap(QtGui.QPixmap(f"pictures/image{item}.png"))  # here to set the data from database
            self.training_image.setObjectName(f"training_image_{item}")

            self.department_label = QLabel(self.training)
            self.department_label.setObjectName(u"department_label")
            self.department_label.setGeometry(QRect(230, 50, 111, 31))
            font = QFont()
            font.setBold(True)
            font.setWeight(75)
            self.department_label.setFont(font)
            self.department_label.setStyleSheet(u"color: white;\n"
                                                "font-weight: bold;\n"
                                                "border: none;")
            self.department_label.setText("Department: ")

            self.department_db = QLabel(self.training)
            self.department_db.setObjectName(u"department_db")
            self.department_db.setGeometry(QRect(340, 50, 581, 31))
            font1 = QFont()
            font1.setPointSize(8)
            font1.setBold(False)
            font1.setWeight(50)
            self.department_db.setFont(font1)
            self.department_db.setStyleSheet(u"color: white;\n"
                                             "font-weight: regular;\n"
                                             "border: none;\n"
                                             "bold: none;")
            self.department_db.setText(f"{row_data[item][2]}")

            self.description_label = QLabel(self.training)
            self.description_label.setObjectName(u"description_label")
            self.description_label.setGeometry(QRect(230, 80, 101, 21))
            self.description_label.setFont(font)
            self.description_label.setStyleSheet(u"color: white;\n"
                                                 "font-weight: bold;\n"
                                                 "border: none;")
            self.description_label.setText("Description: ")

            self.description_db = QLabel(self.training)
            self.description_db.setObjectName(u"description_db")
            self.description_db.setGeometry(QRect(230, 100, 691, 81))
            self.description_db.setStyleSheet(u"color: white;\n"
                                              "font-weight: regular;\n"
                                              "border: none;")
            self.description_db.setAlignment(Qt.AlignLeft | Qt.AlignTop)
            self.description_db.setWordWrap(True)
            self.description_db.setText(f"{row_data[item][3]}")

            self.training_name_db = QLabel(self.training)
            self.training_name_db.setObjectName(u"training_name_db")
            self.training_name_db.setGeometry(QRect(230, 20, 691, 31))
            font2 = QFont()
            font2.setPointSize(12)
            font2.setBold(True)
            font2.setWeight(75)
            self.training_name_db.setFont(font2)
            self.training_name_db.setStyleSheet(u"color: white;\n"
                                                "font-weight: bold;\n"
                                                "border: none;\n"
                                                "text-align: left;\n")
            self.training_name_db.setText(f"{row_data[item][1]}")

            self.participant_label = QLabel(self.training)
            self.participant_label.setObjectName(u"participant_label")
            self.participant_label.setGeometry(QRect(20, 170, 101, 31))
            self.participant_label.setFont(font)
            self.participant_label.setStyleSheet(u"color: white;\n"
                                                 "font-weight: bold;\n"
                                                 "border: none;")
            self.participant_label.setText("Participant:")

            self.status_label = QLabel(self.training)
            self.status_label.setObjectName(u"status_label")
            self.status_label.setGeometry(QRect(20, 200, 61, 31))
            self.status_label.setFont(font)
            self.status_label.setStyleSheet(u"color: white;\n"
                                            "font-weight: bold;\n"
                                            "border: none;")
            self.status_label.setText("Status:")

            self.status_db = QLabel(self.training)
            self.status_db.setObjectName(u"status_db")
            self.status_db.setGeometry(QRect(90, 200, 71, 31))
            self.status_db.setFont(font1)

            if row_data[item][6] == "Approved":
                self.status_db.setStyleSheet(u"color: lightgreen;\n"
                                             "font-weight: bold;\n"
                                             "border: none;\n")

                self.publish_button = QPushButton(self.training)
                self.publish_button.setObjectName(u"publish_button")
                self.publish_button.setGeometry(QRect(810, 200, 112, 34))
                self.publish_button.setStyleSheet(u"color: white;\n"
                                                  "font-weight: bold;\n"
                                                  "border-radius: 10px;\n"
                                                  "background: #008287;\n")
                self.publish_button.setProperty("trainingID", training_id)
                self.publish_button.clicked.connect(lambda _, publish_btn=self.publish_button:
                                                    self.publish_training(publish_btn))

                self.modify_button = QPushButton(self.training)
                self.modify_button.setObjectName(u"modify_button")
                self.modify_button.setGeometry(QRect(570, 200, 112, 34))
                self.modify_button.setStyleSheet(u"color: white;\n"
                                                 u"font-weight: bold;\n"
                                                 u"border-radius: 10px;\n"
                                                 u"background: #008287;\n")
                self.modify_button.setText("Modify")
                self.modify_button.clicked.connect(lambda _, trainingid=training_id: self.modify_training(trainingid))

                self.view_more_button = QPushButton(self.training)
                self.view_more_button.setObjectName(u"view_more_button")
                self.view_more_button.setGeometry(QRect(690, 200, 112, 34))
                self.view_more_button.setStyleSheet(u"color: white;\n"
                                                    u"font-weight: bold;\n"
                                                    u"border-radius: 10px;\n"
                                                    u"background: #008287;\n")
                self.view_more_button.setText("View more")
                self.view_more_button.clicked.connect(lambda _, trainingid=training_id: self.view_training(trainingid))

            elif row_data[item][6] == "Cancelled":
                self.status_db.setStyleSheet(u"color: #FE8886;\n"
                                             "font-weight: bold;\n"
                                             "border: none;\n")

                self.publish_button = QPushButton(self.training)
                self.publish_button.setObjectName(u"publish_button")
                self.publish_button.setGeometry(QRect(810, 200, 112, 34))
                self.publish_button.setStyleSheet(u"color: white;\n"
                                                  "font-weight: bold;\n"
                                                  "border-radius: 10px;\n"
                                                  "background: #008287;\n")
                self.publish_button.setProperty("trainingID", training_id)
                self.publish_button.clicked.connect(lambda _, publish_btn=self.publish_button:
                                                    self.publish_training(publish_btn))

                self.view_more_button = QPushButton(self.training)
                self.view_more_button.setObjectName(u"view_more_button")
                self.view_more_button.setGeometry(QRect(690, 200, 112, 34))
                self.view_more_button.setStyleSheet(u"color: white;\n"
                                                    u"font-weight: bold;\n"
                                                    u"border-radius: 10px;\n"
                                                    u"background: #008287;\n")
                self.view_more_button.setText("View More")
                self.view_more_button.clicked.connect(lambda _, trainingid=training_id: self.view_training(trainingid))

            elif row_data[item][6] == "Pending":
                self.status_db.setStyleSheet(u"color: #FFAE42;\n"
                                             "font-weight: bold;\n"
                                             "border: none;\n")

                self.publish_button = QPushButton(self.training)
                self.publish_button.setObjectName(u"publish_button")
                self.publish_button.setGeometry(QRect(810, 200, 112, 34))
                self.publish_button.setStyleSheet(u"color: white;\n"
                                                  "font-weight: bold;\n"
                                                  "border-radius: 10px;\n"
                                                  "background: #008287;\n")
                self.publish_button.setProperty("trainingID", training_id)
                self.publish_button.clicked.connect(lambda _, publish_btn=self.publish_button:
                                                    self.publish_training(publish_btn))

                self.modify_button = QPushButton(self.training)
                self.modify_button.setObjectName(u"modify_button")
                self.modify_button.setGeometry(QRect(690, 200, 112, 34))
                self.modify_button.setStyleSheet(u"color: white;\n"
                                                 "font-weight: bold;\n"
                                                 "border-radius: 10px;\n"
                                                 "background: #008287;\n")
                self.modify_button.setText("Modify")
                self.modify_button.clicked.connect(lambda _, trainingid=training_id: self.modify_training(trainingid))

                self.approval_button = QPushButton(self.training)
                self.approval_button.setObjectName(u"approval_button")
                self.approval_button.setGeometry(QRect(570, 200, 112, 34))
                self.approval_button.setStyleSheet(u"color: white;\n"
                                                   "font-weight: bold;\n"
                                                   "border-radius: 10px;\n"
                                                   "background: #008287;\n")
                self.approval_button.setText("Approval")
                self.approval_button.clicked.connect(lambda _, trainingid=training_id:
                                                     self.approve_training(trainingid))

            else:  # past training
                self.status_db.setStyleSheet(u"color: #EABFFF;\n"
                                             "font-weight: bold;\n"
                                             "border: none;\n")

                self.publish_button = QPushButton(self.training)
                self.publish_button.setObjectName(u"publish_button")
                self.publish_button.setGeometry(QRect(810, 200, 112, 34))
                self.publish_button.setStyleSheet(u"color: white;\n"
                                                  "font-weight: bold;\n"
                                                  "border-radius: 10px;\n"
                                                  "background: #008287;\n")
                self.publish_button.setProperty("trainingID", training_id)
                self.publish_button.clicked.connect(lambda _, publish_btn=self.publish_button:
                                                    self.publish_training(publish_btn))

                self.view_more_button = QPushButton(self.training)
                self.view_more_button.setObjectName(u"view_more_button")
                self.view_more_button.setGeometry(QRect(690, 200, 112, 34))
                self.view_more_button.setStyleSheet(u"color: white;\n"
                                                    u"font-weight: bold;\n"
                                                    u"border-radius: 10px;\n"
                                                    u"background: #008287;\n")
                self.view_more_button.setText("View More")
                self.view_more_button.clicked.connect(lambda _, trainingid=training_id: self.view_training(trainingid))

            self.status_db.setText(f"{row_data[item][6]}")
            publish = row_data[item][7]
            if publish == 1:
                self.publish_button.setText("Unpublished")
            else:
                self.publish_button.setText("Publish")

            self.participant_db = QLabel(self.training)
            self.participant_db.setObjectName(u"participant_db")
            self.participant_db.setGeometry(QRect(130, 170, 91, 31))
            self.participant_db.setFont(font1)
            self.participant_db.setStyleSheet(u"color: white;\n"
                                              "font-weight: regular;\n"
                                              "border: none;\n"
                                              "bold: none;")
            self.participant_db.setText(f"{application_count}"" / " f"{row_data[item][5]}")

        # Adjust the size of the scroll area's contents
        self.scrollAreaWidgetContents_2.setMinimumHeight(50 + rows * (frame_height + frame_spacing))

    def search_training_hr(self):
        try:
            keywords = self.search_bar.text()

            # Query the database based on the keywords and date range
            connectDatabase()
            self.cursor.execute(
                "SELECT DISTINCT t.trainingID, t.trainingName, d.departmentName, t.short_description, t.brochure, "
                "t.max_par, t.status, t.publish "
                "FROM training t "
                "JOIN department d ON d.departmentID = t.departmentID "
                "WHERE (t.trainingName LIKE ? OR d.departmentName LIKE ?) "
                "ORDER BY CASE WHEN t.status = 'Pending' THEN 1 "
                "              WHEN t.status = 'Approved' THEN 2 "
                "              WHEN t.status = 'Cancelled' THEN 3 "
                "              ELSE 4 END",
                ('%' + keywords + '%', '%' + keywords + '%'))
            search_results = self.cursor.fetchall()
            print(search_results)

            # Display the search results
            self.update_search_results(search_results)
            self.search_bar.setText("")
            self.search_bar.setPlaceholderText("  Search...")

        except Exception as e:
            # Show error message box or print the error
            error_message = "An error occurred: " + str(e)
            QMessageBox.critical(self, "Error", error_message, QMessageBox.Ok)

    def update_search_results(self, search_results):
        # self.items = search_results
        n = len(search_results)
        # Define the size and position of each frame
        frame_width = 931
        frame_height = 251
        frame_spacing = 20

        # Clear the existing contents of the scroll area
        for frame in self.scrollAreaWidgetContents_2.findChildren(QtWidgets.QFrame):
            # Remove child widgets from the frame
            for child_widget in frame.children():
                child_widget.deleteLater()
            # Remove the frame itself
            frame.deleteLater()

        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 50, frame_width,
                                                                 n * (frame_height + frame_spacing)))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")

        self.create_button = QPushButton(self.scrollAreaWidgetContents_2)
        self.create_button.setObjectName(u"create_button")
        self.create_button.setGeometry(QRect(808, 3, 121, 41))
        font1 = QFont()
        font1.setPointSize(9)
        font1.setBold(True)
        font1.setWeight(75)
        self.create_button.setFont(font1)
        self.create_button.setStyleSheet(u"color: white;\n"
                                         "font-weight: bold;\n"
                                         "border: 1px solid white;\n"
                                         "border-radius: 10px;")
        icon2 = QIcon()
        icon2.addFile(u"create.png", QSize(), QIcon.Normal, QIcon.Off)
        self.create_button.setIcon(icon2)
        self.create_button.setIconSize(QSize(30, 36))
        self.create_button.setCheckable(False)
        self.create_button.setText("Create")
        self.create_button.clicked.connect(self.create_new_training)

        for item in range(n):
            training_id = search_results[item][0]
            self.cursor.execute("SELECT COUNT(a.applicationID) "
                                "FROM application a "
                                "JOIN training t ON t.trainingID = a.trainingID "
                                "WHERE t.trainingID = ? AND a.applicationStatus = ?",
                                (training_id, self.app_status,))
            application_count = str(self.cursor.fetchone()[0])

            self.training = QFrame(self.scrollAreaWidgetContents_2)
            self.training.setObjectName(u"training")
            self.training.setGeometry(QRect(0, 50 + (item * (frame_height + frame_spacing)), frame_width, frame_height))
            self.training.setStyleSheet(u"border: 1px solid white;\n"
                                        "background: #8A8A8A;\n"
                                        "border-radius: 10px;")
            self.training.setFrameShape(QFrame.StyledPanel)
            self.training.setFrameShadow(QFrame.Raised)

            blob_data = search_results[item][4]

            image = Image.open(BytesIO(blob_data))
            image.save(f"pictures/image{item}.png", "PNG")

            self.training_image = QLabel(self.training)

            self.training_image.setGeometry(QtCore.QRect(20, 10, 200, 150))
            self.training_image.setScaledContents(True)
            self.training_image.setPixmap(QtGui.QPixmap(f"pictures/image{item}.png"))  # here to set the data from database
            self.training_image.setObjectName(f"training_image_{item}")


            self.department_label = QLabel(self.training)
            self.department_label.setObjectName(u"department_label")
            self.department_label.setGeometry(QRect(230, 50, 111, 31))
            font = QFont()
            font.setBold(True)
            font.setWeight(75)
            self.department_label.setFont(font)
            self.department_label.setStyleSheet(u"color: white;\n"
                                                "font-weight: bold;\n"
                                                "border: none;")
            self.department_label.setText("Department: ")

            self.department_db = QLabel(self.training)
            self.department_db.setObjectName(u"department_db")
            self.department_db.setGeometry(QRect(340, 50, 581, 31))
            font1 = QFont()
            font1.setPointSize(8)
            font1.setBold(False)
            font1.setWeight(50)
            self.department_db.setFont(font1)
            self.department_db.setStyleSheet(u"color: white;\n"
                                             "font-weight: regular;\n"
                                             "border: none;\n"
                                             "bold: none;")
            self.department_db.setText(f"{search_results[item][2]}")

            self.description_label = QLabel(self.training)
            self.description_label.setObjectName(u"description_label")
            self.description_label.setGeometry(QRect(230, 80, 101, 21))
            self.description_label.setFont(font)
            self.description_label.setStyleSheet(u"color: white;\n"
                                                 "font-weight: bold;\n"
                                                 "border: none;")
            self.description_label.setText("Description: ")

            self.description_db = QLineEdit(self.training)
            self.description_db.setObjectName(u"description_db")
            self.description_db.setGeometry(QRect(230, 100, 691, 81))
            self.description_db.setStyleSheet(u"color: white;\n"
                                              "font-weight: regular;\n"
                                              "border: none;")
            self.description_db.setAlignment(Qt.AlignLeft | Qt.AlignTop)

            self.description_db.setText(f"{search_results[item][3]}")

            self.training_name_db = QLabel(self.training)
            self.training_name_db.setObjectName(u"training_name_db")
            self.training_name_db.setGeometry(QRect(230, 20, 691, 31))
            font2 = QFont()
            font2.setPointSize(12)
            font2.setBold(True)
            font2.setWeight(75)
            self.training_name_db.setFont(font2)
            self.training_name_db.setStyleSheet(u"color: white;\n"
                                                "font-weight: bold;\n"
                                                "border: none;\n"
                                                "text-align: left;\n")
            self.training_name_db.setText(f"{search_results[item][1]}")

            self.participant_label = QLabel(self.training)
            self.participant_label.setObjectName(u"participant_label")
            self.participant_label.setGeometry(QRect(20, 170, 101, 31))
            self.participant_label.setFont(font)
            self.participant_label.setStyleSheet(u"color: white;\n"
                                                 "font-weight: bold;\n"
                                                 "border: none;")
            self.participant_label.setText("Participant:")

            self.status_label = QLabel(self.training)
            self.status_label.setObjectName(u"status_label")
            self.status_label.setGeometry(QRect(20, 200, 61, 31))
            self.status_label.setFont(font)
            self.status_label.setStyleSheet(u"color: white;\n"
                                            "font-weight: bold;\n"
                                            "border: none;")
            self.status_label.setText("Status:")

            self.status_db = QLabel(self.training)
            self.status_db.setObjectName(u"status_db")
            self.status_db.setGeometry(QRect(90, 200, 71, 31))
            self.status_db.setFont(font1)

            self.modify_button = QPushButton(self.training)
            self.modify_button.setObjectName(u"modify_button")
            self.modify_button.setGeometry(QRect(810, 200, 112, 34))
            self.modify_button.setStyleSheet(u"color: white;\n"
                                                "font-weight: bold;\n"
                                                "border-radius: 10px;\n"
                                                "background: #008287;\n")
            self.modify_button.setProperty("trainingID", training_id)
            self.modify_button.clicked.connect(lambda _, trainingid=training_id: self.modify_training(trainingid))

            self.approval_button.setText("Approval")

            if search_results[item][6] == "Approved":
                self.status_db.setStyleSheet(u"color: lightgreen;\n"
                                             "font-weight: bold;\n"
                                             "border: none;\n")

                self.publish_button = QPushButton(self.training)
                self.publish_button.setObjectName(u"publish_button")
                self.publish_button.setGeometry(QRect(810, 200, 112, 34))
                self.publish_button.setStyleSheet(u"color: white;\n"
                                                  "font-weight: bold;\n"
                                                  "border-radius: 10px;\n"
                                                  "background: #008287;\n")
                self.publish_button.setProperty("trainingID", training_id)
                self.publish_button.clicked.connect(lambda _, publish_btn=self.publish_button:
                                                    self.publish_training(publish_btn))

                self.modify_button = QPushButton(self.training)
                self.modify_button.setObjectName(u"modify_button")
                self.modify_button.setGeometry(QRect(570, 200, 112, 34))
                self.modify_button.setStyleSheet(u"color: white;\n"
                                                 u"font-weight: bold;\n"
                                                 u"border-radius: 10px;\n"
                                                 u"background: #008287;\n")
                self.modify_button.setText("Modify")
                self.modify_button.clicked.connect(lambda _, trainingid=training_id: self.modify_training(trainingid))

                self.view_more_button = QPushButton(self.training)
                self.view_more_button.setObjectName(u"view_more_button")
                self.view_more_button.setGeometry(QRect(690, 200, 112, 34))
                self.view_more_button.setStyleSheet(u"color: white;\n"
                                                    u"font-weight: bold;\n"
                                                    u"border-radius: 10px;\n"
                                                    u"background: #008287;\n")
                self.view_more_button.setText("Modify")
                self.view_more_button.clicked.connect(lambda _, trainingid=training_id: self.view_training(trainingid))
                self.modify_button.clicked.connect(lambda _, trainingid=training_id: self.modify_training(trainingid))

            elif search_results[item][6] == "Cancelled":
                self.status_db.setStyleSheet(u"color: #FE8886;\n"
                                             "font-weight: bold;\n"
                                             "border: none;\n")

                self.publish_button = QPushButton(self.training)
                self.publish_button.setObjectName(u"publish_button")
                self.publish_button.setGeometry(QRect(810, 200, 112, 34))
                self.publish_button.setStyleSheet(u"color: white;\n"
                                                  "font-weight: bold;\n"
                                                  "border-radius: 10px;\n"
                                                  "background: #008287;\n")
                self.publish_button.setProperty("trainingID", training_id)
                self.publish_button.clicked.connect(
                    lambda _, publish_btn=self.publish_button: self.publish_training(publish_btn))

                self.view_more_button = QPushButton(self.training)
                self.view_more_button.setObjectName(u"view_more_button")
                self.view_more_button.setGeometry(QRect(690, 200, 112, 34))
                self.view_more_button.setStyleSheet(u"color: white;\n"
                                                    u"font-weight: bold;\n"
                                                    u"border-radius: 10px;\n"
                                                    u"background: #008287;\n")
                self.view_more_button.setText("View More")
                self.view_more_button.clicked.connect(lambda _, trainingid=training_id: self.view_training(trainingid))
                self.modify_button.clicked.connect(lambda _, trainingid=training_id: self.modify_training(trainingid))

            elif search_results[item][6] == "Pending":
                self.status_db.setStyleSheet(u"color: #FFAE42;\n"
                                             "font-weight: bold;\n"
                                             "border: none;\n")

                self.publish_button = QPushButton(self.training)
                self.publish_button.setObjectName(u"publish_button")
                self.publish_button.setGeometry(QRect(810, 200, 112, 34))
                self.publish_button.setStyleSheet(u"color: white;\n"
                                                  "font-weight: bold;\n"
                                                  "border-radius: 10px;\n"
                                                  "background: #008287;\n")
                self.publish_button.setProperty("trainingID", training_id)
                self.publish_button.clicked.connect(lambda _, publish_btn=self.publish_button:
                                                    self.publish_training(publish_btn))

                self.modify_button = QPushButton(self.training)
                self.modify_button.setObjectName(u"modify_button")
                self.modify_button.setGeometry(QRect(690, 200, 112, 34))
                self.modify_button.setStyleSheet(u"color: white;\n"
                                                 "font-weight: bold;\n"
                                                 "border-radius: 10px;\n"
                                                 "background: #008287;\n")
                self.modify_button.setText("Modify")
                self.modify_button.clicked.connect(lambda _, trainingid=training_id: self.modify_training(trainingid))

                self.approval_button = QPushButton(self.training)
                self.approval_button.setObjectName(u"approval_button")
                self.approval_button.setGeometry(QRect(570, 200, 112, 34))
                self.approval_button.setStyleSheet(u"color: white;\n"
                                                   "font-weight: bold;\n"
                                                   "border-radius: 10px;\n"
                                                   "background: #008287;\n")
                self.approval_button.setText("Approval")
                self.approval_button.clicked.connect(lambda _, trainingid=training_id:
                                                     self.approve_training(trainingid))
                self.modify_button.clicked.connect(lambda _, trainingid=training_id: self.modify_training(trainingid))

            else:  # past training
                self.status_db.setStyleSheet(u"color: #EABFFF;\n"
                                             "font-weight: bold;\n"
                                             "border: none;\n")

                self.publish_button = QPushButton(self.training)
                self.publish_button.setObjectName(u"publish_button")
                self.publish_button.setGeometry(QRect(810, 200, 112, 34))
                self.publish_button.setStyleSheet(u"color: white;\n"
                                                  "font-weight: bold;\n"
                                                  "border-radius: 10px;\n"
                                                  "background: #008287;\n")
                self.publish_button.setProperty("trainingID", training_id)
                self.publish_button.clicked.connect(lambda _, publish_btn=self.publish_button:
                                                    self.publish_training(publish_btn))

                self.view_more_button = QPushButton(self.training)
                self.view_more_button.setObjectName(u"view_more_button")
                self.view_more_button.setGeometry(QRect(690, 200, 112, 34))
                self.view_more_button.setStyleSheet(u"color: white;\n"
                                                    u"font-weight: bold;\n"
                                                    u"border-radius: 10px;\n"
                                                    u"background: #008287;\n")
                self.view_more_button.setText("View More")
                self.view_more_button.clicked.connect(lambda _, trainingid=training_id: self.view_training(trainingid))
                self.modify_button.clicked.connect(lambda _, trainingid=training_id: self.modify_training(trainingid))

            self.status_db.setText(f"{search_results[item][6]}")
            publish = search_results[item][7]
            if publish == 1:
                self.publish_button.setText("Unpublished")
            else:
                self.publish_button.setText("Publish")

            self.participant_db = QLabel(self.training)
            self.participant_db.setObjectName(u"participant_db")
            self.participant_db.setGeometry(QRect(130, 170, 91, 31))
            self.participant_db.setFont(font1)
            self.participant_db.setStyleSheet(u"color: white;\n"
                                              "font-weight: regular;\n"
                                              "border: none;\n"
                                              "bold: none;")
            self.participant_db.setText(f"{application_count}"" / " f"{search_results[item][5]}")

        # Adjust the size of the scroll area's contents
        self.scrollAreaWidgetContents_2.setMinimumHeight(50 + n * (frame_height + frame_spacing))

        # Set the scroll area widget
        self.scrollArea.setWidget(self.scrollAreaWidgetContents_2)

        
       
    
    def create_new_training(self):
        try:
            self.dialog = CreateNewTraining()
            self.dialog.show()
        except Exception as e:
            # Show error message box or print the error
            error_message = "An error occurred: " + str(e)
            QMessageBox.critical(self, "Error", error_message, QMessageBox.Ok)
            print(error_message)

    def modify_training(self, training_id):
        try:
            self.dialog = ModifyTraining(training_id)
            self.dialog.show()
        except Exception as e:
            # Show error message box or print the error
            error_message = "An error occurred: " + str(e)
            QMessageBox.critical(self, "Error", error_message, QMessageBox.Ok)
            print(error_message)

    def publish_training(self, publish_btn):
        button = publish_btn  # Get the button object that emitted the signal
        training_id = button.property("trainingID")  # Get the training ID from the button's property

        if button.text() == "Publish":
            button.setText("Unpublished")
            # Update the database to set the publishing status to 1
            self.cursor.execute("UPDATE training SET publish = 1 WHERE trainingID = ?", (training_id,))
            connect.commit()
        else:
            button.setText("Publish")
            # Update the database to set the publishing status to 0
            self.cursor.execute("UPDATE training SET publish = 0 WHERE trainingID = ?", (training_id,))
            connect.commit()


    def view_training(self, training_id):
        pass

    def approve_training(self, training_id):
        self.training_id = training_id
        loadUi("hr_approval.ui", self)
        
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setMinimumSize(QtCore.QSize(1280, 720))
        self.centralwidget.setMaximumSize(QtCore.QSize(1280, 720))
        self.centralwidget.setAutoFillBackground(False)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.side_frame = QtWidgets.QFrame(self.centralwidget)
        self.side_frame.setMinimumSize(QtCore.QSize(240, 0))
        self.side_frame.setMaximumSize(QtCore.QSize(240, 16777215))
        self.side_frame.setStyleSheet("border: 1px solid white;")
        self.side_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.side_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.side_frame.setObjectName("side_frame")
        self.profile_frame = QtWidgets.QFrame(self.side_frame)
        self.profile_frame.setGeometry(QtCore.QRect(14, 80, 212, 329))
        self.profile_frame.setStyleSheet("border-radius: 10px;")
        self.profile_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.profile_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.profile_frame.setObjectName("profile_frame")
        self.profile_button = QtWidgets.QPushButton(self.profile_frame)
        self.profile_button.setGeometry(QtCore.QRect(63, 40, 90, 90))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.profile_button.sizePolicy().hasHeightForWidth())
        self.profile_button.setSizePolicy(sizePolicy)
        self.profile_button.setMinimumSize(QtCore.QSize(90, 90))
        self.profile_button.setMaximumSize(QtCore.QSize(90, 90))
        self.profile_button.setStyleSheet("border: none;\n"
"border-radius: 50%;\n"
"")
        self.profile_button.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("profile.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.profile_button.setIcon(icon)
        self.profile_button.setIconSize(QtCore.QSize(90, 90))
        self.profile_button.setObjectName("profile_button")
        self.name_label = QtWidgets.QLabel(self.profile_frame)
        self.name_label.setGeometry(QtCore.QRect(10, 150, 191, 20))
        self.name_label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.name_label.setStyleSheet("border: none;\n"
"color: white;\n"
"font-weight: bold;\n"
"")
        self.name_label.setAlignment(QtCore.Qt.AlignCenter)
        self.name_label.setObjectName("name_label")
        self.staff_id_label = QtWidgets.QLabel(self.profile_frame)
        self.staff_id_label.setGeometry(QtCore.QRect(10, 200, 191, 20))
        self.staff_id_label.setStyleSheet("border: none;\n"
"color: white;\n"
"font-weight: bold;")
        self.staff_id_label.setAlignment(QtCore.Qt.AlignCenter)
        self.staff_id_label.setObjectName("staff_id_label")
        self.department_label = QtWidgets.QLabel(self.profile_frame)
        self.department_label.setGeometry(QtCore.QRect(10, 250, 191, 20))
        self.department_label.setStyleSheet("border: none;\n"
"color: white;\n"
"font-weight: bold;")
        self.department_label.setAlignment(QtCore.Qt.AlignCenter)
        self.department_label.setObjectName("department_label")
        self.name_db = QtWidgets.QLabel(self.profile_frame)
        self.name_db.setGeometry(QtCore.QRect(10, 170, 191, 20))
        self.name_db.setStyleSheet("border: none;\n"
"color: white;")
        self.name_db.setText("")
        self.name_db.setAlignment(QtCore.Qt.AlignCenter)
        self.name_db.setObjectName("name_db")
        self.id_db = QtWidgets.QLabel(self.profile_frame)
        self.id_db.setGeometry(QtCore.QRect(10, 220, 191, 20))
        self.id_db.setStyleSheet("border: none;\n"
"color: white;")
        self.id_db.setText("")
        self.id_db.setAlignment(QtCore.Qt.AlignCenter)
        self.id_db.setObjectName("id_db")
        self.department_db = QtWidgets.QLabel(self.profile_frame)
        self.department_db.setGeometry(QtCore.QRect(10, 270, 191, 20))
        self.department_db.setStyleSheet("border: none;\n"
"color: white;")
        self.department_db.setText("")
        self.department_db.setAlignment(QtCore.Qt.AlignCenter)
        self.department_db.setObjectName("department_db")
        self.list_button = QtWidgets.QPushButton(self.side_frame)
        self.list_button.setGeometry(QtCore.QRect(14, 470, 211, 91))
        self.list_button.setStyleSheet("color: white;\n"
"font-weight: bold;\n"
"border-radius: 10px;")
        self.list_button.setObjectName("list_button")
        self.logout_button = QtWidgets.QPushButton(self.side_frame)
        self.logout_button.setGeometry(QtCore.QRect(14, 650, 51, 41))
        self.logout_button.setStyleSheet("border: none;\n"
"border-radius: 50%;")
        self.logout_button.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("logout.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.logout_button.setIcon(icon1)
        self.logout_button.setIconSize(QtCore.QSize(45, 45))
        self.logout_button.setObjectName("logout_button")
        self.notification_menu_dot = QtWidgets.QLabel(self.side_frame)
        self.notification_menu_dot.setGeometry(QtCore.QRect(170, 570, 21, 21))
        self.notification_menu_dot.setStyleSheet("border: none;")
        self.notification_menu_dot.setText("")
        self.notification_menu_dot.setScaledContents(True)
        self.notification_menu_dot.setObjectName("notification_menu_dot")
        self.horizontalLayout.addWidget(self.side_frame)
        self.main_frame = QtWidgets.QFrame(self.centralwidget)
        self.main_frame.setStyleSheet("border: 1px solid white;")
        self.main_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.main_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.main_frame.setObjectName("main_frame")
        self.header = QtWidgets.QLabel(self.main_frame)
        self.header.setGeometry(QtCore.QRect(14, 14, 971, 81))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.header.sizePolicy().hasHeightForWidth())
        self.header.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(22)
        font.setBold(True)
        font.setWeight(75)
        self.header.setFont(font)
        self.header.setStyleSheet("border: none;\n"
"border-bottom: 1px solid white;\n"
"color: white;\n"
"font-weight: bold;\n"
"")
        self.header.setObjectName("header")
        self.scrollArea = QtWidgets.QScrollArea(self.main_frame)
        self.scrollArea.setGeometry(QtCore.QRect(14, 99, 971, 581))
        self.scrollArea.setStyleSheet("border: none;")
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 945, 581))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.training_name_db = QtWidgets.QPushButton(self.scrollAreaWidgetContents_2)
        self.training_name_db.setGeometry(QtCore.QRect(10, 10, 681, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.training_name_db.setFont(font)
        self.training_name_db.setStyleSheet("color: white;\n"
"font-weight: bold;\n"
"border: none;\n"
"text-align: left;\n"
"")
        self.training_name_db.setObjectName("training_name_db")
        self.training_status_db = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.training_status_db.setGeometry(QtCore.QRect(850, 10, 71, 31))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(False)
        font.setWeight(50)
        self.training_status_db.setFont(font)
        self.training_status_db.setStyleSheet("color: lightblue;\n"
"font-weight: regular;\n"
"border: none;\n"
"bold: none;")
        self.training_status_db.setObjectName("training_status_db")
        self.training_status_label = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.training_status_label.setGeometry(QtCore.QRect(710, 10, 131, 31))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.training_status_label.setFont(font)
        self.training_status_label.setStyleSheet("color: white;\n"
"font-weight: bold;\n"
"border: none;")
        self.training_status_label.setObjectName("training_status_label")
        self.application_table = QtWidgets.QTableWidget(self.scrollAreaWidgetContents_2)
        self.application_table.setGeometry(QtCore.QRect(0, 50, 931, 531))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.application_table.sizePolicy().hasHeightForWidth())
        self.application_table.setSizePolicy(sizePolicy)
        self.application_table.setStyleSheet("qproperty-uniformRowHeights: true;")
        self.application_table.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.application_table.setShowGrid(True)
        self.application_table.setGridStyle(QtCore.Qt.SolidLine)
        self.application_table.setCornerButtonEnabled(False)
        self.application_table.setObjectName("application_table")
        self.application_table.setColumnCount(5)
        self.application_table.setRowCount(4)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.application_table.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.application_table.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.application_table.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.application_table.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.application_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.application_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.application_table.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.application_table.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.application_table.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.NoBrush)
        item.setForeground(brush)
        self.application_table.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.NoBrush)
        item.setForeground(brush)
        self.application_table.setItem(0, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.NoBrush)
        item.setBackground(brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.NoBrush)
        item.setForeground(brush)
        self.application_table.setItem(0, 2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.NoBrush)
        item.setForeground(brush)
        self.application_table.setItem(0, 3, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("success.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        item.setIcon(icon2)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.NoBrush)
        item.setBackground(brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.NoBrush)
        item.setForeground(brush)
        self.application_table.setItem(0, 4, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.NoBrush)
        item.setForeground(brush)
        self.application_table.setItem(1, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.NoBrush)
        item.setForeground(brush)
        self.application_table.setItem(1, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.NoBrush)
        item.setBackground(brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.NoBrush)
        item.setForeground(brush)
        self.application_table.setItem(1, 2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.NoBrush)
        item.setForeground(brush)
        self.application_table.setItem(1, 3, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("reject.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        item.setIcon(icon3)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.NoBrush)
        item.setForeground(brush)
        self.application_table.setItem(1, 4, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.NoBrush)
        item.setForeground(brush)
        self.application_table.setItem(2, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.NoBrush)
        item.setForeground(brush)
        self.application_table.setItem(2, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.NoBrush)
        item.setBackground(brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.NoBrush)
        item.setForeground(brush)
        self.application_table.setItem(2, 2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.NoBrush)
        item.setForeground(brush)
        self.application_table.setItem(2, 3, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        item.setIcon(icon3)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.NoBrush)
        item.setBackground(brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.NoBrush)
        item.setForeground(brush)
        self.application_table.setItem(2, 4, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.NoBrush)
        item.setForeground(brush)
        self.application_table.setItem(3, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.NoBrush)
        item.setForeground(brush)
        self.application_table.setItem(3, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.NoBrush)
        item.setBackground(brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.NoBrush)
        item.setForeground(brush)
        self.application_table.setItem(3, 2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.NoBrush)
        item.setForeground(brush)
        self.application_table.setItem(3, 3, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("pictures/pending.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        item.setIcon(icon4)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.NoBrush)
        item.setBackground(brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.NoBrush)
        item.setForeground(brush)
        self.application_table.setItem(3, 4, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.NoBrush)
        item.setForeground(brush)
        self.application_table.setItem(4, 4, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.NoBrush)
        item.setForeground(brush)
        self.application_table.setItem(5, 4, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.NoBrush)
        item.setForeground(brush)
        self.application_table.setItem(5, 5, item)
        self.application_table.horizontalHeader().setVisible(True)
        self.application_table.verticalHeader().setVisible(False)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents_2)
        self.horizontalLayout.addWidget(self.main_frame)
       

        self.retranslateUi()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.name_label.setText(_translate("MainWindow", "Name"))
        self.staff_id_label.setText(_translate("MainWindow", "Staff ID"))
        self.department_label.setText(_translate("MainWindow", "Department"))
        self.list_button.setText(_translate("MainWindow", "Training List"))
        self.header.setText(_translate("MainWindow", "Approval"))
        self.training_name_db.setText(_translate("MainWindow", "Cyber Security"))
        self.training_status_db.setText(_translate("MainWindow", "Pending"))
        self.training_status_label.setText(_translate("MainWindow", "Training Status:"))
        self.application_table.setSortingEnabled(True)
        item = self.application_table.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", "1"))
        item = self.application_table.verticalHeaderItem(1)
        item.setText(_translate("MainWindow", "2"))
        item = self.application_table.verticalHeaderItem(2)
        item.setText(_translate("MainWindow", "3"))
        item = self.application_table.verticalHeaderItem(3)
        item.setText(_translate("MainWindow", "4"))
        item = self.application_table.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Index"))
        item = self.application_table.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Employee ID"))
        item = self.application_table.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Name"))
        item = self.application_table.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Department"))
        item = self.application_table.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Status"))
        __sortingEnabled = self.application_table.isSortingEnabled()
        self.application_table.setSortingEnabled(False)
        item = self.application_table.item(0, 0)
        item.setText(_translate("MainWindow", "1"))
        item = self.application_table.item(0, 1)
        item.setText(_translate("MainWindow", "123"))
        item = self.application_table.item(0, 2)
        item.setText(_translate("MainWindow", "Devus Lee"))
        item = self.application_table.item(0, 3)
        item.setText(_translate("MainWindow", "IT"))
        item = self.application_table.item(0, 4)
        item.setText(_translate("MainWindow", "Approved"))
        item = self.application_table.item(1, 0)
        item.setText(_translate("MainWindow", "2"))
        item = self.application_table.item(1, 1)
        item.setText(_translate("MainWindow", "345"))
        item = self.application_table.item(1, 2)
        item.setText(_translate("MainWindow", "Tan Yi Jia"))
        item = self.application_table.item(1, 3)
        item.setText(_translate("MainWindow", "Human Resource"))
        item = self.application_table.item(1, 4)
        item.setText(_translate("MainWindow", "Rejected"))
        item = self.application_table.item(2, 0)
        item.setText(_translate("MainWindow", "3"))
        item = self.application_table.item(2, 1)
        item.setText(_translate("MainWindow", "567"))
        item = self.application_table.item(2, 2)
        item.setText(_translate("MainWindow", "Teh Ger Min"))
        item = self.application_table.item(2, 3)
        item.setText(_translate("MainWindow", "Finance"))
        item = self.application_table.item(2, 4)
        item.setText(_translate("MainWindow", "Rejected"))
        item = self.application_table.item(3, 0)
        item.setText(_translate("MainWindow", "4"))
        item = self.application_table.item(3, 1)
        item.setText(_translate("MainWindow", "789"))
        item = self.application_table.item(3, 2)
        item.setText(_translate("MainWindow", "Derrick Chew Min Chiang"))
        item = self.application_table.item(3, 3)
        item.setText(_translate("MainWindow", "Finance"))
        item = self.application_table.item(3, 4)
        item.setText(_translate("MainWindow", "Pending"))
        self.application_table.setSortingEnabled(__sortingEnabled)

    def reset(self):
        try:
            # Define the size and position of each frame
            frame_width = 931
            frame_height = 251
            frame_spacing = 20


            # Clear the existing contents of the scroll area
            for frame in self.scrollAreaWidgetContents_2.findChildren(QtWidgets.QFrame):
                # Remove child widgets from the frame
                for child_widget in frame.children():
                    child_widget.deleteLater()
                # Remove the frame itself
                frame.deleteLater()

            connectDatabase()
            self.cursor = connect.cursor()
            self.cursor.execute(
                "SELECT t.trainingID, t.trainingName, d.departmentName, t.short_description, t.brochure, t.max_par, "
                "t.status, t.publish, " 
                "CASE WHEN t.date >= DATE('now') THEN t.date ELSE NULL END AS happening_soon_date "
                "FROM training t "
                "JOIN department d ON d.departmentID = t.departmentID "
                "ORDER BY happening_soon_date DESC, t.status")
            row_data = self.cursor.fetchall()
            rows = len(row_data)

            self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
            self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 50, frame_width,
                                                                     rows * (frame_height + frame_spacing)))
            self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")

            self.create_button = QPushButton(self.scrollAreaWidgetContents_2)
            self.create_button.setObjectName(u"create_button")
            self.create_button.setGeometry(QRect(808, 3, 121, 41))
            font1 = QFont()
            font1.setPointSize(9)
            font1.setBold(True)
            font1.setWeight(75)
            self.create_button.setFont(font1)
            self.create_button.setStyleSheet(u"color: white;\n"
                                             "font-weight: bold;\n"
                                             "border: 1px solid white;\n"
                                             "border-radius: 10px;")
            icon2 = QIcon()
            icon2.addFile(u"create.png", QSize(), QIcon.Normal, QIcon.Off)
            self.create_button.setIcon(icon2)
            self.create_button.setIconSize(QSize(30, 36))
            self.create_button.setCheckable(False)
            self.create_button.setText("Create")
            self.create_button.clicked.connect(self.create_new_training)

            self.app_status = "approved"

            for item in range(rows):
                training_id = row_data[item][0]
                self.cursor.execute("SELECT COUNT(a.applicationID) "
                                    "FROM application a "
                                    "JOIN training t ON t.trainingID = a.trainingID "
                                    "WHERE t.trainingID = ? AND a.applicationStatus = ?",
                                    (training_id, self.app_status,))
                application_count = str(self.cursor.fetchone()[0])

                self.training = QFrame(self.scrollAreaWidgetContents_2)
                self.training.setObjectName(u"training")
                self.training.setGeometry(QRect(0, 50 + (item * (frame_height + frame_spacing)), frame_width, frame_height))
                self.training.setStyleSheet(u"border: 1px solid white;\n"
                                            "background: #8A8A8A;\n"
                                            "border-radius: 10px;")
                self.training.setFrameShape(QFrame.StyledPanel)
                self.training.setFrameShadow(QFrame.Raised)

                blob_data = row_data[item][4]

                image = Image.open(BytesIO(blob_data))
                image.save(f"pictures/image{item}.png", "PNG")

                self.training_image = QLabel(self.training)

                self.training_image.setGeometry(QtCore.QRect(20, 10, 200, 150))
                self.training_image.setScaledContents(True)
                self.training_image.setPixmap(QtGui.QPixmap(f"pictures/image{item}.png"))  # here to set the data from database
                self.training_image.setObjectName(f"training_image_{item}")

                self.department_label = QLabel(self.training)
                self.department_label.setObjectName(u"department_label")
                self.department_label.setGeometry(QRect(230, 50, 111, 31))
                font = QFont()
                font.setBold(True)
                font.setWeight(75)
                self.department_label.setFont(font)
                self.department_label.setStyleSheet(u"color: white;\n"
                                                    "font-weight: bold;\n"
                                                    "border: none;")
                self.department_label.setText("Department: ")

                self.department_db = QLabel(self.training)
                self.department_db.setObjectName(u"department_db")
                self.department_db.setGeometry(QRect(340, 50, 581, 31))
                font1 = QFont()
                font1.setPointSize(8)
                font1.setBold(False)
                font1.setWeight(50)
                self.department_db.setFont(font1)
                self.department_db.setStyleSheet(u"color: white;\n"
                                                 "font-weight: regular;\n"
                                                 "border: none;\n"
                                                 "bold: none;")
                self.department_db.setText(f"{row_data[item][2]}")

                self.description_label = QLabel(self.training)
                self.description_label.setObjectName(u"description_label")
                self.description_label.setGeometry(QRect(230, 80, 101, 21))
                self.description_label.setFont(font)
                self.description_label.setStyleSheet(u"color: white;\n"
                                                     "font-weight: bold;\n"
                                                     "border: none;")
                self.description_label.setText("Description: ")

                self.description_db = QLineEdit(self.training)
                self.description_db.setObjectName(u"description_db")
                self.description_db.setGeometry(QRect(230, 100, 691, 81))
                self.description_db.setStyleSheet(u"color: white;\n"
                                                  "font-weight: regular;\n"
                                                  "border: none;")
                self.description_db.setAlignment(Qt.AlignLeft | Qt.AlignTop)

                self.description_db.setText(f"{row_data[item][3]}")

                self.training_name_db = QLabel(self.training)
                self.training_name_db.setObjectName(u"training_name_db")
                self.training_name_db.setGeometry(QRect(230, 20, 691, 31))
                font2 = QFont()
                font2.setPointSize(12)
                font2.setBold(True)
                font2.setWeight(75)
                self.training_name_db.setFont(font2)
                self.training_name_db.setStyleSheet(u"color: white;\n"
                                                    "font-weight: bold;\n"
                                                    "border: none;\n"
                                                    "text-align: left;\n")
                self.training_name_db.setText(f"{row_data[item][1]}")

                self.participant_label = QLabel(self.training)
                self.participant_label.setObjectName(u"participant_label")
                self.participant_label.setGeometry(QRect(20, 170, 101, 31))
                self.participant_label.setFont(font)
                self.participant_label.setStyleSheet(u"color: white;\n"
                                                     "font-weight: bold;\n"
                                                     "border: none;")
                self.participant_label.setText("Participant:")

                self.status_label = QLabel(self.training)
                self.status_label.setObjectName(u"status_label")
                self.status_label.setGeometry(QRect(20, 200, 61, 31))
                self.status_label.setFont(font)
                self.status_label.setStyleSheet(u"color: white;\n"
                                                "font-weight: bold;\n"
                                                "border: none;")
                self.status_label.setText("Status:")

                self.status_db = QLabel(self.training)
                self.status_db.setObjectName(u"status_db")
                self.status_db.setGeometry(QRect(90, 200, 71, 31))
                self.status_db.setFont(font1)
                self.modify_button.clicked.connect(lambda _, trainingid=training_id: self.modify_training(trainingid))

                if row_data[item][6] == "Approved":
                    self.status_db.setStyleSheet(u"color: lightgreen;\n"
                                                 "font-weight: bold;\n"
                                                 "border: none;\n")

                    self.publish_button = QPushButton(self.training)
                    self.publish_button.setObjectName(u"publish_button")
                    self.publish_button.setGeometry(QRect(810, 200, 112, 34))
                    self.publish_button.setStyleSheet(u"color: white;\n"
                                                      "font-weight: bold;\n"
                                                      "border-radius: 10px;\n"
                                                      "background: #008287;\n")
                    self.publish_button.setProperty("trainingID", training_id)
                    self.publish_button.clicked.connect(lambda _, publish_btn=self.publish_button:
                                                        self.publish_training(publish_btn))

                    self.modify_button = QPushButton(self.training)
                    self.modify_button.setObjectName(u"modify_button")
                    self.modify_button.setGeometry(QRect(570, 200, 112, 34))
                    self.modify_button.setStyleSheet(u"color: white;\n"
                                                     u"font-weight: bold;\n"
                                                     u"border-radius: 10px;\n"
                                                     u"background: #008287;\n")
                    self.modify_button.setText("Modify")
                    self.modify_button.clicked.connect(lambda _, trainingid=training_id: self.modify_training(trainingid))

                    self.view_more_button = QPushButton(self.training)
                    self.view_more_button.setObjectName(u"view_more_button")
                    self.view_more_button.setGeometry(QRect(690, 200, 112, 34))
                    self.view_more_button.setStyleSheet(u"color: white;\n"
                                                        u"font-weight: bold;\n"
                                                        u"border-radius: 10px;\n"
                                                        u"background: #008287;\n")
                    self.view_more_button.setText("Modify")
                    self.view_more_button.clicked.connect(lambda _, trainingid=training_id: self.view_training(trainingid))
                    self.modify_button.clicked.connect(lambda _, trainingid=training_id: self.modify_training(trainingid))

                elif row_data[item][6] == "Cancelled":
                    self.status_db.setStyleSheet(u"color: #FE8886;\n"
                                                 "font-weight: bold;\n"
                                                 "border: none;\n")

                    self.publish_button = QPushButton(self.training)
                    self.publish_button.setObjectName(u"publish_button")
                    self.publish_button.setGeometry(QRect(810, 200, 112, 34))
                    self.publish_button.setStyleSheet(u"color: white;\n"
                                                      "font-weight: bold;\n"
                                                      "border-radius: 10px;\n"
                                                      "background: #008287;\n")
                    self.publish_button.setProperty("trainingID", training_id)
                    self.publish_button.clicked.connect(
                        lambda _, publish_btn=self.publish_button: self.publish_training(publish_btn))

                    self.view_more_button = QPushButton(self.training)
                    self.view_more_button.setObjectName(u"view_more_button")
                    self.view_more_button.setGeometry(QRect(690, 200, 112, 34))
                    self.view_more_button.setStyleSheet(u"color: white;\n"
                                                        u"font-weight: bold;\n"
                                                        u"border-radius: 10px;\n"
                                                        u"background: #008287;\n")
                    self.view_more_button.setText("View More")
                    self.view_more_button.clicked.connect(lambda _, trainingid=training_id: self.view_training(trainingid))
                    self.modify_button.clicked.connect(lambda _, trainingid=training_id: self.modify_training(trainingid))

                elif row_data[item][6] == "Pending":
                    self.status_db.setStyleSheet(u"color: #FFAE42;\n"
                                                 "font-weight: bold;\n"
                                                 "border: none;\n")

                    self.publish_button = QPushButton(self.training)
                    self.publish_button.setObjectName(u"publish_button")
                    self.publish_button.setGeometry(QRect(810, 200, 112, 34))
                    self.publish_button.setStyleSheet(u"color: white;\n"
                                                      "font-weight: bold;\n"
                                                      "border-radius: 10px;\n"
                                                      "background: #008287;\n")
                    self.publish_button.setProperty("trainingID", training_id)
                    self.publish_button.clicked.connect(lambda _, publish_btn=self.publish_button:
                                                        self.publish_training(publish_btn))

                    self.modify_button = QPushButton(self.training)
                    self.modify_button.setObjectName(u"modify_button")
                    self.modify_button.setGeometry(QRect(690, 200, 112, 34))
                    self.modify_button.setStyleSheet(u"color: white;\n"
                                                     "font-weight: bold;\n"
                                                     "border-radius: 10px;\n"
                                                     "background: #008287;\n")
                    self.modify_button.setText("Modify")
                    self.modify_button.clicked.connect(lambda _, trainingid=training_id: self.modify_training(trainingid))

                    self.approval_button = QPushButton(self.training)
                    self.approval_button.setObjectName(u"approval_button")
                    self.approval_button.setGeometry(QRect(570, 200, 112, 34))
                    self.approval_button.setStyleSheet(u"color: white;\n"
                                                       "font-weight: bold;\n"
                                                       "border-radius: 10px;\n"
                                                       "background: #008287;\n")
                    self.approval_button.setText("Approval")
                    self.approval_button.clicked.connect(lambda _, trainingid=training_id:
                                                         self.approve_training(trainingid))
                    self.modify_button.clicked.connect(lambda _, trainingid=training_id: self.modify_training(trainingid))

                else:  # past training
                    self.status_db.setStyleSheet(u"color: #EABFFF;\n"
                                                 "font-weight: bold;\n"
                                                 "border: none;\n")

                    self.publish_button = QPushButton(self.training)
                    self.publish_button.setObjectName(u"publish_button")
                    self.publish_button.setGeometry(QRect(810, 200, 112, 34))
                    self.publish_button.setStyleSheet(u"color: white;\n"
                                                      "font-weight: bold;\n"
                                                      "border-radius: 10px;\n"
                                                      "background: #008287;\n")
                    self.publish_button.setProperty("trainingID", training_id)
                    self.publish_button.clicked.connect(lambda _, publish_btn=self.publish_button:
                                                        self.publish_training(publish_btn))

                    self.view_more_button = QPushButton(self.training)
                    self.view_more_button.setObjectName(u"view_more_button")
                    self.view_more_button.setGeometry(QRect(690, 200, 112, 34))
                    self.view_more_button.setStyleSheet(u"color: white;\n"
                                                        u"font-weight: bold;\n"
                                                        u"border-radius: 10px;\n"
                                                        u"background: #008287;\n")
                    self.view_more_button.setText("View More")
                    self.view_more_button.clicked.connect(lambda _, trainingid=training_id: self.view_training(trainingid))
                    self.modify_button.clicked.connect(lambda _, trainingid=training_id: self.modify_training(trainingid))

                self.status_db.setText(f"{row_data[item][6]}")
                publish = row_data[item][7]
                if publish == 1:
                    self.publish_button.setText("Unpublished")
                else:
                    self.publish_button.setText("Publish")

                self.participant_db = QLabel(self.training)
                self.participant_db.setObjectName(u"participant_db")
                self.participant_db.setGeometry(QRect(130, 170, 91, 31))
                self.participant_db.setFont(font1)
                self.participant_db.setStyleSheet(u"color: white;\n"
                                                  "font-weight: regular;\n"
                                                  "border: none;\n"
                                                  "bold: none;")
                self.participant_db.setText(f"{application_count}"" / " f"{row_data[item][5]}")

            # Adjust the size of the scroll area's contents
            self.scrollAreaWidgetContents_2.setMinimumHeight(50 + rows * (frame_height + frame_spacing))

            # Set the scroll area widget
            self.scrollArea.setWidget(self.scrollAreaWidgetContents_2)

        except Exception as e:
            # Show error message box or print the error
            error_message = "An error occurred: " + str(e)
            # QMessageBox.critical(self, "Error", error_message, QMessageBox.Ok)

    
    def gotoProfile(self):
        #make a popup window to view profile information
        self.profile = Profile()
        self.profile.show()

class CreateNewTraining(QMainWindow):
    def __init__(self):
        super(CreateNewTraining,self).__init__()

        self.setObjectName("Create New Training")
        self.setWindowTitle("Create Training")
        self.resize(1280, 720)
        self.setMinimumSize(QtCore.QSize(1280, 720))
        self.setMaximumSize(QtCore.QSize(1280, 720))
        self.setStyleSheet("background-color: #696969;")

        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setMinimumSize(QtCore.QSize(1280, 720))
        self.centralwidget.setMaximumSize(QtCore.QSize(1280, 720))
        self.centralwidget.setAutoFillBackground(False)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.main_frame = QtWidgets.QFrame(self.centralwidget)
        self.main_frame.setStyleSheet("border: 1px solid white;")
        self.main_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.main_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.main_frame.setObjectName("main_frame")

        self.header = QtWidgets.QLabel(self.main_frame)
        self.header.setGeometry(QtCore.QRect(14, 14, 1221, 81))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.header.sizePolicy().hasHeightForWidth())
        self.header.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(22)
        font.setBold(True)
        font.setWeight(75)
        self.header.setFont(font)
        self.header.setStyleSheet("border: none;\n"
                                  "border-bottom: 1px solid white;\n"
                                  "color: white;\n"
                                  "font-weight: bold;\n")
        self.header.setObjectName("header")
        self.header.setText("New Training")

        self.training_name_label = QtWidgets.QLabel(self.main_frame)
        self.training_name_label.setGeometry(QtCore.QRect(60, 140, 121, 31))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.training_name_label.setFont(font)
        self.training_name_label.setStyleSheet("border: none;\n"
                                               "color: white;")
        self.training_name_label.setObjectName("training_name_label")
        self.training_name_label.setText("Training Name")

        self.cost_label = QtWidgets.QLabel(self.main_frame)
        self.cost_label.setGeometry(QtCore.QRect(60, 360, 111, 31))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.cost_label.setFont(font)
        self.cost_label.setStyleSheet("border: none;\n"
                                      "color: white;")
        self.cost_label.setObjectName("cost_label")
        self.cost_label.setText("Cost Per Pax")

        self.datetime_label = QtWidgets.QLabel(self.main_frame)
        self.datetime_label.setGeometry(QtCore.QRect(430, 140, 111, 31))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.datetime_label.setFont(font)
        self.datetime_label.setStyleSheet("border: none;\n"
                                          "color: white;")
        self.datetime_label.setObjectName("datetime_label")
        self.datetime_label.setText("Date & Time")

        self.department_label = QtWidgets.QLabel(self.main_frame)
        self.department_label.setGeometry(QtCore.QRect(430, 250, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.department_label.setFont(font)
        self.department_label.setStyleSheet("border: none;\n"
                                            "color: white;")
        self.department_label.setObjectName("department_label")
        self.department_label.setText("Department")

        self.brochure_label = QtWidgets.QLabel(self.main_frame)
        self.brochure_label.setGeometry(QtCore.QRect(860, 200, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.brochure_label.setFont(font)
        self.brochure_label.setStyleSheet("border: none;\n"
                                          "color: white;")
        self.brochure_label.setObjectName("brochure_label")
        self.brochure_label.setText("Brochure")

        self.max_participants_label = QtWidgets.QLabel(self.main_frame)
        self.max_participants_label.setGeometry(QtCore.QRect(220, 360, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.max_participants_label.setFont(font)
        self.max_participants_label.setStyleSheet("border: none;\n"
                                                  "color: white;")
        self.max_participants_label.setObjectName("max_participants_label")
        self.max_participants_label.setText("Max Participants")

        self.venue_label = QtWidgets.QLabel(self.main_frame)
        self.venue_label.setGeometry(QtCore.QRect(60, 250, 51, 31))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.venue_label.setFont(font)
        self.venue_label.setStyleSheet("border: none;\n"
                                       "color: white;")
        self.venue_label.setObjectName("venue_label")
        self.venue_label.setText("Venue")

        self.short_description_label = QtWidgets.QLabel(self.main_frame)
        self.short_description_label.setGeometry(QtCore.QRect(60, 470, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.short_description_label.setFont(font)
        self.short_description_label.setStyleSheet("border: none;\n"
                                                   "color: white;")
        self.short_description_label.setObjectName("short_description_label")
        self.short_description_label.setText("Short Description")

        self.description_label = QtWidgets.QLabel(self.main_frame)
        self.description_label.setGeometry(QtCore.QRect(430, 390, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.description_label.setFont(font)
        self.description_label.setStyleSheet("border: none;\n"
                                             "color: white;")
        self.description_label.setObjectName("description_label")
        self.description_label.setText("Description")

        self.date_pick = QtWidgets.QDateEdit(self.main_frame)
        self.date_pick.setGeometry(QtCore.QRect(430, 180, 121, 41))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.date_pick.setFont(font)
        self.date_pick.setStyleSheet("color: #00ced1;"
                                     "QCalendarWidget {\n"
                                     "    background: white;\n"
                                     "    color: black;}\n"
                                     "QCalendarWidget QAbstractItemView:enabled {\n"
                                     "    color: white;}\n"
                                     "QCalendarWidget QWidget#qt_calendar_navigationbar {\n"
                                     "    color: white;}\n"
                                     "QCalendarWidget QAbstractItemView:selected {\n"
                                     "    color: white;}\n"
                                     "QCalendarWidget QAbstractItemView:focus {\n"
                                     "    color: black;}\n"
                                     "QCalendarWidget QMenu {\n"
                                     "    color: black;}")

        # Set the default date to today's date
        current_date = datetime.now()
        self.date_pick.setDate(current_date)
        self.date_pick.setCalendarPopup(True)
        self.date_pick.setObjectName("date_pick")

        self.time_pick = QtWidgets.QTimeEdit(self.main_frame)
        self.time_pick.setGeometry(QtCore.QRect(580, 180, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.time_pick.setFont(font)
        self.time_pick.setStyleSheet("color: #00ced1;")
        self.time_pick.setAlignment(QtCore.Qt.AlignCenter)
        self.time_pick.setObjectName("time_pick")
        self.time_pick.setDisplayFormat("HH:mm")

        self.brochure_button = QtWidgets.QPushButton(self.main_frame)
        self.brochure_button.setGeometry(QtCore.QRect(860, 250, 321, 201))
        self.brochure_button.setStyleSheet("border-radius: 10px;")
        # self.brochure_button.setText("")  # get the brochure image input from hr
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("add.png"),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.brochure_button.setIcon(icon)
        self.brochure_button.setIconSize(QtCore.QSize(60, 60))
        self.brochure_button.setObjectName("brochure_button")
        self.brochure_button.clicked.connect(self.add_brochure)

        self.new_training_name = QtWidgets.QLabel(self.main_frame)
        self.new_training_name.setGeometry(QtCore.QRect(60, 180, 311, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.new_training_name.setFont(font)
        self.new_training_name.setStyleSheet("borde: 1px solid white;\n"
                                             "color: black;\n"
                                             "background: white;\n"
                                             "border-radius: 10px;")
        # self.new_training_name.setText("")
        self.new_training_name.setObjectName("new_training_name")

        self.cost = QtWidgets.QLabel(self.main_frame)
        self.cost.setGeometry(QtCore.QRect(60, 400, 111, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.cost.setFont(font)
        self.cost.setStyleSheet("borde: 1px solid white;\n"
                                "color: black;\n"
                                "background: white;\n"
                                "border-radius: 10px;")
        # self.cost.setText("")
        self.cost.setObjectName("cost")

        self.description = QtWidgets.QLineEdit(self.main_frame)
        self.description.setGeometry(QtCore.QRect(430, 440, 371, 211))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.description.setFont(font)
        self.description.setStyleSheet("borde: 1px solid white;\n"
                                       "color: black;\n"
                                       "background: white;\n"
                                       "border-radius: 10px;")
        # self.description.setText("")

        self.description.setObjectName("description")

        self.short_description = QtWidgets.QLineEdit(self.main_frame)
        self.short_description.setGeometry(QtCore.QRect(60, 510, 311, 141))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.short_description.setFont(font)
        self.short_description.setStyleSheet("borde: 1px solid white;\n"
                                             "color: black;\n"
                                             "background: white;\n"
                                             "border-radius: 10px;")
        # self.short_description.setText("")

        self.short_description.setObjectName("short_description")

        self.max_participants = QtWidgets.QLabel(self.main_frame)
        self.max_participants.setGeometry(QtCore.QRect(220, 400, 111, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.max_participants.setFont(font)
        self.max_participants.setStyleSheet("borde: 1px solid white;\n"
                                            "color: black;\n"
                                            "background: white;\n"
                                            "border-radius: 10px;")
        # self.max_participants.setText("")
        self.max_participants.setObjectName("max_participants")

        self.venue = QtWidgets.QLabel(self.main_frame)
        self.venue.setGeometry(QtCore.QRect(60, 290, 311, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.venue.setFont(font)
        self.venue.setStyleSheet("borde: 1px solid white;\n"
                                 "color: black;\n"
                                 "background: white;\n"
                                 "border-radius: 10px;")
        # self.venue.setText("")
        self.venue.setObjectName("venue")

        connectDatabase()
        self.cursor = connect.cursor()
        self.cursor.execute("SELECT * FROM department")
        department_list = self.cursor.fetchall()

        self.department_pick = QtWidgets.QComboBox(self.main_frame)
        self.department_pick.setGeometry(QtCore.QRect(430, 290, 291, 41))
        self.department_pick.setStyleSheet("color:  #00ced1;")
        self.department_pick.setEditText("  Select Department ")
        self.department_pick.setObjectName("department_pick")
        self.department_pick.addItems([department[1] for department in department_list])


        self.check_box = QtWidgets.QCheckBox(self.main_frame)
        self.check_box.setGeometry(QtCore.QRect(430, 350, 301, 23))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.check_box.setFont(font)
        self.check_box.setStyleSheet("border: none;\n"
                                     "color: white;")
        self.check_box.setObjectName("check_box")
        self.check_box.setText("Add participants by department")

        # selected_date = self.date_pick.date().toString("yyyy-MM-dd")  # Retrieve the selected date as a string
        selected_time = self.time_pick.time().toString("HH:mm")  # Retrifeve the selected time as a string
        # brochure_image_path = self.brochure_image_path  # Assuming you have stored the brochure image path in a variable
        new_training_name_text = self.new_training_name.text()
        cost_text = self.cost.text()
        description_text = self.description.text()
        short_description_text = self.short_description.text()
        venue_text = self.venue.text()
        department_input = self.department_pick.currentText()  # Retrieve the selected department
        add_participants_by_department = self.check_box.isChecked()  # Retrieve the state of the checkbox

        self.create_button = QtWidgets.QPushButton(self.main_frame)
        self.create_button.setGeometry(QtCore.QRect(939, 600, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.create_button.setFont(font)
        self.create_button.setText("Create")
        self.create_button.setStyleSheet("color: white;\n"
                                         "font-weight: bold;\n"
                                         "border-radius: 10px;\n"
                                         "background: #008287;")
        self.create_button.setObjectName("create_button")
        self.create_button.clicked.connect(self.created_training)

        self.cancel_button = QtWidgets.QPushButton(self.main_frame)
        self.cancel_button.setGeometry(QtCore.QRect(1060, 600, 111, 41))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.cancel_button.setFont(font)
        self.cancel_button.setText("Cancel")
        self.cancel_button.setStyleSheet("color: white;\n"
                                         "font-weight: bold;\n"
                                         "border-radius: 10px;\n"
                                         "background: #008287;")
        self.cancel_button.setObjectName("cancel_button")
        self.cancel_button.clicked.connect(self.reject)

        self.horizontalLayout.addWidget(self.main_frame)

        # QtCore.QMetaObject.connectSlotsByName(self)

    def reject(self):
        self.close()

    def gotoProfile(self):
        #make a popup window to view profile information
        self.profile = Profile()
        self.profile.show()


    def add_brochure(self):
        file_dialog = QtWidgets.QFileDialog()
        image_path, _ = file_dialog.getOpenFileName(
            self, "Select Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp)"
        )

        if image_path:
            pixmap = QtGui.QPixmap(image_path)
            self.brochure_button.setPixmap(pixmap.scaled(
                self.brochure_button.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation
            ))


    def created_training(self):
        pass


    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.name_label.setText(_translate("MainWindow", "Name"))
        self.staff_id_label.setText(_translate("MainWindow", "Staff ID"))
        self.department_label.setText(_translate("MainWindow", "Department"))
        self.list_button.setText(_translate("MainWindow", "Training List"))
        self.header.setText(_translate("MainWindow", "Training List"))
        self.department_label_2.setText(_translate("MainWindow", "Department: "))
        self.description_label.setText(_translate("MainWindow", "Description: "))
        self.department_label_3.setText(_translate("MainWindow", "Participant:"))
        self.department_label_4.setText(_translate("MainWindow", "Status:"))
        self.publish_button.setText(_translate("MainWindow", "Publish"))
        self.modify_button.setText(_translate("MainWindow", "Modify"))
        self.approval_button.setText(_translate("MainWindow", "Approval"))
        self.create_button.setText(_translate("MainWindow", "Create"))
        self.search_bar.setPlaceholderText(_translate("MainWindow", "  Search..."))


class ModifyTraining(QMainWindow):
    def __init__(self, trainingID):
        super(ModifyTraining, self).__init__()
        self.trainingID = trainingID

        self.setObjectName("Create New Training")
        self.setWindowTitle("Create Training")
        self.resize(1280, 720)
        self.setMinimumSize(QtCore.QSize(1280, 720))
        self.setMaximumSize(QtCore.QSize(1280, 720))
        self.setStyleSheet("background-color: #696969;")

        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setMinimumSize(QtCore.QSize(1280, 720))
        self.centralwidget.setMaximumSize(QtCore.QSize(1280, 720))
        self.centralwidget.setAutoFillBackground(False)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.main_frame = QtWidgets.QFrame(self.centralwidget)
        self.main_frame.setStyleSheet("border: 1px solid white;")
        self.main_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.main_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.main_frame.setObjectName("main_frame")

        self.header = QtWidgets.QLabel(self.main_frame)
        self.header.setGeometry(QtCore.QRect(14, 14, 1221, 81))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.header.sizePolicy().hasHeightForWidth())
        self.header.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(22)
        font.setBold(True)
        font.setWeight(75)
        self.header.setFont(font)
        self.header.setStyleSheet("border: none;\n"
                                  "border-bottom: 1px solid white;\n"
                                  "color: white;\n"
                                  "font-weight: bold;\n")
        self.header.setObjectName("header")
        self.header.setText("New Training")

        self.training_name_label = QtWidgets.QLabel(self.main_frame)
        self.training_name_label.setGeometry(QtCore.QRect(60, 140, 121, 31))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.training_name_label.setFont(font)
        self.training_name_label.setStyleSheet("border: none;\n"
                                               "color: white;")
        self.training_name_label.setObjectName("training_name_label")
        self.training_name_label.setText("Training Name")

        self.cost_label = QtWidgets.QLabel(self.main_frame)
        self.cost_label.setGeometry(QtCore.QRect(60, 360, 111, 31))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.cost_label.setFont(font)
        self.cost_label.setStyleSheet("border: none;\n"
                                      "color: white;")
        self.cost_label.setObjectName("cost_label")
        self.cost_label.setText("Cost Per Pax")

        self.datetime_label = QtWidgets.QLabel(self.main_frame)
        self.datetime_label.setGeometry(QtCore.QRect(430, 140, 111, 31))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.datetime_label.setFont(font)
        self.datetime_label.setStyleSheet("border: none;\n"
                                          "color: white;")
        self.datetime_label.setObjectName("datetime_label")
        self.datetime_label.setText("Date & Time")

        self.department_label = QtWidgets.QLabel(self.main_frame)
        self.department_label.setGeometry(QtCore.QRect(430, 250, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.department_label.setFont(font)
        self.department_label.setStyleSheet("border: none;\n"
                                            "color: white;")
        self.department_label.setObjectName("department_label")
        self.department_label.setText("Department")

        self.brochure_label = QtWidgets.QLabel(self.main_frame)
        self.brochure_label.setGeometry(QtCore.QRect(860, 200, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.brochure_label.setFont(font)
        self.brochure_label.setStyleSheet("border: none;\n"
                                          "color: white;")
        self.brochure_label.setObjectName("brochure_label")
        self.brochure_label.setText("Brochure")

        self.max_participants_label = QtWidgets.QLabel(self.main_frame)
        self.max_participants_label.setGeometry(QtCore.QRect(220, 360, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.max_participants_label.setFont(font)
        self.max_participants_label.setStyleSheet("border: none;\n"
                                                  "color: white;")
        self.max_participants_label.setObjectName("max_participants_label")
        self.max_participants_label.setText("Max Participants")

        self.venue_label = QtWidgets.QLabel(self.main_frame)
        self.venue_label.setGeometry(QtCore.QRect(60, 250, 51, 31))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.venue_label.setFont(font)
        self.venue_label.setStyleSheet("border: none;\n"
                                       "color: white;")
        self.venue_label.setObjectName("venue_label")
        self.venue_label.setText("Venue")

        self.short_description_label = QtWidgets.QLabel(self.main_frame)
        self.short_description_label.setGeometry(QtCore.QRect(60, 470, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.short_description_label.setFont(font)
        self.short_description_label.setStyleSheet("border: none;\n"
                                                   "color: white;")
        self.short_description_label.setObjectName("short_description_label")
        self.short_description_label.setText("Short Description")

        self.description_label = QtWidgets.QLabel(self.main_frame)
        self.description_label.setGeometry(QtCore.QRect(430, 390, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.description_label.setFont(font)
        self.description_label.setStyleSheet("border: none;\n"
                                             "color: white;")
        self.description_label.setObjectName("description_label")
        self.description_label.setText("Description")

        self.date_pick = QtWidgets.QDateEdit(self.main_frame)
        self.date_pick.setGeometry(QtCore.QRect(430, 180, 121, 41))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.date_pick.setFont(font)
        self.date_pick.setStyleSheet("color: #00ced1;"
                                     "QCalendarWidget {\n"
                                     "    background: white;\n"
                                     "    color: black;}\n"
                                     "QCalendarWidget QAbstractItemView:enabled {\n"
                                     "    color: white;}\n"
                                     "QCalendarWidget QWidget#qt_calendar_navigationbar {\n"
                                     "    color: white;}\n"
                                     "QCalendarWidget QAbstractItemView:selected {\n"
                                     "    color: white;}\n"
                                     "QCalendarWidget QAbstractItemView:focus {\n"
                                     "    color: black;}\n"
                                     "QCalendarWidget QMenu {\n"
                                     "    color: black;}")

        # Set the default date to today's date
        current_date = datetime.now()
        self.date_pick.setDate(current_date)
        self.date_pick.setCalendarPopup(True)
        self.date_pick.setObjectName("date_pick")

        self.time_pick = QtWidgets.QTimeEdit(self.main_frame)
        self.time_pick.setGeometry(QtCore.QRect(580, 180, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.time_pick.setFont(font)
        self.time_pick.setStyleSheet("color: #00ced1;")
        self.time_pick.setAlignment(QtCore.Qt.AlignCenter)
        self.time_pick.setObjectName("time_pick")
        self.time_pick.setDisplayFormat("HH:mm")

        self.brochure_button = QtWidgets.QPushButton(self.main_frame)
        self.brochure_button.setGeometry(QtCore.QRect(860, 250, 321, 201))
        self.brochure_button.setStyleSheet("border-radius: 10px;")
        # self.brochure_button.setText("")  # get the brochure image input from hr
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("add.png"),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.brochure_button.setIcon(icon)
        self.brochure_button.setIconSize(QtCore.QSize(60, 60))
        self.brochure_button.setObjectName("brochure_button")
        self.brochure_button.clicked.connect(self.add_brochure)

        self.new_training_name = QtWidgets.QLineEdit(self.main_frame)
        self.new_training_name.setGeometry(QtCore.QRect(60, 180, 311, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.new_training_name.setFont(font)
        self.new_training_name.setStyleSheet("borde: 1px solid white;\n"
                                             "color: black;\n"
                                             "background: white;\n"
                                             "border-radius: 10px;")
        # self.new_training_name.setText("")
        self.new_training_name.setObjectName("new_training_name")

        self.cost = QtWidgets.QLineEdit(self.main_frame)
        self.cost.setGeometry(QtCore.QRect(60, 400, 111, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.cost.setFont(font)
        self.cost.setStyleSheet("borde: 1px solid white;\n"
                                "color: black;\n"
                                "background: white;\n"
                                "border-radius: 10px;")
        # self.cost.setText("")
        self.cost.setObjectName("cost")

        self.description = QtWidgets.QLineEdit(self.main_frame)
        self.description.setGeometry(QtCore.QRect(430, 440, 371, 211))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.description.setFont(font)
        self.description.setStyleSheet("borde: 1px solid white;\n"
                                       "color: black;\n"
                                       "background: white;\n"
                                       "border-radius: 10px;")
        # self.description.setText("")
        self.description.setObjectName("description")

        self.short_description = QtWidgets.QLineEdit(self.main_frame)
        self.short_description.setGeometry(QtCore.QRect(60, 510, 311, 141))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.short_description.setFont(font)
        self.short_description.setStyleSheet("borde: 1px solid white;\n"
                                             "color: black;\n"
                                             "background: white;\n"
                                             "border-radius: 10px;")
        # self.short_description.setText("")

        self.short_description.setObjectName("short_description")

        self.max_participants = QtWidgets.QLabel(self.main_frame)
        self.max_participants.setGeometry(QtCore.QRect(220, 400, 111, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.max_participants.setFont(font)
        self.max_participants.setStyleSheet("borde: 1px solid white;\n"
                                            "color: black;\n"
                                            "background: white;\n"
                                            "border-radius: 10px;")
        # self.max_participants.setText("")
        self.max_participants.setObjectName("max_participants")

        self.venue = QtWidgets.QLineEdit(self.main_frame)
        self.venue.setGeometry(QtCore.QRect(60, 290, 311, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.venue.setFont(font)
        self.venue.setStyleSheet("borde: 1px solid white;\n"
                                 "color: black;\n"
                                 "background: white;\n"
                                 "border-radius: 10px;")
        # self.venue.setText("")
        self.venue.setObjectName("venue")

        connectDatabase()
        self.cursor = connect.cursor()
        self.cursor.execute("SELECT * FROM department")
        department_list = self.cursor.fetchall()

        self.department_pick = QtWidgets.QComboBox(self.main_frame)
        self.department_pick.setGeometry(QtCore.QRect(430, 290, 291, 41))
        self.department_pick.setStyleSheet("color:  #00ced1;")
        self.department_pick.setEditText("  Select Department ")
        self.department_pick.setObjectName("department_pick")
        self.department_pick.addItems([department[1] for department in department_list])


        self.check_box = QtWidgets.QCheckBox(self.main_frame)
        self.check_box.setGeometry(QtCore.QRect(430, 350, 301, 23))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.check_box.setFont(font)
        self.check_box.setStyleSheet("border: none;\n"
                                     "color: white;")
        self.check_box.setObjectName("check_box")
        self.check_box.setText("Add participants by department")

        # selected_date = self.date_pick.date().toString("yyyy-MM-dd")  # Retrieve the selected date as a string
        selected_time = self.time_pick.time().toString("HH:mm")  # Retrifeve the selected time as a string
        # brochure_image_path = self.brochure_image_path  # Assuming you have stored the brochure image path in a variable
        new_training_name_text = self.new_training_name.text()
        cost_text = self.cost.text()
        description_text = self.description.text()
        short_description_text = self.short_description.text()
        venue_text = self.venue.text()
        department_input = self.department_pick.currentText()  # Retrieve the selected department
        add_participants_by_department = self.check_box.isChecked()  # Retrieve the state of the checkbox

        self.create_button = QtWidgets.QPushButton(self.main_frame)
        self.create_button.setGeometry(QtCore.QRect(939, 600, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.create_button.setFont(font)
        self.create_button.setText("Create")
        self.create_button.setStyleSheet("color: white;\n"
                                         "font-weight: bold;\n"
                                         "border-radius: 10px;\n"
                                         "background: #008287;")
        self.create_button.setObjectName("create_button")
        self.create_button.clicked.connect(self.created_training)

        self.cancel_button = QtWidgets.QPushButton(self.main_frame)
        self.cancel_button.setGeometry(QtCore.QRect(1060, 600, 111, 41))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.cancel_button.setFont(font)
        self.cancel_button.setText("Cancel")
        self.cancel_button.setStyleSheet("color: white;\n"
                                         "font-weight: bold;\n"
                                         "border-radius: 10px;\n"
                                         "background: #008287;")
        self.cancel_button.setObjectName("cancel_button")
        self.cancel_button.clicked.connect(self.reject)

        connectDatabase()
        self.cursor = connect.cursor()
        self.cursor.execute("SELECT trainingID, trainingName, status, date, time, duration, venue, short_description, description, max_par, brochure, departmentID, publish, cost from training WHERE trainingID = ?", (self.trainingID,))
        training = self.cursor.fetchall()

        self.header.setText("Modify Training")

        self.new_training_name.setText(training[0][1])
        #allow label to be edited 

        self.venue.setText(training[0][6])
        self.cost.setText(str(training[0][13]))
        self.short_description.setText(training[0][7])
        #make date 
        date = datetime.strptime(training[0][3], '%d-%m-%Y').strftime('%d-%m-%Y')
        self.date_pick.setDate(QtCore.QDate.fromString(date, "dd-MM-yyyy"))
        self.time_pick.setTime(QtCore.QTime.fromString(training[0][4], "HH:mm"))
        self.check_box.hide()
        self.description.setText(training[0][8])

        self.max_participants_label.hide()
        self.max_participants.hide()

        self.brochure_button.setIconSize(QtCore.QSize(200, 200))
        self.brochure_button.setIcon(QtGui.QIcon(f"pictures/image{trainingID}.png"))
        self.create_button.setText("Modify")
        self.cancel_button.clicked.connect(self.reject)
        self.create_button.clicked.connect(self.modify_training)
        
        self.horizontalLayout.addWidget(self.main_frame)

    def modify_training(self):
        connectDatabase()
        self.cursor = connect.cursor()
        self.cursor.execute("UPDATE training SET trainingName = ?, date = ?, time = ?, venue = ?, short_description = ?, description = ?, cost = ? WHERE trainingID = ?", (self.new_training_name.text(), self.date_pick.date().toString("dd-MM-yyyy"), self.time_pick.time().toString("HH:mm"), self.venue.text(), (str(self.short_description.text())), (str(self.description.text())), self.cost.text(), self.trainingID))
        connect.commit()
        self.close()
        


    def reject(self):
        self.close()
    
    def gotoProfile(self):
        #make a popup window to view profile information
        self.profile = Profile()
        self.profile.show()


    def add_brochure(self):
        file_dialog = QtWidgets.QFileDialog()
        image_path, _ = file_dialog.getOpenFileName(
            self, "Select Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp)"
        )

        if image_path:
            pixmap = QtGui.QPixmap(image_path)
            self.brochure_button.setPixmap(pixmap.scaled(
                self.brochure_button.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation
            ))


    def created_training(self):
        pass


    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.name_label.setText(_translate("MainWindow", "Name"))
        self.staff_id_label.setText(_translate("MainWindow", "Staff ID"))
        self.department_label.setText(_translate("MainWindow", "Department"))
        self.list_button.setText(_translate("MainWindow", "Training List"))
        self.header.setText(_translate("MainWindow", "Training List"))
        self.department_label_2.setText(_translate("MainWindow", "Department: "))
        self.description_label.setText(_translate("MainWindow", "Description: "))
        self.department_label_3.setText(_translate("MainWindow", "Participant:"))
        self.department_label_4.setText(_translate("MainWindow", "Status:"))
        self.publish_button.setText(_translate("MainWindow", "Publish"))
        self.modify_button.setText(_translate("MainWindow", "Modify"))
        self.approval_button.setText(_translate("MainWindow", "Approval"))
        self.create_button.setText(_translate("MainWindow", "Create"))
        self.search_bar.setPlaceholderText(_translate("MainWindow", "  Search..."))

    def gotoProfile(self):
        #make a popup window to view profile information
        self.profile = Profile()
        self.profile.show()



class View(QMainWindow):
    def __init__(self):
        super(View, self).__init__()


        loadUi("mytraining.ui", self)
        self.logout_button.clicked.connect(gotologin)
        self.profile_button.clicked.connect(self.gotoProfile)
        self.notification_button.clicked.connect(gotoNotification)
        self.list_button.clicked.connect(gotoview)
        self.my_training_button.clicked.connect(gotoTraining)
        cursor.execute('SELECT name, employeeID, departmentID FROM employee WHERE employeeID = ?', (employeeID, )) 
        display = cursor.fetchall()
        self.employeeID = display[0][1]
        self.name_db.setText(display[0][0])  
        self.id_db.setText(str(display[0][1]))
        cursor.execute('SELECT departmentName FROM department WHERE departmentID=?', (display[0][2],))
        self.department_db.setText(cursor.fetchone()[0])
        self.profile_button.setIcon(QtGui.QIcon("pictures/profile.png"))
        self.logout_button.setIcon(QtGui.QIcon("pictures/logout.png"))
        # Define the size and position of each frame
        frame_width = 931
        frame_height = 251
        frame_spacing = 20

        # Right frame
        self.main_frame = QtWidgets.QFrame(self.centralwidget)
        self.main_frame.setStyleSheet("border: 1px solid white;")
        self.main_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.main_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.main_frame.setObjectName("main_frame")

        # Title for the page
        # need to reset the title after switch tab
        self.header = QtWidgets.QLabel(self.main_frame)
        self.header.setGeometry(QtCore.QRect(10, 10, 971, 81))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.header.sizePolicy().hasHeightForWidth())
        self.header.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(22)

        font.setWeight(75)
        self.header.setFont(font)
        self.header.setStyleSheet("border: none;\nborder-bottom: 1px solid white;\ncolor: white;")
        self.header.setText("Training List")  # here to set the title
        self.header.setObjectName("header")

        # scrolling area to display lists of trainings
        self.scrollArea = QtWidgets.QScrollArea(self.main_frame)
        self.scrollArea.setGeometry(QtCore.QRect(14, 99, 971, 581))
        self.scrollArea.setStyleSheet("border: none;")
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")

        # search input and button
        self.search_bar = QtWidgets.QLineEdit(self.main_frame)
        self.search_bar.setGeometry(QtCore.QRect(805, 60, 141, 25))
        self.search_bar.setStyleSheet("QLineEdit {color: white;}\nQLineEdit::placeholder {color: white;}\nQLineEdit "
                                      "{border-radius: 10px;\nborder: 1px solid white;}\n")
        self.search_bar.setObjectName("search_bar")
        self.search_button = QtWidgets.QPushButton(self.main_frame)
        self.search_button.setGeometry(QtCore.QRect(950, 57, 31, 34))
        self.search_button.setStyleSheet("border: none;")
        self.search_button.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("pictures/search.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.search_button.setIcon(icon2)
        self.search_button.setIconSize(QtCore.QSize(25, 25))
        self.search_bar.setPlaceholderText("  Search...")
        self.search_button.setObjectName("search_button")
        self.search_button.clicked.connect(self.searchTraining)

        self.horizontalLayout.addWidget(self.main_frame)
        self.setCentralWidget(self.centralwidget)

        connectDatabase()

        self.cursor = connect.cursor()

        self.cursor.execute("SELECT departmentID from employee WHERE employeeID = ?", (employeeID, ))
        departmentID = self.cursor.fetchone()[0]

        self.cursor.execute(
            "SELECT t.trainingID, t.trainingName, d.departmentName, t.short_description, t.brochure, t.publish, t.status FROM training t, department d"
            " WHERE d.departmentID = t.departmentID AND t.departmentID = ? AND t.publish = 1 AND t.trainingID NOT IN (SELECT trainingID FROM application WHERE employeeID = ?)", (departmentID, employeeID, ))
        row_data = self.cursor.fetchall()  # Fetch all rows of data
        rows = len(row_data)  # Calculate the length of fetched data

# [training id, trainingName, department name, description, brochure, application status]

        # Scroll area content widget
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, frame_width, rows *
                                                                 (frame_height + frame_spacing)))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        number = 0
        # Loop to create and position the frames
        for item in range(rows):
            
            number = number + 1
            self.training = QtWidgets.QFrame(self.scrollAreaWidgetContents_2)
            self.training.setGeometry(QtCore.QRect(0, item * (frame_height + frame_spacing), frame_width, frame_height))
            self.training.setStyleSheet("border: 1px solid white;\nbackground: #8A8A8A;\nborder-radius: 10px;")
            self.training.setFrameShape(QtWidgets.QFrame.StyledPanel)
            self.training.setFrameShadow(QtWidgets.QFrame.Raised)
            self.training.setObjectName("training")

            blob_data = row_data[item][4]

            image = Image.open(BytesIO(blob_data))
            image.save(f"pictures/image{item}.png", "PNG")

            self.training_image = QtWidgets.QLabel(self.training)

            self.training_image.setGeometry(QtCore.QRect(20, 10, 200, 150))
            self.training_image.setScaledContents(True)
            self.training_image.setPixmap(QtGui.QPixmap(f"pictures/image{item}.png"))  # here to set the data from database
            self.training_image.setObjectName(f"training_image_{item}")
            

            self.department_label_2 = QtWidgets.QLabel(self.training)
            self.department_label_2.setGeometry(QtCore.QRect(230, 50, 111, 31))
            font = QtGui.QFont()

            font.setWeight(75)
            self.department_label_2.setFont(font)
            self.department_label_2.setStyleSheet("color: white;\nborder: none;")
            self.department_label_2.setText("Department: ")
            self.department_label_2.setObjectName("department_label_2")

            self.department_db_2 = QtWidgets.QLabel(self.training)
            self.department_db_2.setGeometry(QtCore.QRect(340, 50, 581, 31))
            font = QtGui.QFont()
            font.setPointSize(8)

            font.setWeight(50)
            self.department_db_2.setFont(font)
            self.department_db_2.setStyleSheet("color: white;\nfont-weight: regular;\nborder: none;")
            self.department_db_2.setText(f"{row_data[item][2]}")
            self.department_db_2.setObjectName("department_db_2")

            self.description_label = QtWidgets.QLabel(self.training)
            self.description_label.setGeometry(QtCore.QRect(230, 80, 101, 21))
            font = QtGui.QFont()

            font.setWeight(75)
            self.description_label.setFont(font)
            self.description_label.setStyleSheet("color: white;\nborder: none;")
            self.description_label.setText("Description: ")
            self.description_label.setObjectName("description_label")

            self.description_db = QtWidgets.QLabel(self.training)
            self.description_db.setGeometry(QtCore.QRect(230, 100, 691, 81))
            self.description_db.setStyleSheet("color: white;\nfont-weight: regular;\nborder: none;")
            self.description_db.setText(f"{row_data[item][3]}")
            self.description_db.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
            self.description_db.setWordWrap(True)
            self.description_db.setObjectName("description_db")

            self.view_button = QtWidgets.QPushButton(self.training)
            self.view_button.setGeometry(QtCore.QRect(810, 200, 112, 34))
            self.view_button.setStyleSheet(
                "color: white;\nborder-radius: 10px;\nbackground: #008287;")
            self.view_button.setText("View More")
            self.view_button.setObjectName("view_button")
            self.view_button.clicked.connect(lambda _, training_id=row_data[item][0]:
                                             self.viewTrainingDetails(training_id))

            self.training_name_db = QtWidgets.QPushButton(self.training)
            self.training_name_db.setGeometry(QtCore.QRect(230, 20, 691, 31))
            font = QtGui.QFont()
            font.setPointSize(12)
            font.setWeight(75)
            self.training_name_db.setFont(font)
            self.training_name_db.setStyleSheet("color: white;\nborder: none;\ntext-align: left;\n")
            self.training_name_db.setText(f"{row_data[item][1]}")
            self.training_name_db.setObjectName("training_name_db")
            self.training_name_db.clicked.connect(lambda _, training_id=row_data[item][0]:
                                                  self.viewTrainingDetails(training_id))

        # Adjust the size of the scroll area's contents
        self.scrollAreaWidgetContents_2.setMinimumHeight(rows * (frame_height + frame_spacing))

        # Set the initial training items using row_data
        self.updateSearchResults(row_data)

        # Set the scroll area widget
        self.scrollArea.setWidget(self.scrollAreaWidgetContents_2)
        self.setCentralWidget(self.centralwidget)
        QtCore.QMetaObject.connectSlotsByName(self)


    def gotoProfile(self):
        #make a popup window to view profile information
        self.profile = Profile()
        self.profile.show()

    def registerTraining(self):
        connectDatabase()
        self.cursor = connect.cursor()
        self.cursor.execute(
            "INSERT INTO notification (notification_status, notification_date, employeeID, trainingID, is_read ) VALUES (?,?,?,?,?)", ("pending", datetime.now().strftime('%d-%m-%Y %H:%M'), employeeID, self.trainingID ,0)
        )
        connect.commit()
        self.cursor = connect.cursor()
        self.cursor.execute(
            "INSERT INTO application (employeeID, trainingID, applicationStatus, applicationDate) VALUES (?,?,?,?)", (employeeID, self.trainingID, "pending", datetime.now().strftime('%d-%m-%Y %H:%M'))
        )
        connect.commit()
        gotoview()
    
    def showImagePopUp(self, pictureName):
        popup = ImagePopup(self)
        popup.setImage(QtGui.QPixmap(pictureName))
        popup.show()

    def viewTrainingDetails(self, trainingID):
        self.trainingID = trainingID
        try:
            print("Clicked ID:", trainingID)
            loadUi("training_details.ui", self)
            self.logout_button.clicked.connect(gotologin)
            self.profile_button.clicked.connect(self.gotoProfile)
            self.notification_button.clicked.connect(gotoNotification)
            self.list_button.clicked.connect(gotoview)
            self.my_training_button.clicked.connect(gotoTraining)

            connectDatabase()
            cursor.execute('SELECT name, employeeID, departmentID FROM employee WHERE employeeID = ?', (employeeID,))
            display = cursor.fetchall()
            self.name_db.setText(display[0][0])
            self.id_db.setText(str(display[0][1]))
            cursor.execute('SELECT departmentName FROM department WHERE departmentID=?', (display[0][2],))
            self.department_db.setText(cursor.fetchone()[0])
            self.profile_button.setIcon(QtGui.QIcon("pictures/profile.png"))
            self.header.setText("Training Details")

            self.cursor = connect.cursor()
            self.cursor.execute(
                "SELECT t.trainingName, t.status, t.cost, t.date, t.time, t.venue,t.duration, d.departmentName, t.short_description, t.brochure, t.max_par "
                "FROM training t, department d WHERE d.departmentID = t.departmentID AND t.trainingID = ?",
                (trainingID,))
            display = self.cursor.fetchall()
            #Result of display = [('Training 1', 'Pending', 100, '2021-04-01', '09:00:00', 'IT', 'Short description', 'Brochure')]
            self.training.setText(f"{display[0][0]}")

            date = datetime.strptime(display[0][3], "%d-%m-%Y")
            date = date.strftime("%d %B %Y")
            time = datetime.strptime(display[0][4], "%H:%M")
            time = time.strftime("%H:%M")
            self.date_db.setText(f"{date}")
            self.time_db.setText(f"{time}")
            self.venue_db.setText(f"{display[0][5]}")
            self.duration_db.setText(f"{display[0][6]}")
            self.department_db_2.setText(f"{display[0][7]}")
            self.description_db.setText(f"{display[0][8]}")

            self.brochure_button.setIconSize(QtCore.QSize(200, 200))
            self.brochure_button.setIcon(QtGui.QIcon(f"pictures/image{trainingID}.png"))
            self.brochure_button.clicked.connect(lambda: self.showImagePopUp(f"pictures/image{trainingID}.png"))

            self.register_button.clicked.connect(self.registerTraining)

            self.number_participants_db.setText(f"{display[0][10]}")

        except Exception as e:
            logging.exception("An error occurred in viewTrainingDetails:")


    def searchTraining(self):
        try:
            keywords = self.search_bar.text()

            # Query the database based on the keywords
            connectDatabase()
            self.cursor.execute(
                "SELECT DISTINCT t.trainingID, t.trainingName, d.departmentName, t.short_description, t.brochure"
                " FROM training t "
                "JOIN department d ON d.departmentID = t.departmentID "
                "WHERE (t.trainingName LIKE ? OR d.departmentName LIKE ? "
                "OR t.date LIKE ? OR t.time LIKE ?)",
                ('%' + keywords + '%', '%' + keywords + '%', '%' + keywords + '%',
                 '%' + keywords + '%'))
            
            search_results = self.cursor.fetchall()


            # Display the search results
            self.updateSearchResults(search_results)

        except Exception as e:
            # Show error message box or print the error
            error_message = "An error occurred: " + str(e)
            print(error_message)



    def updateSearchResults(self, search_results):
        # Define the size and position of each frame
        frame_width = 931
        frame_height = 251
        frame_spacing = 20
        n = len(search_results)

        # Clear the existing contents of the scroll area
        for frame in self.scrollAreaWidgetContents_2.findChildren(QtWidgets.QFrame):
            # Remove child widgets from the frame
            for child_widget in frame.children():
                child_widget.deleteLater()
            # Remove the frame itself
            frame.deleteLater()

        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, frame_width, n *
                                                                 (frame_height + frame_spacing)))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        # Loop to create and position the frames
        for item in range(n):

            self.training = QtWidgets.QFrame(self.scrollAreaWidgetContents_2)
            self.training.setGeometry(QtCore.QRect(0, item * (frame_height + frame_spacing), frame_width, frame_height))
            self.training.setStyleSheet("border: 1px solid white;\nbackground: #8A8A8A;\nborder-radius: 10px;")
            self.training.setFrameShape(QtWidgets.QFrame.StyledPanel)
            self.training.setFrameShadow(QtWidgets.QFrame.Raised)
            self.training.setObjectName("training")

            blob_data = search_results[item][4]

            image = Image.open(BytesIO(blob_data))
            image.save(f"pictures/image{item}.png", "PNG")

            self.training_image = QtWidgets.QLabel(self.training)

            self.training_image.setGeometry(QtCore.QRect(20, 10, 200, 150))
            self.training_image.setScaledContents(True)
            self.training_image.setPixmap(QtGui.QPixmap(f"pictures/image{item}.png"))  # here to set the data from database
            self.training_image.setObjectName(f"training_image_{item}")
            

            self.department_label_2 = QtWidgets.QLabel(self.training)
            self.department_label_2.setGeometry(QtCore.QRect(230, 50, 111, 31))
            font = QtGui.QFont()

            font.setWeight(75)
            self.department_label_2.setFont(font)
            self.department_label_2.setStyleSheet("color: white;\nborder: none;")
            self.department_label_2.setText("Department: ")
            self.department_label_2.setObjectName("department_label_2")

            self.department_db_2 = QtWidgets.QLabel(self.training)
            self.department_db_2.setGeometry(QtCore.QRect(340, 50, 581, 31))
            font = QtGui.QFont()
            font.setPointSize(8)

            font.setWeight(50)
            self.department_db_2.setFont(font)
            self.department_db_2.setStyleSheet("color: white;\nfont-weight: regular;\nborder: none;")
            self.department_db_2.setText(f"{search_results[item][2]}")
            self.department_db_2.setObjectName("department_db_2")

            self.description_label = QtWidgets.QLabel(self.training)
            self.description_label.setGeometry(QtCore.QRect(230, 80, 101, 21))
            font = QtGui.QFont()

            font.setWeight(75)
            self.description_label.setFont(font)
            self.description_label.setStyleSheet("color: white;\nborder: none;")
            self.description_label.setText("Description: ")
            self.description_label.setObjectName("description_label")

            self.description_db = QtWidgets.QLabel(self.training)
            self.description_db.setGeometry(QtCore.QRect(230, 100, 691, 81))
            self.description_db.setStyleSheet("color: white;\nfont-weight: regular;\nborder: none;")
            self.description_db.setText(f"{search_results[item][3]}")
            self.description_db.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
            self.description_db.setWordWrap(True)
            self.description_db.setObjectName("description_db")

            self.view_button = QtWidgets.QPushButton(self.training)
            self.view_button.setGeometry(QtCore.QRect(810, 200, 112, 34))
            self.view_button.setStyleSheet(
                "color: white;\nborder-radius: 10px;\nbackground: #008287;")
            self.view_button.setText("View More")
            self.view_button.setObjectName("view_button")
            self.view_button.clicked.connect(lambda _, training_id=search_results[item][0]:
                                             self.viewTrainingDetails(training_id))

            self.training_name_db = QtWidgets.QPushButton(self.training)
            self.training_name_db.setGeometry(QtCore.QRect(230, 20, 691, 31))
            font = QtGui.QFont()
            font.setPointSize(12)
            font.setWeight(75)
            self.training_name_db.setFont(font)
            self.training_name_db.setStyleSheet("color: white;\nborder: none;\ntext-align: left;\n")
            self.training_name_db.setText(f"{search_results[item][1]}")
            self.training_name_db.setObjectName("training_name_db")
            self.training_name_db.clicked.connect(lambda _, training_id=search_results[item][0]:
                                                  self.viewTrainingDetails(training_id))

        # Adjust the size of the scroll area's contents
        self.scrollAreaWidgetContents_2.setMinimumHeight(n * (frame_height + frame_spacing))

        # Set the scroll area widget
        self.scrollArea.setWidget(self.scrollAreaWidgetContents_2)
        self.setCentralWidget(self.centralwidget)
        QtCore.QMetaObject.connectSlotsByName(self)




    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
      
        self.department_label_2.setText(_translate("MainWindow", "Department: "))
        self.description_label.setText(_translate("MainWindow", "Description: "))
        self.view_button.setText(_translate("MainWindow", "View More"))

class Profile(QMainWindow):
    def __init__(self):
        super(Profile, self).__init__()
        loadUi("profile.ui", self)

        self.setFixedWidth(960)
        self.setFixedHeight(540)

        connectDatabase()
        self.cursor = connect.cursor()
        self.cursor.execute(
            "SELECT e.employeeID, e.name, e.gender, e.email, e.phone_no, e.role, e.password, e.departmentID"
            " FROM employee e WHERE e.employeeID = ?", (employeeID,))
        display = self.cursor.fetchall()
        self.staff_id_db.setText(str(display[0][0])) 
        self.name_db.setText(display[0][1])
        self.gender_db.setText(display[0][2])
        self.email_db.setText(display[0][3])
        self.phone_db.setText(str(display[0][4].replace("*", "")))
        self.role_db.setText(display[0][5])
        self.profile.setPixmap(QtGui.QPixmap("pictures/profile.png"))
        self.department_db.setText(str(display[0][7]))
    
    def gotoProfile(self):
        #make a popup window to view profile information
        self.profile = Profile()
        self.profile.show()



class Notification(QMainWindow):
    def __init__(self):
        super(Notification, self).__init__()
        loadUi("notification.ui", self)


        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setMinimumSize(QtCore.QSize(1280, 720))
        self.centralwidget.setMaximumSize(QtCore.QSize(1280, 720))
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")

        # Side frame
        self.side_frame = QtWidgets.QFrame(self.centralwidget)
        self.side_frame.setMinimumSize(QtCore.QSize(240, 0))
        self.side_frame.setMaximumSize(QtCore.QSize(240, 16777215))
        self.side_frame.setStyleSheet("border: 1px solid white;")
        self.side_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.side_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.side_frame.setObjectName("side_frame")

        # profile frame to display profile details (ID, Name, Department)
        self.profile_frame = QtWidgets.QFrame(self.side_frame)
        self.profile_frame.setGeometry(QtCore.QRect(14, 14, 212, 329))
        self.profile_frame.setStyleSheet("border-radius: 10px;")
        self.profile_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.profile_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.profile_frame.setObjectName("profile_frame")
        
        # profile button to see more profile details
        self.profile_button = QtWidgets.QPushButton(self.profile_frame)
        self.profile_button.setGeometry(QtCore.QRect(63, 40, 90, 90))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.profile_button.sizePolicy().hasHeightForWidth())
        self.profile_button.setSizePolicy(sizePolicy)
        self.profile_button.setMinimumSize(QtCore.QSize(90, 90))
        self.profile_button.setMaximumSize(QtCore.QSize(90, 90))
        self.profile_button.setStyleSheet("border: none;\nborder-radius: 50%;\n")
        self.profile_button.setText("")
        self.profile_button.setIcon(QtGui.QIcon("pictures/profile.png"))
        self.profile_button.setIconSize(QtCore.QSize(90, 90))
        self.profile_button.setObjectName("profile_button")
        # display name
        self.name_label = QtWidgets.QLabel(self.profile_frame)
        self.name_label.setGeometry(QtCore.QRect(10, 150, 191, 20))
        self.name_label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.name_label.setStyleSheet("border: none;\ncolor: white;\nfont-weight: ;\n")
        self.name_label.setAlignment(QtCore.Qt.AlignCenter)
        self.name_label.setObjectName("name_label")
        # display id
        self.staff_id_label = QtWidgets.QLabel(self.profile_frame)
        self.staff_id_label.setGeometry(QtCore.QRect(10, 200, 191, 20))
        self.staff_id_label.setStyleSheet("border: none;\ncolor: white;\nfont-weight: ;")
        self.staff_id_label.setAlignment(QtCore.Qt.AlignCenter)
        self.staff_id_label.setObjectName("staff_id_label")
        # display department
        self.department_label = QtWidgets.QLabel(self.profile_frame)
        self.department_label.setGeometry(QtCore.QRect(10, 250, 191, 20))
        self.department_label.setStyleSheet("border: none;\ncolor: white;\nfont-weight: ;")
        self.department_label.setAlignment(QtCore.Qt.AlignCenter)
        self.department_label.setObjectName("department_label")
        # calling the user details from db and set it in these variable
        self.name_db = QtWidgets.QLabel(self.profile_frame)
        self.name_db.setGeometry(QtCore.QRect(10, 170, 191, 20))
        self.name_db.setStyleSheet("border: none;\ncolor: white;")
        self.name_db.setAlignment(QtCore.Qt.AlignCenter)
        self.name_db.setObjectName("name_db")
        self.id_db = QtWidgets.QLabel(self.profile_frame)
        self.id_db.setGeometry(QtCore.QRect(10, 220, 191, 20))
        self.id_db.setStyleSheet("border: none;\ncolor: white;")
        self.id_db.setAlignment(QtCore.Qt.AlignCenter)
        self.id_db.setObjectName("id_db")
        self.department_db = QtWidgets.QLabel(self.profile_frame)
        self.department_db.setGeometry(QtCore.QRect(10, 270, 191, 20))
        self.department_db.setStyleSheet("border: none;\ncolor: white;")
        self.department_db.setAlignment(QtCore.Qt.AlignCenter)
        self.department_db.setObjectName("department_db")
        cursor.execute("SELECT name, employeeID, departmentName FROM employee e, department d WHERE e.departmentID="
                       "d.departmentID AND employeeID = ?", (employeeID, ))
        info = cursor.fetchone()
        self.id = str(info[1])
        self.name_db.setText(info[0])
        self.id_db.setText(str(info[1]))
        self.department_db.setText(info[2])

        # View my training button
        self.my_training_button = QtWidgets.QPushButton(self.side_frame)
        self.my_training_button.setGeometry(QtCore.QRect(14, 450, 211, 91))
        self.my_training_button.setStyleSheet("color: white;\nfont-weight: ;\nborder-radius: 10px;")
        self.my_training_button.setObjectName("my_training_button")

        # View whole training lists button
        self.list_button = QtWidgets.QPushButton(self.side_frame)
        self.list_button.setGeometry(QtCore.QRect(14, 350, 211, 91))
        self.list_button.setStyleSheet("color: white;\nfont-weight: ;\nborder-radius: 10px;")
        self.list_button.setObjectName("list_button")

        # Notification button
        self.notification_button = QtWidgets.QPushButton(self.side_frame)
        self.notification_button.setGeometry(QtCore.QRect(14, 550, 211, 91))
        self.notification_button.setStyleSheet("color: white;\nfont-weight: ;\nborder-radius: 10px;")
        self.notification_button.setObjectName("notification_button")

        # Log out button
        self.logout_button = QtWidgets.QPushButton(self.side_frame)
        self.logout_button.setGeometry(QtCore.QRect(14, 650, 51, 41))
        self.logout_button.setStyleSheet("border: none;\nborder-radius: 50%;")
        self.logout_button.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("logout.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.logout_button.setIcon(icon1)
        self.logout_button.setIconSize(QtCore.QSize(45, 45))
        self.logout_button.setObjectName("logout_button")

        # Notification dot
        self.notification_menu_dot = QtWidgets.QLabel(self.side_frame)
        self.notification_menu_dot.setGeometry(QtCore.QRect(170, 570, 21, 21))
        self.notification_menu_dot.setStyleSheet("border: none;")
        self.notification_menu_dot.setText("")
        self.notification_menu_dot.setScaledContents(True)
        self.notification_menu_dot.setObjectName("notification_menu_dot")
        cursor.execute("SELECT count(is_read) FROM notification WHERE employeeID=? AND is_read=0", self.id)
        unread = cursor.fetchone()[0]
        if unread > 0:
            self.notification_menu_dot.setPixmap(QtGui.QPixmap("dot.webp"))
        else:
            self.notification_menu_dot.clear()
        self.horizontalLayout.addWidget(self.side_frame)

        # Right frame
        self.main_frame = QtWidgets.QFrame(self.centralwidget)
        self.main_frame.setStyleSheet("border: 1px solid white;")
        self.main_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.main_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.main_frame.setObjectName("main_frame")

        # Title for the page
        # need to reset the title after switch tab
        self.header = QtWidgets.QLabel(self.main_frame)
        self.header.setGeometry(QtCore.QRect(14, 14, 971, 81))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.header.sizePolicy().hasHeightForWidth())
        self.header.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(22)
        font.setBold(True)
        font.setWeight(75)
        self.header.setFont(font)
        self.header.setStyleSheet("border: none;\nborder-bottom: 1px solid white;\ncolor: white;\nfont-weight: ;\n")
        self.header.setText("Notification")
        self.header.setObjectName("header")

        # Define the size and position of each frame
        cursor.execute("SELECT t.trainingName, n.notification_status, n.notification_date, n.is_read FROM training t, "
                       "notification n, employee e WHERE n.trainingID=t.trainingID AND n.employeeID=e.employeeID AND "
                       "n.employeeID=? ORDER BY n.notificationID DESC", (employeeID, ))
        data = cursor.fetchall()
        self.rows = len(data)

        # scrolling area to display lists of trainings
        self.scrollArea = QtWidgets.QScrollArea(self.main_frame)
        self.scrollArea.setGeometry(QtCore.QRect(14, 99, 971, 581))
        self.scrollArea.setStyleSheet("border: none;")
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 945, self.rows * (91+19)))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")

        self.logout_button.clicked.connect(gotologin)
        self.profile_button.clicked.connect(self.gotoProfile)
        self.notification_button.clicked.connect(gotoNotification)
        self.list_button.clicked.connect(gotoview)
        self.my_training_button.clicked.connect(gotoTraining)
        cursor.execute('SELECT name, employeeID, departmentID FROM employee WHERE employeeID = ?', (employeeID, )) 
        display = cursor.fetchall()
        self.employeeID = display[0][1]
        self.name_db.setText(display[0][0])   
        self.id_db.setText(str(display[0][1]))
        cursor.execute('SELECT departmentName FROM department WHERE departmentID=?', (display[0][2],))
        self.department_db.setText(cursor.fetchone()[0])
        self.profile_button.setIcon(QtGui.QIcon("pictures/profile.png"))
        self.logout_button.setIcon(QtGui.QIcon("pictures/logout.png"))

        # template for each the notification
        for row in range(self.rows):
            date_time = datetime.strptime(data[row][2], "%d-%m-%Y %H:%M")
            date = date_time.strftime("%d %B %Y")
            time = date_time.strftime("%H:%M")
            self.notification_frame = QtWidgets.QFrame(self.scrollAreaWidgetContents_2)
            self.notification_frame.setGeometry(QtCore.QRect(10, row * (91+19), 921, 91))
            self.notification_frame.setStyleSheet("border: 1px solid white;\nborder-radius: 10px;")
            self.notification_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
            self.notification_frame.setFrameShadow(QtWidgets.QFrame.Raised)
            self.notification_frame.setObjectName("notification_frame")
            self.status_image = QtWidgets.QLabel(self.notification_frame)
            self.status_image.setGeometry(QtCore.QRect(15, 10, 75, 75))
            self.status_image.setStyleSheet("border: none;")
            self.status_image.setText("")
            self.status_image.setScaledContents(True)
            self.status_image.setObjectName("status_image")
            if data[row][1] == "pending":
                self.status_image.setPixmap(QtGui.QPixmap("pictures/pending.png"))
            elif data[row][1] == "approved":
                self.status_image.setPixmap(QtGui.QPixmap("pictures/success.png"))
            else:
                self.status_image.setPixmap(QtGui.QPixmap("pictures/reject.png"))
            self.training_name = QtWidgets.QLabel(self.notification_frame)
            self.training_name.setGeometry(QtCore.QRect(110, 3, 721, 31))
            font = QtGui.QFont()
            font.setPointSize(10)
            font.setBold(True)
            font.setWeight(75)
            self.training_name.setFont(font)
            self.training_name.setStyleSheet("border: none;\ncolor: white;")
            self.training_name.setText(data[row][0])
            self.training_name.setObjectName("training_name")
            self.time = QtWidgets.QLabel(self.notification_frame)
            self.time.setGeometry(QtCore.QRect(810, 40, 68, 19))
            font = QtGui.QFont()
            font.setPointSize(8)
            font.setBold(False)
            font.setWeight(50)
            self.time.setFont(font)
            self.time.setStyleSheet("border: none;\ncolor: white;")
            self.time.setText(time)
            self.time.setAlignment(QtCore.Qt.AlignCenter)
            self.time.setObjectName("time")
            self.notification_text = QtWidgets.QLabel(self.notification_frame)
            self.notification_text.setGeometry(QtCore.QRect(110, 33, 721, 51))
            font = QtGui.QFont()
            font.setPointSize(10)
            font.setBold(False)
            font.setWeight(50)
            self.notification_text.setFont(font)
            self.notification_text.setStyleSheet("border: none;\ncolor: white;")
            if data[row][1] == "pending":
                self.notification_text.setText("The request to join the training is pending. Will notify you later when"
                                               " the request is approved or rejected.")
            elif data[row][1] == "approved":
                self.notification_text.setText("You are successfully approved by HR department to join the training.")
            elif data[row][1] == "rejected":
                self.notification_text.setText("You are rejected by HR department to join the training.")
            else:
                self.notification_text.setText("The training cancelled.")
            self.notification_text.setScaledContents(False)
            self.notification_text.setWordWrap(True)
            self.notification_text.setObjectName("notification_text")
            self.date = QtWidgets.QLabel(self.notification_frame)
            self.date.setGeometry(QtCore.QRect(758, 60, 161, 20))
            font = QtGui.QFont()
            font.setBold(False)
            font.setWeight(50)
            self.date.setFont(font)
            self.date.setStyleSheet("border: none;\ncolor: white;")
            self.date.setText(date)
            self.date.setAlignment(QtCore.Qt.AlignCenter)
            self.date.setObjectName("date")
            self.notification_dot = QtWidgets.QLabel(self.notification_frame)
            self.notification_dot.setGeometry(QtCore.QRect(880, 10, 21, 21))
            self.notification_dot.setStyleSheet("border: none;")
            self.notification_dot.setText("")
            self.notification_dot.setScaledContents(True)
            self.notification_dot.setObjectName("notification_dot")
            if data[row][3] == 0:
                self.notification_dot.setPixmap(QtGui.QPixmap("dot.webp"))
            else:
                self.notification_dot.clear()
            self.status_image.raise_()
            self.training_name.raise_()
            self.notification_text.raise_()
            self.date.raise_()
            self.time.raise_()
            self.notification_dot.raise_()

        # Adjust the size of the scroll area's contents
        self.scrollAreaWidgetContents_2.setMinimumHeight(self.rows * (91+19))

        # scroll bar
        self.scrollArea.setWidget(self.scrollAreaWidgetContents_2)

        # search input and button
        self.search_button = QtWidgets.QPushButton(self.main_frame)
        self.search_button.setGeometry(QtCore.QRect(950, 57, 31, 34))
        self.search_button.setStyleSheet("border: none;")
        self.search_button.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("search.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.search_button.setIcon(icon2)
        self.search_button.setIconSize(QtCore.QSize(25, 25))
        self.search_button.setObjectName("search_button")
        self.search_bar = QtWidgets.QLineEdit(self.main_frame)
        self.search_bar.setGeometry(QtCore.QRect(805, 60, 141, 25))
        self.search_bar.setStyleSheet("QLineEdit {color: white;}\nQLineEdit::placeholder {color: white;}\nQLineEdit "
                                      "{border-radius: 10px;\nborder: 1px solid white;}\n")
        self.search_bar.setObjectName("search_bar")
        self.search_button.clicked.connect(self.search_notification)

        # update the notification has been read
        cursor.execute("UPDATE notification SET is_read=1 WHERE is_read=0 AND employeeID=?", self.id)
        connect.commit()

        self.horizontalLayout.addWidget(self.main_frame)

        self.retranslateUi()
    

    def search_notification(self):
        try:
            # remove the notification frame and child widgets
            for frame in self.scrollAreaWidgetContents_2.findChildren(QtWidgets.QFrame):
                # Remove child widgets from the frame
                for child_widget in frame.children():
                    child_widget.deleteLater()
                # Remove the frame itself
                frame.deleteLater()
        except:
            pass
        keywords = self.search_bar.text()
        cursor.execute("SELECT t.trainingName, n.notification_status, n.notification_date FROM training t, notification"
                       " n, employee e WHERE n.trainingID=t.trainingID AND n.employeeID=e.employeeID AND n.employeeID=?"
                       " AND (t.trainingName LIKE ? OR n.notification_status LIKE ? OR n.notification_date LIKE ? OR "
                       "strftime('%m', n.notification_date)=strftime('%m', ?)) ORDER BY n.notificationID DESC",
                       (self.id, '%'+keywords+'%', '%'+keywords+'%', '%'+keywords+'%', '%'+keywords+'%'))
        data = cursor.fetchall()
        rows = len(data)

        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 945, rows * (91 + 19)))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        for row in range(rows):
            date_time = datetime.strptime(data[row][2], "%d-%m-%Y %H:%M")
            date = date_time.strftime("%d %B %Y")
            time = date_time.strftime("%H:%M")
            self.notification_frame = QtWidgets.QFrame(self.scrollAreaWidgetContents_2)
            self.notification_frame.setGeometry(QtCore.QRect(10, row * (91 + 19), 921, 91))
            self.notification_frame.setStyleSheet("border: 1px solid white;\nborder-radius: 10px;")
            self.notification_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
            self.notification_frame.setFrameShadow(QtWidgets.QFrame.Raised)
            self.notification_frame.setObjectName("notification_frame")
            self.status_image = QtWidgets.QLabel(self.notification_frame)
            self.status_image.setGeometry(QtCore.QRect(15, 10, 75, 75))
            self.status_image.setStyleSheet("border: none;")
            self.status_image.setText("")
            self.status_image.setScaledContents(True)
            self.status_image.setObjectName("status_image")
            if data[row][1] == "pending":
                self.status_image.setPixmap(QtGui.QPixmap("pending.png"))
            elif data[row][1] == "approved":
                self.status_image.setPixmap(QtGui.QPixmap("success.png"))
            else:
                self.status_image.setPixmap(QtGui.QPixmap("reject.png"))
            self.training_name = QtWidgets.QLabel(self.notification_frame)
            self.training_name.setGeometry(QtCore.QRect(110, 3, 721, 31))
            font = QtGui.QFont()
            font.setPointSize(10)
            font.setBold(True)
            font.setWeight(75)
            self.training_name.setFont(font)
            self.training_name.setStyleSheet("border: none;\ncolor: white;")
            self.training_name.setText(data[row][0])
            self.training_name.setObjectName("training_name")
            self.time = QtWidgets.QLabel(self.notification_frame)
            self.time.setGeometry(QtCore.QRect(810, 40, 68, 19))
            font = QtGui.QFont()
            font.setPointSize(8)
            font.setBold(False)
            font.setWeight(50)
            self.time.setFont(font)
            self.time.setStyleSheet("border: none;\ncolor: white;")
            self.time.setText(time)
            self.time.setAlignment(QtCore.Qt.AlignCenter)
            self.time.setObjectName("time")
            self.notification_text = QtWidgets.QLabel(self.notification_frame)
            self.notification_text.setGeometry(QtCore.QRect(110, 33, 721, 51))
            font = QtGui.QFont()
            font.setPointSize(10)
            font.setBold(False)
            font.setWeight(50)
            self.notification_text.setFont(font)
            self.notification_text.setStyleSheet("border: none;\ncolor: white;")
            if data[row][1] == "pending":
                self.notification_text.setText("The request to join the training is pending. Will notify you later when"
                                               " the request is approved or rejected.")
            elif data[row][1] == "approved":
                self.notification_text.setText("You are successfully approved by HR department to join the training.")
            elif data[row][1] == "rejected":
                self.notification_text.setText("You are rejected by HR department to join the training.")
            else:
                self.notification_text.setText("The training cancelled.")
            self.notification_text.setScaledContents(False)
            self.notification_text.setWordWrap(True)
            self.notification_text.setObjectName("notification_text")
            self.date = QtWidgets.QLabel(self.notification_frame)
            self.date.setGeometry(QtCore.QRect(758, 60, 161, 20))
            font = QtGui.QFont()
            font.setBold(False)
            font.setWeight(50)
            self.date.setFont(font)
            self.date.setStyleSheet("border: none;\ncolor: white;")
            self.date.setText(date)
            self.date.setAlignment(QtCore.Qt.AlignCenter)
            self.date.setObjectName("date")
            self.status_image.raise_()
            self.training_name.raise_()
            self.notification_text.raise_()
            self.date.raise_()
            self.time.raise_()

        # Adjust the size of the scroll area's contents
        self.scrollAreaWidgetContents_2.setMinimumHeight(rows * (91 + 19))

        # scroll bar
        self.scrollArea.setWidget(self.scrollAreaWidgetContents_2)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.name_label.setText(_translate("MainWindow", "Name"))
        self.staff_id_label.setText(_translate("MainWindow", "Staff ID"))
        self.department_label.setText(_translate("MainWindow", "Department"))
        self.my_training_button.setText(_translate("MainWindow", "My Training"))
        self.list_button.setText(_translate("MainWindow", "Training List"))
        self.notification_button.setText(_translate("MainWindow", "Notification"))
        self.search_bar.setPlaceholderText(_translate("MainWindow", "  Search..."))
    
    def gotoProfile(self):
        #make a popup window to view profile information
        self.profile = Profile()
        self.profile.show()

        
class MyTraining(QMainWindow):
    def __init__(self):
        super(MyTraining, self).__init__()

        loadUi("mytraining.ui", self)
        self.logout_button.clicked.connect(gotologin)
        self.profile_button.clicked.connect(self.gotoProfile)
        self.notification_button.clicked.connect(gotoNotification)
        self.list_button.clicked.connect(gotoview)
        self.my_training_button.clicked.connect(gotoTraining)
        cursor.execute('SELECT name, employeeID, departmentID FROM employee WHERE employeeID = ?', (employeeID, )) 
        display = cursor.fetchall()
        self.employeeID = display[0][1]
        self.name_db.setText(display[0][0])   
        self.id_db.setText(str(display[0][1]))
        cursor.execute('SELECT departmentName FROM department WHERE departmentID=?', (display[0][2],))
        self.department_db.setText(cursor.fetchone()[0])
        self.profile_button.setIcon(QtGui.QIcon("pictures/profile.png"))
        self.logout_button.setIcon(QtGui.QIcon("pictures/logout.png"))

        # Define the size and position of each frame
        frame_width = 931
        frame_height = 251
        frame_spacing = 20

        # Right frame
        self.main_frame = QtWidgets.QFrame(self.centralwidget)
        self.main_frame.setStyleSheet("border: 1px solid white;")
        self.main_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.main_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.main_frame.setObjectName("main_frame")

        # Title for the page
        # need to reset the title after switch tab
        self.header = QtWidgets.QLabel(self.main_frame)
        self.header.setGeometry(QtCore.QRect(10, 10, 971, 81))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.header.sizePolicy().hasHeightForWidth())
        self.header.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(22)

        font.setWeight(75)
        self.header.setFont(font)
        self.header.setStyleSheet("border: none;\nborder-bottom: 1px solid white;\ncolor: white;")
        self.header.setText("My Training")  # here to set the title
        self.header.setObjectName("header")

        # scrolling area to display lists of trainings
        self.scrollArea = QtWidgets.QScrollArea(self.main_frame)
        self.scrollArea.setGeometry(QtCore.QRect(14, 99, 971, 581))
        self.scrollArea.setStyleSheet("border: none;")
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")

        # search input and button
        self.search_bar = QtWidgets.QLineEdit(self.main_frame)
        self.search_bar.setGeometry(QtCore.QRect(805, 60, 141, 25))
        self.search_bar.setStyleSheet("QLineEdit {color: white;}\nQLineEdit::placeholder {color: white;}\nQLineEdit "
                                      "{border-radius: 10px;\nborder: 1px solid white;}\n")
        self.search_bar.setObjectName("search_bar")
        self.search_button = QtWidgets.QPushButton(self.main_frame)
        self.search_button.setGeometry(QtCore.QRect(950, 57, 31, 34))
        self.search_button.setStyleSheet("border: none;")
        self.search_button.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("pictures/search.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.search_button.setIcon(icon2)
        self.search_button.setIconSize(QtCore.QSize(25, 25))
        self.search_bar.setPlaceholderText("  Search...")
        self.search_button.setObjectName("search_button")
        self.search_button.clicked.connect(self.searchTraining)

        self.horizontalLayout.addWidget(self.main_frame)
        self.setCentralWidget(self.centralwidget)

        connectDatabase()
        self.cursor = connect.cursor()
        global employee_id
        employee_id = 1  # Change this to the desired employee ID
        self.cursor.execute(
            "SELECT t.trainingID, t.trainingName, d.departmentName, t.short_description, t.brochure, a.applicationStatus "
            "FROM application a "
            "JOIN training t ON a.trainingID = t.trainingID "
            "JOIN department d ON d.departmentID = t.departmentID "
            "WHERE a.employeeID = ?", (employeeID,))
        row_data = self.cursor.fetchall()  # Fetch all rows of data
        rows = len(row_data)  # Calculate the length of fetched data


        # Scroll area content widget
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, frame_width, rows *
                                                                 (frame_height + frame_spacing)))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")

        # Loop to create and position the frames
        for item in range(rows):
            status = row_data[item][5]

            self.training = QtWidgets.QFrame(self.scrollAreaWidgetContents_2)
            self.training.setGeometry(QtCore.QRect(0, item * (frame_height + frame_spacing), frame_width, frame_height))
            self.training.setStyleSheet("border: 1px solid white;\nbackground: #8A8A8A;\nborder-radius: 10px;")
            self.training.setFrameShape(QtWidgets.QFrame.StyledPanel)
            self.training.setFrameShadow(QtWidgets.QFrame.Raised)
            self.training.setObjectName("training")


            blob_data = row_data[item][4]

            image = Image.open(BytesIO(blob_data))
            image.save(f"pictures/image{item}.png", "PNG")

            self.training_image = QtWidgets.QLabel(self.training)

            self.training_image.setGeometry(QtCore.QRect(20, 10, 200, 150))
            self.training_image.setScaledContents(True)
            self.training_image.setPixmap(QtGui.QPixmap(f"pictures/image{item}.png"))  # here to set the data from database
            self.training_image.setObjectName(f"training_image_{item}")

            self.department_label_2 = QtWidgets.QLabel(self.training)
            self.department_label_2.setGeometry(QtCore.QRect(230, 50, 111, 31))
            font = QtGui.QFont()
            font.setBold(True)
            font.setWeight(75)
            self.department_label_2.setFont(font)
            self.department_label_2.setStyleSheet("color: white;\nborder: none;")
            self.department_label_2.setText("Department: ")
            self.department_label_2.setObjectName("department_label_2")

            self.department_db_2 = QtWidgets.QLabel(self.training)
            self.department_db_2.setGeometry(QtCore.QRect(340, 50, 581, 31))
            font = QtGui.QFont()
            font.setPointSize(8)
            font.setBold(False)
            font.setWeight(50)
            self.department_db_2.setFont(font)
            self.department_db_2.setStyleSheet("color: white;\nfont-weight: regular;\nborder: none;")
            self.department_db_2.setText(f"{row_data[item][2]}")
            self.department_db_2.setObjectName("department_db_2")

            self.description_label = QtWidgets.QLabel(self.training)
            self.description_label.setGeometry(QtCore.QRect(230, 80, 101, 21))
            font = QtGui.QFont()
            font.setBold(True)
            font.setWeight(75)
            self.description_label.setFont(font)
            self.description_label.setStyleSheet("color: white;\nfont-weight: ;\nborder: none;")
            self.description_label.setText("Description: ")
            self.description_label.setObjectName("description_label")

            self.description_db = QtWidgets.QLabel(self.training)
            self.description_db.setGeometry(QtCore.QRect(230, 100, 691, 81))
            self.description_db.setStyleSheet("color: white;\nfont-weight: regular;\nborder: none;")
            self.description_db.setText(f"{row_data[item][3]}")
            self.description_db.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
            self.description_db.setWordWrap(True)
            self.description_db.setObjectName("description_db")

            self.status_label = QtWidgets.QLabel(self.training)
            self.status_label.setGeometry(QtCore.QRect(835, 150, 85, 40))
            font = QtGui.QFont()
            font.setBold(True)
            font.setWeight(85)
            self.status_label.setFont(font)
            self.status_label.setStyleSheet("color: white;\nfont-weight: ;\nborder: none;")
            self.status_label.setText("Status: \n" + status)
            self.status_label.setObjectName("status_label")

            self.view_button = QtWidgets.QPushButton(self.training)
            self.view_button.setGeometry(QtCore.QRect(810, 200, 112, 34))
            self.view_button.setStyleSheet(
                "color: white;\nfont-weight: ;\nborder-radius: 10px;\nbackground: #008287;")
            self.view_button.setText("View More")
            self.view_button.setObjectName("view_button")
            self.view_button.clicked.connect(lambda _, training_id=row_data[item][0]:
                                             self.viewTrainingDetails(training_id))
            

            self.training_name_db = QtWidgets.QPushButton(self.training)
            self.training_name_db.setGeometry(QtCore.QRect(230, 20, 691, 31))
            font = QtGui.QFont()
            font.setPointSize(12)
            font.setBold(True)
            font.setWeight(75)
            self.training_name_db.setFont(font)
            self.training_name_db.setStyleSheet("color: white;\nfont-weight: ;\nborder: none;\ntext-align: left;\n")
            self.training_name_db.setText(f"{row_data[item][1]}")
            self.training_name_db.setObjectName("training_name_db")
            self.training_name_db.clicked.connect(lambda _, training_id=row_data[item][0]:
                                                  self.viewTrainingDetails(training_id))

        # Adjust the size of the scroll area's contents
        self.scrollAreaWidgetContents_2.setMinimumHeight(rows * (frame_height + frame_spacing))

        # Set the initial training items using row_data
        self.updateSearchResults(row_data)

        # Set the scroll area widget
        self.scrollArea.setWidget(self.scrollAreaWidgetContents_2)
        self.setCentralWidget(self.centralwidget)
        QtCore.QMetaObject.connectSlotsByName(self)

    def gotoProfile(self):
        #make a popup window to view profile information
        self.profile = Profile()
        self.profile.show()

    def viewTrainingDetails(self, trainingID):

        try:
            print("Clicked ID:", trainingID)
            loadUi("training_details.ui", self)
            self.logout_button.clicked.connect(gotologin)
            self.profile_button.clicked.connect(self.gotoProfile)
            self.notification_button.clicked.connect(gotoNotification)
            self.list_button.clicked.connect(gotoview)
            self.my_training_button.clicked.connect(gotoTraining)
            connectDatabase()
            cursor.execute('SELECT name, employeeID, departmentID FROM employee WHERE employeeID = ?', (employeeID,))
            display = cursor.fetchall()
            self.name_db.setText(display[0][0])
            self.id_db.setText(str(display[0][1]))
            cursor.execute('SELECT departmentName FROM department WHERE departmentID=?', (display[0][2],))
            self.department_db.setText(cursor.fetchone()[0])
            self.profile_button.setIcon(QtGui.QIcon("pictures/profile.png"))
            self.header.setText("Training Details")

            self.cursor = connect.cursor()
            self.cursor.execute(
                "SELECT t.trainingName, t.status, t.cost, t.date, t.time, t.venue,t.duration, d.departmentName, t.short_description, t.brochure, t.max_par "
                "FROM training t, department d WHERE d.departmentID = t.departmentID AND t.trainingID = ?",
                (trainingID,))
            display = self.cursor.fetchall()
            #Result of display = [('Training 1', 'Pending', 100, '2021-04-01', '09:00:00', 'IT', 'Short description', 'Brochure')]
            self.training.setText(f"{display[0][0]}")

            date = datetime.strptime(display[0][3], "%d-%m-%Y")
            date = date.strftime("%d %B %Y")
            time = datetime.strptime(display[0][4], "%H:%M")
            time = time.strftime("%H:%M")
            self.date_db.setText(f"{date}")
            self.time_db.setText(f"{time}")
            self.venue_db.setText(f"{display[0][5]}")
            self.duration_db.setText(f"{display[0][6]}")
            self.department_db_2.setText(f"{display[0][7]}")
            self.description_db.setText(f"{display[0][8]}")

            self.brochure_button.setIconSize(QtCore.QSize(200, 200))
            self.brochure_button.setIcon(QtGui.QIcon(f"pictures/image{trainingID}.png"))
            self.brochure_button.clicked.connect(lambda: self.showImagePopUp(f"pictures/image{trainingID}.png"))

            self.register_button.hide()

            self.number_participants_db.setText(f"{display[0][10]}")


        except Exception as e:
            logging.exception("An error occurred in viewTrainingDetails:")

    def searchTraining(self):
        try:
            keywords = self.search_bar.text()

            # Query the database based on the keywords
            connectDatabase()
            self.cursor.execute(
                "SELECT DISTINCT a.trainingID, t.trainingName, d.departmentName, t.short_description, t.brochure, "
                "a.applicationStatus FROM training t "
                "JOIN department d ON d.departmentID = t.departmentID "
                "JOIN application a ON a.trainingID = t.trainingID "
                "WHERE (t.trainingName LIKE ? OR d.departmentName LIKE ? "
                "OR t.date LIKE ? OR t.time LIKE ?) AND a.employeeID = ?",
                ('%' + keywords + '%', '%' + keywords + '%', '%' + keywords + '%',
                 '%' + keywords + '%', employee_id))
            search_results = self.cursor.fetchall()

            # Display the search results
            self.updateSearchResults(search_results)

        except Exception as e:
            # Show error message box or print the error
            error_message = "An error occurred: " + str(e)


    def updateSearchResults(self, search_results):
        # self.items = search_results
        n = len(search_results)
        # Define the size and position of each frame
        frame_width = 931
        frame_height = 251
        frame_spacing = 20

        # Clear the existing contents of the scroll area
        for frame in self.scrollAreaWidgetContents_2.findChildren(QtWidgets.QFrame):
            # Remove child widgets from the frame
            for child_widget in frame.children():
                child_widget.deleteLater()
            # Remove the frame itself
            frame.deleteLater()

        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, frame_width,
                                                                 n * (frame_height + frame_spacing)))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")

        # Loop to create and position the frames for search results
        for item in range(n):
            status = search_results[item][5]

            self.training = QtWidgets.QFrame(self.scrollAreaWidgetContents_2)
            self.training.setGeometry(QtCore.QRect(0, item * (frame_height + frame_spacing), frame_width, frame_height))
            self.training.setStyleSheet("border: 1px solid white;\nbackground: #8A8A8A;\nborder-radius: 10px;")
            self.training.setFrameShape(QtWidgets.QFrame.StyledPanel)
            self.training.setFrameShadow(QtWidgets.QFrame.Raised)
            self.training.setObjectName("training")
            
            blob_data = search_results[item][4]

            image = Image.open(BytesIO(blob_data))
            image.save(f"pictures/image{item}.png", "PNG")

            self.training_image = QtWidgets.QLabel(self.training)

            self.training_image.setGeometry(QtCore.QRect(20, 10, 200, 150))
            self.training_image.setScaledContents(True)
            self.training_image.setPixmap(QtGui.QPixmap(f"pictures/image{item}.png"))  # here to set the data from database
            self.training_image.setObjectName(f"training_image_{item}")

            self.department_label_2 = QtWidgets.QLabel(self.training)
            self.department_label_2.setGeometry(QtCore.QRect(230, 50, 111, 31))
            font = QtGui.QFont()
            font.setBold(True)
            font.setWeight(75)
            self.department_label_2.setFont(font)
            self.department_label_2.setStyleSheet("color: white;\nfont-weight: ;\nborder: none;")
            self.department_label_2.setText("Department: ")
            self.department_label_2.setObjectName("department_label_2")

            self.department_db_2 = QtWidgets.QLabel(self.training)
            self.department_db_2.setGeometry(QtCore.QRect(340, 50, 581, 31))
            font = QtGui.QFont()
            font.setPointSize(8)
            font.setBold(False)
            font.setWeight(50)
            self.department_db_2.setFont(font)
            self.department_db_2.setStyleSheet("color: white;\nfont-weight: regular;\nborder: none;\: none;")
            self.department_db_2.setText(f"{search_results[item][2]}")
            self.department_db_2.setObjectName("department_db_2")

            self.description_label = QtWidgets.QLabel(self.training)
            self.description_label.setGeometry(QtCore.QRect(230, 80, 101, 21))
            font = QtGui.QFont()
            font.setBold(True)
            font.setWeight(75)
            self.description_label.setFont(font)
            self.description_label.setStyleSheet("color: white;\nfont-weight: ;\nborder: none;")
            self.description_label.setText("Description: ")
            self.description_label.setObjectName("description_label")

            self.description_db = QtWidgets.QLabel(self.training)
            self.description_db.setGeometry(QtCore.QRect(230, 100, 691, 81))
            self.description_db.setStyleSheet("color: white;\nfont-weight: regular;\nborder: none;")
            self.description_db.setText(f"{search_results[item][3]}")
            self.description_db.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
            self.description_db.setWordWrap(True)
            self.description_db.setObjectName("description_db")

            self.status_label = QtWidgets.QLabel(self.training)
            self.status_label.setGeometry(QtCore.QRect(835, 150, 85, 40))
            font = QtGui.QFont()
            font.setBold(True)
            font.setWeight(85)
            self.status_label.setFont(font)
            self.status_label.setStyleSheet("color: white;\nfont-weight: ;\nborder: none;")
            self.status_label.setText("Status: \n" + status)
            self.status_label.setObjectName("status_label")

            self.view_button = QtWidgets.QPushButton(self.training)
            self.view_button.setGeometry(QtCore.QRect(810, 200, 112, 34))
            self.view_button.setStyleSheet(
                "color: white;\nfont-weight: ;\nborder-radius: 10px;\nbackground: #008287;")
            self.view_button.setText("View More")
            self.view_button.setObjectName("view_button")
            self.view_button.clicked.connect(lambda _, training_id=search_results[item][0]:
                                             self.viewTrainingDetails(training_id))

            self.training_name_db = QtWidgets.QPushButton(self.training)
            self.training_name_db.setGeometry(QtCore.QRect(230, 20, 691, 31))
            font = QtGui.QFont()
            font.setPointSize(12)
            font.setBold(True)
            font.setWeight(75)
            self.training_name_db.setFont(font)
            self.training_name_db.setStyleSheet("color: white;\nfont-weight: ;\nborder: none;\ntext-align: left;\n")
            self.training_name_db.setText(f"{search_results[item][1]}")
            self.training_name_db.setObjectName("training_name_db")
            self.training_name_db.clicked.connect(lambda _, training_id=search_results[item][0]:
                                                  self.viewTrainingDetails(training_id))

        # Adjust the size of the scroll area's contents
        self.scrollAreaWidgetContents_2.setMinimumHeight(n * (frame_height + frame_spacing))

        # Set the scroll area widget
        self.scrollArea.setWidget(self.scrollAreaWidgetContents_2)

            
    def showImagePopUp(self, pictureName):
        popup = ImagePopup(self)
        popup.setImage(QtGui.QPixmap(pictureName))
        popup.show()
            
def gotoview():
        viewtraining = View()
        widget.addWidget(viewtraining)
        widget.setCurrentIndex(widget.currentIndex()+1)

def gotoNotification():
        mainwindow = Notification()
        widget.addWidget(mainwindow)
        widget.setCurrentIndex(widget.currentIndex()+1)

def gotologin():
        login = Login()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex()+1)

def gotoTraining():
        training = MyTraining()
        widget.addWidget(training)
        widget.setCurrentIndex(widget.currentIndex()+1)

def gotoHrView():
        hrview = HrView()
        widget.addWidget(hrview)
        widget.setCurrentIndex(widget.currentIndex()+1)


app = QApplication(sys.argv)

mainwindow = Login()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedWidth(1280)
widget.setFixedHeight(720)
widget.show()
app.exec_()

