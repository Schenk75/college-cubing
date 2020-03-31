import sys
import sqlite3
import datetime
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from UI.Ui_main import Ui_MainWindow
from UI.Ui_main_other_ import Ui_MainOtherWindow
from UI.Ui_login import Ui_LoginWindow
from UI.Ui_register import Ui_RegisterWindow
from spider import *
from update import *
from college import *

caDB = 'sqlDB/caDB.db'

# 本人视角主页面
class Main_window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(Main_window, self).__init__(parent)
        self.setupUi(self)
        self.setFixedSize(self.width(), self.height())
        # 绑定刷新按钮
        self.pushButton_3.clicked.connect(self.btn_update)
        # 绑定更新pb按钮
        self.pushButton_2.clicked.connect(self.btn_update_pb)
        # 绑定修改个人信息按钮
        self.pushButton.clicked.connect(self.btn_change_id)
        # 绑定我的高校按钮
        self.pushButton_5.clicked.connect(self.btn_college)
        # 绑定高校列表按钮
        self.pushButton_4.clicked.connect(self.btn_college_list)

    # 刷新官方成绩和pb界面事件(重新爬虫)
    def btn_update(self):
        self.update_table(self.account_id)
        reply = QMessageBox.information(self, "提示", '刷新成功')
    
    # 刷新官方成绩和pb界面事件(不重新爬虫)
    def btn_update_not(self):
        self.update_table(self.account_id, False)
        # print('done')

    # 更新PB事件
    def btn_update_pb(self):
        self.update_pb_window = Update_PB_window(self.account_id)
        self.update_pb_window.show()
        self.update_pb_window.pushButton.clicked.connect(self.btn_update_not)
    
    # 修改个人信息事件
    def btn_change_id(self):
        self.change_id_window = Change_ID_window(self.account_id)
        self.change_id_window.show()
        self.change_id_window.pushButton.clicked.connect(self.btn_update_not)

    # 单个高校显示事件
    def btn_college(self):
        conn = sqlite3.connect(caDB)
        cursor = conn.cursor()
        cursor.execute(f"SELECT college FROM userTable WHERE id='{self.account_id}'")
        college = cursor.fetchall()[0][0]
        self.college_window = College_window(college)
        self.college_window.show()
        conn.close()

    # 高校列表显示事件
    def btn_college_list(self):
        self.college_list_window = College_List_window()
        self.college_list_window.show()

    # 初始化主页以及pb页的表格的格式
    def init_table(self, account_id, update=False):
        conn = sqlite3.connect(caDB)
        cursor = conn.cursor()
        self.account_id = account_id
        cursor.execute(f"SELECT wcaid FROM userTable WHERE id='{self.account_id}'")
        try: self.wcaid = cursor.fetchall()[0][0]
        except: self.wcaid = ''
        if update:
            self.update_wca(self.wcaid)
        
        # 编辑基本信息表
        self.tableWidget_2.setColumnCount(4)
        # 设置水平和垂直方向表格为自适应的伸缩模式
        self.tableWidget_2.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget_2.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # 将表格变为禁止编辑
        self.tableWidget_2.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # 将行与列的高度设置为所显示的内容的宽度高度匹配
        QTableWidget.resizeColumnsToContents(self.tableWidget_2)
        QTableWidget.resizeRowsToContents(self.tableWidget_2)
        # 个人基本信息提取
        cursor.execute(f"SELECT name, college, entertime, leavetime FROM userTable WHERE id='{account_id}'")
        (name, college, entertime, leavetime) = cursor.fetchall()[0]
        state = ['在读', '毕业']
        current_date = int(''.join(str(datetime.date.today()).split('-')))
        entertime = int(''.join(entertime.split('-')))
        leavetime = int(''.join(leavetime.split('-')))
        state = state[0] if entertime < current_date < leavetime else state[1]
        # 设置水平方向表格头标签
        self.tableWidget_2.setHorizontalHeaderLabels([f'姓名:{name}', f'高校:{college}', f'状态:{state}', f'WCAID:{self.wcaid}'])

        # 生成wca成绩表
        self.tableWidget.setColumnCount(8)
        self.tableWidget.setRowCount(17)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        QTableWidget.resizeColumnsToContents(self.tableWidget)
        QTableWidget.resizeRowsToContents(self.tableWidget)
        self.tableWidget.setHorizontalHeaderLabels(['单次', '地区排名', '洲际排名', '世界排名', '平均', '地区排名', '洲际排名', '世界排名'])
        self.tableWidget.setVerticalHeaderLabels(['三阶', '二阶', '四阶', '五阶', '六阶', '七阶', '三盲', '最少步', '单手', '魔表', '五魔方', '金字塔', '斜转', 'SQ1', '四盲', '五盲', '多盲'])
        # 添加数据
        cursor.execute(f"SELECT * FROM wcaTable WHERE wcaid='{self.wcaid}'")
        temp = cursor.fetchall()[0]
        for i in range(1, 18):
            try:
                record = temp[i].split()
                for j in range(4):
                    new = QTableWidgetItem(record[j])
                    self.tableWidget.setItem(i-1, j, new)
                try:
                    for j in range(4):
                        new = QTableWidgetItem(record[4+j])
                        self.tableWidget.setItem(i-1, 4+j, new)
                except: pass
            except: pass

        # 生成pb表
        self.tableWidget_3.setColumnCount(4)
        self.tableWidget_3.setRowCount(17)
        self.tableWidget_3.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget_3.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget_3.setEditTriggers(QAbstractItemView.NoEditTriggers)
        QTableWidget.resizeColumnsToContents(self.tableWidget_3)
        QTableWidget.resizeRowsToContents(self.tableWidget_3)
        self.tableWidget_3.setHorizontalHeaderLabels(['单次', '日期', '平均', '日期'])
        self.tableWidget_3.setVerticalHeaderLabels(['三阶', '二阶', '四阶', '五阶', '六阶', '七阶', '三盲', '最少步', '单手', '魔表', '五魔方', '金字塔', '斜转', 'SQ1', '四盲', '五盲', '多盲'])
        # 添加数据
        cursor.execute(f"SELECT * FROM pbTable WHERE id='{account_id}'")
        temp = cursor.fetchall()[0]
        for i in range(1, 18):
            try:
                record = temp[i].split()
                for j in range(4):
                    try:
                        if record[j] != '*':
                            new = QTableWidgetItem(record[j])
                            self.tableWidget_3.setItem(i-1, j, new)
                        else:
                            new = QTableWidgetItem('')
                            self.tableWidget_3.setItem(i-1, j, new)
                    except: pass
            except: pass
        conn.close()

    # 刷新主页以及pb页的表格
    def update_table(self, account_id, update=True):
        conn = sqlite3.connect(caDB)
        cursor = conn.cursor()
        cursor.execute(f"SELECT wcaid FROM userTable WHERE id='{account_id}'")
        try: self.wcaid = cursor.fetchall()[0][0]
        except: self.wcaid = ''
        if update:
            self.update_wca(self.wcaid)
        
        cursor.execute(f"SELECT name, college, entertime, leavetime FROM userTable WHERE id='{account_id}'")
        (name, college, entertime, leavetime) = cursor.fetchall()[0]
        state = ['在读', '毕业']
        current_date = int(''.join(str(datetime.date.today()).split('-')))
        entertime = int(''.join(entertime.split('-')))
        leavetime = int(''.join(leavetime.split('-')))
        state = state[0] if entertime < current_date < leavetime else state[1]

        # 设置水平方向表格头标签
        self.tableWidget_2.setHorizontalHeaderLabels([f'姓名:{name}', f'高校:{college}', f'状态:{state}', f'WCAID:{self.wcaid}'])

        # 生成wca成绩表
        cursor.execute(f"SELECT * FROM wcaTable WHERE wcaid='{self.wcaid}'")
        temp = cursor.fetchall()[0]
        for i in range(1, 18):
            try:
                record = temp[i].split()
                for j in range(4):
                    new = QTableWidgetItem(record[j])
                    
                    self.tableWidget.setItem(i-1, j, new)
                try:
                    for j in range(4):
                        new = QTableWidgetItem(record[4+j])
                        self.tableWidget.setItem(i-1, 4+j, new)
                except: pass
            except: pass

        # 生成pb表
        cursor.execute(f"SELECT * FROM pbTable WHERE id='{account_id}'")
        temp = cursor.fetchall()[0]
        # print(temp[1])
        for i in range(1, 18):
            try:
                record = temp[i].split()
                # print(i, record)
                for j in range(4):
                    try:
                        if record[j] != '*':
                            new = QTableWidgetItem(record[j])
                            self.tableWidget_3.setItem(i-1, j, new)
                        else:
                            new = QTableWidgetItem('')
                            self.tableWidget_3.setItem(i-1, j, new)
                    except: pass
            except: pass
        conn.close()

    # 更新wca成绩
    def update_wca(self, wcaid):
        # print(wcaid)
        conn = sqlite3.connect(caDB)
        cursor = conn.cursor()

        # 如果数据库的wca成绩表里没有这个人的wcaid，则插入
        cursor.execute(f"SELECT wcaid FROM wcaTable WHERE wcaid='{wcaid}'")
        res = cursor.fetchall()
        if res == []:
            cursor.execute(f"INSERT INTO wcaTable (wcaid) VALUES ('{wcaid}')")
            conn.commit()
        
        # 数据库中wca成绩更新
        wca_best = get_best(wcaid)
        # print(wca_best)
        columns = {'三阶':'E333', '二阶':'E222', '四阶':'E444', '五阶':'E555', '六阶':'E666', '七阶':'E777', '三盲':'E333bf', '最少步':'E333fm', '单手':'E333oh', '魔表':'Eclock', '五魔方':'Eminx', '金字塔':'Epyram', '斜转':'Eskewb', 'SQ1':'Esq1', '四盲':'E444bf', '五盲':'E555bf', '多盲':'E333mbf'}
        for i in columns:
            try: 
                temp = ' '.join(wca_best[i])
                cursor.execute(f"UPDATE wcaTable SET {columns[i]} = '{temp}' WHERE wcaid='{wcaid}'")
                conn.commit()
            except: pass
        conn.close()


