from DbAccess import *
import DTO.locations as DTO
from settings import *


class LocationDAO:

    def __init__(self):
        self.place_name = [""]  
        self.location_list = {}
        self.location_cbo = []

    def execute(self, sql):
        return dbaccess().exe_sql(sql)

    # select文を作成
    def select(self, Dbname):
        # セレクト文を作成
        sql = "Select * from {}".format(Dbname)
        return sql
    
   # select文を作成
    def select_location(self):
        # _comb = ('location_id', 'p_rank', 'place_name')
        return dbaccess().SELECT_Column(MST_LOCATIONS,'location_id', 'place_name', 'p_rank')
    
    # place_nameをセット
    def set_location(self):
        locations = self.select_location()
        for location in locations:
            # コンボボックスのリストに追加
            self.location_list[location['location_id']] = location['p_rank'] + ':' + location['place_name']
            # self.location_cbo.append(location['place_name'])

        # locationデータ取得
        return self.location_list