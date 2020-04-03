# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\coding\python\college_cubing\college_cubing\UI\record_pk.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_RecordPKWindow(object):
    def setupUi(self, RecordPKWindow):
        RecordPKWindow.setObjectName("RecordPKWindow")
        RecordPKWindow.resize(480, 600)
        self.centralwidget = QtWidgets.QWidget(RecordPKWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(10, 40, 461, 551))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(250, 10, 21, 16))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(11)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(80, 10, 151, 22))
        self.comboBox.setObjectName("comboBox")
        self.comboBox_2 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_2.setGeometry(QtCore.QRect(290, 10, 151, 22))
        self.comboBox_2.setObjectName("comboBox_2")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(10, 10, 31, 28))
        self.pushButton.setObjectName("pushButton")
        RecordPKWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(RecordPKWindow)
        QtCore.QMetaObject.connectSlotsByName(RecordPKWindow)

    def retranslateUi(self, RecordPKWindow):
        _translate = QtCore.QCoreApplication.translate
        RecordPKWindow.setWindowTitle(_translate("RecordPKWindow", "校记录PK"))
        self.label.setText(_translate("RecordPKWindow", "VS"))
        self.pushButton.setText(_translate("RecordPKWindow", "PK"))
