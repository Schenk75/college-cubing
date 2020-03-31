# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\coding\python\ca_management\UI\main_other.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


"""根据ui文件修改而来，添加 self.MainOtherWindow = MainOtherWindow 以便于修改窗体标题"""


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainOtherWindow(object):
    def setupUi(self, MainOtherWindow):
        self.MainOtherWindow = MainOtherWindow
        self.MainOtherWindow.setObjectName("MainOtherWindow")
        self.MainOtherWindow.resize(800, 574)
        self.centralwidget = QtWidgets.QWidget(self.MainOtherWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(10, 10, 781, 601))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.tableWidget = QtWidgets.QTableWidget(self.tab)
        self.tableWidget.setGeometry(QtCore.QRect(0, 50, 771, 471))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.tableWidget_2 = QtWidgets.QTableWidget(self.tab)
        self.tableWidget_2.setGeometry(QtCore.QRect(0, 10, 771, 31))
        self.tableWidget_2.setObjectName("tableWidget_2")
        self.tableWidget_2.setColumnCount(0)
        self.tableWidget_2.setRowCount(0)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tableWidget_3 = QtWidgets.QTableWidget(self.tab_2)
        self.tableWidget_3.setGeometry(QtCore.QRect(0, 10, 771, 521))
        self.tableWidget_3.setObjectName("tableWidget_3")
        self.tableWidget_3.setColumnCount(0)
        self.tableWidget_3.setRowCount(0)
        self.tabWidget.addTab(self.tab_2, "")
        self.MainOtherWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(self.MainOtherWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(self.MainOtherWindow)

    def retranslateUi(self, MainOtherWindow):
        _translate = QtCore.QCoreApplication.translate
        MainOtherWindow.setWindowTitle(_translate("MainOtherWindow", "主页"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainOtherWindow", "主页"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainOtherWindow", "练习PB"))
