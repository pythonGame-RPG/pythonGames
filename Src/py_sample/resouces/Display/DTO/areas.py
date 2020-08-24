import tkinter as tk
from DbAccess import *
from settings import *
from datetime import *

class Location:
    def __init__(self):
        self.location_id = tk.StringVar()
        self.grid_x = tk.StringVar()
        self.grid_y = tk.StringVar()
        self.lord_gene_id = tk.StringVar()
        self.character_id = tk.StringVar()
        self.place_name = tk.StringVar()
        self.p_rank = tk.StringVar()
        self.is_sea = tk.IntVar()
        self.is_battle = tk.IntVar()
        self.is_guild = tk.IntVar()
        self.g_point = tk.StringVar()
        self.g_rank = tk.StringVar()
        self.is_church = tk.IntVar()
        self.c_point = tk.StringVar()
        self.c_rank = tk.StringVar()
        self.is_blacksmith = tk.IntVar()
        self.b_point = tk.StringVar()
        self.b_rank = tk.StringVar()
        self.assets = tk.StringVar()
        self.civilization = tk.StringVar()
        self.population = tk.StringVar()
        self.ins_date = datetime.now()
        self.ins_id = None
        self.upd_date = datetime.now()
        self.upd_id = None

        self.bk_num = 0
        self.bk_total_sense = 0

    def init(self):
        pass

    def insert_location(self):
        dbaccess().insert(self, )

    def select_location(self, where = None):
        dbaccess().SELECT_All(MST_LOCATIONS)
    
    # location_nameをセット
    def set_location_name(self):
        location_name = [""]
        # locationデータ取得
        locations = self.select_location()
        for data in locations:
            location_name.append(data)
        
        return location_namer