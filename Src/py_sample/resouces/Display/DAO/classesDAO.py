import tkinter as tk
from DbAccess import *
from DTO.classes import *
from settings import *

class ClassDAO():
    def __init__(self):
        self.class_list = {}
        self.class_cbo = []
        self.classes = None
    
    def execute(self, sql):
        return dbaccess().exe_sql(sql)

    # select文を作成
    def select_class(self):
        return dbaccess().SELECT_Column(MST_CLASSES, ['*', ' concat(c_rank, ":", class_name) as class_cbo'])
    
    # class_nameをセット
    def set_class(self):
        self.classs = self.select_class()
        for _class in self.classs:
            # コンボボックスのリストに追加
            # self.class_list[_class['class_id']] = _class['c_rank'] + ':' + _class['class_name']
            self.class_cbo.append(_class['class_cbo'])

        # classデータ
        return self.class_cbo

    # TODO:レベル比例で取得可能ランク変動
    def pickup_class(self, class_cbo):
        s_class = [_class for _class in self.classes if _class['class_cbo'] == class_cbo]
        return s_class[0]
