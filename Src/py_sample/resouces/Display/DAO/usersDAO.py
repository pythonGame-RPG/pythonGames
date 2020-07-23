from DbAccess import *
import DTO.fields as DTO
from settings import *


class FieldDAO:

    def __init__(self):
        self.field_list = {}
        self.field_cbo = []
        self.fields = None

    def execute(self, sql):
        return dbaccess().exe_sql(sql)

    # select文を作成
    def select(self, Dbname):
        # セレクト文を作成
        sql = "Select * from {}".format(Dbname)
        return sql
    
   # select文を作成
    def select_field(self):
        return dbaccess().SELECT_Column(MST_FIELDS, ['*', ' concat(f_rank, ":", field_name) as field_cbo'])
    
    # place_nameをセット
    def set_field(self, stay_field=None, rank_range=None):
        self.field_cbo = []
        # self.fields = self.select_field()
        self.fields = self.set_target_field(stay_field, rank_range)
        for field in self.fields:
            # コンボボックスのリストに追加
            self.field_cbo.append(field['field_cbo'])

        # fieldデータ
        return self.field_cbo

    def pickup_field(self, field_cbo):
        s_field = [field for field in self.fields if field['field_cbo'] == field_cbo]
        return s_field[0]

    # rankによる取得制限あり
    def set_target_field(self,stay_field, rank_range):
        self.field_cbo = []
        return dbaccess().SELECT_Column(MST_FIELDS,['*', ' concat(f_rank, ":", field_name) as field_cbo'],stay_field, rank_range)