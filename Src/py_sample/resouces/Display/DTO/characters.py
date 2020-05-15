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
        self.HP = tk.StringVar()
        self.MP = tk.StringVar()
        self.sta = tk.StringVar()
        self.atk = tk.StringVar()
        self.vit = tk.StringVar()
        self.mag = tk.StringVar()
        self.des = tk.StringVar()
        self.agi = tk.StringVar()
        self.total = tk.StringVar()
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
        
    def init(self, gene, race):
        
        self.sex.set(0)
        self.charisma.set(1)
        self.karma.set(1)
        self.fortune.set(1)
        self.intelligence.set(1)
        self.level.set(1)

        # self.set_status(gene,race)

    # gene値変更時
    def set_status(self, ch_text, gene_data, race_data):
        # ステータス設定
        ch_text.set(self.calculate_status(gene_data, race_data))
        # self.total.set(self.calculate_total(gene, race))
        # total&rank
        # self.agi.set(int(gene.s_agi.get()) * int(self.level.get()) + int(race.p_agi.get()))

    # LEVEL値変更時
    def set_status_all(self,gene, race):
        # ステータス設定
        self.HP.set(self.calculate_status(gene.s_HP.get(), race.p_HP.get()))
        self.MP.set(self.calculate_status(gene.s_MP.get(), race.p_MP.get()))
        self.sta.set(self.calculate_status(gene.s_sta.get(), race.p_sta.get()))
        self.atk.set(self.calculate_status(gene.s_atk.get(), race.p_atk.get()))
        self.vit.set(self.calculate_status(gene.s_vit.get(), race.p_vit.get()))
        self.mag.set(self.calculate_status(gene.s_mag.get(), race.p_mag.get()))
        self.des.set(self.calculate_status(gene.s_des.get(), race.p_des.get()))
        self.agi.set(self.calculate_status(gene.s_agi.get(), race.p_agi.get()))
        self.total.set(self.calculate_total(gene, race))
    
    def calculate_status(self, gene_data, race_data):
        status_data = None
        try:
            status_data = int(gene_data) * int(self.level.get()) + int(race_data)
        except:
            status_data = 1
        return status_data

    def calculate_total(self, gene, race):
        status_data = None
        try:
            status_data = str(int(gene.total_sense.get()) * int(self.level.get()) 
            + int(race.total_pattern.get()) + int(self.charisma.get()) 
            + int(self.karma.get()) + int(self.intelligence.get()) + int(self.fortune.get()))
        except:
            status_data = 20
        return status_data


