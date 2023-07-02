import logging
import datetime
from functools import partial
from io import BytesIO
from PIL import Image
from PyQt5 import Qt
from PyQt5.QtCore import QSize, QRect, Qt, QByteArray
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QWidget, QFrame, QSizePolicy, QPushButton, QLabel, QScrollArea, QMessageBox
from PyQt5.uic import loadUi
import sys
import sqlite3
from PyQt5 import QtWidgets
from qtpy import QtCore, QtGui

global employeeID
connect = sqlite3.connect('StaffTrainingSystem')
cursor = connect.cursor()


def connect_database():
    try:
        global connect
        global cursor
        # connect to database
        connect = sqlite3.connect("StaffTrainingSystem")
        cursor = connect.cursor()
    except ConnectionError:
        # Show error message box
        QMessageBox.critical(None, "Error", "Cannot connect to database!", QMessageBox.Ok)


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
            self.toggle_zoom()

    def toggle_zoom(self):
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


class Login(QtWidgets.QMainWindow):
    def __init__(self):
        super(Login, self).__init__()
        loadUi("login.ui", self)
        self.login_btn.clicked.connect(self.login_function)
        self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)

    def login_function(self):
        try:
            email = self.email_input.text()
            password = self.password_input.text()
            connect_database()
            cursor.execute('SELECT * FROM employee WHERE email=? AND password=?', (email, password))
            if cursor.fetchone():
                cursor.execute('SELECT employeeID, departmentID FROM employee WHERE email=? AND password=?',
                               (email, password))
                data = cursor.fetchall()
                global employeeID
                employeeID = data[0][0]
                department_id = data[0][1]
                if department_id == 4:
                    gotoHrView()
                else:
                    gotoview()
            else:
                QMessageBox.critical(None, "Error", "Invalid Email or Password.", QMessageBox.Ok)

        except Exception as e:
            QMessageBox.critical(None, "Error", str(e), QMessageBox.Ok)


