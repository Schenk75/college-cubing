import sys
import sqlite3
import datetime
import csv
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from UI.Ui_college_ import Ui_CollegeWindow
from UI.Ui_college_list import Ui_CollegeListWindow
from UI.Ui_record_pk import Ui_RecordPKWindow
from main import *
from spider import *

caDB = 'sqlDB/caDB.db'

# 高校列表界面
class College_List_window(QMainWindow, Ui_CollegeListWindow):
    def __init__(self, parent=None):
        super(College_List_window, self).__init__(parent)
        self.setupUi(self)
        self.setFixedSize(self.width(), self.height())
        self.init_window()
        self.pushButton.clicked.connect(self.btn_record_pk)

    def init_window(self):
        conn = sqlite3.connect(caDB)
        cursor = conn.cursor()
        # 获取所有高校名
        cursor.execute("SELECT name FROM collegeTable ORDER BY name DESC")
        college_list = [item[0] for item in cursor.fetchall()]
        num_colleges = len(college_list)
        self.tableWidget.setRowCount(num_colleges)
        self.tableWidget.setColumnCount(1)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.verticalHeader().setVisible(False)  #隐藏垂直头标签
        self.tableWidget.horizontalHeader().setVisible(False)

        for i in range(len(college_list)):
            new_btn = QCommandLinkButton(college_list[i])
            new_btn.clicked.connect(lambda: self.btn_college(self.sender().text()))
            self.tableWidget.setCellWidget(i, 0, new_btn)
        conn.close()

    # 点击某一高校的事件
    def btn_college(self, college):
        self.college_window = College_window(college)
        self.college_window.show()

    # 校记录Pk事件
    def btn_record_pk(self):
        self.record_pk_window = Record_PK_window()
        self.record_pk_window.show()


