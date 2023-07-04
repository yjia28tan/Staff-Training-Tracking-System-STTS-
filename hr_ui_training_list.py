# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'hr_training_list.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1280, 720)
        MainWindow.setMinimumSize(QtCore.QSize(1280, 720))
        MainWindow.setMaximumSize(QtCore.QSize(1280, 720))
        MainWindow.setStyleSheet("background-color: #696969;")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
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
        self.training = QtWidgets.QFrame(self.scrollAreaWidgetContents_2)
        self.training.setGeometry(QtCore.QRect(0, 50, 931, 251))
        self.training.setStyleSheet("border: 1px solid white;\n"
"background: #8A8A8A;\n"
"border-radius: 10px;")
        self.training.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.training.setFrameShadow(QtWidgets.QFrame.Raised)
        self.training.setObjectName("training")
        self.training_image = QtWidgets.QLabel(self.training)
        self.training_image.setGeometry(QtCore.QRect(20, 10, 200, 150))
        self.training_image.setText("")
        self.training_image.setObjectName("training_image")
        self.department_label_2 = QtWidgets.QLabel(self.training)
        self.department_label_2.setGeometry(QtCore.QRect(230, 50, 111, 31))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.department_label_2.setFont(font)
        self.department_label_2.setStyleSheet("color: white;\n"
"font-weight: bold;\n"
"border: none;")
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
"border: none;\n"
"bold: none;")
        self.department_db_2.setText("")
        self.department_db_2.setObjectName("department_db_2")
        self.description_label = QtWidgets.QLabel(self.training)
        self.description_label.setGeometry(QtCore.QRect(230, 80, 101, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.description_label.setFont(font)
        self.description_label.setStyleSheet("color: white;\n"
"font-weight: bold;\n"
"border: none;")
        self.description_label.setObjectName("description_label")
        self.description_db = QtWidgets.QLabel(self.training)
        self.description_db.setGeometry(QtCore.QRect(230, 100, 691, 81))
        self.description_db.setStyleSheet("color: white;\n"
"font-weight: regular;\n"
"border: none;")
        self.description_db.setText("")
        self.description_db.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.description_db.setWordWrap(True)
        self.description_db.setObjectName("description_db")
        self.training_name_db = QtWidgets.QPushButton(self.training)
        self.training_name_db.setGeometry(QtCore.QRect(230, 20, 691, 31))
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
        self.training_name_db.setText("")
        self.training_name_db.setObjectName("training_name_db")
        self.department_label_3 = QtWidgets.QLabel(self.training)
        self.department_label_3.setGeometry(QtCore.QRect(20, 170, 101, 31))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.department_label_3.setFont(font)
        self.department_label_3.setStyleSheet("color: white;\n"
"font-weight: bold;\n"
"border: none;")
        self.department_label_3.setObjectName("department_label_3")
        self.department_label_4 = QtWidgets.QLabel(self.training)
        self.department_label_4.setGeometry(QtCore.QRect(20, 200, 61, 31))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.department_label_4.setFont(font)
        self.department_label_4.setStyleSheet("color: white;\n"
"font-weight: bold;\n"
"border: none;")
        self.department_label_4.setObjectName("department_label_4")
        self.department_db_3 = QtWidgets.QLabel(self.training)
        self.department_db_3.setGeometry(QtCore.QRect(90, 200, 71, 31))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(False)
        font.setWeight(50)
        self.department_db_3.setFont(font)
        self.department_db_3.setStyleSheet("color: lightgreen;\n"
"font-weight: regular;\n"
"border: none;\n"
"bold: none;")
        self.department_db_3.setText("")
        self.department_db_3.setObjectName("department_db_3")
        self.department_db_4 = QtWidgets.QLabel(self.training)
        self.department_db_4.setGeometry(QtCore.QRect(130, 170, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(False)
        font.setWeight(50)
        self.department_db_4.setFont(font)
        self.department_db_4.setStyleSheet("color: white;\n"
"font-weight: regular;\n"
"border: none;\n"
"bold: none;")
        self.department_db_4.setText("")
        self.department_db_4.setObjectName("department_db_4")
        self.publish_button = QtWidgets.QPushButton(self.training)
        self.publish_button.setGeometry(QtCore.QRect(810, 200, 112, 34))
        self.publish_button.setStyleSheet("color: white;\n"
"font-weight: bold;\n"
"border-radius: 10px;\n"
"background: #008287;\n"
"")
        self.publish_button.setObjectName("publish_button")
        self.modify_button = QtWidgets.QPushButton(self.training)
        self.modify_button.setGeometry(QtCore.QRect(690, 200, 112, 34))
        self.modify_button.setStyleSheet("color: white;\n"
"font-weight: bold;\n"
"border-radius: 10px;\n"
"background: #008287;\n"
"")
        self.modify_button.setObjectName("modify_button")
        self.approval_button = QtWidgets.QPushButton(self.training)
        self.approval_button.setGeometry(QtCore.QRect(570, 200, 112, 34))
        self.approval_button.setStyleSheet("color: white;\n"
"font-weight: bold;\n"
"border-radius: 10px;\n"
"background: #008287;\n"
"")
        self.approval_button.setObjectName("approval_button")
        self.create_button = QtWidgets.QPushButton(self.scrollAreaWidgetContents_2)
        self.create_button.setGeometry(QtCore.QRect(808, 3, 121, 41))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.create_button.setFont(font)
        self.create_button.setStyleSheet("color: white;\n"
"font-weight: bold;\n"
"border: 1px solid white;\n"
"border-radius: 10px;")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("create.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.create_button.setIcon(icon2)
        self.create_button.setIconSize(QtCore.QSize(30, 36))
        self.create_button.setCheckable(False)
        self.create_button.setObjectName("create_button")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents_2)
        self.search_button = QtWidgets.QPushButton(self.main_frame)
        self.search_button.setGeometry(QtCore.QRect(950, 57, 31, 34))
        self.search_button.setStyleSheet("border: none;")
        self.search_button.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("search.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.search_button.setIcon(icon3)
        self.search_button.setIconSize(QtCore.QSize(25, 25))
        self.search_button.setObjectName("search_button")
        self.search_bar = QtWidgets.QLineEdit(self.main_frame)
        self.search_bar.setGeometry(QtCore.QRect(805, 60, 141, 25))
        self.search_bar.setStyleSheet("QLineEdit {color: white;}\n"
"QLineEdit::placeholder {color: white;}\n"
"QLineEdit {border-radius: 10px;\n"
"    border: 1px solid white;}\n"
"\n"
"")
        self.search_bar.setObjectName("search_bar")
        self.horizontalLayout.addWidget(self.main_frame)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
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


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())