class HrView(QtWidgets.QMainWindow):
    def __init__(self):
        super(HrView, self).__init__()
        loadUi("hr_training_list(no_box_template).ui", self)

        self.header.setText("Training Lists")
        # Define the size and position of each frame
        frame_width = 931
        frame_height = 251
        frame_spacing = 20

        # connectDatabase()
        cursor.execute('SELECT name, employeeID, departmentID FROM employee WHERE employeeID = ?', (employeeID,))
        display = cursor.fetchall()

        self.employeeID = display[0][1]
        self.name_db.setText(display[0][0])
        self.id_db.setText(str(display[0][1]))
        cursor.execute('SELECT departmentName FROM department WHERE departmentID=?', (display[0][2],))
        self.department_db.setText(cursor.fetchone()[0])
        self.profile_button.setIcon(QtGui.QIcon("profile.png"))
        self.profile_button.clicked.connect(self.goto_profile)
        self.logout_button.setIcon(QtGui.QIcon("logout.png"))
        self.logout_button.clicked.connect(gotologin)
        # Connect the button's clicked signal to the reset function
        self.list_button.clicked.connect(self.reset)

        self.search_button.clicked.connect(self.search_training_hr)

        connect_database()
        self.cursor = connect.cursor()
        self.cursor.execute(
            "SELECT t.trainingID, t.trainingName, d.departmentName, t.short_description, t.brochure, t.max_par, "
            "t.status, t.publish, t.cost, t.date, t.time, t.venue,"
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
            date = datetime.datetime.strptime(row_data[item][9], "%Y-%m-%d")
            date = date.strftime("%d %B %Y")
            training_id = row_data[item][0]
            self.cursor.execute("SELECT COUNT(a.applicationID) "
                                "FROM application a "
                                "JOIN training t ON t.trainingID = a.trainingID "
                                "WHERE t.trainingID = ? AND a.applicationStatus = ?",
                                (training_id, self.app_status,))
            application_count = str(self.cursor.fetchone()[0])

            # training frame
            self.training = QFrame(self.scrollAreaWidgetContents_2)
            self.training.setObjectName(u"training")
            self.training.setGeometry(QRect(0, 50 + (item * (frame_height + frame_spacing)),
                                            frame_width, frame_height))
            self.training.setStyleSheet(u"border: 1px solid white;\n"
                                        "background: #8A8A8A;\n"
                                        "border-radius: 10px;")
            self.training.setFrameShape(QFrame.StyledPanel)
            self.training.setFrameShadow(QFrame.Raised)

            # training image
            blob_data = row_data[item][4]
            pixmap = QtGui.QPixmap()
            pixmap.loadFromData(blob_data)

            self.training_image = QLabel(self.training)
            self.training_image.setGeometry(QtCore.QRect(20, 10, 200, 150))
            self.training_image.setScaledContents(True)
            self.training_image.setPixmap(pixmap)
            self.training_image.setObjectName(f"training_image_{training_id}")

            # training Name
            self.training_name_db = QLabel(self.training)
            self.training_name_db.setObjectName(u"training_name_db")
            self.training_name_db.setGeometry(QRect(230, 20, 691, 31))
            font3 = QFont()
            font3.setPointSize(12)
            font3.setBold(True)
            font3.setWeight(75)
            self.training_name_db.setFont(font3)
            self.training_name_db.setStyleSheet(u"color: white;\n"
                                                "font-weight: bold;\n"
                                                "border: none;\n"
                                                "text-align: left;\n"
                                                "")
            self.training_name_db.setText(f"{row_data[item][1]}")

            # department label
            self.department_label_2 = QLabel(self.training)
            self.department_label_2.setObjectName(u"department_label_2")
            self.department_label_2.setGeometry(QRect(230, 50, 111, 31))
            font1 = QFont()
            font1.setBold(True)
            font1.setWeight(75)
            self.department_label_2.setFont(font1)
            self.department_label_2.setStyleSheet(u"color: white;\n"
                                                  "font-weight: bold;\n"
                                                  "border: none;")
            self.department_label_2.setText("Department:")

            # department database
            self.department_db_2 = QLabel(self.training)
            self.department_db_2.setObjectName(u"department_db_2")
            self.department_db_2.setGeometry(QRect(340, 50, 581, 31))
            font2 = QFont()
            font2.setPointSize(8)
            font2.setBold(False)
            font2.setWeight(50)
            self.department_db_2.setFont(font2)
            self.department_db_2.setStyleSheet(u"color: white;\n"
                                               "font-weight: regular;\n"
                                               "border: none;\n"
                                               "bold: none;")
            self.department_db_2.setText(f"{row_data[item][2]}")

            # description label
            self.description_label = QLabel(self.training)
            self.description_label.setObjectName(u"description_label")
            self.description_label.setGeometry(QRect(230, 80, 101, 21))
            self.description_label.setFont(font1)
            self.description_label.setStyleSheet(u"color: white;\n"
                                                 "font-weight: bold;\n"
                                                 "border: none;")
            self.description_label.setText("Description:")

            # description database
            self.description_db = QLabel(self.training)
            self.description_db.setObjectName(u"description_db")
            self.description_db.setGeometry(QRect(230, 100, 691, 61))
            self.description_db.setStyleSheet(u"color: white;\n"
                                              "font-weight: regular;\n"
                                              "border: none;")
            self.description_db.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)
            self.description_db.setWordWrap(True)
            self.description_db.setText(f"{row_data[item][3]}")

            # date label
            self.date_label = QLabel(self.training)
            self.date_label.setObjectName(u"date_label")
            self.date_label.setGeometry(QRect(20, 160, 51, 31))
            self.date_label.setFont(font1)
            self.date_label.setStyleSheet(u"color: white;\n"
                                          "font-weight: bold;\n"
                                          "border: none;")
            self.date_label.setText("Date:")

            # date db
            self.date_db = QLabel(self.training)
            self.date_db.setObjectName(u"date_db")
            self.date_db.setGeometry(QRect(80, 160, 141, 31))
            self.date_db.setFont(font2)
            self.date_db.setStyleSheet(u"color: white;\n"
                                       "font-weight: regular;\n"
                                       "border: none;\n"
                                       "bold: none;")
            self.date_db.setText(f"{date}")

            # time label
            self.time_label = QLabel(self.training)
            self.time_label.setObjectName(u"time_label")
            self.time_label.setGeometry(QRect(240, 160, 51, 31))
            self.time_label.setFont(font1)
            self.time_label.setStyleSheet(u"color: white;\n"
                                          "font-weight: bold;\n"
                                          "border: none;")
            self.time_label.setText("Time:")

            # time db
            self.time_db = QLabel(self.training)
            self.time_db.setObjectName(u"time_db")
            self.time_db.setGeometry(QRect(300, 160, 51, 31))
            self.time_db.setFont(font2)
            self.time_db.setStyleSheet(u"color: white;\n"
                                       "font-weight: regular;\n"
                                       "border: none;\n"
                                       "bold: none;")
            self.time_db.setText(f"{row_data[item][10]}")

            # venue label
            self.venue_label = QLabel(self.training)
            self.venue_label.setObjectName(u"venue_label")
            self.venue_label.setGeometry(QRect(20, 190, 61, 21))
            self.venue_label.setFont(font1)
            self.venue_label.setStyleSheet(u"color: white;\n"
                                           "font-weight: bold;\n"
                                           "border: none;")
            self.venue_label.setText("Venue:")

            # venue db
            self.venue_db = QLabel(self.training)
            self.venue_db.setObjectName(u"venue_db")
            self.venue_db.setGeometry(QRect(90, 190, 471, 21))
            self.venue_db.setFont(font2)
            self.venue_db.setStyleSheet(u"color: white;\n"
                                        "font-weight: regular;\n"
                                        "border: none;\n"
                                        "bold: none;")
            self.venue_db.setText(f"{row_data[item][11]}")

            # status label
            self.status_label = QLabel(self.training)
            self.status_label.setObjectName(u"status_label")
            self.status_label.setGeometry(QRect(20, 210, 61, 31))
            self.status_label.setFont(font1)
            self.status_label.setStyleSheet(u"color: white;\n"
                                            "font-weight: bold;\n"
                                            "border: none;")
            self.status_label.setText("Status:")

            # status db
            self.status_db = QLabel(self.training)
            self.status_db.setObjectName(u"status_db")
            self.status_db.setGeometry(QRect(90, 210, 78, 31))
            self.status_db.setFont(font2)

            # participants label
            self.participant_label = QLabel(self.training)
            self.participant_label.setObjectName(u"participant_label")
            self.participant_label.setGeometry(QRect(180, 210, 101, 31))
            self.participant_label.setFont(font1)
            self.participant_label.setStyleSheet(u"color: white;\n"
                                                 "font-weight: bold;\n"
                                                 "border: none;")
            self.participant_label.setText("Participant:")

            # participants db
            self.participant_db = QLabel(self.training)
            self.participant_db.setObjectName(u"participant_db")
            self.participant_db.setGeometry(QRect(290, 210, 81, 31))
            self.participant_db.setFont(font2)
            self.participant_db.setStyleSheet(u"color: white;\n"
                                              "font-weight: regular;\n"
                                              "border: none;\n"
                                              "bold: none;")
            self.participant_db.setText(f"{application_count}"" / " f"{row_data[item][5]}")

            # cost label
            self.cost_label = QLabel(self.training)
            self.cost_label.setObjectName(u"cost_label")
            self.cost_label.setGeometry(QRect(390, 210, 51, 31))
            self.cost_label.setFont(font1)
            self.cost_label.setStyleSheet(u"color: white;\n"
                                          "font-weight: bold;\n"
                                          "border: none;")
            self.cost_label.setText("Cost:")

            # cost db
            self.cost_db = QLabel(self.training)
            self.cost_db.setObjectName(u"cost_db")
            self.cost_db.setGeometry(QRect(440, 210, 81, 31))
            self.cost_db.setFont(font2)
            self.cost_db.setStyleSheet(u"color: white;\n"
                                       "font-weight: regular;\n"
                                       "border: none;\n"
                                       "bold: none;")
            self.cost_db.setText(f"{row_data[item][8]}")

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
                self.modify_button.clicked.connect(lambda _, trainingid=training_id:
                                                   self.modify_training(trainingid))

                self.view_more_button = QPushButton(self.training)
                self.view_more_button.setObjectName(u"view_more_button")
                self.view_more_button.setGeometry(QRect(690, 200, 112, 34))
                self.view_more_button.setStyleSheet(u"color: white;\n"
                                                    u"font-weight: bold;\n"
                                                    u"border-radius: 10px;\n"
                                                    u"background: #008287;\n")
                self.view_more_button.setText("View More")
                self.view_more_button.clicked.connect(lambda _, trainingid=training_id:
                                                      self.view_particpants(trainingid))

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
                self.view_more_button.clicked.connect(lambda _, trainingid=training_id:
                                                      self.view_particpants(trainingid))

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
                self.modify_button.clicked.connect(lambda _, trainingid=training_id:
                                                   self.modify_training(trainingid))

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
                                                      self.view_particpants(trainingid))

            self.status_db.setText(f"{row_data[item][6]}")
            publish = row_data[item][7]
            if publish == 1:
                self.publish_button.setText("Unpublished")
            else:
                self.publish_button.setText("Publish")

        # Adjust the size of the scroll area's contents
        self.scrollAreaWidgetContents_2.setMinimumHeight(50 + rows * (frame_height + frame_spacing))

        # Set the scroll area widget
        self.scrollArea.setWidget(self.scrollAreaWidgetContents_2)

    def search_training_hr(self):
        try:
            keywords = self.search_bar.text()

            # Query the database based on the keywords and date range
            connect_database()
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
            date = datetime.datetime.strptime(search_results[item][9], "%Y-%m-%d")
            date = date.strftime("%d %B %Y")
            training_id = search_results[item][0]
            self.cursor.execute("SELECT COUNT(a.applicationID) "
                                "FROM application a "
                                "JOIN training t ON t.trainingID = a.trainingID "
                                "WHERE t.trainingID = ? AND a.applicationStatus = ?",
                                (training_id, self.app_status,))
            application_count = str(self.cursor.fetchone()[0])

            # training frame
            self.training = QFrame(self.scrollAreaWidgetContents_2)
            self.training.setObjectName(u"training")
            self.training.setGeometry(QRect(0, 50 + (item * (frame_height + frame_spacing)),
                                            frame_width, frame_height))
            self.training.setStyleSheet(u"border: 1px solid white;\n"
                                        "background: #8A8A8A;\n"
                                        "border-radius: 10px;")
            self.training.setFrameShape(QFrame.StyledPanel)
            self.training.setFrameShadow(QFrame.Raised)

            # training image
            blob_data = search_results[item][4]
            pixmap = QtGui.QPixmap()
            pixmap.loadFromData(blob_data)

            self.training_image = QLabel(self.training)
            self.training_image.setGeometry(QtCore.QRect(20, 10, 200, 150))
            self.training_image.setScaledContents(True)
            self.training_image.setPixmap(pixmap)
            self.training_image.setObjectName(f"training_image_{training_id}")

            # training Name
            self.training_name_db = QLabel(self.training)
            self.training_name_db.setObjectName(u"training_name_db")
            self.training_name_db.setGeometry(QRect(230, 20, 691, 31))
            font3 = QFont()
            font3.setPointSize(12)
            font3.setBold(True)
            font3.setWeight(75)
            self.training_name_db.setFont(font3)
            self.training_name_db.setStyleSheet(u"color: white;\n"
                                                "font-weight: bold;\n"
                                                "border: none;\n"
                                                "text-align: left;\n"
                                                "")
            self.training_name_db.setText(f"{search_results[item][1]}")

            # department label
            self.department_label_2 = QLabel(self.training)
            self.department_label_2.setObjectName(u"department_label_2")
            self.department_label_2.setGeometry(QRect(230, 50, 111, 31))
            font1 = QFont()
            font1.setBold(True)
            font1.setWeight(75)
            self.department_label_2.setFont(font1)
            self.department_label_2.setStyleSheet(u"color: white;\n"
                                                  "font-weight: bold;\n"
                                                  "border: none;")
            self.department_label_2.setText("Department:")

            # department database
            self.department_db_2 = QLabel(self.training)
            self.department_db_2.setObjectName(u"department_db_2")
            self.department_db_2.setGeometry(QRect(340, 50, 581, 31))
            font2 = QFont()
            font2.setPointSize(8)
            font2.setBold(False)
            font2.setWeight(50)
            self.department_db_2.setFont(font2)
            self.department_db_2.setStyleSheet(u"color: white;\n"
                                               "font-weight: regular;\n"
                                               "border: none;\n"
                                               "bold: none;")
            self.department_db_2.setText(f"{search_results[item][2]}")

            # description label
            self.description_label = QLabel(self.training)
            self.description_label.setObjectName(u"description_label")
            self.description_label.setGeometry(QRect(230, 80, 101, 21))
            self.description_label.setFont(font1)
            self.description_label.setStyleSheet(u"color: white;\n"
                                                 "font-weight: bold;\n"
                                                 "border: none;")
            self.description_label.setText("Description:")

            # description database
            self.description_db = QLabel(self.training)
            self.description_db.setObjectName(u"description_db")
            self.description_db.setGeometry(QRect(230, 100, 691, 61))
            self.description_db.setStyleSheet(u"color: white;\n"
                                              "font-weight: regular;\n"
                                              "border: none;")
            self.description_db.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)
            self.description_db.setWordWrap(True)
            self.description_db.setText(f"{search_results[item][3]}")

            # date label
            self.date_label = QLabel(self.training)
            self.date_label.setObjectName(u"date_label")
            self.date_label.setGeometry(QRect(20, 160, 51, 31))
            self.date_label.setFont(font1)
            self.date_label.setStyleSheet(u"color: white;\n"
                                          "font-weight: bold;\n"
                                          "border: none;")
            self.date_label.setText("Date:")

            # date db
            self.date_db = QLabel(self.training)
            self.date_db.setObjectName(u"date_db")
            self.date_db.setGeometry(QRect(80, 160, 141, 31))
            self.date_db.setFont(font2)
            self.date_db.setStyleSheet(u"color: white;\n"
                                       "font-weight: regular;\n"
                                       "border: none;\n"
                                       "bold: none;")
            self.date_db.setText(f"{date}")

            # time label
            self.time_label = QLabel(self.training)
            self.time_label.setObjectName(u"time_label")
            self.time_label.setGeometry(QRect(240, 160, 51, 31))
            self.time_label.setFont(font1)
            self.time_label.setStyleSheet(u"color: white;\n"
                                          "font-weight: bold;\n"
                                          "border: none;")
            self.time_label.setText("Time:")

            # time db
            self.time_db = QLabel(self.training)
            self.time_db.setObjectName(u"time_db")
            self.time_db.setGeometry(QRect(300, 160, 51, 31))
            self.time_db.setFont(font2)
            self.time_db.setStyleSheet(u"color: white;\n"
                                       "font-weight: regular;\n"
                                       "border: none;\n"
                                       "bold: none;")
            self.time_db.setText(f"{search_results[item][10]}")

            # venue label
            self.venue_label = QLabel(self.training)
            self.venue_label.setObjectName(u"venue_label")
            self.venue_label.setGeometry(QRect(20, 190, 61, 21))
            self.venue_label.setFont(font1)
            self.venue_label.setStyleSheet(u"color: white;\n"
                                           "font-weight: bold;\n"
                                           "border: none;")
            self.venue_label.setText("Venue:")

            # venue db
            self.venue_db = QLabel(self.training)
            self.venue_db.setObjectName(u"venue_db")
            self.venue_db.setGeometry(QRect(90, 190, 471, 21))
            self.venue_db.setFont(font2)
            self.venue_db.setStyleSheet(u"color: white;\n"
                                        "font-weight: regular;\n"
                                        "border: none;\n"
                                        "bold: none;")
            self.venue_db.setText(f"{search_results[item][11]}")

            # status label
            self.status_label = QLabel(self.training)
            self.status_label.setObjectName(u"status_label")
            self.status_label.setGeometry(QRect(20, 210, 61, 31))
            self.status_label.setFont(font1)
            self.status_label.setStyleSheet(u"color: white;\n"
                                            "font-weight: bold;\n"
                                            "border: none;")
            self.status_label.setText("Status:")

            # status db
            self.status_db = QLabel(self.training)
            self.status_db.setObjectName(u"status_db")
            self.status_db.setGeometry(QRect(90, 210, 78, 31))
            self.status_db.setFont(font2)

            # participants label
            self.participant_label = QLabel(self.training)
            self.participant_label.setObjectName(u"participant_label")
            self.participant_label.setGeometry(QRect(180, 210, 101, 31))
            self.participant_label.setFont(font1)
            self.participant_label.setStyleSheet(u"color: white;\n"
                                                 "font-weight: bold;\n"
                                                 "border: none;")
            self.participant_label.setText("Participant:")

            # participants db
            self.participant_db = QLabel(self.training)
            self.participant_db.setObjectName(u"participant_db")
            self.participant_db.setGeometry(QRect(290, 210, 81, 31))
            self.participant_db.setFont(font2)
            self.participant_db.setStyleSheet(u"color: white;\n"
                                              "font-weight: regular;\n"
                                              "border: none;\n"
                                              "bold: none;")
            self.participant_db.setText(f"{application_count}"" / " f"{search_results[item][5]}")

            # cost label
            self.cost_label = QLabel(self.training)
            self.cost_label.setObjectName(u"cost_label")
            self.cost_label.setGeometry(QRect(390, 210, 51, 31))
            self.cost_label.setFont(font1)
            self.cost_label.setStyleSheet(u"color: white;\n"
                                          "font-weight: bold;\n"
                                          "border: none;")
            self.cost_label.setText("Cost:")

            # cost db
            self.cost_db = QLabel(self.training)
            self.cost_db.setObjectName(u"cost_db")
            self.cost_db.setGeometry(QRect(440, 210, 81, 31))
            self.cost_db.setFont(font2)
            self.cost_db.setStyleSheet(u"color: white;\n"
                                       "font-weight: regular;\n"
                                       "border: none;\n"
                                       "bold: none;")
            self.cost_db.setText(f"{search_results[item][8]}")

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
                self.view_more_button.setText("View More")
                self.view_more_button.clicked.connect(lambda _, trainingid=training_id: self.view_particpants(trainingid))

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
                self.view_more_button.clicked.connect(lambda _, trainingid=training_id: self.view_particpants(trainingid))

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
                self.view_more_button.clicked.connect(lambda _, trainingid=training_id: self.view_particpants(trainingid))

            self.status_db.setText(f"{search_results[item][6]}")
            publish = search_results[item][7]
            if publish == 1:
                self.publish_button.setText("Unpublished")
            else:
                self.publish_button.setText("Publish")


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
        try:
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
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e), QMessageBox.Ok)
            print(str(e))

    def modify_training(self, training_id):
        try:
            self.dialog = ModifyTraining(int(training_id))
            self.dialog.exec_()
        except Exception as e:
            # Show error message box or print the error
            error_message = "An error occurred: " + str(e)
            QMessageBox.critical(self, "Error", error_message, QMessageBox.Ok)

    def view_particpants(self, training_id):
        try:
            view_training_particpants = ParticipantList(training_id)
            widget.addWidget(view_training_particpants)
            widget.setCurrentIndex(widget.currentIndex() + 1)

        except Exception as e:
            # Show error message box or print the error
            error_message = "An error occurred: " + str(e)
            QMessageBox.critical(self, "Error", error_message, QMessageBox.Ok)
            print(error_message)

    def approve_training(self, training_id):
        try:
            approval_window = Approval(training_id)
            widget.addWidget(approval_window)
            widget.setCurrentIndex(widget.currentIndex() + 1)

        except Exception as e:
            # Show error message box or print the error
            error_message = "An error occurred: " + str(e)
            QMessageBox.critical(self, "Error", error_message, QMessageBox.Ok)
            print(error_message)

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

            connect_database()
            self.cursor = connect.cursor()
            self.cursor.execute(
                "SELECT t.trainingID, t.trainingName, d.departmentName, t.short_description, t.brochure, t.max_par, "
                "t.status, t.publish, t.cost, t.date, t.time, t.venue,"
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
                date = datetime.datetime.strptime(row_data[item][9], "%Y-%m-%d")
                date = date.strftime("%d %B %Y")
                training_id = row_data[item][0]
                self.cursor.execute("SELECT COUNT(a.applicationID) "
                                    "FROM application a "
                                    "JOIN training t ON t.trainingID = a.trainingID "
                                    "WHERE t.trainingID = ? AND a.applicationStatus = ?",
                                    (training_id, self.app_status,))
                application_count = str(self.cursor.fetchone()[0])

                # training frame
                self.training = QFrame(self.scrollAreaWidgetContents_2)
                self.training.setObjectName(u"training")
                self.training.setGeometry(QRect(0, 50 + (item * (frame_height + frame_spacing)),
                                                frame_width, frame_height))
                self.training.setStyleSheet(u"border: 1px solid white;\n"
                                            "background: #8A8A8A;\n"
                                            "border-radius: 10px;")
                self.training.setFrameShape(QFrame.StyledPanel)
                self.training.setFrameShadow(QFrame.Raised)

                # training image
                blob_data = row_data[item][4]
                pixmap = QtGui.QPixmap()
                pixmap.loadFromData(blob_data)

                self.training_image = QLabel(self.training)
                self.training_image.setGeometry(QtCore.QRect(20, 10, 200, 150))
                self.training_image.setScaledContents(True)
                self.training_image.setPixmap(pixmap)
                self.training_image.setObjectName(f"training_image_{training_id}")

                # training Name
                self.training_name_db = QLabel(self.training)
                self.training_name_db.setObjectName(u"training_name_db")
                self.training_name_db.setGeometry(QRect(230, 20, 691, 31))
                font3 = QFont()
                font3.setPointSize(12)
                font3.setBold(True)
                font3.setWeight(75)
                self.training_name_db.setFont(font3)
                self.training_name_db.setStyleSheet(u"color: white;\n"
                                                    "font-weight: bold;\n"
                                                    "border: none;\n"
                                                    "text-align: left;\n"
                                                    "")
                self.training_name_db.setText(f"{row_data[item][1]}")

                # department label
                self.department_label_2 = QLabel(self.training)
                self.department_label_2.setObjectName(u"department_label_2")
                self.department_label_2.setGeometry(QRect(230, 50, 111, 31))
                font1 = QFont()
                font1.setBold(True)
                font1.setWeight(75)
                self.department_label_2.setFont(font1)
                self.department_label_2.setStyleSheet(u"color: white;\n"
                                                      "font-weight: bold;\n"
                                                      "border: none;")
                self.department_label_2.setText("Department:")

                # department database
                self.department_db_2 = QLabel(self.training)
                self.department_db_2.setObjectName(u"department_db_2")
                self.department_db_2.setGeometry(QRect(340, 50, 581, 31))
                font2 = QFont()
                font2.setPointSize(8)
                font2.setBold(False)
                font2.setWeight(50)
                self.department_db_2.setFont(font2)
                self.department_db_2.setStyleSheet(u"color: white;\n"
                                                   "font-weight: regular;\n"
                                                   "border: none;\n"
                                                   "bold: none;")
                self.department_db_2.setText(f"{row_data[item][2]}")

                # description label
                self.description_label = QLabel(self.training)
                self.description_label.setObjectName(u"description_label")
                self.description_label.setGeometry(QRect(230, 80, 101, 21))
                self.description_label.setFont(font1)
                self.description_label.setStyleSheet(u"color: white;\n"
                                                     "font-weight: bold;\n"
                                                     "border: none;")
                self.description_label.setText("Description:")

                # description database
                self.description_db = QLabel(self.training)
                self.description_db.setObjectName(u"description_db")
                self.description_db.setGeometry(QRect(230, 100, 691, 61))
                self.description_db.setStyleSheet(u"color: white;\n"
                                                  "font-weight: regular;\n"
                                                  "border: none;")
                self.description_db.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)
                self.description_db.setWordWrap(True)
                self.description_db.setText(f"{row_data[item][3]}")

                # date label
                self.date_label = QLabel(self.training)
                self.date_label.setObjectName(u"date_label")
                self.date_label.setGeometry(QRect(20, 160, 51, 31))
                self.date_label.setFont(font1)
                self.date_label.setStyleSheet(u"color: white;\n"
                                              "font-weight: bold;\n"
                                              "border: none;")
                self.date_label.setText("Date:")

                # date db
                self.date_db = QLabel(self.training)
                self.date_db.setObjectName(u"date_db")
                self.date_db.setGeometry(QRect(80, 160, 141, 31))
                self.date_db.setFont(font2)
                self.date_db.setStyleSheet(u"color: white;\n"
                                           "font-weight: regular;\n"
                                           "border: none;\n"
                                           "bold: none;")
                self.date_db.setText(f"{date}")

                # time label
                self.time_label = QLabel(self.training)
                self.time_label.setObjectName(u"time_label")
                self.time_label.setGeometry(QRect(240, 160, 51, 31))
                self.time_label.setFont(font1)
                self.time_label.setStyleSheet(u"color: white;\n"
                                              "font-weight: bold;\n"
                                              "border: none;")
                self.time_label.setText("Time:")

                # time db
                self.time_db = QLabel(self.training)
                self.time_db.setObjectName(u"time_db")
                self.time_db.setGeometry(QRect(300, 160, 51, 31))
                self.time_db.setFont(font2)
                self.time_db.setStyleSheet(u"color: white;\n"
                                           "font-weight: regular;\n"
                                           "border: none;\n"
                                           "bold: none;")
                self.time_db.setText(f"{row_data[item][10]}")

                # venue label
                self.venue_label = QLabel(self.training)
                self.venue_label.setObjectName(u"venue_label")
                self.venue_label.setGeometry(QRect(20, 190, 61, 21))
                self.venue_label.setFont(font1)
                self.venue_label.setStyleSheet(u"color: white;\n"
                                               "font-weight: bold;\n"
                                               "border: none;")
                self.venue_label.setText("Venue:")

                # venue db
                self.venue_db = QLabel(self.training)
                self.venue_db.setObjectName(u"venue_db")
                self.venue_db.setGeometry(QRect(90, 190, 471, 21))
                self.venue_db.setFont(font2)
                self.venue_db.setStyleSheet(u"color: white;\n"
                                            "font-weight: regular;\n"
                                            "border: none;\n"
                                            "bold: none;")
                self.venue_db.setText(f"{row_data[item][11]}")

                # status label
                self.status_label = QLabel(self.training)
                self.status_label.setObjectName(u"status_label")
                self.status_label.setGeometry(QRect(20, 210, 61, 31))
                self.status_label.setFont(font1)
                self.status_label.setStyleSheet(u"color: white;\n"
                                                "font-weight: bold;\n"
                                                "border: none;")
                self.status_label.setText("Status:")

                # status db
                self.status_db = QLabel(self.training)
                self.status_db.setObjectName(u"status_db")
                self.status_db.setGeometry(QRect(90, 210, 78, 31))
                self.status_db.setFont(font2)

                # participants label
                self.participant_label = QLabel(self.training)
                self.participant_label.setObjectName(u"participant_label")
                self.participant_label.setGeometry(QRect(180, 210, 101, 31))
                self.participant_label.setFont(font1)
                self.participant_label.setStyleSheet(u"color: white;\n"
                                                     "font-weight: bold;\n"
                                                     "border: none;")
                self.participant_label.setText("Participant:")

                # participants db
                self.participant_db = QLabel(self.training)
                self.participant_db.setObjectName(u"participant_db")
                self.participant_db.setGeometry(QRect(290, 210, 81, 31))
                self.participant_db.setFont(font2)
                self.participant_db.setStyleSheet(u"color: white;\n"
                                                  "font-weight: regular;\n"
                                                  "border: none;\n"
                                                  "bold: none;")
                self.participant_db.setText(f"{application_count}"" / " f"{row_data[item][5]}")

                # cost label
                self.cost_label = QLabel(self.training)
                self.cost_label.setObjectName(u"cost_label")
                self.cost_label.setGeometry(QRect(390, 210, 51, 31))
                self.cost_label.setFont(font1)
                self.cost_label.setStyleSheet(u"color: white;\n"
                                              "font-weight: bold;\n"
                                              "border: none;")
                self.cost_label.setText("Cost:")

                # cost db
                self.cost_db = QLabel(self.training)
                self.cost_db.setObjectName(u"cost_db")
                self.cost_db.setGeometry(QRect(440, 210, 81, 31))
                self.cost_db.setFont(font2)
                self.cost_db.setStyleSheet(u"color: white;\n"
                                           "font-weight: regular;\n"
                                           "border: none;\n"
                                           "bold: none;")
                self.cost_db.setText(f"{row_data[item][8]}")

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
                    self.modify_button.clicked.connect(lambda _, trainingid=training_id:
                                                       self.modify_training(trainingid))

                    self.view_more_button = QPushButton(self.training)
                    self.view_more_button.setObjectName(u"view_more_button")
                    self.view_more_button.setGeometry(QRect(690, 200, 112, 34))
                    self.view_more_button.setStyleSheet(u"color: white;\n"
                                                        u"font-weight: bold;\n"
                                                        u"border-radius: 10px;\n"
                                                        u"background: #008287;\n")
                    self.view_more_button.setText("View More")
                    self.view_more_button.clicked.connect(lambda _, trainingid=training_id:
                                                          self.view_particpants(trainingid))

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
                    self.view_more_button.clicked.connect(lambda _, trainingid=training_id:
                                                          self.view_particpants(trainingid))

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
                    self.modify_button.clicked.connect(lambda _, trainingid=training_id:
                                                       self.modify_training(trainingid))

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
                                                          self.view_particpants(trainingid))

                self.status_db.setText(f"{row_data[item][6]}")
                publish = row_data[item][7]
                if publish == 1:
                    self.publish_button.setText("Unpublished")
                else:
                    self.publish_button.setText("Publish")

            # Adjust the size of the scroll area's contents
            self.scrollAreaWidgetContents_2.setMinimumHeight(50 + rows * (frame_height + frame_spacing))

            # Set the scroll area widget
            self.scrollArea.setWidget(self.scrollAreaWidgetContents_2)

        except Exception as e:
            # Show error message box or print the error
            error_message = "An error occurred: " + str(e)
            QMessageBox.critical(self, "Error", error_message, QMessageBox.Ok)

    def goto_profile(self):
        # make a popup window to view profile information
        self.profile = Profile()
        self.profile.show()


