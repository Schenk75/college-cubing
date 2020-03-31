# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\coding\python\ca_management\UI\update_pb.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_UpdatePBWindow(object):
    def setupUi(self, UpdatePBWindow):
        UpdatePBWindow.setObjectName("UpdatePBWindow")
        UpdatePBWindow.resize(800, 642)
        self.centralwidget = QtWidgets.QWidget(UpdatePBWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(350, 590, 101, 41))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(11)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(10, 10, 781, 571))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        UpdatePBWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(UpdatePBWindow)
        QtCore.QMetaObject.connectSlotsByName(UpdatePBWindow)

    def retranslateUi(self, UpdatePBWindow):
        _translate = QtCore.QCoreApplication.translate
        UpdatePBWindow.setWindowTitle(_translate("UpdatePBWindow", "更新PB"))
        self.pushButton.setText(_translate("UpdatePBWindow", "保存"))
