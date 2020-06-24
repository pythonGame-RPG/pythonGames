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
        return dbaccess().SELECT_Column(MST_RACES, ['*', ' concat(r_rank, ":", race_name) as race_cbo'])
    
    # race_nameをセット
    def set_race(self):
        self.races = self.select_race()
        for race in self.races:
            # コンボボックスのリストに追加
            # self.race_list[race['race_id']] = race['r_rank'] + ':' + race['race_name']
            self.race_cbo.append(race['race_cbo'])

        # raceデータ
        return self.race_cbo

    # レベル異存なし取得
    def pickup_race(self, race_cbo):
        s_race = [race for race in self.races if race['r_rank'] + ':' + race['race_name'] == race_cbo]
        return s_race[0]

    # SELECT SQL
    def select_races(self):
        sql="""
            SELECT 
            *
            FROM dbo.races 
            WHERE is_deleted = 0
            ORDER BY race_id
        """
        self.races = dbaccess().exe_sql(sql)
        return self.races

    def insert_race(self, race):
        pass

    # NOTE:レベルによって選択可能データを制限
    def set_target_race(self,level):
        self.race_cbo = []
        # racesプレースホルダ 
        sql="""
            WITH RECURSIVE races AS (
                SELECT 
                race_id, 
                race_name, 
                p_HP,
                p_MP,
                p_sta,
                p_atk,
                p_vit,
                p_mag,
                p_des,
                p_agi,
                total_pattern,
                parent_race1_id, 
                evolution1_level, 
                100                 AS over_evolution1_lv, 
                parent_race2_id, 
                evolution2_level,
                0                 AS over_evolution2_lv, 
                parent_race3_id, 
                evolution3_level, 
                0                 AS over_evolution3_lv,
                r_rank,
                concat(r_rank, ":", race_name) as race_cbo
                FROM dbo.races 
                WHERE parent_race1_id = 0
                UNION ALL

                SELECT 
                child.race_id, 
                child.race_name, 
                child.p_HP,
                child.p_MP,
                child.p_sta,
                child.p_atk,
                child.p_vit,
                child.p_mag,
                child.p_des,
                child.p_agi,
                child.total_pattern,
                child.parent_race1_id, 
                child.evolution1_level, 
                races.evolution1_level AS over_evolution1_lv, 
                child.parent_race2_id, 
                child.evolution2_level,
                races.evolution2_level AS over_evolution2_lv, 
                child.parent_race3_id, 
                child.evolution3_level, 
                races.evolution3_level AS over_evolution3_lv,
                child.r_rank,
                concat(child.r_rank, ":", child.race_name) as race_cbo
                FROM dbo.races AS child, races
                WHERE races.race_id = child.parent_race1_id

                UNION ALL
                SELECT 
                child.race_id, 
                child.race_name, 
                child.p_HP,
                child.p_MP,
                child.p_sta,
                child.p_atk,
                child.p_vit,
                child.p_mag,
                child.p_des,
                child.p_agi,
                child.total_pattern,
                child.parent_race1_id, 
                child.evolution1_level, 
                races.evolution1_level AS over_evolution1_lv, 
                child.parent_race2_id, 
                child.evolution2_level,
                races.evolution2_level AS over_evolution2_lv, 
                child.parent_race3_id, 
                child.evolution3_level, 
                races.evolution3_level AS over_evolution3_lv,
                child.r_rank,
                concat(child.r_rank, ":", child.race_name) as race_cbo
                FROM dbo.races AS child, races
                WHERE races.race_id = child.parent_race2_id

                UNION ALL
                SELECT 
                child.race_id, 
                child.race_name, 
                child.p_HP,
                child.p_MP,
                child.p_sta,
                child.p_atk,
                child.p_vit,
                child.p_mag,
                child.p_des,
                child.p_agi,
                child.total_pattern,
                child.parent_race1_id, 
                child.evolution1_level, 
                races.evolution1_level AS over_evolution1_lv, 
                child.parent_race2_id, 
                child.evolution2_level,
                races.evolution2_level AS over_evolution2_lv, 
                child.parent_race3_id, 
                child.evolution3_level, 
                races.evolution3_level AS over_evolution3_lv,
                child.r_rank,
                concat(child.r_rank, ":", child.race_name) as race_cbo
                FROM dbo.races AS child, races
                WHERE races.race_id = child.parent_race3_id
            )
            SELECT * FROM races

            WHERE (evolution1_level <= {0}
                AND over_evolution1_lv+1 > {0})
                OR(evolution2_level <= {0}
                AND over_evolution2_lv+1 > {0})
                OR(evolution3_level <= {0}
                AND over_evolution3_lv+1 > {0});
        """
        sql = sql.format(level)
        self.races = dbaccess().exe_sql(sql)
        
        for race in self.races:
            # コンボボックスのリストに追加
            # self.race_list[race['race_id']] = race['r_rank'] + ':' + race['race_name']
            self.race_cbo.append(race['race_cbo'])
        # self.race_cbo.append("")

        # raceデータ
        return self.race_cbo
        
    

    