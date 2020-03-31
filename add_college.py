import sqlite3

caDB = 'sqlDB/caDB.db'

# 初始化数据库
def init_db():
    conn = sqlite3.connect(caDB)
    cursor = conn.cursor()
    # cursor.execute('''CREATE TABLE userTable (
    #                     id text primary key,
    #                     name text not null,
    #                     password text not null,
    #                     college text not null,
    #                     entertime text not null,
    #                     leavetime text not null,
    #                     wcaid text
    #                 );''')
    cursor.execute('''CREATE TABLE collegeTable (   
                        name text primary key,
                        s333 text, a333 text,
                        s222 text, a222 text,
                        s444 text, a444 text,
                        s555 text, a555 text,
                        s666 text, a666 text,
                        s777 text, a777 text,
                        s333bf text, a333bf text,
                        s333fm text, a333fm text,
                        s333oh text, a333oh text,
                        sclock text, aclock text,
                        sminx text, aminx text,
                        spyram text, apyram text,
                        sskewb text, askewb text,
                        ssq1 text, asq1 text,
                        s444bf text, a444bf text,
                        s555bf text, a555bf text,
                        s333mbf text, a333mbf text
                    );''')
    # cursor.execute('''CREATE TABLE wcaTable (
    #                     wcaid text primary key,
    #                     E333 text,
    #                     E222 text,
    #                     E444 text,
    #                     E555 text,
    #                     E666 text,
    #                     E777 text,
    #                     E333oh text,
    #                     E333fm text,
    #                     E333bf text,
    #                     Esq1 text,
    #                     Eskewb text,
    #                     Epyram text,
    #                     Eminx text,
    #                     Eclock text,
    #                     E444bf text,
    #                     E555bf text,
    #                     E333mbf text
    #                 );''')
    # cursor.execute('''CREATE TABLE pbTable (
    #                     id text primary key,
    #                     E333 text,
    #                     E222 text,
    #                     E444 text,
    #                     E555 text,
    #                     E666 text,
    #                     E777 text,
    #                     E333oh text,
    #                     E333fm text,
    #                     E333bf text,
    #                     Esq1 text,
    #                     Eskewb text,
    #                     Epyram text,
    #                     Eminx text,
    #                     Eclock text,
    #                     E444bf text,
    #                     E555bf text,
    #                     E333mbf text
    #                 );''')
    conn.close()

# 手动添加高校
def add_college(college):
    import sqlite3
    caDB = 'sqlDB/caDB.db'
    conn = sqlite3.connect(caDB)
    cursor = conn.cursor()

    cursor.execute(f"SELECT name FROM collegeTable WHERE name='{college}'")
    temp = cursor.fetchall()
    if temp == []:
        cursor.execute(f"INSERT INTO collegeTable (name) VALUES ('{college}')")
        conn.commit()
        print('添加成功')
    else: print('添加失败，该高校已存在')

    conn.close()

if __name__ =='__main__':
    # init_db()

    # college_list = ['上海交通大学', '上海大学', '上海工程技术大学', '上海师范大学', '东南大学', '中山大学', '北京大学', '华东师范大学', '华东理工大学', '南京大学', '南开大学', '哈尔滨工业大学', '复旦大学', '武汉大学', '浙江大学', '清华大学', '西安交通大学']
    # for college in college_list:
    #     add_college(college)

    college = input('输入高校名：(退出按q)')
    while college not in 'qQ':
        add_college(college)
        college = input('输入高校名：(退出按q)')

    # conn = sqlite3.connect(caDB)
    # cursor = conn.cursor()
    # cursor.execute("SELECT name FROM collegeTable")
    # college_list = [item[0] for item in cursor.fetchall()]
    # print(college_list)
    # conn.close()