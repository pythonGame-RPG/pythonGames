import tkinter as tk
from DbAccess import *
from settings import *
from datetime import *

class Location:
    def __init__(self):
        self.location_id = tk.StringVar()
        self.field_id = tk.StringVar()
        self.lord_gene_id = tk.StringVar()
        self.character_id = tk.StringVar()
        self.location_name = tk.StringVar()
        self.l_rank = tk.StringVar()
        self.is_battle = tk.IntVar()
        self.area = tk.IntVar()
        self.population = tk.IntVar()
        self.p_density = tk.IntVar()
        self.stress = tk.IntVar()
        self.hate = tk.IntVar()
        self.power = tk.IntVar()
        self.welfare = tk.IntVar()
        self.technology = tk.IntVar()
        self.military = tk.IntVar()
        self.civil_point = tk.IntVar()
        self.civilization = tk.DoubleVar()
        self.innovation = tk.IntVar()
        self.strength = tk.IntVar()
        self.assets = tk.IntVar()
        self.GDP = tk.IntVar()
        self.tax = tk.DoubleVar()
        self.develop = tk.DoubleVar()
        self.disparity = tk.DoubleVar()
        self.version = 1
        self.is_deleted = 0
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