from DbAccess import *
import DTO.spots as DTO
from settings import *

class SpotDAO:

    def __init__(self):
        self.spot_list = {}
        self.spot_cbo = []
        self.spots = DTO.Spot()

    def execute(self, sql):
        return dbaccess().exe_sql(sql)

    # select文を作成
    def select(self):
        # セレクト文を作成
        sql = "Select * from {} order by field_id, location_id".format(MST_SPOTS)
        return self.execute(sql)
    
    # delete/insert用
    def select_data(self,l_x, r_x, l_y, r_y):
        where = """
                  {0} <= grid_x
              AND grid_x <= {1}
              AND {2} <= grid_y
              AND grid_y <= {3}
        """.format(l_x, r_x, l_y, r_y)

        return dbaccess().SELECT_Column_A(MST_SPOTS, '*', where)
    
   # select文を実行
    def select_spot(self):
        return dbaccess().SELECT_Column(MST_SPOTS, ['*', ' concat(l_rank, ":", spot_name) as spot_cbo'])
    
    # place_nameをセット
    def set_spot(self,stay_spot, rank_range):
        self.spot_cbo = []
        # self.spots = self.select_spot()
        self.spots = self.set_target_spot(stay_spot, rank_range)
        for spot in self.spots:
            # コンボボックスのリストに追加
            self.spot_cbo.append(spot['spot_cbo'])

        # spotデータ
        return self.spot_cbo

    def pickup_spot(self, spot_cbo):
        s_spot = [spot for spot in self.spots if spot['spot_cbo'] == spot_cbo]
        return s_spot[0]

    # rankによる取得制限あり
    def set_target_spot(self,stay_spot, rank_range):
        self.spot_cbo = []
        return dbaccess().SELECT_Column(MST_SPOTS,['*', ' concat(l_rank, ":", spot_name) as spot_cbo'],stay_spot, rank_range)

    """
    # CSVバルクインサート
    def bulk_insert_spots(self, csv_data):
        csv_data = str(csv_data).replace('\\','/')
        return dbaccess().BULK_INSERT_Column(MST_SPOTS,csv_data)
    """
    
    def bulk_insert_spots(self, values):
        return dbaccess().BULK_INSERT_Column2(MST_SPOTS,values,18)
    
    def updateSpot(self, bk_kingdom_id, new_kingdom_id, new_location_id, target_grids):

        DTO_data = {
            'field_id':new_kingdom_id,
            'location_id':new_location_id,
            'upd_date':self.spots.upd_date,
            'upd_id':self.spots.upd_id
        }
        for data in target_grids:
            where = {
                'field_id':bk_kingdom_id,
                'grid_x':data[0],
                'grid_y':data[1]
            }
            res = dbaccess().UPDATE_Column(MST_SPOTS, DTO_data, where)
        return
    
    def dupplicate_delete(self, l_k_x, r_k_x, l_k_y, r_k_y):
        
        where = """
            WHERE {0} <= grid_x
              AND grid_x <= {1}
              AND {2} <= grid_y
              AND grid_y <= {3}
        """.format(l_k_x, r_k_x, l_k_y, r_k_y)

        return dbaccess().BASIC_DELETE(MST_SPOTS,where)