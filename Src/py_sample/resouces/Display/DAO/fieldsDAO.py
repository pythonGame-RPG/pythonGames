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
        return dbaccess().SELECT_Column(MST_FIELDS, '*', ' concat(f_rank, ":", field_name) as field_cbo')
    
    # field_nameをセット
    def set_field(self):
        self.fields = self.select_field()
        for field in self.fields:
            # コンボボックスのリストに追加
            # self.field_list[field['field_id']] = field['f_rank'] + ':' + field['field_name']
            self.field_cbo.append(field['field_cbo'])
        # self.field_cbo.append("")

        # fieldデータ
        return self.field_cbo

    # レベル異存なし取得
    def pickup_field(self, field_cbo):
        s_field = [field for field in self.fields if field['field_cbo'] == field_cbo]
        return s_field[0]