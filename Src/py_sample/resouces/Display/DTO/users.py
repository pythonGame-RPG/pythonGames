import tkinter as tk
from DbAccess import *
from settings import *
from datetime import *

class User:
    def __init__(self):
        self.user_id = tk.StringVar()
        self.password = tk.StringVar()
        self.name = tk.StringVar()
        self.is_admin = tk.StringVar()
        self.is_sec = tk.StringVar()
        self.is_save = tk.StringVar()
        self.play_time = tk.StringVar()
        self.total_amount = tk.StringVar()
        self.money = tk.StringVar()
        self.cost = tk.StringVar()
        self.version = tk.StringVar()
        self.is_deleted = tk.StringVar()
        self.ins_date = datetime.now()
        self.ins_id = None
        self.upd_date = datetime.now()
        self.upd_id = None

    def init(self):
        self.is_admin.set('0')
        self.is_sec.set('0')
        self.is_save.set('0')
        self.play_time.set('0')
        self.total_amount.set('0')
        self.money.set('0')
        self.cost.set('0')
        self.version.set('0')
        self.is_deleted.set('0')
        self.ins_date = datetime.now()
        self.ins_id = None
        self.upd_date = datetime.now()
        self.upd_id = None

    def select_user(self, where = None):
        dbaccess().SELECT_All(MST_USERS)
    
    # user_nameをセット
    def set_user_name(self):
        user_name = [""]
        # userデータ取得
        users = self.select_user()
        for data in users:
            user_name.append(data)
        
        return user_name