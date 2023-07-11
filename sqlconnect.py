import datetime
import pymysql
import traceback
from time import sleep

class PyMySQL(object):
    create_table = """
        CREATE TABLE login_information (   
            id INT not null PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(255) NOT NULL,
            pwd VARCHAR(255) NOT NULL
        ) DEFAULT CHARSET = utf8
    """
    select = 'SELECT * FROM login_information'
    update = 'UPDATE login_information SET '
    delete = 'DELETE FROM login_information WHERE '
    insert = 'INSERT INTO login_information(name, pwd) '

    create_table2 = """
        CREATE TABLE question_information (
            id INT not null PRIMARY KEY AUTO_INCREMENT,
            question_str VARCHAR(100) NOT NULL,
            time DATE NOT NULL 
        ) DEFAULT CHARSET = utf8
    """
    create_table3 = """
        CREATE TABLE question_data (
             id INT NOT null PRIMARY KEY AUTO_INCREMENT,
             question_str VARCHAR(100) NOT NULL,
             anstime DATE NOT NULL 
        ) DEFAULT CHARSET = utf8
    """
    
    Insert_question = 'INSERT INTO question_information(question_str,time)'
    Insert_data = 'INSERT INTO question_data(question_str,anstime)'
    def __init__(self, host, user, pwd, db):
        self.conn = pymysql.connect(host=host, user=user, password=pwd, db=db)
        self.cursor = self.conn.cursor()
        print("数据库连接成功!")
    
    def closeAll(self):
        self.conn.close()
        self.cursor.close()
        print("资源释放完毕!")

    def create_table_func(self):
        self.cursor.execute("DROP TABLE IF EXISTS login_information")
        self.cursor.execute(PyMySQL.create_table)
        print('数据表创建完毕')

    def insert_date(self, name, pwd):
        try:
            self.cursor.execute(PyMySQL.insert + 'VALUES("{}", "{}")'.format(name, pwd))
            self.conn.commit()
            print("数据插入成功!")
            return 1
        except:
            print(traceback.format_exc())
            self.conn.rollback()
            print("数据插入失败!")
            return 0

    def update_data(self, pwd, id):
        try:
            self.cursor.execute(PyMySQL.update + 'pwd={} WHERE id={}'.format(pwd, id))
            self.conn.commit()
            print("数据更新成功!")
        except:
            print(traceback.format_exc())
            self.conn.rollback()
            print("数据更新失败!")

    def delete_data(self, id):
        try:
            self.cursor.execute(PyMySQL.delete + 'id = {}'.format(id))
            self.conn.commit()
            print("数据删除成功!")
        except:
            print(traceback.format_exc())
            self.conn.rollback()
            print("数据删除失败!")

    def select_data(self):
        self.cursor.execute(PyMySQL.select)
        all_data = self.cursor.fetchall()
        for i in all_data:
            print('查询结果为：{}'.format(i))

    def get_message(self, name, pwd):
        sql = "select * from login_information where name='{}' and pwd='{}'".format(name, pwd)
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        data = []
        for k in result:
            target = {}
            for j in range(len(self.cursor.description)):
                target[self.cursor.description[j][0]] = k[j]
                data.append(target)
        
        if len(data) != 0:
            return 1
        else:
            return 0
    
    def get_information(self):
        sql = "select * from login_information"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        ls = []
        for tup in result:
            l = []
            for j in range(3):
                l.append(tup[j])
            ls. append(l)
        return ls
    
    def updata_id(self):
        sql1 = "ALTER  TABLE login_information DROP id"
        sql2 = "ALTER  TABLE login_information ADD id BIGINT(20) PRIMARY KEY NOT NULL AUTO_INCREMENT FIRST"
        self.cursor.execute(sql1)
        self.cursor.execute(sql2)

    def create_table_fun2(self):
        self.cursor.execute("DROP TABLE IF EXISTS question_information")
        self.cursor.execute(PyMySQL.create_table2)
        print('问题数据表创建完毕')

    def select_question(self,question_str):
        time = datetime.date.today()
        try:
            self.cursor.execute(PyMySQL.Insert_question + 'VALUES("{}", "{}")'.format(question_str,time))
            self.conn.commit()
            print("问题信息插入成功!")
            return 1
        except:
            print(traceback.format_exc())
            self.conn.rollback()
            print("问题信息插入失败!")
            return 0
    
    def get_tables(self):
        sql = "SELECT question_str FROM question_information INTO OUTFILE 'D:/Dataspace/mysql/Uploads/text.txt';"
        self.cursor.execute(sql)

    def create_table_fun3(self):
        self.cursor.execute("DROP TABLE IF EXISTS question_data")
        self.cursor.execute(PyMySQL.create_table3)
        print('问题数据表创建完毕')

    def insert_question(self, question_str):
        anstime = datetime.date.today()
        try:
            self.cursor.execute(PyMySQL.Insert_data + 'VALUES("{}", "{}")'.format(question_str,anstime))
            self.conn.commit()
            print("问题信息插入成功!")
            return 1
        except:
            print(traceback.format_exc())
            self.conn.rollback()
            print("问题信息插入失败!")
            return 0

    def get_max_question(self):
        sql4 = "select question_str from question_data where anstime BETWEEN '2023-06-07' and '2023-06-13' group by question_str order by COUNT(question_str) desc LIMIT 3"
        self.cursor.execute(sql4)
        result1 = self.cursor.fetchall()
        return result1

    def get_index_max_question(self):
        result = []
        result1 = self.get_max_question()
        max_question_list = [row[0] for row in result1]
        question_list = list(reversed(max_question_list))
        str1, str2, str3 = max_question_list[0], max_question_list[1], max_question_list[2]
        # 创建字典映射日期和问题字符串到索引位置
        index_map = {
            '2023-06-07': 0,
            '2023-06-08': 1,
            '2023-06-09': 2,
            '2023-06-10': 3,
            '2023-06-11': 4,
            '2023-06-12': 5,
            '2023-06-13': 6
        }
        
        sql5 = "SELECT anstime, question_str, COUNT(*) AS ques_count FROM question_data WHERE anstime BETWEEN '2023-06-07' AND '2023-06-13' AND question_str IN ('{}', '{}', '{}') GROUP BY anstime, question_str".format(str1, str2, str3)
        self.cursor.execute(sql5)
        result2 = self.cursor.fetchall()

        for x in result2:
            anstime = x[0]
            question_str = x[1]
            ques_count = x[2]

            # 使用字典获取索引位置
            anstime_str = anstime.strftime('%Y-%m-%d')
            index = index_map.get(anstime_str)
            if index is not None:
                result.append([index, question_list.index(question_str), ques_count])
        return result

# if __name__ == "__main__":
#     mydb = PyMySQL('localhost','root','ysj528528','chatbot')