import tkinter as tk
from datetime import *


class Character:
    def __init__(self):
        self.name = tk.StringVar()
        self.sex = tk.StringVar()
        self.gene_id = tk.StringVar()
        self.race_id = tk.StringVar()      
        self.location_id = tk.StringVar()
        self.age = tk.IntVar()
        self.birth = tk.StringVar()
        self.birthplace = tk.StringVar()
        self.title = tk.StringVar()
        self.class1 = tk.StringVar()
        self.class2 = tk.StringVar()
        self.class3 = tk.StringVar()
        self.ep = tk.IntVar()
        self.level = tk.StringVar()
        self.guild_rank = tk.StringVar()
        self.state = tk.IntVar()  # 編集なし
        self.charisma = tk.StringVar()
        self.karma = tk.StringVar()
        self.fortune = tk.StringVar()
        self.intelligence = tk.StringVar()
        self.HP = tk.IntVar()
        self.MP = tk.IntVar()
        self.sta = tk.IntVar()
        self.atk = tk.IntVar()
        self.bit = tk.IntVar()
        self.mag = tk.IntVar()
        self.des = tk.IntVar()
        self.agi = tk.IntVar()
        self.talent1 = tk.StringVar()
        self.talent2 = tk.StringVar()
        self.talent3 = tk.StringVar()
        self.is_leader = tk.IntVar()
        self.party1 = tk.IntVar()
        self.party2 = tk.IntVar()
        self.party3 = tk.IntVar()
        self.is_dangeon = tk.IntVar()
        self.is_master = tk.IntVar()
        self.is_user = tk.IntVar()
        self.is_retire = tk.IntVar()
        self.dangeon_id = tk.IntVar()
        self.master_id = tk.IntVar()
        self.user_id = tk.StringVar()
        self.ins_date = datetime.now()
        self.ins_id = None
        self.upd_date = datetime.now()
        self.upd_id = None

        
    def init(self):
        
        self.sex.set(0)
        self.level.set(1)
        self.charisma.set(1)
        self.karma.set(1)
        self.fortune.set(1)
        self.intelligence.set(1)
        

    # def get_name
    # 入力文字数制限
    """
    def character_limit(self,entry_text, num):
        if len(str(entry_text.get())) > 0:
            entry_text.set(str(entry_text.get())[:num])
    """

