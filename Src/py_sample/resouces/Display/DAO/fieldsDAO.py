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
    
    # 王候補をピックアップ
    def chooseCharacter(self,s_x,s_y,e_x,e_y):

        l_x = 0
        l_y = 0
        r_x = 0
        r_y = 0
        
        # TODO:面倒だから元結良い方法ないかな入れ替え処理
        if s_x < e_x:
            l_x = e_x
            r_x = s_x
        else:
            l_x = s_x
            r_x = e_x

        if s_y < e_y:
            l_y = e_y
            r_y = s_y
        else:
            l_y = s_y
            r_y = e_y

        where = """grid_x >= {0} and 
                   grid_x <= {1} and
                   grid_y <= {2} and
                   grid_y >= {3} """.format(l_x,l_y,r_x,r_y)
        sort = "name"

        #return dbaccess().SELECT_Column_A(MST_CHARACTERS,[' * '] ,where,sort)
        return dbaccess().SELECT_Column_A(MST_CHARACTERS,[' * '])

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
    
    # 王国登録
    def insert_field(self,entry_list):
        res = dbaccess().INSERT_Column(MST_FIELDS, entry_list[0])
        return dbaccess().SELECT_Column(MST_FIELDS, '*', {'field_id':res})