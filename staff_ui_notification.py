from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import sqlite3
from datetime import datetime


connect = sqlite3.connect('StaffTrainingSystem')
cursor = connect.cursor()


class Notification(object):
    def setupUi(self, StaffMainWindow):
        StaffMainWindow.setObjectName("MainWindow")
        StaffMainWindow.resize(1280, 720)
        StaffMainWindow.setMinimumSize(QtCore.QSize(1280, 720))
        StaffMainWindow.setMaximumSize(QtCore.QSize(1280, 720))
        StaffMainWindow.setStyleSheet("background-color: #696969;")

        # should remove later after combine login page
        self.email = "test"
        self.password = 123123

        self.centralwidget = QtWidgets.QWidget(StaffMainWindow)
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
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("profile.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.profile_button.setIcon(icon)
        self.profile_button.setIconSize(QtCore.QSize(90, 90))
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
                       "d.departmentID AND e.email=? AND e.password=?", (self.email, self.password))
        info = cursor.fetchone()
        self.id = str(info[1])
        self.name_db.setText(info[0])
        self.id_db.setText(str(info[1]))
        self.department_db.setText(info[2])

        # View my training button
        self.my_training_button = QtWidgets.QPushButton(self.side_frame)
        self.my_training_button.setGeometry(QtCore.QRect(14, 450, 211, 91))
        self.my_training_button.setStyleSheet("color: white;\nfont-weight: bold;\nborder-radius: 10px;")
        self.my_training_button.setObjectName("my_training_button")

        # View whole training lists button
        self.list_button = QtWidgets.QPushButton(self.side_frame)
        self.list_button.setGeometry(QtCore.QRect(14, 350, 211, 91))
        self.list_button.setStyleSheet("color: white;\nfont-weight: bold;\nborder-radius: 10px;")
        self.list_button.setObjectName("list_button")

        # Notification button
        self.notification_button = QtWidgets.QPushButton(self.side_frame)
        self.notification_button.setGeometry(QtCore.QRect(14, 550, 211, 91))
        self.notification_button.setStyleSheet("color: white;\nfont-weight: bold;\nborder-radius: 10px;")
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
        self.header.setStyleSheet("border: none;\nborder-bottom: 1px solid white;\ncolor: white;\nfont-weight: bold;\n")
        self.header.setText("Notification")
        self.header.setObjectName("header")

        # Define the size and position of each frame
        cursor.execute("SELECT t.trainingName, n.notification_status, n.notification_date, n.is_read FROM training t, "
                       "notification n, employee e WHERE n.trainingID=t.trainingID AND n.employeeID=e.employeeID AND "
                       "n.employeeID=? ORDER BY n.notificationID DESC", self.id)
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
        # template for each the notification
        for row in range(self.rows):
            date_time = datetime.strptime(data[row][2], "%Y-%m-%d %H:%M")
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
        StaffMainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(StaffMainWindow)
        QtCore.QMetaObject.connectSlotsByName(StaffMainWindow)

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
            date_time = datetime.strptime(data[row][2], "%Y-%m-%d %H:%M")
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

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Staff Training Tracking System"))
        self.name_label.setText(_translate("MainWindow", "Name"))
        self.staff_id_label.setText(_translate("MainWindow", "Staff ID"))
        self.department_label.setText(_translate("MainWindow", "Department"))
        self.my_training_button.setText(_translate("MainWindow", "My Training"))
        self.list_button.setText(_translate("MainWindow", "Training List"))
        self.notification_button.setText(_translate("MainWindow", "Notification"))
        self.search_bar.setPlaceholderText(_translate("MainWindow", "  Search..."))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Notification()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
