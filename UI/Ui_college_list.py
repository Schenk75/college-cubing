# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\coding\python\ca_management\UI\college_list.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_CollegeListWindow(object):
    def setupUi(self, CollegeListWindow):
        CollegeListWindow.setObjectName("CollegeListWindow")
        CollegeListWindow.resize(339, 591)
        self.centralwidget = QtWidgets.QWidget(CollegeListWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(15, 10, 311, 571))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        CollegeListWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(CollegeListWindow)
        QtCore.QMetaObject.connectSlotsByName(CollegeListWindow)

    def retranslateUi(self, CollegeListWindow):
        _translate = QtCore.QCoreApplication.translate
        CollegeListWindow.setWindowTitle(_translate("CollegeListWindow", "高校列表"))
