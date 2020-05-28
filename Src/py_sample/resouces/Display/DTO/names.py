import tkinter as tk
from datetime import *
from DbAccess import *
from settings import *

class Name:
    def __init__(self):
        self.name = None
        self.users_num = 1
        self.trend = 0
        self.is_deleted = 0
        self.version = 0
        self.ins_date = datetime.now()
        self.ins_id = None
        self.upd_date = datetime.now()
        self.upd_id = None
        self.ins_name ={}

    def init(self):
        pass

    def select_name(self, where = None):
        dbaccess().SELECT_All(MST_RACES)

    # nameをセット
    def set_name(self):
        name = [""]
        # nameデータ取得
        names = self.select_name()
        for data in names:
            name.append(data)
        
        return name

    def set_select_name(self, s_name):
        self.name.set(s_name['name'])
        self.p_HP.set(s_name['p_HP'])
        self.p_MP.set(s_name['p_MP'])
        self.p_sta.set(s_name['p_sta'])
        self.p_atk.set(s_name['p_atk'])
        self.p_vit.set(s_name['p_vit'])
        self.p_mag.set(s_name['p_mag'])
        self.p_des.set(s_name['p_des'])
        self.p_agi.set(s_name['p_agi'])
        self.total_pattern.set(s_name['total_pattern'])
