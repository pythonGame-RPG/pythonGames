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
        self.is_war = tk.StringVar()
        self.castle = tk.StringVar()
        self.area = tk.StringVar()
        self.population = tk.StringVar()
        self.p_density = tk.StringVar()
        self.stress = tk.StringVar()
        self.hate = tk.StringVar()
        self.civil_point = tk.StringVar()
        self.civilization = tk.StringVar()
        self.victory = tk.StringVar()
        self.defeat = tk.StringVar()
        self.strength = tk.StringVar()
        self.assets = tk.StringVar()
        self.GDP = tk.StringVar()
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
        dbaccess().SELECT_All(MST_fieldS)
    
    # field_nameをセット
    def set_field_name(self):
        field_name = [""]
        # fieldデータ取得
        fields = self.select_field()
        for data in fields:
            field_name.append(data)
        
        return field_name