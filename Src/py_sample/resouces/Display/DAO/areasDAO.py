from DbAccess import *
import DTO.areas as DTO
from settings import *

class AreaDAO:

    def __init__(self):
        self.area_list = {}
        self.area_cbo = []
        self.areas = DTO.Area()

    def execute(self, sql):
        return dbaccess().exe_sql(sql)

    # select文を作成
    def select(self):
        # セレクト文を作成
        sql = "Select * from {} order by field_id, location_id".format(MST_AREAS)
        return self.execute(sql)
    
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

    """
    # CSVバルクインサート
    def bulk_insert_areas(self, csv_data):
        csv_data = str(csv_data).replace('\\','/')
        return dbaccess().BULK_INSERT_Column(MST_AREAS,csv_data)
    """

    def bulk_insert_areas(self, values):
        return dbaccess().BULK_INSERT_Column2(MST_AREAS,values,20)
    
    def updateArea(self, bk_kingdom_id, new_kingdom_id, new_location_id, target_grids):

        DTO_data = {
            'field_id':new_kingdom_id,
            'location_id':new_location_id,
            'upd_date':str(self.areas.upd_date),
            'upd_id':self.areas.upd_id
        }
        for data in target_grids:
            where = {
                'field_id':bk_kingdom_id,
                'grid_x':data[0],
                'grid_y':data[1]
            }
            res = dbaccess().UPDATE_Column(MST_AREAS, DTO_data, where)
        return
    
    def dupplicate_delete(self, l_k_x, r_k_x, l_k_y, r_k_y):
        
        where = """
            WHERE {0} <= grid_x
              AND grid_x <= {1}
              AND {2} <= grid_y
              AND grid_y <= {3}
        """.format(l_k_x, r_k_x, l_k_y, r_k_y)

        return dbaccess().BASIC_DELETE(MST_AREAS,where)