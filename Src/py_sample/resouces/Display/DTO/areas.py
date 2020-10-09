import tkinter as tk
from DbAccess import *
from settings import *
from datetime import *

class Area:
    def __init__(self):
        self.grid_x = 0
        self.grid_y = 0
        self.location_id = 0
        self.field_id = 0
        self.is_maxHeight = 0
        self.height = 0
        self.is_river = 0
        self.depth = 0
        self.landlord_gene_id = 0
        self.character_id = 0
        self.assets = 0
        self.civil_point = 0
        self.family = 0
        self.is_public = 0
        self.version = 0
        self.ins_date = datetime.now()
        self.ins_id = ''
        self.upd_date = datetime.now()
        self.upd_id = ''

        self.bk_num = 0
        self.bk_total_sense = 0

    def init(self):
        pass

    def insert_area(self):
        dbaccess().insert(self, )

    def select_area(self, where = None):
        dbaccess().SELECT_All(MST_AREAS)
    
    # area_nameをセット
    def set_area_name(self):
        area_name = [""]
        # areaデータ取得
        areas = self.select_area()
        for data in areas:
            area_name.append(data)
        
        return area_namer