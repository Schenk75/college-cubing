import sys
import sqlite3
import datetime
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from UI.Ui_change_id import Ui_ChangeIDWindow
from UI.Ui_update_pb import Ui_UpdatePBWindow
from spider import *

caDB = 'sqlDB/caDB.db'

# 修改个人信息页面
class Change_ID_window(QMainWindow, Ui_ChangeIDWindow):
    def __init__(self, account_id, parent=None):
        super(Change_ID_window, self).__init__(parent)
        self.account_id = account_id
        self.setupUi(self)
        self.setFixedSize(self.width(), self.height())
        # 修改个人信息按钮
        self.pushButton.clicked.connect(self.btn_change)

    # 修改个人信息按钮事件
    def btn_change(self):
        conn = sqlite3.connect(caDB)
        cursor = conn.cursor()
        # 获取用户输入
        origin_password = self.lineEdit.text()
        new_password = self.lineEdit_2.text()
        new_wcaid = self.lineEdit_3.text().upper()

        cursor.execute(f"SELECT password, wcaid FROM userTable WHERE id='{self.account_id}'")
        (right_password, wcaid) = cursor.fetchall()[0]
        # 比对原密码
        if right_password != origin_password:
            reply = QMessageBox.warning(self, "警告", "原密码错误！")
            return

        # 若已有wcaid，则不允许更改
        if wcaid and new_wcaid:
            reply = QMessageBox.warning(self, "警告", "你已添加WCAID，禁止更改！")
            return

        # 修改密码
        if right_password == origin_password and new_password:
            cursor.execute(f"UPDATE userTable SET password='{new_password}' WHERE id='{self.account_id}'")
            conn.commit()

        # 新增wcaid
        if not wcaid and new_wcaid:
            cursor.execute(f"INSERT INTO wcaTable (wcaid) VALUES ('{new_wcaid}')")
            conn.commit()
            cursor.execute(f"UPDATE userTable SET wcaid='{new_wcaid}' WHERE id='{self.account_id}'")
            conn.commit()
            # 数据库中wca成绩更新
            wca_best = get_best(new_wcaid)
            # print(wca_best)
            columns = {'三阶':'E333', '二阶':'E222', '四阶':'E444', '五阶':'E555', '六阶':'E666', '七阶':'E777', '三盲':'E333bf', '最少步':'E333fm', '单手':'E333oh', '魔表':'Eclock', '五魔方':'Eminx', '金字塔':'Epyram', '斜转':'Eskewb', 'SQ1':'Esq1', '四盲':'E444bf', '五盲':'E555bf', '多盲':'E333mbf'}
            for i in columns:
                try: 
                    temp = ' '.join(wca_best[i])
                    cursor.execute(f"UPDATE wcaTable SET {columns[i]} = '{temp}' WHERE wcaid='{new_wcaid}'")
                    conn.commit()
                except: pass
            
        conn.close()
        reply = QMessageBox.information(self, "提示", '修改成功')
        self.close()


# 更新pb界面
class Update_PB_window(QMainWindow, Ui_UpdatePBWindow):
    def __init__(self, account_id, parent=None):
        super(Update_PB_window, self).__init__(parent)
        self.account_id = account_id
        self.setupUi(self)
        self.setFixedSize(self.width(), self.height())
        self.init_window()
        # 绑定更新按钮
        self.pushButton.clicked.connect(self.btn_update_pb)

    # 更新pb事件
    def btn_update_pb(self):
        # 获取表格内容并导入pbTable
        conn = sqlite3.connect(caDB)
        cursor = conn.cursor()
        events = ['E333', 'E222', 'E444', 'E555', 'E666', 'E777', 'E333bf', 'E333fm', 'E333oh', 'Eclock', 'Eminx', 'Epyram', 'Eskewb', 'Esq1', 'E444bf', 'E555bf', 'E333mbf']
        # try: print(self.tableWidget.item(0, 0).text())
        # except: print('fuck')
        for i in range(17):
            temp = ''
            for j in range(4):
                try:
                    if self.tableWidget.item(i, j).text():
                        temp += self.tableWidget.item(i, j).text() + ' '
                    else:
                        temp += '* '
                except: 
                    temp += '* '
            cursor.execute(f"UPDATE pbTable SET {events[i]}='{temp}' WHERE id='{self.account_id}'")
            conn.commit()
        conn.close()
        self.close()

    # 初始化更新pb界面
    def init_window(self):
        conn = sqlite3.connect(caDB)
        cursor = conn.cursor()
        # 生成pb表
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setRowCount(17)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        QTableWidget.resizeColumnsToContents(self.tableWidget)
        QTableWidget.resizeRowsToContents(self.tableWidget)
        self.tableWidget.setHorizontalHeaderLabels(['单次', '日期', '平均', '日期'])
        self.tableWidget.setVerticalHeaderLabels(['三阶', '二阶', '四阶', '五阶', '六阶', '七阶', '三盲', '最少步', '单手', '魔表', '五魔方', '金字塔', '斜转', 'SQ1', '四盲', '五盲', '多盲'])

        # 将已有信息填入
        cursor.execute(f"SELECT * FROM pbTable WHERE id='{self.account_id}'")
        temp = cursor.fetchall()[0]
        for i in range(1, 18):
            try:
                record = temp[i].split()
                for j in range(4):
                    try:
                        if record[j] != '*':
                            new = QTableWidgetItem(record[j])
                            self.tableWidget.setItem(i-1, j, new)
                    except: pass
            except: pass

        conn.close()
