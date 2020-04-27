import tkinter as tk
from DbAccess import *
from settings import *

class Gene:
    def __init__(self):
        self.gene_name = tk.StringVar()
        self.is_gene_name = tk.IntVar()
        self.personal_code = tk.IntVar()
        self.s_HP = tk.IntVar()
        self.s_MP = tk.IntVar()
        self.s_sta = tk.IntVar()
        self.s_atk = tk.IntVar()
        self.s_bit = tk.IntVar()
        self.s_mag = tk.IntVar()
        self.s_des = tk.IntVar()
        self.s_agi = tk.IntVar()
        self.total_sense = tk.IntVar()
        self.gene_rank = tk.StringVar()
        self.ins_date = None
        self.ins_id = None
        self.upd_date = None
        self.upd_id = None

        self.bk_num = 0
        self.bk_total_sense = 0

    def init(self):
        self.personal_code.set(1)
        self.s_HP.set(1)
        self.s_MP.set(1)
        self.s_sta.set(1)
        self.s_atk.set(1)
        self.s_bit.set(1)
        self.s_mag.set(1)
        self.s_des.set(1)
        self.s_agi.set(1)

    def insert_gene(self):
        dbaccess().insert(self, MST_GENES)

    