# 单个高校界面
class College_window(QMainWindow, Ui_CollegeWindow):
    def __init__(self, college, parent=None):
        super(College_window, self).__init__(parent)
        self.college = college
        self.setupUi(self)
        self.CollegeWindow.setWindowTitle(self.college)  # 修改窗口标题为高校名
        self.pushButton.clicked.connect(self.btn_update_record)
        self.init_window()
        self.setFixedSize(self.width(), self.height())
        self.pushButton_2.clicked.connect(self.btn_export)

    # 初始化界面
    def init_window(self):
        conn = sqlite3.connect(caDB)
        cursor = conn.cursor()

        # 获取该高校的魔方社社员
        cursor.execute(f"SELECT name, id, entertime, leavetime, wcaid FROM userTable WHERE college='{self.college}'")
        info = cursor.fetchall()
        oncampus = []   # 在校生
        graduates = []  # 已毕业生
        name_id_dict = {}
        current_date = int(''.join(str(datetime.date.today()).split('-')))  # 当前日期
        for i in range(len(info)):
            (name, account_id, entertime, leavetime, _) = info[i]
            name_id_dict[name] = account_id
            entertime = int(''.join(entertime.split('-')))
            leavetime = int(''.join(leavetime.split('-')))
            if entertime < current_date < leavetime: oncampus.append(name)
            else: graduates.append(name)
        # print(oncampus, '\n', graduates)

        # 在校社员表
        self.tableWidget.setRowCount(len(oncampus))
        self.tableWidget.setColumnCount(1)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.verticalHeader().setVisible(False)  #隐藏垂直头标签
        self.tableWidget.setHorizontalHeaderLabels(['在校社员'])
        for i in range(len(oncampus)):
            new_btn = QCommandLinkButton(oncampus[i])
            new_btn.clicked.connect(lambda: self.btn_member(name_id_dict[self.sender().text()]))
            self.tableWidget.setCellWidget(i, 0, new_btn)

        # 毕业社员表
        self.tableWidget_3.setRowCount(len(graduates))
        self.tableWidget_3.setColumnCount(1)
        self.tableWidget_3.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget_3.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget_3.verticalHeader().setVisible(False)  #隐藏垂直头标签
        self.tableWidget_3.setHorizontalHeaderLabels(['已毕业社员'])
        for i in range(len(graduates)):
            new_btn = QCommandLinkButton(graduates[i])
            new_btn.clicked.connect(lambda: self.btn_member(name_id_dict[self.sender().text()]))
            self.tableWidget_3.setCellWidget(i, 0, new_btn)

        # 校记录表
        self.tableWidget_2.setRowCount(34)
        self.tableWidget_2.setColumnCount(5)
        self.tableWidget_2.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget_2.setHorizontalHeaderLabels(['单次', '平均', '姓名', '比赛', '日期'])
        self.tableWidget_2.setVerticalHeaderLabels(['三阶', '', '二阶', '', '四阶', '', '五阶', '', '六阶', '', '七阶', '', '三盲', '', '最少步', '', '单手', '', '魔表', '', '五魔方', '', '金字塔', '', '斜转', '', 'SQ1', '', '四盲', '', '五盲', '', '多盲', ''])
        self.tableWidget_2.setColumnWidth(0, 70)
        self.tableWidget_2.setColumnWidth(1, 70)
        self.tableWidget_2.setColumnWidth(2, 70)
        self.tableWidget_2.setColumnWidth(3, 225)
        self.tableWidget_2.setColumnWidth(4, 95)
        # 获取数据库中的校记录
        cursor.execute(f"SELECT * FROM collegeTable WHERE name='{self.college}'")
        info = list(cursor.fetchall()[0])[1:]
        for i, record in enumerate(info):
            try: 
                record = record.split('%*')
                record[3] = '-'.join([record[3][:4], record[3][4:6], record[3][6:]])
            except: continue
            # 单次记录
            if i % 2 == 0:
                new = QTableWidgetItem(record[0])
                self.tableWidget_2.setItem(i, 0, new)
                new = QTableWidgetItem(record[1])
                self.tableWidget_2.setItem(i, 2, new)
                new = QTableWidgetItem(record[2])
                self.tableWidget_2.setItem(i, 3, new)
                new = QTableWidgetItem(record[3])
                self.tableWidget_2.setItem(i, 4, new)
            # 平均记录
            else:
                new = QTableWidgetItem(record[0])
                self.tableWidget_2.setItem(i, 1, new)
                new = QTableWidgetItem(record[1])
                self.tableWidget_2.setItem(i, 2, new)
                new = QTableWidgetItem(record[2])
                self.tableWidget_2.setItem(i, 3, new)
                new = QTableWidgetItem(record[3])
                self.tableWidget_2.setItem(i, 4, new)

        conn.close()

    # 更新校记录事件
    def btn_update_record(self):
        conn = sqlite3.connect(caDB)
        cursor = conn.cursor()
        # 获取高校所有社员信息
        cursor.execute(f"SELECT name, wcaid, entertime, leavetime FROM userTable WHERE college='{self.college}'")
        info = cursor.fetchall()
        # print(info)

        # 获取高校当前校记录
        cursor.execute(f"SELECT * FROM collegeTable WHERE name='{self.college}'")
        current_record = list(cursor.fetchall()[0])[1:]
        events = ['333', '222', '444', '555', '666', '777', '333bf', '333fm', '333oh', 'clock', 'minx', 'pyram', 'skewb', 'sq1', '444bf', '555bf', '333mbf']
        # print(current_record)

        # 更新数据库中的信息
        for member in info:
            wcaid = member[1]
            entertime = member[2]
            leavetime = member[3]
            entertime = int(''.join(entertime.split('-')))
            leavetime = int(''.join(leavetime.split('-')))
            member_pb = get_best_oncampus(wcaid, entertime, leavetime)
            # print(member[0], member_pb)
            for i, event in enumerate(events):
                m_pb_single = member_pb[event]['single']
                m_pb_avg = member_pb[event]['avg']
                try: 
                    curr_single = current_record[2*i].split("%*")[0]
                    if not isinstance(curr_single, list): curr_single = format_time(curr_single)
                except: 
                    if i == 16: curr_single = [float('-inf'), float('inf')]
                    else: curr_single = float('inf')
                try: 
                    curr_avg = current_record[2*i+1].split("%*")[0]
                    if not isinstance(curr_avg, list): curr_avg = format_time(curr_avg)
                except: 
                    if i == 16: curr_avg = [float('-inf'), float('inf')] 
                    else: curr_avg = float('inf')
                # print(m_pb_single, m_pb_avg)
                # print(curr_single, curr_avg)
                if i == 16:   # 多盲计分
                    # print(m_pb_single, m_pb_avg)
                    # print(curr_single, curr_avg)
                    if m_pb_single[0][0] > curr_single[0] or (m_pb_single[0][0] == curr_single[0] and m_pb_single[0][1] < curr_single[1]):
                        current_record[2*i] = '%*'.join([m_pb_single[1], member[0], m_pb_single[2], m_pb_single[3]])
                    if m_pb_avg[0][0] > curr_avg[0] or (m_pb_avg[0][0] == curr_avg[0] and m_pb_avg[0][1] < curr_avg[1]):
                        current_record[2*i] = '%*'.join([m_pb_avg[1], member[0], m_pb_avg[2], m_pb_avg[3]]) 
                else:
                    if m_pb_single[0] < curr_single:
                        current_record[2*i] = '%*'.join([m_pb_single[1], member[0], m_pb_single[2], m_pb_single[3]])
                    if m_pb_avg[0] < curr_avg:
                        current_record[2*i+1] = '%*'.join([m_pb_avg[1], member[0], m_pb_avg[2], m_pb_avg[3]])
                # print(current_record, '\n')
            # print(current_record, '\n')
        table_title = ['s333', 'a333', 's222', 'a222', 's444', 'a444', 's555', 'a555', 's666', 'a666', 's777', 'a777', 's333bf', 'a333bf', 's333fm', 'a333fm', 's333oh', 'a333oh', 'sclock', 'aclock', 'sminx', 'aminx', 'spyram', 'apyram', 'sskewb', 'askewb', 'ssq1', 'asq1', 's444bf', 'a444bf', 's555bf', 'a555bf', 's333mbf', 'a333mbf']
        # 更新数据库中的校记录
        for i in range(len(table_title)):
            cursor.execute(f"UPDATE collegeTable SET {table_title[i]}='{current_record[i]}' WHERE name='{self.college}'")
            conn.commit()
        reply = QMessageBox.information(self, "提示", '更新成功')
        conn.close()
        self.init_window()  # 刷新界面显示

    # 跳转别人的主页事件
    def btn_member(self, account_id):
        # print(account_id)
        self.main_other_window = Main_Other_window(account_id)
        self.main_other_window.show()

    # 导出校记录事件
    def btn_export(self):
        conn = sqlite3.connect(caDB)
        cursor = conn.cursor()

        # 获取校记录
        cursor.execute(f"SELECT * FROM collegeTable WHERE name='{self.college}'")
        record = list(cursor.fetchall()[0])[1:]

        # 创建文件
        file_name = f'{self.college}校记录 {str(datetime.date.today())}.csv'
        f = open(file_name, 'w', encoding='gbk', newline='')
        csv_writer = csv.writer(f)
        event_list = ['三阶', '', '二阶', '', '四阶', '', '五阶', '', '六阶', '', '七阶', '', '三盲', '', '最少步', '', '单手', '', '魔表', '', '五魔方', '', '金字塔', '', '斜转', '', 'SQ1', '', '四盲', '', '五盲', '', '多盲', '']
        csv_writer.writerow(['', '单次', '平均', '姓名', '比赛', '日期'])  # 列名
        for i, event in enumerate(event_list):
            try: 
                record[i] = record[i].split('%*')
                record[i][3] = '-'.join([record[i][3][:4], record[i][3][4:6], record[i][3][6:]])
            except: record[i] = ['', '', '', '']
            if i % 2 == 0:  # 单次
                content = [event, record[i][0], '', record[i][1], record[i][2], record[i][3]]
            else:  # 平均
                content = [event, '', record[i][0], record[i][1], record[i][2], record[i][3]]
            csv_writer.writerow(content)

        f.close()
        reply = QMessageBox.information(self, "提示", '导出成功')
        conn.close()


