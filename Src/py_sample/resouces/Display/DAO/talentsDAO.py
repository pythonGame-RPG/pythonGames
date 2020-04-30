import tkinter as tk
from DbAccess import *
from DTO.talents import *
from settings import *

class TalentDAO():
    def __init__(self):
        self.talent_name = [""] 
        self.talent_list = {}
        self.talent_cbo = []
    
    def execute(self, sql):
        return dbaccess().exe_sql(sql)

    # select文を作成
    def select_talent(self):
        _comb = ('talent_id', 't_rank', 'talent_name')
        return dbaccess().SELECT_Column(MST_TALENTS,'talent_id', 'talent_name', 't_rank')
    
    # talent_nameをセット
    def set_talent(self):
        talents = self.select_talent()
        for talent in talents:
            # コンボボックスのリストに追加
            self.talent_list[talent['talent_id']] = talent['t_rank'] + ':' + talent['talent_name']
            # self.talent_cbo.append(talent['talent_name'])

        # talentデータ
        return self.talent_list

    # def select
