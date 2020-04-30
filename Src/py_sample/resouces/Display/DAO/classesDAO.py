import tkinter as tk
from DbAccess import *
from DTO.classes import *
from settings import *

class ClassDAO():
    def __init__(self):
        self.class_name = [""] 
        self.class_list = {}
        self.class_cbo = []
    
    def execute(self, sql):
        return dbaccess().exe_sql(sql)

    # select文を作成
    def select_class(self):
        _comb = ('class_id', 'c_rank', 'class_name')
        return dbaccess().SELECT_Column(MST_CLASSES,'class_id', 'class_name', 'c_rank')
    
    # class_nameをセット
    def set_class(self):
        classes = self.select_class()
        for _class in classes:
            # コンボボックスのリストに追加
            self.class_list[_class['class_id']] = _class['c_rank'] + ':' + _class['class_name']
            # self.class_cbo.append(class['class_name'])

        # classデータ
        return self.class_list

    # def select
