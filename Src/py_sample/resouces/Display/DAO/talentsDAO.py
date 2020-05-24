import tkinter as tk
from DbAccess import *
from DTO.talents import *
from settings import *

class TalentDAO():
    def __init__(self):
        self.talent_name = [""] 
        self.talent_list = {}
        self.talent_cbo = []
        self.talents = None
    
    def execute(self, sql):
        return dbaccess().exe_sql(sql)

    # select文を作成
    def select_talent(self):
        return dbaccess().SELECT_Column(MST_TALENTS, ['*', ' concat(t_rank, ":", talent_name) as talent_cbo'])
    
    # talent_nameをセット
    def set_talent(self):
        self.talents = self.select_talent()
        for talent in self.talents:
            # コンボボックスのリストに追加
            # self.talent_list[talent['talent_id']] = talent['t_rank'] + ':' + talent['talent_name']
            self.talent_cbo.append(talent['talent_cbo'])
        # talentデータ
        return self.talent_cbo

    # TODO:レベル比例で取得可能ランク変動
    def pickup_talent(self, talent_cbo):
        s_talent = [talent for talent in self.talents if talent['talent_cbo'] == talent_cbo]
        return s_talent[0]

    # def select
