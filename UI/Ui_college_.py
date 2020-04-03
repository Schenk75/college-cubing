# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\coding\python\ca_management\UI\college.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


"""根据ui文件修改而来，添加 self.CollegeWindow = CollegeWindow 以便于修改窗体标题"""

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_CollegeWindow(object):
    def setupUi(self, CollegeWindow):
        self.CollegeWindow = CollegeWindow
        self.CollegeWindow.setObjectName("CollegeWindow")
        self.CollegeWindow.resize(800, 599)
        self.centralwidget = QtWidgets.QWidget(self.CollegeWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(10, 10, 161, 281))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.tableWidget_2 = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget_2.setGeometry(QtCore.QRect(180, 40, 611, 541))
        self.tableWidget_2.setObjectName("tableWidget_2")
        self.tableWidget_2.setColumnCount(0)
        self.tableWidget_2.setRowCount(0)
        self.tableWidget_3 = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget_3.setGeometry(QtCore.QRect(10, 300, 161, 281))
        self.tableWidget_3.setObjectName("tableWidget_3")
        self.tableWidget_3.setColumnCount(0)
        self.tableWidget_3.setRowCount(0)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(430, 10, 61, 21))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(740, 10, 51, 31))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(680, 10, 51, 31))
        self.pushButton_2.setObjectName("pushButton_2")
        self.CollegeWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(self.CollegeWindow)
        QtCore.QMetaObject.connectSlotsByName(self.CollegeWindow)

    def retranslateUi(self, CollegeWindow):
        _translate = QtCore.QCoreApplication.translate
        CollegeWindow.setWindowTitle(_translate("CollegeWindow", "高校"))
        self.label.setText(_translate("CollegeWindow", "校记录"))
        self.pushButton.setText(_translate("CollegeWindow", "更新"))
        self.pushButton_2.setText(_translate("CollegeWindow", "导出"))
