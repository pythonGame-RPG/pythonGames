# MySQLdbのインポート
import MySQLdb
from contextlib import closing
from select import *

# データベースへの接続とカーソルの生成
conn = MySQLdb.connect(
    host='localhost',
    user='root',
    passwd='root',
    db='dbo')
cursor = conn.cursor()

# ここに実行したいコードを入力します
class users:
    def __init__(self):
        self.id = 0
        self.user_id = 0
        self.password = 0
        self.ins_date = 0
        self.ins_id = 0
        self.upd_date = 0
        self.upd_id = 0
        self.name = "unknown"
        self.is_deleted = 0
        self.is_admin = 0
        self.is_sec = 0
        self.is_save = 0
        self.play_time = 0
        self.total_amount = 0


    def execute(self, sql):
        with closing(conn.cursor()) as cursor:
            cursor.execute(select.onwith())
            rows = cursor.fetchall()
        # keyが一致した場合に、取得したデータを格納する
        for data in rows:
            # TODO:★keyを取得するメソッド
            data = 1
    
    # select文を作成
    def select(self, Dbname):
        # カンマ区切りでリストをstrにここでは使わない
        # data_str = ",".join(map(str, data))
        # セレクト文を作成
        sql = format("Select * from {0}", Dbname)
        return sql

    def where(self, select, datas):
        user_id = format("user_id = {}", str(datas[0]))
        password = format("password = {}", str(datas[1]))
        sql_where = format(" where {0} and {1}", user_id, password)
        return select.join(sql_where)
            


    # where文を作成
    # def where(self)

class players:
    def __init__(self):
        self.id = 0
        self.user_id = 0
        self.password = 0
        self.ins_date = 0
        self.ins_id = 0
        self.upd_date = 0
        self.upd_id = 0
        self.name = "unknown"
        self.is_deleted = 0
        self.is_admin = 0
        self.is_sec = 0
        self.is_save = 0
        self.play_time = 0
        self.total_amount = 0

# 保存を実行
conn.commit()

# 接続を閉じる
conn.close()