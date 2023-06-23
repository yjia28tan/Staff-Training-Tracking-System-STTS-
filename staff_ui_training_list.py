# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'training_list.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Staff_MainWindow(object):
    def setupUi(self, StaffMainWindow):
        StaffMainWindow.setObjectName("MainWindow")
        StaffMainWindow.resize(1280, 720)
        StaffMainWindow.setMinimumSize(QtCore.QSize(1280, 720))
        StaffMainWindow.setMaximumSize(QtCore.QSize(1280, 720))
        StaffMainWindow.setStyleSheet("background-color: #696969;")

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
        self.name_db.setText("")  # here to set the data from database
        self.name_db.setAlignment(QtCore.Qt.AlignCenter)
        self.name_db.setObjectName("name_db")
        self.id_db = QtWidgets.QLabel(self.profile_frame)
        self.id_db.setGeometry(QtCore.QRect(10, 220, 191, 20))
        self.id_db.setStyleSheet("border: none;\ncolor: white;")
        self.id_db.setText("")  # here to set the data from database
        self.id_db.setAlignment(QtCore.Qt.AlignCenter)
        self.id_db.setObjectName("id_db")
        self.department_db = QtWidgets.QLabel(self.profile_frame)
        self.department_db.setGeometry(QtCore.QRect(10, 270, 191, 20))
        self.department_db.setStyleSheet("border: none;\ncolor: white;")
        self.department_db.setText("")  # here to set the data from database
        self.department_db.setAlignment(QtCore.Qt.AlignCenter)
        self.department_db.setObjectName("department_db")

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
        self.header.setText("")  # here to set the title
        self.header.setObjectName("header")

        # scrolling area to display lists of trainings
        self.scrollArea = QtWidgets.QScrollArea(self.main_frame)
        self.scrollArea.setGeometry(QtCore.QRect(14, 99, 971, 581))
        self.scrollArea.setStyleSheet("border: none;")
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 945, 581))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")

        # a frame to display training list details
        # template for each the training list
        self.training = QtWidgets.QFrame(self.scrollAreaWidgetContents_2)
        self.training.setGeometry(QtCore.QRect(0, 20, 931, 251))
        self.training.setStyleSheet("border: 1px solid white;\nbackground: #8A8A8A;\nborder-radius: 10px;")
        self.training.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.training.setFrameShadow(QtWidgets.QFrame.Raised)
        self.training.setObjectName("training")
        self.training_image = QtWidgets.QLabel(self.training)
        self.training_image.setGeometry(QtCore.QRect(20, 10, 200, 150))
        self.training_image.setText("")  # here to set the data from database
        self.training_image.setObjectName("training_image")
        self.department_label_2 = QtWidgets.QLabel(self.training)
        self.department_label_2.setGeometry(QtCore.QRect(230, 50, 111, 31))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.department_label_2.setFont(font)
        self.department_label_2.setStyleSheet("color: white;\nfont-weight: bold;\nborder: none;")
        self.department_label_2.setObjectName("department_label_2")
        self.department_db_2 = QtWidgets.QLabel(self.training)
        self.department_db_2.setGeometry(QtCore.QRect(340, 50, 581, 31))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(False)
        font.setWeight(50)
        self.department_db_2.setFont(font)
        self.department_db_2.setStyleSheet("color: white;\nfont-weight: regular;\nborder: none;\nbold: none;")
        self.department_db_2.setText("")  # here to set the data from database
        self.department_db_2.setObjectName("department_db_2")
        self.description_label = QtWidgets.QLabel(self.training)
        self.description_label.setGeometry(QtCore.QRect(230, 80, 101, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.description_label.setFont(font)
        self.description_label.setStyleSheet("color: white;\nfont-weight: bold;\nborder: none;")
        self.description_label.setObjectName("description_label")
        self.description_db = QtWidgets.QLabel(self.training)
        self.description_db.setGeometry(QtCore.QRect(230, 100, 691, 81))
        self.description_db.setStyleSheet("color: white;\nfont-weight: regular;\nborder: none;")
        self.description_db.setText("")  # here to set the data from database
        self.description_db.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.description_db.setWordWrap(True)
        self.description_db.setObjectName("description_db")
        self.view_button = QtWidgets.QPushButton(self.training)
        self.view_button.setGeometry(QtCore.QRect(810, 200, 112, 34))
        self.view_button.setStyleSheet("color: white;\nfont-weight: bold;\nborder-radius: 10px;\nbackground: #008287;")
        self.view_button.setObjectName("view_button")
        self.training_name_db = QtWidgets.QPushButton(self.training)
        self.training_name_db.setGeometry(QtCore.QRect(230, 20, 691, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.training_name_db.setFont(font)
        self.training_name_db.setStyleSheet("color: white;\nfont-weight: bold;\nborder: none;\ntext-align: left;\n")
        self.training_name_db.setText("")  # here to set the data from database
        self.training_name_db.setObjectName("training_name_db")

        # scroll bar
        self.scrollArea.setWidget(self.scrollAreaWidgetContents_2)

        # search input and button
        self.search_bar = QtWidgets.QLineEdit(self.main_frame)
        self.search_bar.setGeometry(QtCore.QRect(805, 60, 141, 25))
        self.search_bar.setStyleSheet("color: white;\nborder-radius: 10px;")
        self.search_bar.setObjectName("search_bar")
        self.search_button = QtWidgets.QPushButton(self.main_frame)
        self.search_button.setGeometry(QtCore.QRect(950, 57, 31, 34))
        self.search_button.setStyleSheet("border: none;")
        self.search_button.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("search.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.search_button.setIcon(icon2)
        self.search_button.setIconSize(QtCore.QSize(25, 25))
        self.search_button.setObjectName("search_button")

        self.horizontalLayout.addWidget(self.main_frame)
        StaffMainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(StaffMainWindow)
        QtCore.QMetaObject.connectSlotsByName(StaffMainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Staff Training Tracking System"))
        self.name_label.setText(_translate("MainWindow", "Name"))
        self.staff_id_label.setText(_translate("MainWindow", "Staff ID"))
        self.department_label.setText(_translate("MainWindow", "Department"))
        self.my_training_button.setText(_translate("MainWindow", "My Training"))
        self.list_button.setText(_translate("MainWindow", "Training List"))
        self.notification_button.setText(_translate("MainWindow", "Notification"))
        self.department_label_2.setText(_translate("MainWindow", "Department: "))
        self.description_label.setText(_translate("MainWindow", "Description: "))
        self.view_button.setText(_translate("MainWindow", "View More"))
        self.search_bar.setPlaceholderText(_translate("MainWindow", "  Search..."))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Staff_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())