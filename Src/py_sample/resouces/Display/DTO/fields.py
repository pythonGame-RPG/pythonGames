import tkinter as tk
from DbAccess import *
from settings import *
from datetime import *

class Field:
    def __init__(self):
        self.field_id = tk.StringVar()
        self.field_name = tk.StringVar()
        self.f_rank = tk.StringVar()
        self.king_gene_id = tk.StringVar()
        self.character_id = tk.StringVar()
        self.contract_id = tk.StringVar()
        self.is_war = tk.IntVar()
        self.area = tk.IntVar()
        self.population = tk.IntVar()
        self.p_density = tk.DoubleVar()
        self.stress = tk.IntVar()
        self.hate = tk.IntVar()
        self.power = tk.IntVar()
        self.welfare = tk.IntVar()
        self.technology = tk.IntVar()
        self.military = tk.IntVar()
        self.civil_point = tk.IntVar()
        self.civilization = tk.IntVar()
        self.innovation = tk.IntVar()
        self.strength = tk.IntVar()
        self.assets = tk.IntVar()
        self.GDP = tk.DoubleVar()
        self.tax = tk.DoubleVar()
        self.disparity = tk.DoubleVar()
        self.develop = tk.DoubleVar()
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

    def insert_field(self):
        dbaccess().insert(self, )

    def select_field(self, where = None):
        dbaccess().SELECT_All(MST_FIELDS)
    
    # field_nameをセット
    def set_field_name(self):
        field_name = [""]
        # fieldデータ取得
        fields = self.select_field()
        for data in fields:
            field_name.append(data)
        
        return field_name