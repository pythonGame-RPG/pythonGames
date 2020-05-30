import tkinter as tk
from datetime import *
from DbAccess import *
from settings import *

class Gene:
    def __init__(self):
        self.gene_name = tk.StringVar()
        self.is_gene_name = tk.IntVar()
        self.personal_code = tk.StringVar()
        self.s_HP = tk.StringVar()
        self.s_MP = tk.StringVar()
        self.s_sta = tk.StringVar()
        self.s_atk = tk.StringVar()
        self.s_vit = tk.StringVar()
        self.s_mag = tk.StringVar()
        self.s_des = tk.StringVar()
        self.s_agi = tk.StringVar()
        self.total_sense = tk.StringVar()
        self.g_rank = tk.StringVar()
        self.ins_date = str("{0:%Y/%m/%d}".format(datetime.now()))
        self.ins_id = tk.StringVar()
        self.upd_date = str("{0:%Y/%m/%d}".format(datetime.now()))
        self.upd_id = tk.StringVar()

    def init(self):
        self.gene_name.set("")
        self.is_gene_name.set(0)
        self.personal_code.set(1)
        self.s_HP.set(1)
        self.s_MP.set(1)
        self.s_sta.set(1)
        self.s_atk.set(1)
        self.s_vit.set(1)
        self.s_mag.set(1)
        self.s_des.set(1)
        self.s_agi.set(1)

    def insert_gene(self):
        dbaccess().insert(self, MST_GENES)

    def set_select_gene(self, s_gene):
        self.gene_name.set(s_gene['gene_name'])
        self.is_gene_name.set(s_gene['is_gene_name'])
        self.personal_code.set(s_gene['personal_code'])
        self.s_HP.set(s_gene['s_HP'])
        self.s_MP.set(s_gene['s_MP'])
        self.s_sta.set(s_gene['s_sta'])
        self.s_atk.set(s_gene['s_atk'])
        self.s_vit.set(s_gene['s_vit'])
        self.s_mag.set(s_gene['s_mag'])
        self.s_des.set(s_gene['s_des'])
        self.s_agi.set(s_gene['s_agi'])


    



