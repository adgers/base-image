import pymysql


d_db_info = {
    'd_db_host': '',
    'd_db_port': 3306,
    'd_db_':''
}



class DBUtils():
    def __init__(self):
        self.conn = pymysql.connect()