# 访客视角主页面
class Main_Other_window(QMainWindow, Ui_MainOtherWindow):
    def __init__(self, account_id, parent=None):
        super(Main_Other_window, self).__init__(parent)
        self.account_id = account_id
        self.setupUi(self)
        self.init_window()
        self.setFixedSize(self.width(), self.height())

    # 初始化界面
    def init_window(self):
        conn = sqlite3.connect(caDB)
        cursor = conn.cursor()

        cursor.execute(f"SELECT * FROM userTable WHERE id='{self.account_id}'")
        (account_id, _, name, college, entertime, leavetime, wcaid) = cursor.fetchall()[0]
        self.MainOtherWindow.setWindowTitle(name)  # 修改窗口标题为高校名

        # 编辑基本信息表
        self.tableWidget_2.setColumnCount(4)
        # 设置水平和垂直方向表格为自适应的伸缩模式
        self.tableWidget_2.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget_2.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # 将表格变为禁止编辑
        self.tableWidget_2.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # 将行与列的高度设置为所显示的内容的宽度高度匹配
        QTableWidget.resizeColumnsToContents(self.tableWidget_2)
        QTableWidget.resizeRowsToContents(self.tableWidget_2)
        # 个人基本信息提取
        state = ['在读', '毕业']
        current_date = int(''.join(str(datetime.date.today()).split('-')))
        entertime = int(''.join(entertime.split('-')))
        leavetime = int(''.join(leavetime.split('-')))
        state = state[0] if entertime < current_date < leavetime else state[1]
        # 设置水平方向表格头标签
        self.tableWidget_2.setHorizontalHeaderLabels([f'姓名:{name}', f'高校:{college}', f'状态:{state}', f'WCAID:{wcaid}'])

        # 生成wca成绩表
        self.tableWidget.setColumnCount(8)
        self.tableWidget.setRowCount(17)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        QTableWidget.resizeColumnsToContents(self.tableWidget)
        QTableWidget.resizeRowsToContents(self.tableWidget)
        self.tableWidget.setHorizontalHeaderLabels(['单次', '地区排名', '洲际排名', '世界排名', '平均', '地区排名', '洲际排名', '世界排名'])
        self.tableWidget.setVerticalHeaderLabels(['三阶', '二阶', '四阶', '五阶', '六阶', '七阶', '三盲', '最少步', '单手', '魔表', '五魔方', '金字塔', '斜转', 'SQ1', '四盲', '五盲', '多盲'])
        # 添加数据
        cursor.execute(f"SELECT * FROM wcaTable WHERE wcaid='{wcaid}'")
        temp = cursor.fetchall()[0]
        for i in range(1, 18):
            try:
                record = temp[i].split()
                for j in range(4):
                    new = QTableWidgetItem(record[j])
                    self.tableWidget.setItem(i-1, j, new)
                try:
                    for j in range(4):
                        new = QTableWidgetItem(record[4+j])
                        self.tableWidget.setItem(i-1, 4+j, new)
                except: pass
            except: pass

        # 生成pb表
        self.tableWidget_3.setColumnCount(4)
        self.tableWidget_3.setRowCount(17)
        self.tableWidget_3.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget_3.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget_3.setEditTriggers(QAbstractItemView.NoEditTriggers)
        QTableWidget.resizeColumnsToContents(self.tableWidget_3)
        QTableWidget.resizeRowsToContents(self.tableWidget_3)
        self.tableWidget_3.setHorizontalHeaderLabels(['单次', '日期', '平均', '日期'])
        self.tableWidget_3.setVerticalHeaderLabels(['三阶', '二阶', '四阶', '五阶', '六阶', '七阶', '三盲', '最少步', '单手', '魔表', '五魔方', '金字塔', '斜转', 'SQ1', '四盲', '五盲', '多盲'])
        # 添加数据
        cursor.execute(f"SELECT * FROM pbTable WHERE id='{account_id}'")
        temp = cursor.fetchall()[0]
        for i in range(1, 18):
            try:
                record = temp[i].split()
                for j in range(4):
                    try:
                        if record[j] != '*':
                            new = QTableWidgetItem(record[j])
                            self.tableWidget_3.setItem(i-1, j, new)
                    except: pass
            except: pass

        conn.close()


