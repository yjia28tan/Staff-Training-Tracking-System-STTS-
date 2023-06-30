import logging
import datetime
from PyQt5 import Qt, uic
from PyQt5.QtCore import QSize, QRect, QMetaObject, QCoreApplication, Qt, QByteArray
from PyQt5.QtGui import QPixmap, QIcon, QFont
from PyQt5.QtWidgets import QWidget, QFrame, QHBoxLayout, QSizePolicy, QPushButton, QLabel, QScrollArea, \
    QLineEdit, QMessageBox
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

        self.search_button.clicked.connect(self.search_training_hr)

        self.create_button.clicked.connect(self.create_new_training)

        connectDatabase()
        self.cursor = connect.cursor()
        self.cursor.execute(
            "SELECT t.trainingID, t.trainingName, d.departmentName, t.short_description, t.brochure, t.max_par, "
            "t.status, t.publish, "
            "CASE WHEN t.date >= DATE('now') THEN t.date ELSE NULL END AS happening_soon_date "
            "FROM training t "
            "JOIN department d ON d.departmentID = t.departmentID "
            "ORDER BY "
            "   CASE WHEN t.status = 'Pending' THEN 0 ELSE 1 END, "
            "   happening_soon_date DESC"
        )
        row_data = self.cursor.fetchall()
        rows = len(row_data)

        self.app_status = "Approved"

        for item in range(rows):
            training_id = row_data[item][0]
            self.cursor.execute("SELECT COUNT(a.applicationID) "
                                "FROM application a "
                                "JOIN training t ON t.trainingID = a.trainingID "
                                "WHERE t.trainingID = ? AND a.applicationStatus = ?",
                                (training_id, self.app_status,))
            application_count = str(self.cursor.fetchone()[0])
            print(application_count)

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
                    "ORDER BY "
                    "   CASE WHEN t.status = 'Pending' THEN 0 ELSE 1 END, "
                    "   happening_soon_date DESC"
                )
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

                self.app_status = "Approved"

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
                    self.training.setGeometry(QRect(0, 50 + (item * (frame_height + frame_spacing)),
                                                    frame_width, frame_height))
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
                        self.view_more_button.clicked.connect(lambda _, trainingid=training_id:
                                                              self.view_training(trainingid))

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
                QMessageBox.critical(self, "Error", error_message, QMessageBox.Ok)

