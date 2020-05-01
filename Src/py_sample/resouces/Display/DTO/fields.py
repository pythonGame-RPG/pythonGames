import tkinter as tk
from DbAccess import *
from settings import *

class Field:
    def __init__(self):
        self.grid_x = tk.IntVar()
        self.grid_y = tk.IntVar()
        self.lord_gene_id = tk.IntVar()
        self.character_id = tk.IntVar()
        self.place_name = tk.IntVar()
        self.p_rank = tk.IntVar()
        self.is_sea = tk.IntVar()
        self.is_battle = tk.IntVar()
        self.is_guild = tk.IntVar()
        self.g_point = tk.IntVar()
        self.g_rank = tk.IntVar()
        self.is_church = tk.IntVar()
        self.c_point = tk.IntVar()
        self.c_rank = tk.IntVar()
        self.is_blacksmith = tk.IntVar()
        self.b_point = tk.IntVar()
        self.b_rank = tk.IntVar()
        self.assets = tk.IntVar()
        self.civilization = tk.IntVar()
        self.population = tk.IntVar()

        self.bk_num = 0
        self.bk_total_sense = 0

    def init(self):
        pass

    def insert_field(self):
        dbaccess().insert(self, )

    def select_field(self, where = None):
        dbaccess().SELECT_All(MST_fieldS)
    
    # field_nameをセット
    def set_field_name(self):
        field_name = [""]
        # fieldデータ取得
        fields = self.select_field()
        for data in fields:
            field_name.append(data)
        
        return field_name