# 注册界面
class Register_window(QMainWindow, Ui_RegisterWindow):
    def __init__(self,parent = None):
        super(Register_window, self).__init__(parent)
        self.setupUi(self)
        self.add_college()
        self.setFixedSize(self.width(), self.height())
        # 绑定注册按钮事件
        self.pushButton.clicked.connect(self.btn_register)
        # self.comboBox.addItem('dd')

    # 添加高校选项
    def add_college(self):
        conn = sqlite3.connect(caDB)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM collegeTable ORDER BY name DESC")
        college_list = [item[0] for item in cursor.fetchall()]
        self.comboBox.addItem('...')
        self.comboBox.addItems(college_list)
        conn.close()

    # 注册账户，若成功则跳转主界面
    def btn_register(self):
        # 获取输入的信息
        account_id = self.lineEdit.text()
        password = self.lineEdit_5.text()
        name = self.lineEdit_4.text()
        college = self.comboBox.currentText()
        entertime = self.dateEdit.date().toString(Qt.ISODate)
        leavetime = self.dateEdit_2.date().toString(Qt.ISODate)
        wcaid = self.lineEdit_2.text().upper()
        input_data = (account_id, password, name, college, entertime, leavetime, wcaid)
        # print(input_data)

        # 防止不完整信息
        if account_id == '' or password == '' or name == '' or college == '...':
            reply = QMessageBox.warning(self, "警告", "信息不能为空，请重新输入！")
            return
        
        # 连接数据库
        conn = sqlite3.connect(caDB)
        cursor = conn.cursor()

        # 不能有重复的用户名
        cursor.execute(f"SELECT name FROM userTable WHERE id LIKE '{account_id}'")
        res = cursor.fetchall()
        if res != []:
            reply = QMessageBox.warning(self, "警告", "已有相同用户名，请重新输入！")
            return

        # 成功注册，录入信息
        # 录入userTable用户基本数据表
        cursor.execute("INSERT INTO userTable VALUES (?,?,?,?,?,?,?)", input_data)
        conn.commit()
        # 录入pbTable练习pb表
        cursor.execute(f"SELECT id FROM pbTable WHERE id='{account_id}'")
        res = cursor.fetchall()
        if res == []: 
            cursor.execute(f"INSERT INTO pbTable (id) VALUES ('{account_id}')")
            conn.commit()
        conn.close()

        # 更新主界面的个人信息
        self.main_window = Main_window()
        self.main_window.init_table(account_id, True)
        self.main_window.show()
        self.close()


