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
    
    # 一件登録
    def insert_race(self, races):
        r_list = {}
        r_list['race_name'] = races.race_name.get()
        r_list['p_HP'] = races.p_HP.get()
        r_list['p_MP'] = races.p_MP.get()
        r_list['p_sta'] = races.p_sta.get()
        r_list['p_atk'] = races.p_atk.get()
        r_list['p_vit'] = races.p_vit.get()
        r_list['p_mag'] = races.p_mag.get()
        r_list['p_des'] = races.p_des.get()
        r_list['p_agi'] = races.p_agi.get()
        r_list['total_pattern'] = races.total_pattern.get()
        r_list['r_rank'] = races.r_rank.get()
        r_list['parent_race1_id'] = 0
        r_list['evolution1_level'] = 100
        r_list['initial_flg'] = races.initial_flg.get()
        r_list['is_deleted'] = 0
        r_list['version'] = 1
        r_list['ins_date'] = races.ins_date
        r_list['ins_id'] = races.ins_id
        r_list['upd_date'] = races.upd_date
        r_list['upd_id'] = races.upd_id

        res = dbaccess().INSERT_Column(MST_RACES, r_list)
        return res
    
    # 進化先種族の更新
    def update_race(self, races):
        # 更新項目を設定
        r_list = {}
        r_list['race_name'] = races.race_name.get()
        r_list['p_HP'] = races.p_HP.get()
        r_list['p_MP'] = races.p_MP.get()
        r_list['p_sta'] = races.p_sta.get()
        r_list['p_atk'] = races.p_atk.get()
        r_list['p_vit'] = races.p_vit.get()
        r_list['p_mag'] = races.p_mag.get()
        r_list['p_des'] = races.p_des.get()
        r_list['p_agi'] = races.p_agi.get()
        r_list['total_pattern'] = races.total_pattern.get()
        r_list['r_rank'] = races.r_rank.get()
        r_list['parent_race1_id'] = races.parent_race1_id.get()
        r_list['evolution1_level'] = races.evolution1_level.get()
        r_list['parent_race2_id'] = races.parent_race2_id.get()
        r_list['evolution2_level'] = races.evolution2_level.get()
        r_list['parent_race3_id'] = races.parent_race3_id.get()
        r_list['evolution3_level'] = races.evolution3_level.get()
        r_list['initial_flg'] = races.initial_flg.get()
        r_list['version'] = races.version.get() + 1
        r_list['upd_date'] = races.upd_date
        r_list['upd_id'] = races.upd_id

        # 抽出条件を設定
        where = {}
        where['race_id'] = races.race_id.get()
        where['is_deleted'] = 0

        res = dbaccess().UPDATE_Column(MST_RACES, r_list, where)

    # 子種族の更新
    def update_child_race(self, baseRases, inRace):
        # 更新項目を設定
        r_list = {}
        r_list['parent_race1_id'] = """
                                    case when parent_race1_id == 0 
                                    then  {0} 
                                    end 
                                    """.format(inRace.race_id.get())
        r_list['parent_race2_id'] = """
                                    case when parent_race1_id != 0 
                                          and parent_race2_id == null
                                    then  {0} 
                                    end 
                                    """.format(inRace.race_id.get())
        r_list['parent_race3_id'] = """
                                    case when parent_race1_id != 0 
                                          and parent_race2_id != null 
                                    then  {0} 
                                    end 
                                    """.format(inRace.race_id.get())
        r_list['version'] = baseRases.version + 1
        r_list['upd_date'] = baseRases.upd_date
        r_list['upd_id'] = baseRases.upd_id.get()

        # 抽出条件を設定
        where = {}
        where['race_id'] = baseRases.race_id.get()
        where['is_deleted'] = 0

        dbaccess().UPDATE_Column(MST_RACES, r_list, where)


        
    

    