class ParticipantList(QtWidgets.QMainWindow):
    def __init__(self, training_id):
        super(ParticipantList, self).__init__()
        training_id = training_id
        connect_database()

        self.setObjectName("MainWindow")
        self.resize(1280, 720)
        self.setMinimumSize(QtCore.QSize(1280, 720))
        self.setMaximumSize(QtCore.QSize(1280, 720))
        self.setAutoFillBackground(False)
        self.setStyleSheet("background-color: #696969;")

        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setMinimumSize(QtCore.QSize(1280, 720))
        self.centralwidget.setMaximumSize(QtCore.QSize(1280, 720))
        self.centralwidget.setAutoFillBackground(False)
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
        self.profile_frame.setGeometry(QtCore.QRect(14, 80, 212, 329))
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
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("profile.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.profile_button.setIcon(icon)
        self.profile_button.setIconSize(QtCore.QSize(90, 90))
        self.profile_button.setObjectName("profile_button")
        self.profile_button.clicked.connect(self.goto_profile)

        # display name
        self.name_label = QtWidgets.QLabel(self.profile_frame)
        self.name_label.setGeometry(QtCore.QRect(10, 150, 191, 20))
        self.name_label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.name_label.setStyleSheet("border: none;\ncolor: white;\nfont-weight: bold;\n")
        self.name_label.setAlignment(QtCore.Qt.AlignCenter)
        self.name_label.setObjectName("name_label")
        self.name_label.setText("Name")

        # display id
        self.staff_id_label = QtWidgets.QLabel(self.profile_frame)
        self.staff_id_label.setGeometry(QtCore.QRect(10, 200, 191, 20))
        self.staff_id_label.setStyleSheet("border: none;\ncolor: white;\nfont-weight: bold;")
        self.staff_id_label.setAlignment(QtCore.Qt.AlignCenter)
        self.staff_id_label.setObjectName("staff_id_label")
        self.staff_id_label.setText("Staff ID")

        # display department
        self.department_label = QtWidgets.QLabel(self.profile_frame)
        self.department_label.setGeometry(QtCore.QRect(10, 250, 191, 20))
        self.department_label.setStyleSheet("border: none;\ncolor: white;\nfont-weight: bold;")
        self.department_label.setAlignment(QtCore.Qt.AlignCenter)
        self.department_label.setObjectName("department_label")
        self.department_label.setText("Department")

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
                       "d.departmentID AND employeeID = ?", (employeeID,))
        info = cursor.fetchone()
        self.id = str(info[1])
        self.name_db.setText(str(info[0]))
        self.id_db.setText(str(info[1]))
        self.department_db.setText(str(info[2]))

        # View whole training lists button
        self.list_button = QtWidgets.QPushButton(self.side_frame)
        self.list_button.setGeometry(QtCore.QRect(14, 470, 211, 91))
        self.list_button.setStyleSheet("color: white;\nfont-weight: bold;\nborder-radius: 10px;")
        self.list_button.setObjectName("list_button")
        self.list_button.setText("Training List")
        self.list_button.clicked.connect(self.back_to_hr_training_lists)

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
        self.horizontalLayout.addWidget(self.side_frame)
        self.logout_button.clicked.connect(gotologin)

        # Right frame
        self.main_frame = QtWidgets.QFrame(self.centralwidget)
        self.main_frame.setStyleSheet("border: 1px solid white;")
        self.main_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.main_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.main_frame.setObjectName("main_frame")

        # Title for the page
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
        self.header.setStyleSheet("border: none;\nborder-bottom: 1px solid white;\ncolor: white;\nfont-weight: bold;\n")
        self.header.setObjectName("header")
        self.header.setText("Participant List")

        # reject training button
        self.delete_button = QtWidgets.QPushButton(self.main_frame)
        self.delete_button.setGeometry(QtCore.QRect(930, 42, 36, 42))
        self.delete_button.setStyleSheet("border: none;")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("trash.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.delete_button.setIcon(icon5)
        self.delete_button.setIconSize(QtCore.QSize(40, 40))
        self.delete_button.setObjectName("delete_button")
        self.delete_button.clicked.connect(lambda: self.delete_training(training_id))

        # Display training name
        self.training_name_db = QtWidgets.QPushButton(self.main_frame)
        self.training_name_db.setGeometry(QtCore.QRect(30, 100, 681, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.training_name_db.setFont(font)
        self.training_name_db.setStyleSheet("color: white;\nfont-weight: bold;\nborder: none;\ntext-align: left;\n")
        self.training_name_db.setObjectName("training_name_db")

        # display training status
        self.training_status_db = QtWidgets.QLabel(self.main_frame)
        self.training_status_db.setGeometry(QtCore.QRect(870, 100, 73, 31))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(False)
        font.setWeight(50)
        self.training_status_db.setFont(font)
        self.training_status_db.setObjectName("training_status_db")

        self.training_status_label = QtWidgets.QLabel(self.main_frame)
        self.training_status_label.setGeometry(QtCore.QRect(730, 100, 131, 31))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.training_status_label.setFont(font)
        self.training_status_label.setStyleSheet("color: white;\nfont-weight: bold;\nborder: none;")
        self.training_status_label.setObjectName("training_status_label")
        self.training_status_label.setText("Training Status:")

        cursor.execute("SELECT trainingName, status FROM training WHERE trainingID=?", (training_id,))
        details = cursor.fetchone()
        self.training_name_db.setText(str(details[0]))
        if details[1] == "Approved":
            self.training_status_db.setStyleSheet("color: lightgreen; border: none;")
            self.delete_button.hide()
        elif details[1] == "Past":
            self.training_status_db.setStyleSheet("color: #EABFFF; border: none;")
        else:
            self.training_status_db.setStyleSheet("color: #FE8886; border: none;")
        self.training_status_db.setText(str(details[1]))

        # retrieve data from db
        cursor.execute("SELECT count(applicationID) FROM application WHERE trainingID=?", (training_id,))
        rows = cursor.fetchone()
        cursor.execute("SELECT a.employeeID, e.name, d.departmentName, a.applicationStatus "
                       "FROM application a, employee e, department d "
                       "WHERE a.employeeID=e.employeeID AND e.departmentID=d.departmentID AND trainingID=?",
                       (training_id,))
        application_info = cursor.fetchall()

        # display table
        self.application_table = QtWidgets.QTableWidget(self.main_frame)
        self.application_table.setGeometry(QtCore.QRect(20, 140, 961, 531))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.application_table.sizePolicy().hasHeightForWidth())
        self.application_table.setSizePolicy(sizePolicy)
        self.application_table.setStyleSheet("qproperty-uniformRowHeights: true;\nborder: none;")
        self.application_table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.application_table.setShowGrid(True)
        self.application_table.setGridStyle(QtCore.Qt.SolidLine)
        self.application_table.setCornerButtonEnabled(False)
        self.application_table.setObjectName("application_table")
        self.application_table.setColumnCount(5)
        self.application_table.setRowCount(rows[0])
        self.application_table.setSortingEnabled(True)

        # Set the header labels
        header_labels = ["Index", "Employee ID", "Name", "Department", "Status"]
        self.application_table.setHorizontalHeaderLabels(header_labels)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.application_table.horizontalHeader().setFont(font)
        self.application_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)

        # insert data to table
        for row, info in enumerate(application_info):
            index_item = QtWidgets.QTableWidgetItem(str(row + 1))
            brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
            brush.setStyle(QtCore.Qt.NoBrush)
            index_item.setForeground(brush)
            index_item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.application_table.setItem(row, 0, index_item)
            for column, data in enumerate(info):
                item = QtWidgets.QTableWidgetItem(str(data))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                item.setForeground(brush)
                self.application_table.setItem(row, column + 1, item)
                if column + 1 == 3:
                    font = QtGui.QFont()
                    font.setBold(True)
                    item.setFont(font)
                if column + 1 == 4:
                    if data == "Approved":
                        button = QtWidgets.QPushButton(data)
                        button.setStyleSheet("color: white;")
                        icon3 = QtGui.QIcon()
                        icon3.addPixmap(QtGui.QPixmap("success.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                        button.setIcon(icon3)
                        self.application_table.setCellWidget(row, column + 1, button)
                    else:
                        button = QtWidgets.QPushButton(data)
                        button.setStyleSheet("color: white;")
                        icon4 = QtGui.QIcon()
                        icon4.addPixmap(QtGui.QPixmap("reject.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                        button.setIcon(icon4)
                        self.application_table.setCellWidget(row, column + 1, button)
        self.application_table.resizeColumnsToContents()
        self.application_table.setColumnWidth(4, 150)
        self.application_table.horizontalHeader().setVisible(True)
        self.application_table.verticalHeader().setVisible(False)
        self.application_table.setSortingEnabled(True)
        self.horizontalLayout.addWidget(self.main_frame)
        self.setCentralWidget(self.centralwidget)

    def back_to_hr_training_lists(self):
        try:
            hr_training_view = HrView()
            widget.addWidget(hr_training_view)
            widget.setCurrentIndex(widget.currentIndex() + 1)
        except Exception as e:
            # Show error message box or print the error
            error_message = "An error occurred: " + str(e)
            QMessageBox.critical(self, "Error", error_message, QMessageBox.Ok)
            print(error_message)

    def goto_profile(self):
        # make a popup window to view profile information
        self.profile = Profile()
        self.profile.show()

    def delete_training(self, training_id):
        delete_box = QtWidgets.QMessageBox()
        delete_box.setIcon(QtWidgets.QMessageBox.Question)
        delete_box.setWindowTitle("Confirmation")
        delete_box.setText("Are you sure you want to delete this training?")
        delete_box.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        confirmation = delete_box.exec_()
        if confirmation == QtWidgets.QMessageBox.Yes:
            cursor.execute("DELETE FROM training WHERE trainingID=?", (training_id,))
            connect.commit()
            cursor.execute("DELETE FROM application WHERE trainingID=?", (training_id,))
            connect.commit()
            cursor.execute("DELETE FROM notification WHERE trainingID=?", (training_id,))
            connect.commit()
            QtWidgets.QMessageBox.information(None, "Infomation", "The training removed.", QtWidgets.QMessageBox.Ok)
            self.back_to_hr_training_lists()


class Approval(QtWidgets.QMainWindow):
    def __init__(self, training_id):
        super(Approval, self).__init__()
        training_id = training_id
        connect_database()
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setMinimumSize(QtCore.QSize(1280, 720))
        self.centralwidget.setMaximumSize(QtCore.QSize(1280, 720))
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.setObjectName("MainWindow")
        self.resize(1280, 720)
        self.setMinimumSize(QtCore.QSize(1280, 720))
        self.setMaximumSize(QtCore.QSize(1280, 720))
        self.setAutoFillBackground(False)
        self.setStyleSheet("background-color: #696969;")

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
        self.profile_frame.setGeometry(QtCore.QRect(14, 80, 212, 329))
        self.profile_frame.setStyleSheet("border-radius: 10px;")
        self.profile_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.profile_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.profile_frame.setObjectName("profile_frame")

        # profile button to see more profile details
        self.profile_button = QtWidgets.QPushButton(self.profile_frame)
        self.profile_button.setGeometry(QtCore.QRect(63, 40, 90, 90))
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.profile_button.sizePolicy().hasHeightForWidth())
        self.profile_button.setSizePolicy(size_policy)
        self.profile_button.setMinimumSize(QtCore.QSize(90, 90))
        self.profile_button.setMaximumSize(QtCore.QSize(90, 90))
        self.profile_button.setStyleSheet("border: none;\nborder-radius: 50%;\n")
        self.profile_button.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("profile.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.profile_button.setIcon(icon)
        self.profile_button.setIconSize(QtCore.QSize(90, 90))
        self.profile_button.clicked.connect(self.goto_profile)
        self.profile_button.setObjectName("profile_button")

        # display name
        self.name_label = QtWidgets.QLabel(self.profile_frame)
        self.name_label.setGeometry(QtCore.QRect(10, 150, 191, 20))
        self.name_label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.name_label.setStyleSheet("border: none;\ncolor: white;\nfont-weight: bold;\n")
        self.name_label.setAlignment(QtCore.Qt.AlignCenter)
        self.name_label.setObjectName("name_label")

        # display id
        self.staff_id_label = QtWidgets.QLabel(self.profile_frame)
        self.staff_id_label.setGeometry(QtCore.QRect(10, 200, 191, 20))
        self.staff_id_label.setStyleSheet("border: none;\ncolor: white;\nfont-weight: bold;")
        self.staff_id_label.setAlignment(QtCore.Qt.AlignCenter)
        self.staff_id_label.setObjectName("staff_id_label")
        self.staff_id_label.setText("Staff ID")

        # display department
        self.department_label = QtWidgets.QLabel(self.profile_frame)
        self.department_label.setGeometry(QtCore.QRect(10, 250, 191, 20))
        self.department_label.setStyleSheet("border: none;\ncolor: white;\nfont-weight: bold;")
        self.department_label.setAlignment(QtCore.Qt.AlignCenter)
        self.department_label.setObjectName("department_label")

        # calling the user details from db and set it in these variable
        self.name_db = QtWidgets.QLabel(self.profile_frame)
        self.name_db.setGeometry(QtCore.QRect(10, 170, 191, 20))
        self.name_db.setStyleSheet("border: none;\ncolor: white;")
        self.name_db.setAlignment(QtCore.Qt.AlignCenter)
        self.name_db.setObjectName("name_db")
        self.name_label.setText("Name")

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
        self.department_label.setText("Department")

        cursor.execute("SELECT name, employeeID, departmentName FROM employee e, department d WHERE e.departmentID="
                       "d.departmentID AND employeeID = ?", (employeeID,))
        info = cursor.fetchone()
        self.id = str(info[1])
        self.name_db.setText(info[0])
        self.id_db.setText(str(info[1]))
        self.department_db.setText(str(info[2]))

        # View whole training lists button
        self.list_button = QtWidgets.QPushButton(self.side_frame)
        self.list_button.setGeometry(QtCore.QRect(14, 470, 211, 91))
        self.list_button.setStyleSheet("color: white;\nfont-weight: bold;\nborder-radius: 10px;")
        self.list_button.setObjectName("list_button")
        self.list_button.setText("Training List")
        self.list_button.clicked.connect(self.back_to_hr_training_lists)

        # Log out button
        self.logout_button = QtWidgets.QPushButton(self.side_frame)
        self.logout_button.setGeometry(QtCore.QRect(14, 650, 51, 41))
        self.logout_button.setStyleSheet("border: none;\nborder-radius: 50%;")
        self.logout_button.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("logout.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.logout_button.setIcon(icon1)
        self.logout_button.setIconSize(QtCore.QSize(45, 45))
        self.logout_button.clicked.connect(gotologin)
        self.logout_button.setObjectName("logout_button")
        self.horizontalLayout.addWidget(self.side_frame)

        # Right frame
        self.main_frame = QtWidgets.QFrame(self.centralwidget)
        self.main_frame.setStyleSheet("border: 1px solid white;")
        self.main_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.main_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.main_frame.setObjectName("main_frame")

        # Title for the page
        self.header = QtWidgets.QLabel(self.main_frame)
        self.header.setGeometry(QtCore.QRect(14, 14, 971, 81))
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.header.sizePolicy().hasHeightForWidth())
        self.header.setSizePolicy(size_policy)
        font = QtGui.QFont()
        font.setPointSize(22)
        font.setBold(True)
        font.setWeight(75)
        self.header.setFont(font)
        self.header.setStyleSheet("border: none;\nborder-bottom: 1px solid white;\ncolor: white;\nfont-weight: bold;\n")
        self.header.setObjectName("header")
        self.header.setText("Approval")

        cursor.execute("SELECT trainingName FROM training WHERE trainingID=?", (training_id,))
        training_name = cursor.fetchone()[0]
        self.training_name_db = QtWidgets.QPushButton(self.main_frame)
        self.training_name_db.setGeometry(QtCore.QRect(30, 100, 681, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.training_name_db.setFont(font)
        self.training_name_db.setStyleSheet("color: white;\nfont-weight: bold;\nborder: none;\ntext-align: left;\n")
        self.training_name_db.setObjectName("training_name_db")
        self.training_name_db.setText(training_name)

        # display training status
        self.training_status_db = QtWidgets.QLabel(self.main_frame)
        self.training_status_db.setGeometry(QtCore.QRect(870, 100, 73, 31))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(False)
        font.setWeight(50)
        self.training_status_db.setFont(font)
        self.training_status_db.setStyleSheet("color: lightblue;\nfont-weight: regular;\nborder: none;")
        self.training_status_db.setObjectName("training_status_db")
        self.training_status_db.setText("Pending")
        self.training_status_label = QtWidgets.QLabel(self.main_frame)
        self.training_status_label.setGeometry(QtCore.QRect(730, 100, 131, 31))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.training_status_label.setFont(font)
        self.training_status_label.setStyleSheet("color: white;\nfont-weight: bold;\nborder: none;")
        self.training_status_label.setObjectName("training_status_label")
        self.training_status_label.setText("Training Status:")

        # retrieve data from db
        cursor.execute("SELECT count(applicationID) FROM application WHERE trainingID=?", (training_id,))
        rows = cursor.fetchone()
        cursor.execute("SELECT a.employeeID, e.name, d.departmentName, a.applicationStatus "
                       "FROM application a, employee e, department d "
                       "WHERE a.employeeID=e.employeeID AND e.departmentID=d.departmentID AND "
                       "trainingID=?", (training_id,))
        application_info = cursor.fetchall()

        # display table
        self.application_table = QtWidgets.QTableWidget(self.main_frame)
        self.application_table.setGeometry(QtCore.QRect(20, 140, 961, 531))
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.application_table.sizePolicy().hasHeightForWidth())
        self.application_table.setSizePolicy(size_policy)
        self.application_table.setStyleSheet("qproperty-uniformRowHeights: true;\nborder: none;")
        self.application_table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.application_table.setShowGrid(True)
        self.application_table.setGridStyle(QtCore.Qt.SolidLine)
        self.application_table.setCornerButtonEnabled(False)
        self.application_table.setObjectName("application_table")
        self.application_table.setColumnCount(5)
        self.application_table.setRowCount(rows[0])
        self.application_table.setSortingEnabled(True)

        # Set the header labels
        header_labels = ["Index", "Employee ID", "Name", "Department", "Status"]
        self.application_table.setHorizontalHeaderLabels(header_labels)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.application_table.horizontalHeader().setFont(font)
        self.application_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)

        # insert data to table
        for row, info in enumerate(application_info):
            index_item = QtWidgets.QTableWidgetItem(str(row + 1))
            brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
            brush.setStyle(QtCore.Qt.NoBrush)
            index_item.setForeground(brush)
            index_item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.application_table.setItem(row, 0, index_item)
            for column, data in enumerate(info):
                item = QtWidgets.QTableWidgetItem(str(data))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                item.setForeground(brush)
                self.application_table.setItem(row, column + 1, item)
                if column + 1 == 3:
                    font = QtGui.QFont()
                    font.setBold(True)
                    item.setFont(font)
                if column + 1 == 4:
                    if data == "Pending":
                        self.application_table.setCellWidget(row, column + 1, self.add_button(data, row, training_id))
                    elif data == "Approved":
                        button = QtWidgets.QPushButton(data)
                        button.setStyleSheet("color: white;")
                        icon3 = QtGui.QIcon()
                        icon3.addPixmap(QtGui.QPixmap("success.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                        button.setIcon(icon3)
                        self.application_table.setCellWidget(row, column + 1, button)
                    else:
                        button = QtWidgets.QPushButton(data)
                        button.setStyleSheet("color: white;")
                        icon4 = QtGui.QIcon()
                        icon4.addPixmap(QtGui.QPixmap("reject.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                        button.setIcon(icon4)
                        self.application_table.setCellWidget(row, column + 1, button)
        self.application_table.resizeColumnsToContents()
        self.application_table.setColumnWidth(4, 150)
        self.application_table.horizontalHeader().setVisible(True)
        self.application_table.verticalHeader().setVisible(False)
        self.application_table.setSortingEnabled(True)

        # reject training button
        self.reject_training_button = QtWidgets.QPushButton(self.main_frame)
        self.reject_training_button.setGeometry(QtCore.QRect(860, 50, 112, 34))
        self.reject_training_button.setStyleSheet("color: white;\n"
                                                  "border-radius: 10px;")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("reject.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.reject_training_button.setIcon(icon3)
        self.reject_training_button.setText("Reject")
        self.reject_training_button.setObjectName("reject_training_button")
        self.reject_training_button.clicked.connect(lambda: self.reject_training(training_id))

        # approve training button
        self.approve_training_button = QtWidgets.QPushButton(self.main_frame)
        self.approve_training_button.setGeometry(QtCore.QRect(740, 50, 112, 34))
        self.approve_training_button.setStyleSheet("color: white;\n"
                                                   "border-radius: 10px;")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("success.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.approve_training_button.setIcon(icon2)
        self.approve_training_button.setText("Approve")
        self.approve_training_button.setObjectName("approve_training_button")
        self.approve_training_button.clicked.connect(lambda: self.approve_training(training_id))

        self.horizontalLayout.addWidget(self.main_frame)
        self.setCentralWidget(self.centralwidget)

    def add_button(self, data, row, training_id):
        button = QtWidgets.QPushButton(data)
        button.setStyleSheet("color: white;")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("pending.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        button.setIcon(icon2)
        button.clicked.connect(lambda: self.approval_participant(row, training_id))
        return button

    def approval_participant(self, data, training_id):
        row_items = []
        for column in range(5):
            item = self.application_table.item(data, column)
            if item is not None:
                row_items.append(item.text())
        approval_box = QtWidgets.QMessageBox()
        approval_box.setIcon(QtWidgets.QMessageBox.Question)
        approval_box.setWindowTitle("Approval")
        approval_box.setText("Do you want to approve this participant to join this training?")
        approval_box.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No |
                                        QtWidgets.QMessageBox.Cancel)
        approval_box.button(QtWidgets.QMessageBox.Yes).setText("Approve")
        approval_box.button(QtWidgets.QMessageBox.No).setText("Reject")
        approval = approval_box.exec_()
        date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        if approval == QtWidgets.QMessageBox.Yes:
            connect_database()
            print("11")
            cursor.execute("UPDATE application SET applicationStatus=? WHERE employeeID=? AND trainingID=?",
                           ("Approved", row_items[1], training_id))
            connect.commit()
            cursor.execute("INSERT INTO notification (notification_status, notification_date, employeeID, trainingID, "
                           "is_read) VALUES ('Approved', ?, ?, ?, 0)", (date_time, self.id, training_id))
            connect.commit()
            self.refresh_table(training_id)
        elif approval == QtWidgets.QMessageBox.No:
            cursor.execute("UPDATE application SET applicationStatus=? WHERE employeeID=? AND trainingID=?",
                           ("Rejected", row_items[1], training_id))
            connect.commit()
            cursor.execute("INSERT INTO notification (notification_status, notification_date, employeeID, trainingID, "
                           "is_read) VALUES ('Rejected', ?, ?, ?, 0)", (date_time, self.id, training_id))
            connect.commit()
            self.refresh_table(training_id)
        else:
            pass

    def refresh_table(self, training_id):
        # clear table content
        self.application_table.clearContents()

        # retrieve data from db
        cursor.execute("SELECT a.employeeID, e.name, d.departmentName, a.applicationStatus FROM application a, employee"
                       " e, department d WHERE a.employeeID=e.employeeID AND e.departmentID=d.departmentID AND "
                       "trainingID=?", (training_id,))
        application_info = cursor.fetchall()

        # insert data to table
        for row, info in enumerate(application_info):
            index_item = QtWidgets.QTableWidgetItem(str(row + 1))
            brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
            brush.setStyle(QtCore.Qt.NoBrush)
            index_item.setForeground(brush)
            index_item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.application_table.setItem(row, 0, index_item)
            for column, data in enumerate(info):
                item = QtWidgets.QTableWidgetItem(str(data))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                item.setForeground(brush)
                self.application_table.setItem(row, column + 1, item)
                if column + 1 == 3:
                    font = QtGui.QFont()
                    font.setBold(True)
                    item.setFont(font)
                if column + 1 == 4:
                    if data == "Pending":
                        self.application_table.setCellWidget(row, column + 1, self.add_button(data, row, training_id))
                    elif data == "Approved":
                        button = QtWidgets.QPushButton(data)
                        button.setStyleSheet("color: white;")
                        icon3 = QtGui.QIcon()
                        icon3.addPixmap(QtGui.QPixmap("success.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                        button.setIcon(icon3)
                        self.application_table.setCellWidget(row, column + 1, button)
                    else:
                        button = QtWidgets.QPushButton(data)
                        button.setStyleSheet("color: white;")
                        icon4 = QtGui.QIcon()
                        icon4.addPixmap(QtGui.QPixmap("reject.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                        button.setIcon(icon4)
                        self.application_table.setCellWidget(row, column + 1, button)
        self.application_table.resizeColumnsToContents()
        self.application_table.setColumnWidth(4, 150)

    def approve_training(self, training_id):
        self.training_id = training_id
        approve_box = QtWidgets.QMessageBox()
        approve_box.setIcon(QtWidgets.QMessageBox.Question)
        approve_box.setWindowTitle("Approval")
        approve_box.setText("Do you want to approve this training?")
        approve_box.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel)
        approve = approve_box.exec_()
        date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        if approve == QtWidgets.QMessageBox.Yes:
            try:
                try:
                    connect_database()
                    cursor = connect.cursor()
                    cursor.execute("""SELECT count(applicationStatus) FROM application WHERE applicationStatus = ? 
                    AND trainingID = ? """, ('Pending', training_id,))
                    pending = cursor.fetchone()[0]
                except Exception as e:
                    QMessageBox.critical(None, "Error", str(e), QMessageBox.Ok)

                if pending > 0:
                    approve_confirm_box = QtWidgets.QMessageBox()
                    approve_confirm_box.setIcon(QtWidgets.QMessageBox.Warning)
                    approve_confirm_box.setWindowTitle("Confirm Participants")
                    approve_confirm_box.setText("Participants in pending status will be considered approved.\n"
                                                "Are you confirm to proceed?")
                    approve_confirm_box.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
                    approve_confirm = approve_confirm_box.exec_()

                    if approve_confirm == QtWidgets.QMessageBox.Yes:
                        try:
                            connect_database()
                            cursor = connect.cursor()
                            cursor.execute("""SELECT employeeID FROM application 
                            WHERE applicationStatus = 'Pending' AND trainingID = ? """, (training_id,))
                            employees = cursor.fetchall()
                            cursor.execute("UPDATE application SET applicationStatus = 'Approved' "
                                           "WHERE applicationStatus = 'Pending' AND trainingID = ? ", (training_id,))
                            connect.commit()
                            for p in range(pending):
                                cursor.execute("""INSERT INTO notification 
                                                  (notification_status, notification_date, employeeID, trainingID, is_read)
                                                  VALUES ('Approved', ?, ?, ?, 0)""",
                                               (date_time, employees[p][0], training_id,))
                                connect.commit()
                            QtWidgets.QMessageBox.information(None, "Infomation",
                                                              "Application of the training cost was already"
                                                              " sent to finance department.",
                                                              QtWidgets.QMessageBox.Ok)
                            cursor.execute("""UPDATE training SET status='Approved' WHERE trainingID = ? """,
                                           (training_id,))
                            connect.commit()
                            self.refresh_table(training_id)
                            self.approve_training_button.deleteLater()
                            self.reject_training_button.deleteLater()
                            self.training_status_db.setText("Approved")
                            self.training_status_db.setStyleSheet("color: lightgreen; border: none;")
                        except Exception as e:
                            QMessageBox.critical(None, "Error", str(e), QMessageBox.Ok)
                            print(str(e))
                    else:  # No for approve question
                        pass
                else:  # No pending application"
                    QtWidgets.QMessageBox.information(None, "Infomation",
                                                      "Application of the training cost was already "
                                                      "sent to finance department.",
                                                      QtWidgets.QMessageBox.Ok)
                    try:
                        cursor = connect.cursor()
                        cursor.execute("""UPDATE training SET status = ? WHERE trainingID = ? """,
                                       ('Approved', training_id,))
                        connect.commit()
                    except Exception as e:
                        QMessageBox.critical(None, "Error", str(e), QMessageBox.Ok)
                    self.approve_training_button.deleteLater()
                    self.reject_training_button.deleteLater()
                    self.training_status_db.setText("Approved")
                    self.training_status_db.setStyleSheet("color: lightgreen; border: none;")
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e), QMessageBox.Ok)
        else:  # approval question NO
            pass

    def reject_training(self, training_id):
        reject_box = QtWidgets.QMessageBox()
        reject_box.setIcon(QtWidgets.QMessageBox.Question)
        reject_box.setWindowTitle("Approval")
        reject_box.setText("Do you want to cancel this training?")
        reject_box.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel)
        reject = reject_box.exec_()
        date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        if reject == QtWidgets.QMessageBox.Yes:
            cursor.execute("SELECT employeeID FROM application WHERE trainingID=?", (training_id,))
            employees = cursor.fetchall()
            cursor.execute("UPDATE application SET applicationStatus='Cancelled' WHERE trainingID=?", (training_id,))
            connect.commit()
            for n in range(len(employees)):
                cursor.execute("INSERT INTO notification (notification_status, notification_date, employeeID, "
                               "trainingID, is_read) VALUES ('Cancelled', ?, ?, ?, 0)", (date_time, employees[n][0],
                                                                                         training_id,))
                connect.commit()

            QtWidgets.QMessageBox.information(None, "Infomation", "The training is cancelled.",
                                              QtWidgets.QMessageBox.Ok)
            cursor.execute("UPDATE training SET status='Cancelled' WHERE trainingID=?", (training_id,))
            connect.commit()
            self.refresh_table(training_id)
            self.approve_training_button.deleteLater()
            self.reject_training_button.deleteLater()
            self.training_status_db.setText("Cancelled")
            self.training_status_db.setStyleSheet("color: #FE8886; border: none;")
        else:  # NO for confirmation box
            pass

    def back_to_hr_training_lists(self):
        try:
            hr_training_view = HrView()
            widget.addWidget(hr_training_view)
            widget.setCurrentIndex(widget.currentIndex() + 1)
        except Exception as e:
            # Show error message box or print the error
            error_message = "An error occurred: " + str(e)
            QMessageBox.critical(self, "Error", error_message, QMessageBox.Ok)
            print(error_message)

    def goto_profile(self):
        # make a popup window to view profile information
        self.profile = Profile()
        self.profile.show()


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
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.header.sizePolicy().hasHeightForWidth())
        self.header.setSizePolicy(size_policy)
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
        current_date = QtCore.QDate.currentDate()
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
        icon.addPixmap(QtGui.QPixmap("add.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.brochure_button.setIcon(icon)
        self.brochure_button.setIconSize(QtCore.QSize(60, 60))
        self.brochure_button.setObjectName("brochure_button")
        self.brochure_button.clicked.connect(self.add_brochure)

        self.new_training_name = QtWidgets.QLineEdit(self.main_frame)
        self.new_training_name.setGeometry(QtCore.QRect(60, 180, 311, 41))
        self.new_training_name.setStyleSheet("border: 1px solid white;\n"
                                             "color: black;\n"
                                             "background: white;\n"
                                             "border-radius: 10px;")
        self.new_training_name.setObjectName("new_training_name")

        self.cost = QtWidgets.QLineEdit(self.main_frame)
        self.cost.setGeometry(QtCore.QRect(60, 400, 111, 41))
        self.cost.setStyleSheet("border: 1px solid white;\n"
                                "color: black;\n"
                                "background: white;\n"
                                "border-radius: 10px;")
        self.cost.setObjectName("cost")

        self.description = QtWidgets.QPlainTextEdit(self.main_frame)
        self.description.setGeometry(QtCore.QRect(430, 440, 371, 211))
        self.description.setStyleSheet("border: 1px solid white;\n"
                                       "color: black;\n"
                                       "background: white;\n"
                                       "border-radius: 10px;")
        self.description.setObjectName("description")

        self.short_description = QtWidgets.QPlainTextEdit(self.main_frame)
        self.short_description.setGeometry(QtCore.QRect(60, 510, 311, 141))
        self.short_description.setStyleSheet("border: 1px solid white;\n"
                                             "color: black;\n"
                                             "background: white;\n"
                                             "border-radius: 10px;")
        self.short_description.setObjectName("short_description")

        self.max_participants = QtWidgets.QLineEdit(self.main_frame)
        self.max_participants.setGeometry(QtCore.QRect(220, 400, 111, 41))
        self.max_participants.setStyleSheet("border: 1px solid white;\n"
                                            "color: black;\n"
                                            "background: white;\n"
                                            "border-radius: 10px;")
        self.max_participants.setObjectName("max_participants")

        self.venue = QtWidgets.QLineEdit(self.main_frame)
        self.venue.setGeometry(QtCore.QRect(60, 290, 311, 41))
        self.venue.setStyleSheet("border: 1px solid white;\n"
                                 "color: black;\n"
                                 "background: white;\n"
                                 "border-radius: 10px;")
        self.venue.setObjectName("venue")

        connect_database()
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
            self, "Select Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp)")

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
            pixmap = brochure_image.pixmap(QtCore.QSize(855, 245))  # Adjust the size as needed
            # Convert QPixmap to bytes using QByteArray
            byte_array = QByteArray()
            buffer = QtCore.QBuffer(byte_array)
            buffer.open(QtCore.QIODevice.WriteOnly)
            pixmap.save(buffer, "PNG")  # Save the pixmap as PNG
            image_data = byte_array.data()

            # Perform validation for each input field
            if not training_name:
                # Training name is empty
                QtWidgets.QMessageBox.warning(self, "Validation Error",
                                              "Please enter a training name.")
                return False

            if not cost_per_person or not cost_per_person.isdigit() or int(cost_per_person) < 0:
                # Cost is empty, not a valid number, or not positive
                QtWidgets.QMessageBox.warning(self, "Validation Error", "Please enter a valid positive cost.")
                return False

            if date <= QtCore.QDate.currentDate():
                # Date is not larger than today's date
                QtWidgets.QMessageBox.warning(self, "Validation Error",
                                              "Please select a date larger than today's date.")
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

            if not image_data:
                # Brochure is not selected
                QtWidgets.QMessageBox.warning(self, "Validation Error", "Please select a brochure image.")
                return False

            else:
                connect_database()
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
                        max_participants, department_id, image_data,  status, publish
                    )
                )

                connect.commit()
                cursor.close()
                connect.close()

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
            # Rollback the transaction in case of an error
            connect.rollback()
            QtWidgets.QMessageBox.critical(self, "Error", str(e), QtWidgets.QMessageBox.Ok)

        except Exception as e:
            # Log the error
            logging.exception("An error occurred: %s", str(e))

            # Show an error message box
            error_message = "An error occurred: " + str(e)
            QtWidgets.QMessageBox.critical(self, "Error", error_message, QtWidgets.QMessageBox.Ok)

        finally:
            # Close the connection if it's still open
            if connect:
                connect.close()


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
        size_policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.header.sizePolicy().hasHeightForWidth())
        self.header.setSizePolicy(size_policy)
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
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.add_department_into_table.sizePolicy().hasHeightForWidth())
        self.add_department_into_table.setSizePolicy(size_policy)
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

        connect_database()
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
        status = "Approved"
        app_date = QtCore.QDate.currentDate()
        app_date_string = app_date.toString("yyyy-MM-dd")

        current_datetime = datetime.datetime.now()
        current_datetime_string = current_datetime.strftime("%Y-%m-%d %H:%M")
        employees_lists = []

        for department in self.department_list_items:
            connect_database()
            self.cursor = connect.cursor()
            self.cursor.execute("SELECT departmentID FROM department WHERE departmentName = ?", (department,))
            department_id1 = self.cursor.fetchone()  # Use fetchone() instead of fetchall()
            department_id = department_id1[0]

            connect_database()
            self.cursor = connect.cursor()
            self.cursor.execute("SELECT employeeID FROM employee WHERE departmentID = ?", (department_id,))
            employees = self.cursor.fetchall()
            employees_lists.extend(employees)

        for employee in employees_lists:
            employee_id = employee[0]
            try:
                connect_database()
                self.cursor = connect.cursor()
                self.cursor.execute("""INSERT INTO application(employeeID, trainingID, applicationStatus, 
                applicationDate) VALUES (?, ?, ?, ?)""",
                                    (employee_id, self.training_id_for_insertion, status, app_date_string))
                connect.commit()

                self.cursor.execute("""INSERT INTO notification(notification_status, notification_date, employeeID,
                trainingID, is_read) VALUES (?, ?, ?, ?, ?)""",
                                    (status, current_datetime_string, employee_id, self.training_id_for_insertion,
                                     False))
                connect.commit()
                # Close the cursor and connection
                cursor.close()
                connect.close()

            except sqlite3.Error as e:
                # Rollback the transaction in case of an error
                connect.rollback()
                QtWidgets.QMessageBox.critical(self, "Error", str(e), QtWidgets.QMessageBox.Ok)

            finally:
                # Close the connection if it's still open
                if connect:
                    connect.close()

        QtWidgets.QMessageBox.information(self, "Success", "Applications added successfully.",
                                          QtWidgets.QMessageBox.Ok)
        self.reject()


class ModifyTraining(QtWidgets.QDialog):
    def __init__(self, trainingID):
        super(ModifyTraining, self).__init__()
        self.trainingID = trainingID

        self.setObjectName("Modify Training")
        self.setWindowTitle("Modify Training")
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
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.header.sizePolicy().hasHeightForWidth())
        self.header.setSizePolicy(size_policy)
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
        self.header.setText("Modify Training")

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
        self.new_training_name.setStyleSheet("border: 1px solid white;\n"
                                             "color: black;\n"
                                             "background: white;\n"
                                             "border-radius: 10px;")
        self.new_training_name.setObjectName("new_training_name")

        self.cost = QtWidgets.QLineEdit(self.main_frame)
        self.cost.setGeometry(QtCore.QRect(60, 400, 111, 41))
        self.cost.setStyleSheet("border: 1px solid white;\n"
                                "color: black;\n"
                                "background: white;\n"
                                "border-radius: 10px;")
        self.cost.setObjectName("cost")

        self.description = QtWidgets.QPlainTextEdit(self.main_frame)
        self.description.setGeometry(QtCore.QRect(430, 440, 371, 211))
        self.description.setStyleSheet("border: 1px solid white;\n"
                                       "color: black;\n"
                                       "background: white;\n"
                                       "border-radius: 10px;")
        self.description.setObjectName("description")

        self.short_description = QtWidgets.QPlainTextEdit(self.main_frame)
        self.short_description.setGeometry(QtCore.QRect(60, 510, 311, 141))
        self.short_description.setStyleSheet("border: 1px solid white;\n"
                                             "color: black;\n"
                                             "background: white;\n"
                                             "border-radius: 10px;")
        self.short_description.setObjectName("short_description")

        self.max_participants = QtWidgets.QLineEdit(self.main_frame)
        self.max_participants.setGeometry(QtCore.QRect(220, 400, 111, 41))
        self.max_participants.setStyleSheet("border: 1px solid white;\n"
                                            "color: black;\n"
                                            "background: white;\n"
                                            "border-radius: 10px;")
        self.max_participants.setObjectName("max_participants")

        self.venue = QtWidgets.QLineEdit(self.main_frame)
        self.venue.setGeometry(QtCore.QRect(60, 290, 311, 41))
        self.venue.setStyleSheet("border: 1px solid white;\n"
                                 "color: black;\n"
                                 "background: white;\n"
                                 "border-radius: 10px;")
        self.venue.setObjectName("venue")

        connect_database()
        self.cursor = connect.cursor()
        self.cursor.execute("SELECT * FROM department")
        department_list = self.cursor.fetchall()

        self.department_pick = QtWidgets.QComboBox(self.main_frame)
        self.department_pick.setGeometry(QtCore.QRect(430, 290, 291, 41))
        self.department_pick.setStyleSheet("color:  #00ced1;")
        self.department_pick.setObjectName("department_pick")
        self.department_pick.addItem("Select Department")  # Add a placeholder item
        self.department_pick.addItems([department[1] for department in department_list])

        self.edit_btn = QtWidgets.QPushButton(self.main_frame)
        self.edit_btn.setGeometry(QtCore.QRect(939, 600, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.edit_btn.setFont(font)
        self.edit_btn.setText("Modify")
        self.edit_btn.setStyleSheet("color: white;\n"
                                    "font-weight: bold;\n"
                                    "border-radius: 10px;\n"
                                    "background: #008287;")
        self.edit_btn.setObjectName("modify_button")
        self.edit_btn.clicked.connect(self.modify_training)

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

        # Fetch training data from the database
        training_data = self.fetch_training_data(trainingID)

        # Set the fetched data to the entry fields
        self.set_training_data(training_data)

    def fetch_training_data(self, trainingID):
        connect_database()
        self.cursor = connect.cursor()
        self.cursor.execute(
            "SELECT trainingID, trainingName, date, time, duration, venue, short_description, description, "
            "max_par, brochure, departmentID, cost from training WHERE trainingID = ?",
            (trainingID,))
        training_data = self.cursor.fetchone()
        return training_data

    def set_training_data(self, training_data):
        self.new_training_name.setText(str(training_data[1]))
        self.venue.setText(str(training_data[5]))

        db_date_str = training_data[2]
        db_date = datetime.datetime.strptime(db_date_str, "%Y-%m-%d")  # Convert to datetime object
        db_date_obj = QtCore.QDate(db_date.year, db_date.month, db_date.day)
        self.date_pick.setDate(db_date_obj)

        db_time = training_data[3]
        db_time_obj = QtCore.QTime.fromString(db_time, "HH:mm")
        self.time_pick.setTime(db_time_obj)

        self.duration_pick.setValue(training_data[4])
        self.short_description.setPlainText(str(training_data[6]))
        self.description.setPlainText(str(training_data[7]))

        department_id = training_data[10]
        department_name = self.get_department_name(department_id)
        if department_name:
            self.department_pick.setCurrentText(department_name)
        else:
            self.department_pick.setCurrentIndex(0)

        max_participants = training_data[8]
        self.max_participants.setText(str(max_participants))
        cost_per_person = float(training_data[11]) / int(training_data[8])
        cost_per_person_str = "{:.2f}".format(cost_per_person)
        self.cost.setText(cost_per_person_str)

        brochure_image_data = training_data[9]  # Assuming the brochure image is stored in the 10th column (index 9)
        pixmap = QtGui.QPixmap()
        pixmap.loadFromData(brochure_image_data)
        self.brochure_button.setIcon(QtGui.QIcon(pixmap))
        self.brochure_button.setIconSize(QtCore.QSize(200, 200))

    def get_department_name(self, department_id):
        connect_database()
        self.cursor = connect.cursor()
        self.cursor.execute("SELECT departmentName FROM department WHERE departmentID = ?", (department_id,))
        department_name = self.cursor.fetchone()
        if department_name:
            return department_name[0]
        return None

    def add_brochure(self):
        file_dialog = QtWidgets.QFileDialog()
        image_path, _ = file_dialog.getOpenFileName(
            self, "Select Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp)")

        if image_path:
            pixmap = QtGui.QPixmap(image_path)
            self.brochure_button.setIcon(QtGui.QIcon(pixmap))  # Set the selected image as the button's icon
            self.brochure_button.setIconSize(QtCore.QSize(855, 245))

    def modify_training(self):
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
            pixmap = brochure_image.pixmap(QtCore.QSize(855, 245))  # Adjust the size as needed
            # Convert QPixmap to bytes using QByteArray
            byte_array = QByteArray()
            buffer = QtCore.QBuffer(byte_array)
            buffer.open(QtCore.QIODevice.WriteOnly)
            pixmap.save(buffer, "PNG")  # Save the pixmap as PNG
            image_data = byte_array.data()

            # Perform validation for each input field
            if not training_name:
                # Training name is empty
                QtWidgets.QMessageBox.warning(self, "Validation Error",
                                              "Please enter a training name.")
                return False

            if not cost_per_person or not cost_per_person.replace('.', '', 1).isdigit() or float(cost_per_person) < 0:
                # Cost is empty, not a valid float, or not positive
                QtWidgets.QMessageBox.warning(self, "Validation Error", "Please enter a valid positive cost.")
                return False

            if date <= QtCore.QDate.currentDate():
                # Date is not larger than today's date
                QtWidgets.QMessageBox.warning(self, "Validation Error",
                                              "Please select a date larger than today's date.")
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

            if not image_data:
                # Brochure is not selected
                QtWidgets.QMessageBox.warning(self, "Validation Error", "Please select a brochure image.")
                return False

            else:
                connect_database()
                self.cursor = connect.cursor()
                self.cursor.execute("SELECT departmentID FROM department where departmentName = ?", (department,))
                dep_id = self.cursor.fetchone()
                department_id = dep_id[0]

                date_str = date.strftime('%Y-%m-%d')  # Convert datetime.date to string
                date1 = datetime.datetime.strptime(date_str, '%Y-%m-%d').strftime('%Y-%m-%d')
                cost = float(cost_per_person) * int(max_participants)

                try:
                    self.cursor.execute(
                        """UPDATE training SET trainingName = ?, cost = ?, date = ?, time = ?, duration = ?, venue = ?,
                        short_description = ?, description = ?, max_par = ?, departmentID = ?, brochure = ?
                        WHERE trainingID = ?""", (
                            training_name, cost, date1, time, duration, venue, short_description_text, description_text,
                            max_participants, department_id, image_data, self.trainingID)
                    )

                    connect.commit()
                    # Close the cursor and connection
                    cursor.close()
                    connect.close()

                    QtWidgets.QMessageBox.information(self, "Success", "Training data inserted successfully.",
                                                      QtWidgets.QMessageBox.Ok)
                    self.close()

                except sqlite3.Error as e:
                    # Rollback the transaction in case of an error
                    connect.rollback()
                    QtWidgets.QMessageBox.critical(self, "Error", str(e), QtWidgets.QMessageBox.Ok)

                finally:
                    # Close the connection if it's still open
                    if connect:
                        connect.close()

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", str(e), QtWidgets.QMessageBox.Ok)


class View(QtWidgets.QMainWindow):
    def __init__(self):
        super(View, self).__init__()
        # Define the trainingID attribute
        # self.trainingID = None

        loadUi("mytraining.ui", self)
        self.logout_button.clicked.connect(gotologin)
        self.profile_button.clicked.connect(self.goto_profile)
        self.notification_button.clicked.connect(goto_notification)
        self.list_button.clicked.connect(gotoview)
        self.my_training_button.clicked.connect(gotoTraining)

        cursor.execute('SELECT name, employeeID, departmentID FROM employee WHERE employeeID = ?', (employeeID,))
        display = cursor.fetchall()
        self.employeeID = display[0][1]
        self.name_db.setText(display[0][0])
        self.id_db.setText(str(display[0][1]))
        cursor.execute('SELECT departmentName FROM department WHERE departmentID=?', (display[0][2],))
        self.department_db.setText(cursor.fetchone()[0])

        self.profile_button.setIcon(QtGui.QIcon("profile.png"))
        self.logout_button.setIcon(QtGui.QIcon("logout.png"))
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
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.header.sizePolicy().hasHeightForWidth())
        self.header.setSizePolicy(size_policy)
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
        icon2.addPixmap(QtGui.QPixmap("search.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.search_button.setIcon(icon2)
        self.search_button.setIconSize(QtCore.QSize(25, 25))
        self.search_bar.setPlaceholderText("  Search...")
        self.search_button.setObjectName("search_button")
        self.search_button.clicked.connect(self.search_training)

        self.horizontalLayout.addWidget(self.main_frame)
        self.setCentralWidget(self.centralwidget)

        connect_database()

        self.cursor = connect.cursor()
        self.cursor.execute(
            "SELECT t.trainingID, t.trainingName, d.departmentName, t.short_description, t.brochure, t.publish, "
            "t.status"
            " FROM training t, department d"
            " WHERE d.departmentID = t.departmentID "
            "AND t.publish = 1 AND t.trainingID NOT IN (SELECT trainingID FROM application WHERE employeeID = ?)",
            (employeeID,))
        row_data = self.cursor.fetchall()  # Fetch all rows of data
        rows = len(row_data)  # Calculate the length of fetched data

        # Scroll area content widget
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, frame_width, rows *
                                                                 (frame_height + frame_spacing)))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")

        # Loop to create and position the frames
        for item in range(rows):
            training_id = row_data[item][0]
            self.training = QtWidgets.QFrame(self.scrollAreaWidgetContents_2)
            self.training.setGeometry(QtCore.QRect(0, item * (frame_height + frame_spacing), frame_width, frame_height))
            self.training.setStyleSheet("border: 1px solid white;\nbackground: #8A8A8A;\nborder-radius: 10px;")
            self.training.setFrameShape(QtWidgets.QFrame.StyledPanel)
            self.training.setFrameShadow(QtWidgets.QFrame.Raised)
            self.training.setObjectName("training")

            blob_data = row_data[item][4]
            pixmap = QtGui.QPixmap()
            pixmap.loadFromData(blob_data)

            self.training_image = QLabel(self.training)
            self.training_image.setGeometry(QtCore.QRect(20, 10, 200, 150))
            self.training_image.setScaledContents(True)
            self.training_image.setPixmap(pixmap)
            self.training_image.setObjectName(f"training_image_{training_id}")

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

    def goto_profile(self):
        # make a popup window to view profile information
        self.profile = Profile()
        self.profile.show()

    def gotoview(self):
        try:
            viewtraining = View()
            widget.addWidget(viewtraining)
            widget.setCurrentIndex(widget.currentIndex() + 1)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e), QMessageBox.Ok)
            print(str(e))

    def register_training(self):
        try:
            connect_database()
            self.cursor = connect.cursor()
            self.cursor.execute("INSERT INTO notification (notification_status, notification_date, employeeID, "
                                "trainingID, is_read ) VALUES (?,?,?,?,?)",
                                ("Pending", datetime.datetime.now().strftime('%Y-%m-%d %H:%M'),
                                 employeeID, self.trainingID, 0))
            connect.commit()
            self.cursor.execute(
                "INSERT INTO application (employeeID, trainingID, applicationStatus, applicationDate) VALUES (?,?,?,?)",
                (employeeID, self.trainingID, "Pending", datetime.datetime.now().strftime('%Y-%m-%d'))
            )
            connect.commit()
            QtWidgets.QMessageBox.information(None, "Infomation", "Successfully registered!",
                                              QtWidgets.QMessageBox.Ok)
            self.gotoview()

        except Exception as e:
            # Handle other exceptions
            error_message = "An error occurred: " + str(e)
            QtWidgets.QMessageBox.critical(self, "Error", error_message, QtWidgets.QMessageBox.Ok)
            print(error_message)

    def show_image_pop_up(self, picture_name):
        popup = ImagePopup(self)
        popup.setImage(QtGui.QPixmap(picture_name))
        popup.show()

    def viewTrainingDetails(self, trainingID):
        self.trainingID = trainingID
        try:
            loadUi("training_details.ui", self)
            self.logout_button.clicked.connect(gotologin)
            self.profile_button.clicked.connect(self.goto_profile)
            self.notification_button.clicked.connect(goto_notification)
            self.list_button.clicked.connect(gotoview)
            self.my_training_button.clicked.connect(gotoTraining)

            connect_database()
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
                "SELECT t.trainingName, t.status, t.cost, t.date, t.time, t.venue,t.duration, d.departmentName, "
                "t.short_description, t.brochure, t.max_par "
                "FROM training t, department d WHERE d.departmentID = t.departmentID AND t.trainingID = ?",
                (trainingID,))
            display = self.cursor.fetchall()
            self.training.setText(f"{display[0][0]}")

            date = datetime.datetime.strptime(display[0][3], "%Y-%m-%d")
            date = date.strftime("%d %B %Y")
            time = datetime.datetime.strptime(display[0][4], "%H:%M")
            time = time.strftime("%H:%M")
            self.date_db.setText(f"{date}")
            self.time_db.setText(f"{time}")
            self.venue_db.setText(f"{display[0][5]}")
            self.duration_db.setText(f"{display[0][6]}")
            self.department_db_2.setText(f"{display[0][7]}")
            self.description_db.setText(f"{display[0][8]}")

            # Retrieve the blob data from the database
            blob_data = display[0][9]
            # Convert the blob data into a QPixmap
            pixmap = QtGui.QPixmap()
            pixmap.loadFromData(blob_data)
            # Set the QPixmap as the icon for the brochure_button
            self.brochure_button.setIcon(QtGui.QIcon(pixmap))
            self.brochure_button.setIconSize(QtCore.QSize(200, 200))
            self.brochure_button.clicked.connect(lambda: self.show_image_pop_up(pixmap))

            self.register_button.clicked.connect(self.register_training)

            self.number_participants_db.setText(f"{display[0][10]}")

        except Exception as error:
            logging.exception("An error occurred in viewTrainingDetails:", str(error))

    def search_training(self):
        try:
            keywords = self.search_bar.text()

            # Query the database based on the keywords
            connect_database()
            self.cursor.execute(
                "SELECT DISTINCT t.trainingID, t.trainingName, d.departmentName, t.short_description, t.brochure "
                "FROM training t "
                "JOIN department d ON d.departmentID = t.departmentID "
                "WHERE publish = 1 AND (t.trainingName LIKE ? OR d.departmentName LIKE ? "
                "OR t.date LIKE ? OR t.time LIKE ?) "
                "AND t.trainingID NOT IN (SELECT trainingID FROM application WHERE employeeID = ?)",
                ('%' + keywords + '%', '%' + keywords + '%', '%' + keywords + '%',
                 '%' + keywords + '%', employeeID))
            search_results = self.cursor.fetchall()

            # Display the search results
            self.updateSearchResults(search_results)

        except Exception as e:
            # Show error message box or print the error
            error_message = "An error occurred: " + str(e)
            QMessageBox.critical(self, "Error", error_message, QMessageBox.Ok)

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
            training_id = search_results[item][0]
            self.training = QtWidgets.QFrame(self.scrollAreaWidgetContents_2)
            self.training.setGeometry(QtCore.QRect(0, item * (frame_height + frame_spacing), frame_width, frame_height))
            self.training.setStyleSheet("border: 1px solid white;\nbackground: #8A8A8A;\nborder-radius: 10px;")
            self.training.setFrameShape(QtWidgets.QFrame.StyledPanel)
            self.training.setFrameShadow(QtWidgets.QFrame.Raised)
            self.training.setObjectName("training")

            blob_data = search_results[item][4]
            pixmap = QtGui.QPixmap()
            pixmap.loadFromData(blob_data)

            self.training_image = QLabel(self.training)
            self.training_image.setGeometry(QtCore.QRect(20, 10, 200, 150))
            self.training_image.setScaledContents(True)
            self.training_image.setPixmap(pixmap)
            self.training_image.setObjectName(f"training_image_{training_id}")

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


class Profile(QtWidgets.QMainWindow):
    def __init__(self):
        super(Profile, self).__init__()
        loadUi("profile.ui", self)

        self.setFixedWidth(960)
        self.setFixedHeight(540)

        connect_database()
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
        self.profile.setPixmap(QtGui.QPixmap("profile.png"))
        self.department_db.setText(str(display[0][7]))


class Notification(QtWidgets.QMainWindow):
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
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.profile_button.sizePolicy().hasHeightForWidth())
        self.profile_button.setSizePolicy(size_policy)
        self.profile_button.setMinimumSize(QtCore.QSize(90, 90))
        self.profile_button.setMaximumSize(QtCore.QSize(90, 90))
        self.profile_button.setStyleSheet("border: none;\nborder-radius: 50%;\n")
        self.profile_button.setText("")
        self.profile_button.setIcon(QtGui.QIcon("profile.png"))
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
                       "d.departmentID AND employeeID = ?", (employeeID,))
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
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.header.sizePolicy().hasHeightForWidth())
        self.header.setSizePolicy(size_policy)
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
                       "n.employeeID=? ORDER BY n.notificationID DESC", (employeeID,))
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
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 945, self.rows * (91 + 19)))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")

        self.logout_button.clicked.connect(gotologin)
        self.profile_button.clicked.connect(self.goto_profile)
        self.notification_button.clicked.connect(goto_notification)
        self.list_button.clicked.connect(gotoview)
        self.my_training_button.clicked.connect(gotoTraining)

        cursor.execute('SELECT name, employeeID, departmentID FROM employee WHERE employeeID = ?', (employeeID,))
        display = cursor.fetchall()
        self.employeeID = display[0][1]
        self.name_db.setText(display[0][0])
        self.id_db.setText(str(display[0][1]))
        cursor.execute('SELECT departmentName FROM department WHERE departmentID=?', (display[0][2],))
        self.department_db.setText(cursor.fetchone()[0])
        self.profile_button.setIcon(QtGui.QIcon("profile.png"))
        self.logout_button.setIcon(QtGui.QIcon("logout.png"))

        # template for each the notification
        for row in range(self.rows):
            date_time = datetime.datetime.strptime(data[row][2], "%Y-%m-%d %H:%M")
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
            if data[row][1] == "Pending":
                self.status_image.setPixmap(QtGui.QPixmap("pending.png"))
            elif data[row][1] == "Approved":
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
            self.time.setGeometry(QtCore.QRect(820, 40, 68, 19))
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
            if data[row][1] == "Pending":
                self.notification_text.setText("The request to join the training is pending. Will notify you later when"
                                               " the request is approved or rejected.")
            elif data[row][1] == "Approved":
                self.notification_text.setText("You are successfully approved by HR department to join the training.")
            elif data[row][1] == "Rejected":
                self.notification_text.setText("You are rejected by HR department to join the training.")
            else:
                self.notification_text.setText("The training is cancelled.")
            self.notification_text.setScaledContents(False)
            self.notification_text.setWordWrap(True)
            self.notification_text.setObjectName("notification_text")

            self.date = QtWidgets.QLabel(self.notification_frame)
            self.date.setGeometry(QtCore.QRect(790, 60, 125, 20))
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
        self.scrollAreaWidgetContents_2.setMinimumHeight(self.rows * (91 + 19))

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
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e), QMessageBox.Ok)

        keywords = self.search_bar.text()
        cursor.execute("SELECT t.trainingName, n.notification_status, n.notification_date "
                       "FROM training t, notification n, employee e "
                       "WHERE n.trainingID=t.trainingID AND n.employeeID=e.employeeID AND n.employeeID=? "
                       "AND (t.trainingName LIKE ? OR n.notification_status LIKE ? OR n.notification_date LIKE ? OR "
                       "strftime('%m', n.notification_date)=strftime('%m', ?)) ORDER BY n.notificationID DESC",
                       (self.id, '%' + keywords + '%', '%' + keywords + '%', '%' + keywords + '%',
                        '%' + keywords + '%'))
        data = cursor.fetchall()
        rows = len(data)

        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 945, rows * (91 + 19)))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        for row in range(rows):
            date_time = datetime.datetime.strptime(data[row][2], "%Y-%m-%d %H:%M")
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
            if data[row][1] == "Pending":
                self.status_image.setPixmap(QtGui.QPixmap("pending.png"))
            elif data[row][1] == "Approved":
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
            if data[row][1] == "Pending":
                self.notification_text.setText("The request to join the training is pending. Will notify you later when"
                                               " the request is approved or rejected.")
            elif data[row][1] == "Approved":
                self.notification_text.setText("You are successfully approved by HR department to join the training.")
            elif data[row][1] == "Rejected":
                self.notification_text.setText("You are rejected by HR department to join the training.")
            else:
                self.notification_text.setText("The training is cancelled.")
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

    def goto_profile(self):
        # make a popup window to view profile information
        self.profile = Profile()
        self.profile.show()


