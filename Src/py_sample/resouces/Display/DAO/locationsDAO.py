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
    
   # select文を作成
    def select_location(self):
        return dbaccess().SELECT_Column(MST_LOCATIONS, '*', ' concat(l_rank, ":", location_name) as location_cbo')
    
    # place_nameをセット
    def set_location(self, ):
        self.location_cbo = []
        self.locations = self.select_location()
        for location in self.locations:
            # コンボボックスのリストに追加
            self.location_cbo.append(location['location_cbo'])
        # self.location_cbo.append("")

        # locationデータ
        return self.location_cbo

    # TODO:レベル比例で取得可能ランク変動
    def pickup_location(self, location_cbo):
        s_location = [location for location in self.locations if location['location_cbo'] == location_cbo]
        return s_location[0]