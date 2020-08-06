from DbAccess import *
import DTO.users as DTO
from settings import *

class UserDAO:

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
        self.user_list = {}
        self.user_cbo = []
        self.users = None

    def execute(self, sql):
        return dbaccess().exe_sql(sql)

    # select文を作成
    def select(self, Dbname):
        # セレクト文を作成
        sql = "Select * from {}".format(Dbname)
        return sql

    def insert_user(self,user):
        u_data = {}
        u_data['user_id'] = user.user_id.get()
        u_data['password'] = user.password.get()
        u_data['name'] = user.name.get()
        u_data['is_admin'] = user.is_admin.get()
        u_data['is_sec'] = user.is_sec.get()
        u_data['is_save'] = user.is_save.get()
        u_data['play_time'] = user.play_time.get()
        u_data['total_amount'] = user.total_amount.get()
        u_data['money'] = user.money.get()
        u_data['cost'] = user.cost.get()
        u_data['version'] = user.version.get()
        u_data['is_deleted'] = user.is_deleted.get()
        u_data['ins_date'] = user.ins_date
        u_data['ins_id'] = user.ins_id
        u_data['upd_date'] = user.upd_date
        u_data['upd_id'] = user.upd_id

        res = dbaccess().INSERT_Column(MST_USERS,u_data)
        return res
    
    # select文を作成
    def select(self, Dbname):
        # セレクト文を作成
        sql = "Select * from {}".format(Dbname)
        return sql

    def where(self, select, datas, bigger = None, smaller = None):
        where_list = []
        # keyとvalueをイコール関係で結びつける
        try:
            for dkey, dvalue in datas.items():
                where_list.append(dkey + ' = '  + '"{}"'.format(dvalue))
        except AttributeError:
            pass
        try:
            # 大なり
            for dkey, dvalue in bigger.items():
                where_list.append(dkey + ' >= '  + '"{}"'.format(dvalue))
        except AttributeError:
            pass
        try:
            # 小なり
            for dkey, dvalue in bigger.items():
                where_list.append(dkey + ' <= '  + '"{}"'.format(dvalue))
        except AttributeError:
            pass
        
        # AND区切りの文字列に変換
        where = " AND ".join(map(str, where_list))
        where = " where " + where
        return select + where

    """
    def pickup_user(self, user_cbo):
        s_user = [user for user in self.users if user['user_cbo'] == user_cbo]
        return s_user[0]

    # rankによる取得制限あり
    def set_target_user(self,stay_user, rank_range):
        self.user_cbo = []
        return dbaccess().SELECT_Column(MST_USERS,['*', ' concat(f_rank, ":", user_name) as user_cbo'],stay_user, rank_range)
    """