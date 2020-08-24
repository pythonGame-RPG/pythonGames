from DbAccess import *
import DTO.areas as DTO
from settings import *

class AreaDAO:

    def __init__(self):
        self.area_list = {}
        self.area_cbo = []
        self.areas = None

    def execute(self, sql):
        return dbaccess().exe_sql(sql)

    # select文を作成
    def select(self, Dbname):
        # セレクト文を作成
        sql = "Select * from {}".format(Dbname)
        return sql
    
   # select文を実行
    def select_area(self):
        return dbaccess().SELECT_Column(MST_AREAS, ['*', ' concat(l_rank, ":", area_name) as area_cbo'])
    
    # place_nameをセット
    def set_area(self,stay_area, rank_range):
        self.area_cbo = []
        # self.areas = self.select_area()
        self.areas = self.set_target_area(stay_area, rank_range)
        for area in self.areas:
            # コンボボックスのリストに追加
            self.area_cbo.append(area['area_cbo'])

        # areaデータ
        return self.area_cbo

    def pickup_area(self, area_cbo):
        s_area = [area for area in self.areas if area['area_cbo'] == area_cbo]
        return s_area[0]

    # rankによる取得制限あり
    def set_target_area(self,stay_area, rank_range):
        self.area_cbo = []
        return dbaccess().SELECT_Column(MST_AREAS,['*', ' concat(l_rank, ":", area_name) as area_cbo'],stay_area, rank_range)