from datetime import datetime
import logging
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
import sys
import sqlite3


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


class MyTraining(QMainWindow):
    def __init__(self):
        super(MyTraining, self).__init__()

        loadUi("mytraining.ui", self)

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
        font.setBold(True)
        font.setWeight(75)
        self.header.setFont(font)
        self.header.setStyleSheet("border: none;\nborder-bottom: 1px solid white;\ncolor: white;\nfont-weight: bold;\n")
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
        icon2.addPixmap(QtGui.QPixmap("search.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
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
            "SELECT t.trainingID, t.trainingName, d.departmentName, t.short_description, t.brochure, "
            "a.applicationStatus FROM application a "
            "JOIN training t ON a.trainingID = t.trainingID "
            "JOIN department d ON d.departmentID = t.departmentID "
            "WHERE a.employeeID = ?", (employee_id,))
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
            self.training_image = QtWidgets.QLabel(self.training)
            self.training_image.setGeometry(QtCore.QRect(20, 10, 200, 150))
            self.training_image.setText(f"{row_data[item][3]}")
            self.training_image.setObjectName("training_image")

            self.department_label_2 = QtWidgets.QLabel(self.training)
            self.department_label_2.setGeometry(QtCore.QRect(230, 50, 111, 31))
            font = QtGui.QFont()
            font.setBold(True)
            font.setWeight(75)
            self.department_label_2.setFont(font)
            self.department_label_2.setStyleSheet("color: white;\nfont-weight: bold;\nborder: none;")
            self.department_label_2.setText("Department: ")
            self.department_label_2.setObjectName("department_label_2")

            self.department_db_2 = QtWidgets.QLabel(self.training)
            self.department_db_2.setGeometry(QtCore.QRect(340, 50, 581, 31))
            font = QtGui.QFont()
            font.setPointSize(8)
            font.setBold(False)
            font.setWeight(50)
            self.department_db_2.setFont(font)
            self.department_db_2.setStyleSheet("color: white;\nfont-weight: regular;\nborder: none;\nbold: none;")
            self.department_db_2.setText(f"{row_data[item][2]}")
            self.department_db_2.setObjectName("department_db_2")

            self.description_label = QtWidgets.QLabel(self.training)
            self.description_label.setGeometry(QtCore.QRect(230, 80, 101, 21))
            font = QtGui.QFont()
            font.setBold(True)
            font.setWeight(75)
            self.description_label.setFont(font)
            self.description_label.setStyleSheet("color: white;\nfont-weight: bold;\nborder: none;")
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
            self.status_label.setStyleSheet("color: white;\nfont-weight: bold;\nborder: none;")
            self.status_label.setText("Status: \n" + status)
            self.status_label.setObjectName("status_label")

            self.view_button = QtWidgets.QPushButton(self.training)
            self.view_button.setGeometry(QtCore.QRect(810, 200, 112, 34))
            self.view_button.setStyleSheet(
                "color: white;\nfont-weight: bold;\nborder-radius: 10px;\nbackground: #008287;")
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
            self.training_name_db.setStyleSheet("color: white;\nfont-weight: bold;\nborder: none;\ntext-align: left;\n")
            self.training_name_db.setText(f"{row_data[item][1]}")
            self.training_name_db.setObjectName("training_name_db")
            self.training_name_db.clicked.connect(lambda _, training_id=row_data[item][0]:
                                                  self.viewTrainingDetails(training_id))

        # Adjust the size of the scroll area's contents
        self.scrollAreaWidgetContents_2.setMinimumHeight(rows * (frame_height + frame_spacing))

        # Set the scroll area widget
        self.scrollArea.setWidget(self.scrollAreaWidgetContents_2)
        self.setCentralWidget(self.centralwidget)
        QtCore.QMetaObject.connectSlotsByName(self)

    def viewTrainingDetails(self, trainingID):
        try:
            loadUi("training_details-mytraining.ui", self)
            self.header.setText("Training Details")
            self.cancel_button.clicked.connect(lambda: self.recreateMyTraining())

            connectDatabase()
            self.cursor = connect.cursor()
            self.cursor.execute(
                "SELECT t.trainingName, d.departmentName, t.short_description, t.brochure "
                "FROM training t, department d WHERE d.departmentID = t.departmentID AND t.trainingID = ?",
                (trainingID,))
            row = self.cursor.fetchall()

            self.training.setText(f"{row[0][0]}")
            date = datetime.strptime(row[0][1], "%d-%m-%Y")
            date = date.strftime("%d %B %Y")
            time = datetime.strptime(row[0][2], "%H:%M")
            time = time.strftime("%H:%M")
            self.date_db.setText(f"{date}")
            self.time_db.setText(f"{time}")
            self.venue_db.setText(f"{row[0][6]}")
            self.duration_db.setText(f"{row[0][5]}")
            self.department_db_2.setText(f"{row[0][7]}")
            self.description_db.setText(f"{row[0][8]}")
            self.brochure_button.setIconSize(QtCore.QSize(200, 200))
            self.brochure_button.setIcon(QtGui.QIcon(f"pictures/image{trainingID}.png"))
            self.number_participants_db.setText(f"{row[0][3]}")

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
                "OR t.date LIKE ? OR t.time LIKE ? OR t.duration LIKE ?) "
                "AND a.employeeID = ?",
                ('%' + keywords + '%', '%' + keywords + '%', '%' + keywords + '%',
                 '%' + keywords + '%', '%' + keywords + '%', employee_id)
            )
            search_results = self.cursor.fetchall()

            if len(search_results) > 0:
                # Display the search results
                self.updateSearchResults(search_results)
            else:
                QMessageBox.information(self, "No Results", "No training matching the search criteria was found.",
                                        QMessageBox.Ok)

        except Exception as e:
            # Show error message box or print the error
            error_message = "An error occurred: " + str(e)
            QMessageBox.critical(self, "Error", error_message, QMessageBox.Ok)

    def updateSearchResults(self, search_results):
        # Define the size and position of each frame
        frame_width = 931
        frame_height = 251
        frame_spacing = 20

        # Clear the existing contents of the scroll area
        layout = self.scrollAreaWidgetContents_2.layout()
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()

        # Create a new layout
        new_layout = QVBoxLayout(self.scrollAreaWidgetContents_2)

        # Loop to create and position the frames for search results
        for item in range(len(search_results)):
            status = search_results[item][5]

            self.training = QtWidgets.QFrame(self.scrollAreaWidgetContents_2)
            self.training.setGeometry(QtCore.QRect(0, item * (frame_height + frame_spacing), frame_width, frame_height))
            self.training.setStyleSheet("border: 1px solid white;\nbackground: #8A8A8A;\nborder-radius: 10px;")
            self.training.setFrameShape(QtWidgets.QFrame.StyledPanel)
            self.training.setFrameShadow(QtWidgets.QFrame.Raised)
            self.training.setObjectName("training")
            self.training_image = QtWidgets.QLabel(self.training)
            self.training_image.setGeometry(QtCore.QRect(20, 10, 200, 150))
            self.training_image.setText(f"{search_results[item][4]}")
            self.training_image.setObjectName("training_image")

            self.department_label_2 = QtWidgets.QLabel(self.training)
            self.department_label_2.setGeometry(QtCore.QRect(230, 50, 111, 31))
            font = QtGui.QFont()
            font.setBold(True)
            font.setWeight(75)
            self.department_label_2.setFont(font)
            self.department_label_2.setStyleSheet("color: white;\nfont-weight: bold;\nborder: none;")
            self.department_label_2.setText("Department: ")
            self.department_label_2.setObjectName("department_label_2")

            self.department_db_2 = QtWidgets.QLabel(self.training)
            self.department_db_2.setGeometry(QtCore.QRect(340, 50, 581, 31))
            font = QtGui.QFont()
            font.setPointSize(8)
            font.setBold(False)
            font.setWeight(50)
            self.department_db_2.setFont(font)
            self.department_db_2.setStyleSheet("color: white;\nfont-weight: regular;\nborder: none;\nbold: none;")
            self.department_db_2.setText(f"{search_results[item][2]}")
            self.department_db_2.setObjectName("department_db_2")

            self.description_label = QtWidgets.QLabel(self.training)
            self.description_label.setGeometry(QtCore.QRect(230, 80, 101, 21))
            font = QtGui.QFont()
            font.setBold(True)
            font.setWeight(75)
            self.description_label.setFont(font)
            self.description_label.setStyleSheet("color: white;\nfont-weight: bold;\nborder: none;")
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
            self.status_label.setStyleSheet("color: white;\nfont-weight: bold;\nborder: none;")
            self.status_label.setText("Status: \n" + status)
            self.status_label.setObjectName("status_label")

            self.view_button = QtWidgets.QPushButton(self.training)
            self.view_button.setGeometry(QtCore.QRect(810, 200, 112, 34))
            self.view_button.setStyleSheet(
                "color: white;\nfont-weight: bold;\nborder-radius: 10px;\nbackground: #008287;")
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
            self.training_name_db.setStyleSheet("color: white;\nfont-weight: bold;\nborder: none;\ntext-align: left;\n")
            self.training_name_db.setText(f"{search_results[item][1]}")
            self.training_name_db.setObjectName("training_name_db")
            self.training_name_db.clicked.connect(lambda _, training_id=search_results[item][0]:
                                                  self.viewTrainingDetails(training_id))

        # Set the new layout on the scroll area
        self.scrollAreaWidgetContents_2.setLayout(new_layout)

    def recreateMyTraining(self):
        self.close()  # Close the current instance
        new_instance = MyTraining()  # Create a new instance of MyTraining
        new_instance.show()  # Show the new instance

if __name__ == "__main__":
    # Create an instance of QApplication
    app = QtWidgets.QApplication(sys.argv)

    # Create an instance of MyTraining
    mainwindow = MyTraining()

    # Show the main window
    mainwindow.show()

    # Execute the application
    sys.exit(app.exec_())
