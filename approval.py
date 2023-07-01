from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import sqlite3
import datetime


connect = sqlite3.connect('StaffTrainingSystem')
cursor = connect.cursor()

# should remove later
training_id = 1


class Approval(object):
    def setupUi(self, HRMainWindow):
        HRMainWindow.setObjectName("MainWindow")
        HRMainWindow.resize(1280, 720)
        HRMainWindow.setMinimumSize(QtCore.QSize(1280, 720))
        HRMainWindow.setMaximumSize(QtCore.QSize(1280, 720))
        HRMainWindow.setAutoFillBackground(False)
        HRMainWindow.setStyleSheet("background-color: #696969;")

        # should remove later after combine login page
        self.email = "test"
        self.password = 123123

        self.centralwidget = QtWidgets.QWidget(HRMainWindow)
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

        # View whole training lists button
        self.list_button = QtWidgets.QPushButton(self.side_frame)
        self.list_button.setGeometry(QtCore.QRect(14, 470, 211, 91))
        self.list_button.setStyleSheet("color: white;\nfont-weight: bold;\nborder-radius: 10px;")
        self.list_button.setObjectName("list_button")

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
        self.training_status_db.setStyleSheet("color: lightblue;\nfont-weight: regular;\nborder: none;")
        self.training_status_db.setObjectName("training_status_db")
        self.training_status_label = QtWidgets.QLabel(self.main_frame)
        self.training_status_label.setGeometry(QtCore.QRect(730, 100, 131, 31))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.training_status_label.setFont(font)
        self.training_status_label.setStyleSheet("color: white;\nfont-weight: bold;\nborder: none;")
        self.training_status_label.setObjectName("training_status_label")

        # retrieve data from db
        cursor.execute("SELECT count(applicationID) FROM application WHERE trainingID=?", (training_id,))
        rows = cursor.fetchone()
        cursor.execute("SELECT a.employeeID, e.name, d.departmentName, a.applicationStatus FROM application a, employee"
                       " e, department d WHERE a.employeeID=e.employeeID AND e.departmentID=d.departmentID AND "
                       "trainingID=?", (training_id,))
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
                    if data == "Pending":
                        self.application_table.setCellWidget(row, column + 1, self.add_button(data, row))
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

        # reject training button
        self.reject_training_button = QtWidgets.QPushButton(self.main_frame)
        self.reject_training_button.setGeometry(QtCore.QRect(860, 50, 112, 34))
        self.reject_training_button.setStyleSheet("color: white;\n"
                                                  "border-radius: 10px;")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("reject.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.reject_training_button.setIcon(icon3)
        self.reject_training_button.setObjectName("reject_training_button")
        self.reject_training_button.clicked.connect(self.reject_training)
        # approve training button
        self.approve_training_button = QtWidgets.QPushButton(self.main_frame)
        self.approve_training_button.setGeometry(QtCore.QRect(740, 50, 112, 34))
        self.approve_training_button.setStyleSheet("color: white;\n"
                                                   "border-radius: 10px;")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("success.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.approve_training_button.setIcon(icon2)
        self.approve_training_button.setObjectName("approve_training_button")
        self.approve_training_button.clicked.connect(self.approve_training)

        self.horizontalLayout.addWidget(self.main_frame)
        HRMainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(HRMainWindow)
        QtCore.QMetaObject.connectSlotsByName(HRMainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.name_label.setText(_translate("MainWindow", "Name"))
        self.staff_id_label.setText(_translate("MainWindow", "Staff ID"))
        self.department_label.setText(_translate("MainWindow", "Department"))
        self.list_button.setText(_translate("MainWindow", "Training List"))
        self.header.setText(_translate("MainWindow", "Approval"))
        # Retrieve data from db
        cursor.execute("SELECT trainingName FROM training WHERE trainingID=?", (training_id,))
        self.training_name_db.setText(_translate("MainWindow", cursor.fetchone()[0]))
        self.training_status_db.setText(_translate("MainWindow", "Pending"))
        self.training_status_label.setText(_translate("MainWindow", "Training Status:"))
        self.application_table.setSortingEnabled(True)
        self.reject_training_button.setText(_translate("MainWindow", "Reject"))
        self.approve_training_button.setText(_translate("MainWindow", "Approve"))

    def add_button(self, data, row):
        button = QtWidgets.QPushButton(data)
        button.setStyleSheet("color: white;")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("pending.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        button.setIcon(icon2)
        button.clicked.connect(lambda: self.approval_participant(row))
        return button

    def approval_participant(self, data):
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
            cursor.execute("UPDATE application SET applicationStatus=? WHERE employeeID=? AND trainingID=?",
                           ("Approved", row_items[1], training_id))
            connect.commit()
            cursor.execute("INSERT INTO notification (notification_status, notification_date, employeeID, trainingID, "
                           "is_read) VALUES ('Approved', ?, ?, ?, 0)", (date_time, self.id, training_id))
            connect.commit()
            self.refresh_table()
        elif approval == QtWidgets.QMessageBox.No:
            cursor.execute("UPDATE application SET applicationStatus=? WHERE employeeID=? AND trainingID=?",
                           ("Rejected", row_items[1], training_id))
            connect.commit()
            cursor.execute("INSERT INTO notification (notification_status, notification_date, employeeID, trainingID, "
                           "is_read) VALUES ('Rejected', ?, ?, ?, 0)", (date_time, self.id, training_id))
            connect.commit()
            self.refresh_table()
        else:
            pass

    def refresh_table(self):
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
                        self.application_table.setCellWidget(row, column + 1, self.add_button(data, row))
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

    def approve_training(self):
        approve_box = QtWidgets.QMessageBox()
        approve_box.setIcon(QtWidgets.QMessageBox.Question)
        approve_box.setWindowTitle("Approval")
        approve_box.setText("Do you want to approve this training?")
        approve_box.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel)
        approve = approve_box.exec_()
        date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        if approve == QtWidgets.QMessageBox.Yes:
            cursor.execute("SELECT count(applicationStatus) FROM application WHERE applicationStatus='Pending' AND "
                           "trainingID=?", (training_id,))
            pending = cursor.fetchone()[0]
            if pending > 0:
                approve_confirm_box = QtWidgets.QMessageBox()
                approve_confirm_box.setIcon(QtWidgets.QMessageBox.Warning)
                approve_confirm_box.setWindowTitle("Confirm Participants")
                approve_confirm_box.setText("Participants in pending status will be considered approved.\nAre you "
                                            "confirm to proceed?")
                approve_confirm_box.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
                approve_confirm = approve_confirm_box.exec_()
                if approve_confirm == QtWidgets.QMessageBox.Yes:
                    cursor.execute("SELECT employeeID FROM application WHERE applicationStatus='Pending' AND "
                                   "trainingID=?", (training_id,))
                    employees = cursor.fetchall()
                    cursor.execute("UPDATE application SET applicationStatus='Approved' WHERE applicationStatus="
                                   "'Pending' AND trainingID=?", (training_id,))
                    connect.commit()
                    for p in range(pending):
                        cursor.execute("INSERT INTO notification (notification_status, notification_date, employeeID, "
                                       "trainingID, is_read) VALUES ('Approved', ?, ?, ?, 0)", (date_time,
                                                                                                employees[p][0],
                                                                                                training_id,))
                        connect.commit()
                    QtWidgets.QMessageBox.information(None, "Infomation", "Application of the training cost was already"
                                                                          " sent to finance department.",
                                                      QtWidgets.QMessageBox.Ok)
                    cursor.execute("UPDATE training SET status='Approved' WHERE trainingID=?", (training_id,))
                    connect.commit()
                    self.refresh_table()
                    self.approve_training_button.deleteLater()
                    self.reject_training_button.deleteLater()
                    self.training_status_db.setText("Approved")
                    self.training_status_db.setStyleSheet("color: lightgreen; border: none;")
            else:
                QtWidgets.QMessageBox.information(None, "Infomation", "Application of the training cost was already "
                                                                      "sent to finance department.",
                                                  QtWidgets.QMessageBox.Ok)
                cursor.execute("UPDATE training SET status='Approved' WHERE trainingID=?", (training_id,))
                connect.commit()
                self.approve_training_button.deleteLater()
                self.reject_training_button.deleteLater()
                self.training_status_db.setText("Approved")
                self.training_status_db.setStyleSheet("color: lightgreen; border: none;")

    def reject_training(self):
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
            self.refresh_table()
            self.approve_training_button.deleteLater()
            self.reject_training_button.deleteLater()
            self.training_status_db.setText("Cancelled")
            self.training_status_db.setStyleSheet("color: #FE8886; border: none;")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Approval()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
