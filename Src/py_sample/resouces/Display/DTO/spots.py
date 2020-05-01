import tkinter as tk
from DbAccess import *
from settings import *

class Spot:
    def __init__(self):
        self.grid_x = tk.IntVar()
        self.grid_y = tk.IntVar()
        self.sgrid_x = tk.IntVar()
        self.sgrid_y = tk.IntVar()
        self.lord_gene_id = tk.IntVar()
        self.character_id = tk.IntVar()
        self.place_name = tk.IntVar()
        self.assets = tk.IntVar()
        self.civilization = tk.IntVar()
        self.population = tk.IntVar()

        self.bk_num = 0
        self.bk_total_sense = 0

    def init(self):
        pass

    def insert_spot(self):
        dbaccess().insert(self, )

    def select_spot(self, where = None):
        dbaccess().SELECT_All(MST_spotS)
    
    # spot_nameをセット
    def set_spot_name(self):
        spot_name = [""]
        # spotデータ取得
        spots = self.select_spot()
        for data in spots:
            spot_name.append(data)
        
        return spot_name