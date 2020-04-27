import tkinter as tk


class Character:
    def __init__(self):
        self.name = tk.StringVar()
        self.sex = tk.IntVar()
        self.gene_id = tk.IntVar()
        self.race_id = tk.IntVar()      
        self.location_id = tk.IntVar()
        self.age = tk.IntVar()
        self.birth = tk.StringVar()
        self.birthplace = tk.StringVar()
        self.title = tk.StringVar()
        self.class1 = tk.StringVar()
        self.class2 = tk.StringVar()
        self.class3 = tk.StringVar()
        self.ep = tk.IntVar()
        self.level = tk.IntVar()
        self.guild_rank = tk.StringVar()
        self.state = tk.IntVar()  # 編集なし
        self.charisma = tk.IntVar()
        self.karma = tk.IntVar()
        self.fortune = tk.IntVar()
        self.intelligence = tk.IntVar()
        self.HP = tk.IntVar()
        self.MP = tk.IntVar()
        self.sta = tk.IntVar()
        self.atk = tk.IntVar()
        self.bit = tk.IntVar()
        self.mag = tk.IntVar()
        self.des = tk.IntVar()
        self.agi = tk.IntVar()
        self.talent1 = tk.IntVar()
        self.talent2 = tk.IntVar()
        self.talent3 = tk.IntVar()
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
        self.ins_date = None
        self.ins_id = None
        self.upd_date = None
        self.upd_id = None

        
    def init(self):
        
        self.level = tk.IntVar()
        self.charisma = tk.IntVar()
        self.karma = tk.IntVar()
        self.fortune = tk.IntVar()
        self.intelligence = tk.IntVar()
        

    # def get_name
    # 入力文字数制限
    """
    def character_limit(self,entry_text, num):
        if len(str(entry_text.get())) > 0:
            entry_text.set(str(entry_text.get())[:num])
    """

