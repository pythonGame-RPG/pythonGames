from DbAccess import *
import DTO.races as DTO
from settings import *


class RaceDAO:

    def __init__(self):
        self.race_name = []  
        self.race_list = {}
        self.race_cbo = []

    def execute(self, sql):
        return dbaccess().exe_sql(sql)

    # select文を作成
    def select(self, Dbname):
        # セレクト文を作成
        sql = "Select * from {}".format(Dbname)
        return sql
    
   # select文を作成
    def select_race(self):
        # _comb = ('race_id', 'r_rank', 'race_name')
        return dbaccess().SELECT_Column(MST_RACES,'race_id', 'race_name', 'r_rank')
    
    # race_nameをセット
    def set_race(self):
        races = self.select_race()
        for race in races:
            # コンボボックスのリストに追加
            self.race_list[race['race_id']] = race['r_rank'] + ':' + race['race_name']
            # self.race_cbo.append(race['race_name'])

        # raceデータ取得
        return self.race_list

    