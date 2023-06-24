from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QRect, QMetaObject, QCoreApplication
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QWidget, QFrame, QLabel, QPushButton, QMenuBar, QStatusBar


class Ui_MyTraining(object):
    def setupUi(self, MyTraining):
        MyTraining.setObjectName("MyTraining")
        MyTraining.resize(1280, 720)
        MyTraining.setMinimumSize(QtCore.QSize(1280, 720))
        MyTraining.setMaximumSize(QtCore.QSize(1280, 720))
        MyTraining.setStyleSheet("background-color: #696969;")

        self.centralwidget = QtWidgets.QWidget(MyTraining)
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
        self.profile_frame.setGeometry(QtCore.QRect(14, 14, 212, 329))
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
                                          "border-radius: 50%;\n")
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
                                      "font-weight: bold;\n")
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

        self.my_training_button = QtWidgets.QPushButton(self.side_frame)
        self.my_training_button.setGeometry(QtCore.QRect(14, 450, 211, 91))
        self.my_training_button.setStyleSheet("color: white;\n"
                                              "font-weight: bold;\n"
                                              "border-radius: 10px;")
        self.my_training_button.setObjectName("my_training_button")
        self.my_training_button.clicked.connect(self.my_training_clicked)

        self.list_button = QtWidgets.QPushButton(self.side_frame)
        self.list_button.setGeometry(QtCore.QRect(14, 350, 211, 91))
        self.list_button.setStyleSheet("color: white;\n"
                                       "font-weight: bold;\n"
                                       "border-radius: 10px;")
        self.list_button.setObjectName("list_button")

        self.notification_button = QtWidgets.QPushButton(self.side_frame)
        self.notification_button.setGeometry(QtCore.QRect(14, 550, 211, 91))
        self.notification_button.setStyleSheet("color: white;\n"
                                               "font-weight: bold;\n"
                                               "border-radius: 10px;")
        self.notification_button.setObjectName("notification_button")

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
                                  "font-weight: bold;\n")
        self.header.setText("")
        self.header.setObjectName("header")

        self.scrollArea = QtWidgets.QScrollArea(self.main_frame)
        self.scrollArea.setGeometry(QtCore.QRect(14, 99, 971, 581))
        self.scrollArea.setStyleSheet("border: none;")
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 950, 581))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents_2)

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
        self.search_button.setObjectName("search_button")

        self.horizontalLayout.addWidget(self.main_frame)
        MyTraining.setCentralWidget(self.centralwidget)

        self.retranslateUi_mytraining(MyTraining)
        QtCore.QMetaObject.connectSlotsByName(MyTraining)

    def retranslateUi(self, MyTraining):
        _translate = QtCore.QCoreApplication.translate
        MyTraining.setWindowTitle(_translate("MyTraining", "MainWindow"))
        self.name_label.setText(_translate("MyTraining", "Name"))
        self.staff_id_label.setText(_translate("MyTraining", "Staff ID"))
        self.department_label.setText(_translate("MyTraining", "Department"))
        self.my_training_button.setText(_translate("MyTraining", "My Training"))
        self.list_button.setText(_translate("MyTraining", "Training List"))
        self.notification_button.setText(_translate("MyTraining", "Notification"))
        self.search_bar.setPlaceholderText(_translate("MyTraining", "  Search..."))

    def my_training_clicked(self):
        # update the title
        self.header.setText("My Training")

        print("Button clicked!")

        self.centralwidget = QWidget(MyTraining)
        self.centralwidget.setObjectName(u"centralwidget")

        self.training = QFrame(self.centralwidget)
        self.training.setObjectName(u"training")
        self.training.setGeometry(QRect(0, 20, 931, 251))
        self.training.setStyleSheet(u"border: 1px solid white;\n"
                                    "background: #8A8A8A;\n"
                                    "border-radius: 10px;")
        self.training.setFrameShape(QFrame.StyledPanel)
        self.training.setFrameShadow(QFrame.Raised)

        self.training_image = QLabel(self.training)
        self.training_image.setObjectName(u"training_image")
        self.training_image.setGeometry(QRect(20, 10, 200, 150))

        self.department_label_2 = QLabel(self.training)
        self.department_label_2.setObjectName(u"department_label_2")
        self.department_label_2.setGeometry(QRect(230, 50, 111, 31))
        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        self.department_label_2.setFont(font)
        self.department_label_2.setStyleSheet(u"color: white;\n"
                                              "font-weight: bold;\n"
                                              "border: none;")

        self.department_db_2 = QLabel(self.training)
        self.department_db_2.setObjectName(u"department_db_2")
        self.department_db_2.setGeometry(QRect(340, 50, 581, 31))
        font1 = QFont()
        font1.setPointSize(8)
        font1.setBold(False)
        font1.setWeight(50)
        self.department_db_2.setFont(font1)
        self.department_db_2.setStyleSheet(u"color: white;\n"
                                           "font-weight: regular;\n"
                                           "border: none;\n"
                                           "bold: none;")

        self.description_label = QLabel(self.training)
        self.description_label.setObjectName(u"description_label")
        self.description_label.setGeometry(QRect(230, 80, 101, 21))
        self.description_label.setFont(font)
        self.description_label.setStyleSheet(u"color: white;\n"
                                             "font-weight: bold;\n"
                                             "border: none;")

        self.description_db = QLabel(self.training)
        self.description_db.setObjectName(u"description_db")
        self.description_db.setGeometry(QRect(230, 100, 691, 81))
        self.description_db.setStyleSheet(u"color: white;\n"
                                          "font-weight: regular;\n"
                                          "border: none;")
        # self.description_db.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)
        self.description_db.setWordWrap(True)

        self.view_button = QPushButton(self.training)
        self.view_button.setObjectName(u"view_button")
        self.view_button.setGeometry(QRect(810, 200, 112, 34))
        self.view_button.setStyleSheet(u"color: white;\n"
                                       "font-weight: bold;\n"
                                       "border-radius: 10px;\n"
                                       "background: #008287;\n"
                                       "")

        self.training_name_db = QPushButton(self.training)
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
                                            "text-align: left;\n"
                                            "")

        MyTraining.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MyTraining)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1280, 26))
        MyTraining.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MyTraining)
        self.statusbar.setObjectName(u"statusbar")
        MyTraining.setStatusBar(self.statusbar)

        self.retranslateUi_mytraining(MyTraining)

        QMetaObject.connectSlotsByName(MyTraining)
        # setupUi

    def retranslateUi_mytraining(self, MyTraining):
        MyTraining.setWindowTitle(QCoreApplication.translate("MyTraining", u"MainWindow", None))
        self.training_image.setText("")
        self.department_label_2.setText(QCoreApplication.translate("MyTraining", u"Department: ", None))
        self.department_db_2.setText("")
        self.description_label.setText(QCoreApplication.translate("MyTraining", u"Description: ", None))
        self.description_db.setText("")
        self.view_button.setText(QCoreApplication.translate("MyTraining", u"View More", None))
        self.training_name_db.setText("")


if __name__                                                                                                                                                                                                                                                                                                == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MyTraining = QtWidgets.QMainWindow()
    ui = Ui_MyTraining()
    ui.setupUi(MyTraining)
    MyTraining.show()
    sys.exit(app.exec_())
