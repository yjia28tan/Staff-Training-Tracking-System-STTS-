import logging
import datetime
from PyQt5 import Qt, uic
from PyQt5.QtCore import QSize, QRect, QMetaObject, QCoreApplication, Qt
from PyQt5.QtGui import QPixmap, QIcon, QFont
from PyQt5.QtWidgets import QApplication, QWidget, QFrame, QHBoxLayout, QSizePolicy, QPushButton, QLabel, QScrollArea, \
    QLineEdit, QMessageBox, QMainWindow
from PyQt5.uic import loadUi
import sys
import sqlite3
from PyQt5 import QtWidgets
from qtpy import QtCore, QtGui


def connectDatabase():
    try:
        global connect
        global cursor
        # connect to database
        connect = sqlite3.connect("StaffTrainingSystem")
        cursor = connect.cursor()
    except ConnectionError:
        # Show error message box
        QMessageBox.critical(None, "Error", "Cannot connect to database!", QMessageBox.Ok)


class HR_Training(QtWidgets.QMainWindow):
    def __init__(self):
        super(HR_Training, self).__init__()
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

            self.training_image = QLabel(self.training)
            self.training_image.setObjectName(u"training_image")
            self.training_image.setGeometry(QRect(20, 10, 200, 150))
            self.training_image.setPixmap(QtGui.QPixmap(f"pictures/image{row_data[item][4]}.png"))

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
                self.view_more_button.setText("Modify")
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

            self.training_image = QLabel(self.training)
            self.training_image.setObjectName(u"training_image")
            self.training_image.setGeometry(QRect(20, 10, 200, 150))
            self.training_image.setPixmap(QtGui.QPixmap(f"pictures/image{search_results[item][4]}.png"))

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

            self.description_db = QLabel(self.training)
            self.description_db.setObjectName(u"description_db")
            self.description_db.setGeometry(QRect(230, 100, 691, 81))
            self.description_db.setStyleSheet(u"color: white;\n"
                                              "font-weight: regular;\n"
                                              "border: none;")
            self.description_db.setAlignment(Qt.AlignLeft | Qt.AlignTop)
            self.description_db.setWordWrap(True)
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
            dialog = CreateNewTraining(self)
            dialog.exec_()
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

    def modify_training(self, training_id):
        pass

    def view_training(self, training_id):
        pass

    def approve_training(self, training_id):
        pass

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

                self.training_image = QLabel(self.training)
                self.training_image.setObjectName(u"training_image")
                self.training_image.setGeometry(QRect(20, 10, 200, 150))
                self.training_image.setPixmap(QtGui.QPixmap(f"pictures/image{row_data[item][4]}.png"))

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
                    self.view_more_button.setText("Modify")
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

            # Set the scroll area widget
            self.scrollArea.setWidget(self.scrollAreaWidgetContents_2)

        except Exception as e:
            # Show error message box or print the error
            error_message = "An error occurred: " + str(e)
            # QMessageBox.critical(self, "Error", error_message, QMessageBox.Ok)

class CreateNewTraining(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        print("called class create training")

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
        current_date = datetime.date.today()
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

        self.description = QtWidgets.QLabel(self.main_frame)
        self.description.setGeometry(QtCore.QRect(430, 440, 371, 211))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.description.setFont(font)
        self.description.setStyleSheet("borde: 1px solid white;\n"
                                       "color: black;\n"
                                       "background: white;\n"
                                       "border-radius: 10px;")
        # self.description.setText("")
        self.description.setWordWrap(True)
        self.description.setObjectName("description")

        self.short_description = QtWidgets.QLabel(self.main_frame)
        self.short_description.setGeometry(QtCore.QRect(60, 510, 311, 141))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.short_description.setFont(font)
        self.short_description.setStyleSheet("borde: 1px solid white;\n"
                                             "color: black;\n"
                                             "background: white;\n"
                                             "border-radius: 10px;")
        # self.short_description.setText("")
        self.short_description.setWordWrap(True)
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


if __name__ == "__main__":
    # Create an instance of QApplication
    app = QtWidgets.QApplication(sys.argv)

    # Create an instance of MyTraining
    main_window = HR_Training()

    # Show the main window
    main_window.show()

    # Execute the application
    sys.exit(app.exec_())
