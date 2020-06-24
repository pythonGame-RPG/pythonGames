import tkinter as tk
from datetime import *
from DbAccess import *
from settings import *

class Race:
    def __init__(self):
        self.race_name = tk.StringVar()
        self.p_HP = tk.StringVar()
        self.p_MP = tk.StringVar()
        self.p_sta = tk.StringVar()
        self.p_atk = tk.StringVar()
        self.p_vit = tk.StringVar()
        self.p_mag = tk.StringVar()
        self.p_des = tk.StringVar()
        self.p_agi = tk.StringVar()
        self.total_pattern = tk.IntVar()
        self.race_rank = tk.StringVar()
        self.parent_race1_id = tk.StringVar()
        self.evolution1_level = tk.StringVar()
        self.parent_race2_id = tk.StringVar()
        self.evolution2_level = tk.StringVar()
        self.parent_race3_id = tk.StringVar()
        self.evolution3_level = tk.StringVar()
        self.initial_flg = tk.IntVar()
        self.ins_date = datetime.now()
        self.ins_id = None
        self.upd_date = datetime.now()
        self.upd_id = None
        self.bk_num = 0
        self.bk_total_sense = 0

    def init(self):
        self.p_HP.set(1)
        self.p_MP.set(1)
        self.p_sta.set(1)
        self.p_atk.set(1)
        self.p_vit.set(1)
        self.p_mag.set(1)
        self.p_des.set(1)
        self.p_agi.set(1)

    def insert_race(self):
        dbaccess().insert(self, )

    def select_race(self, where = None):
        dbaccess().SELECT_All(MST_RACES)

    # race_nameをセット
    def set_race_name(self):
        race_name = [""]
        # raceデータ取得
        races = self.select_race()
        for data in races:
            race_name.append(data)
        
        return race_name

    def set_select_race(self, s_race):
        self.race_name.set(s_race['race_name'])
        self.p_HP.set(s_race['p_HP'])
        self.p_MP.set(s_race['p_MP'])
        self.p_sta.set(s_race['p_sta'])
        self.p_atk.set(s_race['p_atk'])
        self.p_vit.set(s_race['p_vit'])
        self.p_mag.set(s_race['p_mag'])
        self.p_des.set(s_race['p_des'])
        self.p_agi.set(s_race['p_agi'])
        self.total_pattern.set(s_race['total_pattern'])
        self.parent_race1_id.set(s_race['parent_race1_id'])
        self.evolution1_level.set(s_race['evolution1_level'])
        self.parent_race2_id.set(s_race['parent_race2_id'])
        self.evolution2_level.set(s_race['evolution2_level'])
        self.parent_race3_id.set(s_race['parent_race3_id'])
        self.evolution3_level.set(s_race['evolution3_level'])
        self.initial_flg.set(s_race['initial_flg'])