class MyTraining(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyTraining, self).__init__()

        loadUi("mytraining.ui", self)
        self.logout_button.clicked.connect(gotologin)
        self.profile_button.clicked.connect(self.goto_profile)
        self.notification_button.clicked.connect(goto_notification)
        self.list_button.clicked.connect(gotoview)
        self.my_training_button.clicked.connect(gotoTraining)

        cursor.execute('SELECT name, employeeID, departmentID FROM employee WHERE employeeID = ?', (employeeID,))
        display = cursor.fetchall()
        self.employeeID = display[0][1]
        self.name_db.setText(display[0][0])
        self.id_db.setText(str(display[0][1]))
        cursor.execute('SELECT departmentName FROM department WHERE departmentID=?', (display[0][2],))
        self.department_db.setText(cursor.fetchone()[0])
        self.profile_button.setIcon(QtGui.QIcon("profile.png"))
        self.logout_button.setIcon(QtGui.QIcon("logout.png"))

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
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.header.sizePolicy().hasHeightForWidth())
        self.header.setSizePolicy(size_policy)
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
        self.search_bar.setPlaceholderText("  Search...")

        self.search_button = QtWidgets.QPushButton(self.main_frame)
        self.search_button.setGeometry(QtCore.QRect(950, 57, 31, 34))
        self.search_button.setStyleSheet("border: none;")
        self.search_button.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("search.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.search_button.setIcon(icon2)
        self.search_button.setIconSize(QtCore.QSize(25, 25))
        self.search_button.setObjectName("search_button")
        self.search_button.clicked.connect(self.searchTraining)

        self.horizontalLayout.addWidget(self.main_frame)
        self.setCentralWidget(self.centralwidget)

        connect_database()
        self.cursor = connect.cursor()
        self.cursor.execute(
            "SELECT t.trainingID, t.trainingName, d.departmentName, t.short_description, t.brochure, "
            "a.applicationStatus "
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
            training_id = row_data[item][0]
            status = row_data[item][5]

            self.training = QtWidgets.QFrame(self.scrollAreaWidgetContents_2)
            self.training.setGeometry(QtCore.QRect(0, item * (frame_height + frame_spacing), frame_width, frame_height))
            self.training.setStyleSheet("border: 1px solid white;\nbackground: #8A8A8A;\nborder-radius: 10px;")
            self.training.setFrameShape(QtWidgets.QFrame.StyledPanel)
            self.training.setFrameShadow(QtWidgets.QFrame.Raised)
            self.training.setObjectName("training")

            blob_data = row_data[item][4]
            pixmap = QtGui.QPixmap()
            pixmap.loadFromData(blob_data)

            self.training_image = QLabel(self.training)
            self.training_image.setGeometry(QtCore.QRect(20, 10, 200, 150))
            self.training_image.setScaledContents(True)
            self.training_image.setPixmap(pixmap)
            self.training_image.setObjectName(f"training_image_{training_id}")

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

    def goto_profile(self):
        # make a popup window to view profile information
        self.profile = Profile()
        self.profile.show()

    def viewTrainingDetails(self, trainingID):
        try:
            loadUi("training_details.ui", self)
            self.logout_button.clicked.connect(gotologin)
            self.profile_button.clicked.connect(self.goto_profile)
            self.notification_button.clicked.connect(goto_notification)
            self.list_button.clicked.connect(gotoview)
            self.my_training_button.clicked.connect(gotoTraining)

            connect_database()
            cursor.execute('SELECT name, employeeID, departmentID FROM employee WHERE employeeID = ?', (employeeID,))
            display = cursor.fetchall()
            self.name_db.setText(display[0][0])
            self.id_db.setText(str(display[0][1]))
            cursor.execute('SELECT departmentName FROM department WHERE departmentID=?', (display[0][2],))
            self.department_db.setText(cursor.fetchone()[0])
            self.profile_button.setIcon(QtGui.QIcon("profile.png"))
            self.header.setText("Training Details")

            self.cursor = connect.cursor()
            self.cursor.execute(
                "SELECT t.trainingName, t.status, t.cost, t.date, t.time, t.venue,t.duration, d.departmentName, "
                "t.short_description, t.brochure, t.max_par "
                "FROM training t, department d WHERE d.departmentID = t.departmentID AND t.trainingID = ?",
                (trainingID,))
            display = self.cursor.fetchall()
            self.training.setText(f"{display[0][0]}")

            date = datetime.datetime.strptime(display[0][3], "%Y-%m-%d")
            date = date.strftime("%d %B %Y")
            time = datetime.datetime.strptime(display[0][4], "%H:%M")
            time = time.strftime("%H:%M")
            self.date_db.setText(f"{date}")
            self.time_db.setText(f"{time}")
            self.venue_db.setText(f"{display[0][5]}")
            self.duration_db.setText(f"{display[0][6]}")
            self.department_db_2.setText(f"{display[0][7]}")
            self.description_db.setText(f"{display[0][8]}")
            self.number_participants_db.setText(f"{display[0][10]}")

            # Retrieve the blob data from the database
            blob_data = display[0][9]
            # Convert the blob data into a QPixmap
            pixmap = QtGui.QPixmap()
            pixmap.loadFromData(blob_data)
            # Set the QPixmap as the icon for the brochure_button
            self.brochure_button.setIcon(QtGui.QIcon(pixmap))
            self.brochure_button.setIconSize(QtCore.QSize(200, 200))
            self.brochure_button.clicked.connect(lambda: self.show_image_pop_up(pixmap))

            self.register_button.hide()

        except Exception as e:
            logging.exception("An error occurred in viewTrainingDetails:" + str(e))

    def searchTraining(self):
        try:
            keywords = self.search_bar.text()

            # Query the database based on the keywords
            connect_database()
            self.cursor.execute(
                "SELECT DISTINCT a.trainingID, t.trainingName, d.departmentName, t.short_description, t.brochure, "
                "a.applicationStatus FROM training t "
                "JOIN department d ON d.departmentID = t.departmentID "
                "JOIN application a ON a.trainingID = t.trainingID "
                "WHERE (t.trainingName LIKE ? OR d.departmentName LIKE ? "
                "OR t.date LIKE ? OR t.time LIKE ?) AND a.employeeID = ?",
                ('%' + keywords + '%', '%' + keywords + '%', '%' + keywords + '%',
                 '%' + keywords + '%', employeeID))
            search_results = self.cursor.fetchall()

            # Display the search results
            self.updateSearchResults(search_results)

        except Exception as e:
            # Show error message box or print the error
            error_message = "An error occurred: " + str(e)
            QMessageBox.critical(self, "Error", error_message, QMessageBox.Ok)

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
            training_id = search_results[item][0]
            status = search_results[item][5]

            self.training = QtWidgets.QFrame(self.scrollAreaWidgetContents_2)
            self.training.setGeometry(QtCore.QRect(0, item * (frame_height + frame_spacing), frame_width, frame_height))
            self.training.setStyleSheet("border: 1px solid white;\nbackground: #8A8A8A;\nborder-radius: 10px;")
            self.training.setFrameShape(QtWidgets.QFrame.StyledPanel)
            self.training.setFrameShadow(QtWidgets.QFrame.Raised)
            self.training.setObjectName("training")

            blob_data = search_results[item][4]
            pixmap = QtGui.QPixmap()
            pixmap.loadFromData(blob_data)

            self.training_image = QLabel(self.training)
            self.training_image.setGeometry(QtCore.QRect(20, 10, 200, 150))
            self.training_image.setScaledContents(True)
            self.training_image.setPixmap(pixmap)
            self.training_image.setObjectName(f"training_image_{training_id}")

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
            self.department_db_2.setStyleSheet("color: white;\n"
                                               "font-weight: regular;\n"
                                               "border: none;")
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

    def show_image_pop_up(self, picture_name):
        popup = ImagePopup(self)
        popup.setImage(QtGui.QPixmap(picture_name))
        popup.show()


def gotoview():
    try:
        viewtraining = View()
        widget.addWidget(viewtraining)
        widget.setCurrentIndex(widget.currentIndex() + 1)
    except Exception as e:
        QMessageBox.critical(None, "Error", str(e), QMessageBox.Ok)
        print(str(e))



def goto_notification():
    mainwindow = Notification()
    widget.addWidget(mainwindow)
    widget.setCurrentIndex(widget.currentIndex() + 1)


def gotologin():  # log out
    reply = QtWidgets.QMessageBox.question(None, "Log Out", "Are you sure you want to log out?",
                                           QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
    if reply == QtWidgets.QMessageBox.Yes:
        # Clear all memory and log out
        clear_memory()
        login = Login()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)
    else:
        # User chose not to log out, do nothing
        pass


def clear_memory():
    # Clear global variables
    global employeeID
    employeeID = None


def gotoTraining():
    training = MyTraining()
    widget.addWidget(training)
    widget.setCurrentIndex(widget.currentIndex() + 1)


def gotoHrView():
    hrview = HrView()
    widget.addWidget(hrview)
    widget.setCurrentIndex(widget.currentIndex() + 1)


app = QtWidgets.QApplication(sys.argv)
main_window = Login()
widget = QtWidgets.QStackedWidget()
widget.addWidget(main_window)
widget.setFixedWidth(1280)
widget.setFixedHeight(720)
widget.show()
app.exec_()
