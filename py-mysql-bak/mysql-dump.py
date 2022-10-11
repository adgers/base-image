import os
import time
import datetime
import pymysql

D_CONN = pymysql.connect(host='localhost', port=3306, user='root', password='xierui123')

# 定义源库服务器的信息
S_DB_HOST = '172.27.16.4'
S_DB_PORT = '3306'
S_DB_USER = 'root'
S_DB_PASS = 'G5wefFIvq^Kp'
BACKUP_PATH = '/tmp/mysqlback/'
DATETIME = time.strftime('%Y-%m-%d-%H')

# # 定义目标库服务器的信息
D_DB_HOST = '172.27.0.111'
D_DB_PORT = 31002
D_DB_USER = 'root'
D_DB_PASS = 'MqI9C1oYpofHAD'

MYSQL_DUMP_COMM = '/usr/local/mysql/bin/mysqldump'
MYSQL_COMM = '/usr/local/mysql/bin/mysql'

DB_NAMES = './dbs.txt'

TODAYBACKUPPATH = BACKUP_PATH + DATETIME


# print("DATETIME: ", DATETIME, "TODAYBACKUPPATH", TODAYBACKUPPATH)


def run_backup():
    with open('./dbs.txt', "r") as dbs:
        for dbname in dbs.readlines():
            dbname = dbname.strip()
            print("now Starting backup datebases", dbname)
            dumpcmd = MYSQL_DUMP_COMM + " -h " + S_DB_HOST + " -P " + S_DB_PORT + " -u" + S_DB_USER + " -p" + S_DB_PASS + " --set-gtid-purged=off " + " " + dbname + ">" + TODAYBACKUPPATH + '/' + dbname + '.sql'
            try:
                os.system(dumpcmd)
            except IOError:
                print("数据库%s备份未成功" % dbname)
            else:
                print("数据库%s备份成功" % dbname, "备份路径在%s" % TODAYBACKUPPATH + '/' + dbname + '.sql')


def drop_database():
    D_CONN = pymysql.connect(host=D_DB_HOST, port=D_DB_PORT, user=D_DB_USER, password=D_DB_PASS, charset='utf8')
    with open('./dbs.txt', "r") as dbs:
        for dbname in dbs.readlines():
            dbname = dbname.strip()
            # print("now drop datebases", dbname)
            cursor = D_CONN.cursor()
            sql = "drop database " + dbname
            cursor.execute(sql)
            print(f"已删除数据库db %s" % dbname)

            # print(res)
    cursor.close()
    D_CONN.close()


def creat_datebase():
    D_CONN = pymysql.connect(host=D_DB_HOST, port=D_DB_PORT, user=D_DB_USER, password=D_DB_PASS, charset='utf8')
    with open('./dbs.txt', 'r') as  dbs:
        for dbname in dbs.readlines():
            dbname = dbname.strip()
            sql = "create database " + dbname
            print(sql)
            cursor = D_CONN.cursor()
            cursor.execute(sql)
            print(f"已创建db %s" % dbname)
    cursor.close()
    D_CONN.close()


# def get_sql(dir):
#     files = os.listdir(dir)
#     files.sort()
#     dumpcmd =
#

def import_database():
    sqls = os.listdir(TODAYBACKUPPATH)
    sqls.sort()
    print(sqls)


class DbError(Exception):
    pass




if __name__ == '__main__':
    if not os.path.exists(TODAYBACKUPPATH):
        print("Creating backup folder ")
        os.makedirs(TODAYBACKUPPATH)
    run_backup()
    # try:
    #     drop_database()
    #     creat_datebase()
    # except Exception as d:
    #     print(d)




