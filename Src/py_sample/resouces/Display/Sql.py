from select import *
from DbAccess import *

# ここに実行したいコードを入力します
class sql_query:
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
        return dbaccess().exe_sql(sql)
    
    # select文を作成
    def select(self, Dbname):
        # カンマ区切りでリストをstrにここでは使わない
        # data_str = ",".join(map(str, data))
        # セレクト文を作成
        sql = "Select * from {}".format(Dbname)
        return sql

    def where(self, select, datas):
        where_list = []
        # keyとvalueをイコール関係で結びつける
        for dkey, dvalue in datas.items():
            where_list.append(dkey + ' = '  + '"{}"'.format(dvalue))
        # AND区切りの文字列に変換
        where = " AND ".join(map(str, where_list))
        where = " where " + where
        return select + where

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
