import tkinter as tk
from DbAccess import *
from settings import *

class Talent:
    def __init__(self):
        self.race_name = tk.StringVar()
        self.p_HP = tk.IntVar()
        self.p_MP = tk.IntVar()
        self.p_sta = tk.IntVar()
        self.p_atk = tk.IntVar()
        self.p_bit = tk.IntVar()
        self.p_mag = tk.IntVar()
        self.p_des = tk.IntVar()
        self.p_agi = tk.IntVar()
        self.total_sense = tk.IntVar()
        self.race_rank = tk.StringVar()
        self.ins_date = None
        self.ins_id = None
        self.upd_date = None
        self.upd_id = None

        self.bk_num = 0
        self.bk_total_sense = 0

    def init(self):
        self.personal_code.set(1)
        self.p_HP.set(1)
        self.p_MP.set(1)
        self.p_sta.set(1)
        self.p_atk.set(1)
        self.p_bit.set(1)
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