# 登陆界面
class Login_window(QMainWindow, Ui_LoginWindow):
    def __init__(self, parent = None):
        super(Login_window, self).__init__(parent)
        self.setupUi(self)
        self.setFixedSize(self.width(), self.height())
        # 绑定注册按钮事件
        self.pushButton_2.clicked.connect(self.btn_register)
        self.pushButton.clicked.connect(self.btn_login)

    # 从登陆界面跳转到注册界面
    def btn_register(self):
        self.register_window = Register_window()
        self.register_window.show()
        self.close()

    # 登陆操作
    def btn_login(self):
        # 获取输入信息
        account_id = self.lineEdit.text()
        password = self.lineEdit_2.text()

        # 不能漏填
        if account_id == '' or password == '':
            reply = QMessageBox.warning(self, "警告", "信息不能为空，请重新输入！")
            return

        # 连接数据库
        conn = sqlite3.connect(caDB)
        cursor = conn.cursor()

        cursor.execute("SELECT password FROM userTable WHERE id LIKE ? OR wcaid LIKE ?", (account_id, account_id))
        correct_password = cursor.fetchall()
        if correct_password == []:
            reply = QMessageBox.warning(self, "警告", "不存在该账户，请注册！")
            return
        correct_password = correct_password[0][0]
        if correct_password != password:
            reply = QMessageBox.warning(self, "警告", "密码错误，请重试！")
            return

        # 更新主界面的个人信息
        cursor.execute("SELECT id FROM userTable WHERE id LIKE ? OR wcaid LIKE ?", (account_id, account_id))
        temp = cursor.fetchall()
        conn.close()

        self.main_window = Main_window()
        self.main_window.init_table(temp[0][0])
        self.main_window.show()
        self.close()
            

if __name__ =='__main__':
    app = QApplication(sys.argv)
    # main_window = Main_window()
    # main_window.init_table('sck')
    # main_window.show()

    login_window = Login_window()
    login_window.show()

    # main_other_window = Main_Other_window('sck')
    # main_other_window.show()
    sys.exit(app.exec_())