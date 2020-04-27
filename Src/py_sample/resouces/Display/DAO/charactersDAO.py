from DbAccess import *
import DTO.characters as DTO

class CharacterDAO:
    def __init__(self):
        self.ch_name = None


    def execute(self, sql):
        return dbaccess().exe_sql(sql)

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