# 校记录PK界面
class Record_PK_window(QMainWindow, Ui_RecordPKWindow):
    def __init__(self, parent=None):
        super(Record_PK_window, self).__init__(parent)
        self.setupUi(self)
        self.init_window()
        self.pushButton.clicked.connect(self.btn_pk)
        self.setFixedSize(self.width(), self.height())

    # 初始化界面
    def init_window(self):
        conn = sqlite3.connect(caDB)
        cursor = conn.cursor()

        # 添加两个高校选择框
        cursor.execute("SELECT name FROM collegeTable ORDER BY name DESC")
        college_list = [item[0] for item in cursor.fetchall()]
        self.comboBox.addItem('...')
        self.comboBox.addItems(college_list)
        self.comboBox_2.addItem('...')
        self.comboBox_2.addItems(college_list)
        
        # 初始化表格
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(34)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.horizontalHeader().setVisible(False)
        self.tableWidget.setVerticalHeaderLabels(['三阶', '', '二阶', '', '四阶', '', '五阶', '', '六阶', '', '七阶', '', '三盲', '', '最少步', '', '单手', '', '魔表', '', '五魔方', '', '金字塔', '', '斜转', '', 'SQ1', '', '四盲', '', '五盲', '', '多盲', ''])

        conn.close()

    # PK按钮事件
    def btn_pk(self):
        conn = sqlite3.connect(caDB)
        cursor = conn.cursor()
        
        # 获取输入的两所高校
        college1 = self.comboBox.currentText()
        college2 = self.comboBox_2.currentText()

        # 获取两所高校的校记录
        try:
            cursor.execute(f"SELECT * FROM collegeTable WHERE name='{college1}'")
            record1 = list(cursor.fetchall()[0])[1:]
            cursor.execute(f"SELECT * FROM collegeTable WHERE name='{college2}'")
            record2 = list(cursor.fetchall()[0])[1:]
        except:
            reply = QMessageBox.warning(self, "警告", "请选择有效高校！")
            return

        # 将成绩填入表中，并高亮pk获胜的一项
        for i in range(len(record1)):
            # 显示的时间(str)
            try: time_show1 = record1[i].split('%*')[0]
            except: time_show1 = ''
            try: time_show2 = record2[i].split('%*')[0]
            except: time_show2 = ''
            # print(time_show1, time_show2)

            # 比较的时间(float)
            if i > 31:  # 多盲计分
                time_show1 = time_show1.split()
                time_show2 = time_show2.split()
                # print(time_show1, time_show2)
                # 统计分数和时间
                try:
                    score1 = 2 * int(time_show1[0].split('/')[0]) - int(time_show1[0].split('/')[1])
                    time1 = format_time(time_show1[1])
                except:
                    score1, time1 = float('-inf'), float('inf')
                try:
                    score2 = 2 * int(time_show2[0].split('/')[0]) - int(time_show2[0].split('/')[1])
                    time2 = format_time(time_show2[1])
                except:
                    score2, time2 = float('-inf'), float('inf')
                # print(score1, time1)
                # print(score2, time2)
                # 加数据
                if score1 > 0:
                    time_show1 = QTableWidgetItem(' '.join(time_show1))
                    self.tableWidget.setItem(i, 0, time_show1)
                if score2 > 0:
                    time_show2 = QTableWidgetItem(' '.join(time_show2))
                    self.tableWidget.setItem(i, 1, time_show2) 
                # 加高亮
                try:
                    if score1 > score2 or (score1 == score2 and time1 < time2): 
                        self.tableWidget.item(i, 0).setBackground(QBrush(QColor(197,224,180)))
                    if score1 < score2 or (score1 == score2 and time1 > time2): 
                        self.tableWidget.item(i, 1).setBackground(QBrush(QColor(197,224,180)))
                    if score1 == score2 and time1 == time2:
                        self.tableWidget.item(i, 0).setBackground(QBrush(QColor(197,224,180)))
                        self.tableWidget.item(i, 1).setBackground(QBrush(QColor(197,224,180)))
                except: pass
            else:
                # 统计时间
                try: time1 = format_time(time_show1)
                except: time1 = float('inf')
                try: time2 = format_time(time_show2)
                except: time2 = float('inf')
                # print(time1, time2)
                # 加数据
                if time1 < float('inf'):
                    time_show1 = QTableWidgetItem(time_show1)
                    self.tableWidget.setItem(i, 0, time_show1)
                if time2 < float('inf'):
                    time_show2 = QTableWidgetItem(time_show2)
                    self.tableWidget.setItem(i, 1, time_show2) 
                # 加高亮 
                try:
                    if time1 < time2: self.tableWidget.item(i ,0).setBackground(QBrush(QColor(197,224,180)))
                    elif time1 > time2: self.tableWidget.item(i ,1).setBackground(QBrush(QColor(197,224,180)))
                    elif time1 == time2:
                        self.tableWidget.item(i ,0).setBackground(QBrush(QColor(197,224,180)))
                        self.tableWidget.item(i ,1).setBackground(QBrush(QColor(197,224,180)))
                except: pass
                # print(i, time1, time2)
            # print(i, time1, time2)
            # break
        conn.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # college_list_window = College_List_window()
    # college_list_window.show()
    college_window = College_window('上海交通大学')
    college_window.show()
    # record_pk_window = Record_PK_window()
    # record_pk_window.show()

    sys.exit(app.exec_())