class CreateNewTraining(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

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

        self.duration_label = QtWidgets.QLabel(self.main_frame)
        self.duration_label.setGeometry(QtCore.QRect(860, 140, 71, 31))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.duration_label.setFont(font)
        self.duration_label.setStyleSheet("border: none;\n"
                                          "color: white;")
        self.duration_label.setObjectName("duration_label")
        self.duration_label.setText("Duration")

        self.brochure_label = QtWidgets.QLabel(self.main_frame)
        self.brochure_label.setGeometry(QtCore.QRect(860, 270, 81, 31))
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

        self.duration_pick = QtWidgets.QSpinBox(self.main_frame)
        self.duration_pick.setGeometry(QtCore.QRect(860, 180, 101, 41))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.duration_pick.setFont(font)
        self.duration_pick.setStyleSheet("color:  #00ced1;")
        self.duration_pick.setObjectName("duration_pick")

        self.brochure_button = QtWidgets.QPushButton(self.main_frame)
        self.brochure_button.setGeometry(QtCore.QRect(860, 320, 321, 201))
        self.brochure_button.setStyleSheet("border-radius: 10px;")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("add.png"),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.brochure_button.setIcon(icon)
        self.brochure_button.setIconSize(QtCore.QSize(60, 60))
        self.brochure_button.setObjectName("brochure_button")
        self.brochure_button.clicked.connect(self.add_brochure)

        self.new_training_name = QtWidgets.QLineEdit(self.main_frame)
        self.new_training_name.setGeometry(QtCore.QRect(60, 180, 311, 41))
        self.new_training_name.setStyleSheet("borde: 1px solid white;\n"
                                             "color: black;\n"
                                             "background: white;\n"
                                             "border-radius: 10px;")
        self.new_training_name.setObjectName("new_training_name")

        self.cost = QtWidgets.QLineEdit(self.main_frame)
        self.cost.setGeometry(QtCore.QRect(60, 400, 111, 41))
        self.cost.setStyleSheet("borde: 1px solid white;\n"
                                "color: black;\n"
                                "background: white;\n"
                                "border-radius: 10px;")
        self.cost.setObjectName("cost")

        self.description = QtWidgets.QPlainTextEdit(self.main_frame)
        self.description.setGeometry(QtCore.QRect(430, 440, 371, 211))
        self.description.setStyleSheet("borde: 1px solid white;\n"
                                       "color: black;\n"
                                       "background: white;\n"
                                       "border-radius: 10px;")
        self.description.setObjectName("description")

        self.short_description = QtWidgets.QPlainTextEdit(self.main_frame)
        self.short_description.setGeometry(QtCore.QRect(60, 510, 311, 141))
        self.short_description.setStyleSheet("borde: 1px solid white;\n"
                                             "color: black;\n"
                                             "background: white;\n"
                                             "border-radius: 10px;")
        self.short_description.setObjectName("short_description")

        self.max_participants = QtWidgets.QLineEdit(self.main_frame)
        self.max_participants.setGeometry(QtCore.QRect(220, 400, 111, 41))
        self.max_participants.setStyleSheet("borde: 1px solid white;\n"
                                            "color: black;\n"
                                            "background: white;\n"
                                            "border-radius: 10px;")
        self.max_participants.setObjectName("max_participants")

        self.venue = QtWidgets.QLineEdit(self.main_frame)
        self.venue.setGeometry(QtCore.QRect(60, 290, 311, 41))
        self.venue.setStyleSheet("borde: 1px solid white;\n"
                                 "color: black;\n"
                                 "background: white;\n"
                                 "border-radius: 10px;")
        self.venue.setObjectName("venue")

        connectDatabase()
        self.cursor = connect.cursor()
        self.cursor.execute("SELECT * FROM department")
        department_list = self.cursor.fetchall()

        self.department_pick = QtWidgets.QComboBox(self.main_frame)
        self.department_pick.setGeometry(QtCore.QRect(430, 290, 291, 41))
        self.department_pick.setStyleSheet("color:  #00ced1;")
        self.department_pick.setObjectName("department_pick")
        self.department_pick.addItem("Select Department")  # Add a placeholder item
        self.department_pick.addItems([department[1] for department in department_list])
        self.department_pick.setCurrentText("Select Department")  # Set the default placeholder text

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

        self.create_button2 = QtWidgets.QPushButton(self.main_frame)
        self.create_button2.setGeometry(QtCore.QRect(939, 600, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.create_button2.setFont(font)
        self.create_button2.setText("Create")
        self.create_button2.setStyleSheet("color: white;\n"
                                         "font-weight: bold;\n"
                                         "border-radius: 10px;\n"
                                         "background: #008287;")
        self.create_button2.setObjectName("create_button")
        self.create_button2.clicked.connect(self.create_training)

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

    def add_brochure(self):
        file_dialog = QtWidgets.QFileDialog()
        image_path, _ = file_dialog.getOpenFileName(
            self, "Select Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp)"
        )

        if image_path:
            pixmap = QtGui.QPixmap(image_path)
            self.brochure_button.setIcon(QtGui.QIcon(pixmap))  # Set the selected image as the button's icon
            self.brochure_button.setIconSize(QtCore.QSize(855, 245))

    def create_training(self):
        try:
            # Retrieve input values
            training_name = self.new_training_name.text()
            cost_per_person = self.cost.text()
            date = self.date_pick.date().toPyDate()
            time = self.time_pick.time().toString("HH:mm")
            duration = self.duration_pick.value()
            venue = self.venue.text()
            description_text = self.description.toPlainText()
            short_description_text = self.short_description.toPlainText()
            max_participants = self.max_participants.text()
            department = self.department_pick.currentText()

            # Retrieve the icon image
            brochure_image = self.brochure_button.icon()
            if not brochure_image.isNull():
                pixmap = brochure_image.pixmap(QtCore.QSize(855, 245))  # Adjust the size as needed
                # Convert QPixmap to bytes using QByteArray
                byte_array = QByteArray()
                buffer = QtCore.QBuffer(byte_array)
                buffer.open(QtCore.QIODevice.WriteOnly)
                pixmap.save(buffer, "PNG")  # Save the pixmap as PNG
                image_data = byte_array.data()
            else:
                image_data = None

            # Perform validation for each input field
            if not training_name:
                # Training name is empty
                QtWidgets.QMessageBox.warning(self, "Validation Error",
                                              "Please enter a training name.")
                return False

            if not cost_per_person or not cost_per_person.isdigit() or int(cost_per_person) <= 0:
                # Cost is empty, not a valid number, or not positive
                QtWidgets.QMessageBox.warning(self, "Validation Error", "Please enter a valid positive cost.")
                return False

            if date <= datetime.date.today():
                # Date is not larger than today's date
                QtWidgets.QMessageBox.warning(self, "Validation Error", "Please select a date larger than today's date.")
                return False

            if not time:
                # if time empty
                QtWidgets.QMessageBox.warning(self, "Validation Error", "Please enter the time.")
                return False

            if not duration or duration <= 0:
                # Duration is not a positive value
                QtWidgets.QMessageBox.warning(self, "Validation Error", "Please enter a valid positive durations.")
                return False

            if not venue:
                # Venue is empty
                QtWidgets.QMessageBox.warning(self, "Validation Error", "Please enter a venue.")
                return False

            if not short_description_text or len(short_description_text.split()) > 100:
                # Short description exceeds 100 words
                QtWidgets.QMessageBox.warning(self, "Validation Error",
                                              "Short description should not empty and exceed 100 words.")
                return False

            if not description_text:
                QtWidgets.QMessageBox.warning(self, "Validation Error", "Please enter the description.")
                return False

            if not max_participants or not max_participants.isdigit() or int(max_participants) <= 0:
                # Max participants is empty, not a valid number, or not positive
                QtWidgets.QMessageBox.warning(self, "Validation Error",
                                              "Please enter a valid positive maximum participants count.")
                return False

            if department == "Select Department":
                # Department is not selected
                QtWidgets.QMessageBox.warning(self, "Validation Error", "Please select a department.")
                return False

            else:
                connectDatabase()
                self.cursor = connect.cursor()
                self.cursor.execute("SELECT departmentID FROM department where departmentName = ?", (department,))
                dep_id = self.cursor.fetchone()
                department_id = dep_id[0]

                status = "Pending"
                publish = False
                cost = float(cost_per_person) * int(max_participants)

                self.cursor.execute(
                    """INSERT INTO training 
                    (trainingName, cost, date, time, duration, venue, short_description, description, 
                    max_par, departmentID, brochure, status, publish) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (
                        training_name, cost, date, time, duration, venue, short_description_text, description_text,
                        max_participants, department_id, image_data if image_data else None,  status, publish
                    )
                )

                connect.commit()
                # global training_id_for_create_list
                training_id_for_create_list = None
                training_id_for_create_list = self.cursor.lastrowid
                QtWidgets.QMessageBox.information(self, "Success", "Training data inserted successfully.",
                                                  QtWidgets.QMessageBox.Ok)

                if self.check_box.isChecked():
                    if training_id_for_create_list is not None:
                        try:
                            add_participant = AddParticipantPage(training_id_for_create_list, self)
                            add_participant.exec_()
                            self.reject()
                        except Exception as e:
                            # Show error message box or print the error
                            error_message = "An error occurred: " + str(e)
                            QMessageBox.critical(self, "Error", error_message, QMessageBox.Ok)
                    else:
                        # Handle the case where training_id_for_create_list is None
                        # Display an error message or perform appropriate actions
                        error_message = "Training ID is not available."
                        QMessageBox.warning(self, "Error", error_message, QMessageBox.Ok)
                else:
                    self.reject()

        except sqlite3.Error as e:
            QtWidgets.QMessageBox.critical(self, "Error", str(e), QtWidgets.QMessageBox.Ok)


class AddParticipantPage(QtWidgets.QDialog):
    def __init__(self, training_id, parent=None):
        super().__init__(parent)
        self.training_id_for_insertion = training_id
        self.department_list_items = []

        self.setObjectName(u"AddParticipants")
        self.setWindowTitle("Add Participants")
        self.resize(720, 560)
        self.setStyleSheet(u"background-color: #696969;")
        self.main_frame = QFrame(self)
        self.main_frame.setObjectName(u"main_frame")
        self.main_frame.setGeometry(QRect(10, 10, 700, 540))
        self.main_frame.setStyleSheet(u"border: 1px solid white;")
        self.main_frame.setFrameShape(QFrame.StyledPanel)
        self.main_frame.setFrameShadow(QFrame.Raised)

        self.header = QLabel(self.main_frame)
        self.header.setObjectName(u"header")
        self.header.setGeometry(QRect(10, 10, 671, 61))
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.header.sizePolicy().hasHeightForWidth())
        self.header.setSizePolicy(sizePolicy)
        font = QFont()
        font.setPointSize(22)
        font.setBold(True)
        font.setWeight(75)
        self.header.setFont(font)
        self.header.setStyleSheet(u"border: none;\n"
                                  "border-bottom: 1px solid white;\n"
                                  "color: white;\n"
                                  "font-weight: bold;\n")
        self.header.setText("Create Participants List")

        self.scrollArea = QScrollArea(self.main_frame)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setGeometry(QRect(10, 75, 685, 461))
        self.scrollArea.setStyleSheet(u"border: none;")
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scrollArea.setWidgetResizable(True)

        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 664, 461))

        # Initialize the table
        self.add_department_into_table = QtWidgets.QTableWidget(self.scrollAreaWidgetContents)
        self.add_department_into_table.setGeometry(QtCore.QRect(10, 190, 921, 381))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.add_department_into_table.sizePolicy().hasHeightForWidth())
        self.add_department_into_table.setSizePolicy(sizePolicy)
        self.add_department_into_table.setStyleSheet("qproperty-uniformRowHeights: true;")
        self.add_department_into_table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.add_department_into_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.add_department_into_table.setShowGrid(True)
        self.add_department_into_table.setGridStyle(QtCore.Qt.SolidLine)
        self.add_department_into_table.setCornerButtonEnabled(False)
        self.add_department_into_table.setObjectName("department_table")
        self.add_department_into_table.setColumnCount(2)
        self.add_department_into_table.setHorizontalHeaderLabels(["Index", "Department"])
        self.add_department_into_table.setRowCount(0)  # Initially, 0 rows
        # Set the width of column 2
        self.add_department_into_table.setColumnWidth(1, 400)
        self.add_department_into_table.horizontalHeader().setVisible(True)
        self.add_department_into_table.verticalHeader().setVisible(False)

        connectDatabase()
        self.cursor = connect.cursor()
        self.cursor.execute("SELECT * FROM department")
        department_list = self.cursor.fetchall()

        self.department_pick = QtWidgets.QComboBox(self.scrollAreaWidgetContents)
        self.department_pick.setGeometry(QtCore.QRect(10, 120, 281, 51))
        self.department_pick.setStyleSheet(u"color: white;\n"
                                           "border: 1px solid white;")
        self.department_pick.setObjectName("department_pick")
        self.department_pick.addItem("Select Department")  # Add a placeholder item
        self.department_pick.addItems([department[1] for department in department_list])
        self.department_pick.setCurrentText("Select Department")  # Set the default placeholder text

        self.department_label = QLabel(self.scrollAreaWidgetContents)
        self.department_label.setObjectName(u"department_label")
        self.department_label.setGeometry(QRect(10, 70, 131, 41))
        font4 = QFont()
        font4.setPointSize(9)
        font4.setBold(True)
        font4.setWeight(75)
        self.department_label.setFont(font4)
        self.department_label.setStyleSheet(u"color: white;")
        self.department_label.setText("Department")

        self.add_button = QPushButton(self.scrollAreaWidgetContents)
        self.add_button.setObjectName(u"add_button_2")
        self.add_button.setGeometry(QRect(300, 130, 31, 31))
        icon = QIcon()
        icon.addFile(u"plus.png", QSize(), QIcon.Normal, QIcon.Off)
        self.add_button.setIcon(icon)
        self.add_button.setIconSize(QSize(36, 36))
        self.add_button.clicked.connect(self.add_row)

        self.remove_button = QPushButton(self.scrollAreaWidgetContents)
        self.remove_button.setObjectName(u"remove_button_2")
        self.remove_button.setGeometry(QRect(340, 130, 31, 31))
        icon1 = QIcon()
        icon1.addFile(u"minus.png", QSize(), QIcon.Normal, QIcon.Off)
        self.remove_button.setIcon(icon1)
        self.remove_button.setIconSize(QSize(42, 42))
        self.remove_button.clicked.connect(self.remove_row)

        self.cancel_button = QPushButton(self.scrollAreaWidgetContents)
        self.cancel_button.setObjectName(u"cancel_button")
        self.cancel_button.setGeometry(QRect(560, 410, 90, 31))
        self.cancel_button.setFont(font4)
        self.cancel_button.setStyleSheet(u"color: white;\n"
                                         "font-weight: bold;\n"
                                         "border-radius: 10px;\n"
                                         "background: #008287;\n"
                                         "border-color: white;")
        self.cancel_button.setText("Cancel")
        self.cancel_button.clicked.connect(self.reject)

        self.create_button = QPushButton(self.scrollAreaWidgetContents)
        self.create_button.setObjectName(u"create_button")
        self.create_button.setGeometry(QRect(439, 410, 90, 31))
        self.create_button.setFont(font4)
        self.create_button.setStyleSheet(u"color: white;\n"
                                         "border-radius: 10px;\n"
                                         "background: #008287;\n"
                                         "border-color: white;")
        self.create_button.setText("Create")
        self.create_button.clicked.connect(self.add_participant_list)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

    def add_row(self):
        selected_department = self.department_pick.currentText()

        # Check if the selected department is empty
        if selected_department == "Select Department":
            QMessageBox.critical(self, "Error", "Please select a department.")
            return

        # Check for duplicate department in the table
        for row in range(self.add_department_into_table.rowCount()):
            item = self.add_department_into_table.item(row, 1)
            if item and item.text() == selected_department:
                QMessageBox.critical(self, "Error", "Department already exists in the table.")
                return

        # Add the row to the table
        current_row = self.add_department_into_table.rowCount()
        self.add_department_into_table.insertRow(current_row)

        index_item = QtWidgets.QTableWidgetItem(str(current_row + 1))
        index_item.setForeground(QtGui.QColor("white"))  # Set index text color to white
        self.add_department_into_table.setItem(current_row, 0, index_item)

        department_item = QtWidgets.QTableWidgetItem(selected_department)
        department_item.setForeground(QtGui.QColor("white"))  # Set department text color to white
        self.add_department_into_table.setItem(current_row, 1, department_item)
        # self.add_department_into_table.resizeColumnsToContents()

        # Add the selected department to the department items list
        self.department_list_items.append(selected_department)

    def remove_row(self):
        selected_row = self.add_department_into_table.currentRow()
        if selected_row >= 0:
            # Retrieve the department item from the table
            department_item = self.add_department_into_table.item(selected_row, 1)
            if department_item:
                department = department_item.text()

                # Remove the row from the table
                self.add_department_into_table.removeRow(selected_row)

                # Remove the department item from the list
                if department in self.department_list_items:
                    self.department_list_items.remove(department)

                # Update index values of subsequent rows
                row_count = self.add_department_into_table.rowCount()
                for row in range(selected_row, row_count):
                    self.add_department_into_table.item(row, 0).setText(str(row + 1))

    def add_participant_list(self):
        app_status = "Approved"
        app_date = datetime.date.today()

        for department in self.department_list_items:
            connectDatabase()
            self.cursor = connect.cursor()
            self.cursor.execute("SELECT departmentID FROM department WHERE departmentName = ?", (department,))
            department_id1 = self.cursor.fetchone()  # Use fetchone() instead of fetchall()
            department_id = department_id1[0]

            connectDatabase()
            self.cursor = connect.cursor()
            self.cursor.execute("SELECT employeeID FROM employee WHERE departmentID = ?", (department_id,))
            employees = self.cursor.fetchall()
            employee_list = len(employees)

            for employee in range(employee_list):
                employee_id = employees[employee][0]

                connectDatabase()
                self.cursor = connect.cursor()
                self.cursor.execute("""INSERT INTO application(employeeID, trainingID, applicationStatus, applicationDate) 
                        VALUES (?, ?, ?, ?)""", (employee_id, self.training_id_for_insertion, app_status, app_date))
                connect.commit()

        QtWidgets.QMessageBox.information(self, "Success", "Application added successfully.", QtWidgets.QMessageBox.Ok)
        self.reject()


if __name__ == "__main__":
    # Create an instance of QApplication
    app = QtWidgets.QApplication(sys.argv)

    # Create an instance of MyTraining
    main_window = HR_Training()

    # Show the main window
    main_window.show()

    # Execute the application
    sys.exit(app.exec_())
