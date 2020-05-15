from DbAccess import *
import DTO.races as DTO
from settings import *


class RaceDAO:

    def __init__(self):
        self.race_list = {}
        self.race_cbo = []
        self.races = None

    def execute(self, sql):
        return dbaccess().exe_sql(sql)

    # select文を作成
    def select(self, Dbname):
        # セレクト文を作成
        sql = "Select * from {}".format(Dbname)
        return sql
    
   # select文を作成
    def select_race(self):
        return dbaccess().SELECT_Column(MST_RACES, '*', ' concat(r_rank, ":", race_name) as race_cbo')
    
    # race_nameをセット
    def set_race(self):
        self.races = self.select_race()
        for race in self.races:
            # コンボボックスのリストに追加
            # self.race_list[race['race_id']] = race['r_rank'] + ':' + race['race_name']
            self.race_cbo.append(race['race_cbo'])
        # self.race_cbo.append("")

        # raceデータ
        return self.race_cbo

    # レベル異存なし取得
    def pickup_race(self, race_cbo):
        s_race = [race for race in self.races if race['race_cbo'] == race_cbo]
        return s_race[0]

    