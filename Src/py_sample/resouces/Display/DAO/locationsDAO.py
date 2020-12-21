from DbAccess import *
import DTO.locations as DTO
from settings import *

class LocationDAO:

    def __init__(self):
        self.location_list = {}
        self.location_cbo = []
        self.locations = None

    def execute(self, sql):
        return dbaccess().exe_sql(sql)

    # select文を作成
    def select(self, Dbname):
        # セレクト文を作成
        sql = "Select * from {}".format(Dbname)
        return sql
    
   # select文を実行
    def select_location(self):
        return dbaccess().SELECT_Column(MST_LOCATIONS, ['*', ' concat(l_rank, ":", location_name) as location_cbo'])
    
    # place_nameをセット
    def set_location(self,stay_location, rank_range):
        self.location_cbo = []
        # self.locations = self.select_location()
        self.locations = self.set_target_location(stay_location, rank_range)
        for location in self.locations:
            # コンボボックスのリストに追加
            self.location_cbo.append(location['location_cbo'])

        # locationデータ
        return self.location_cbo

    def pickup_location(self, location_cbo):
        s_location = [location for location in self.locations if location['location_cbo'] == location_cbo]
        return s_location[0]

    # rankによる取得制限あり
    def set_target_location(self,stay_location, rank_range):
        self.location_cbo = []
        return dbaccess().SELECT_Column(MST_LOCATIONS,['*', ' concat(l_rank, ":", location_name) as location_cbo'],stay_location, rank_range)

    # 王国登録
    def insert_location(self,entry_list):
        res = dbaccess().INSERT_Column(MST_LOCATIONS, entry_list[0])
        return dbaccess().SELECT_Column(MST_LOCATIONS, '*', {'location_id':res})
