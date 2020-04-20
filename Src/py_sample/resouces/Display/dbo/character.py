import tkinter as tk

class Character:
    def __init__(self):
        self.name = tk.StringVar()
        self.gene_id = None
        self.race_id = None      
        self.age = None
        self.birth = tk.StringVar()
        self.title = tk.StringVar()
        self.class1 = tk.StringVar()
        self.class2 = tk.StringVar()
        self.class3 = tk.StringVar()
        self.level = tk.StringVar()
        self.guild_rank = tk.StringVar()
        self.state = tk.StringVar()
        self.HP = tk.StringVar()
        self.MP = tk.StringVar()
        self.sta = tk.StringVar()
        self.atk = tk.StringVar()
        self.bit = tk.StringVar()
        self.mag = tk.StringVar()
        self.des = tk.StringVar()
        self.agi = tk.StringVar()
        self.talent1 = tk.StringVar()
        self.talent2 = tk.StringVar()
        self.talent3 = tk.StringVar()
        self.dangeon_id = tk.StringVar()
        self.master_id = tk.StringVar()
        self.user_id = tk.StringVar()

        # 桁数制限
        self.guild_rank.trace("w", lambda *args: self.character_limit(self.guild_rank, 1))
        self.level.trace("w", lambda *args: self.character_limit(self.level, 3))
        self.HP.trace("w", lambda *args: self.character_limit(self.HP, 3))
        self.MP.trace("w", lambda *args: self.character_limit(self.MP, 3))
        self.sta.trace("w", lambda *args: self.character_limit(self.sta, 3))
        self.atk.trace("w", lambda *args: self.character_limit(self.atk, 3))
        self.bit.trace("w", lambda *args: self.character_limit(self.bit, 3))
        self.mag.trace("w", lambda *args: self.character_limit(self.mag, 3))
        self.des.trace("w", lambda *args: self.character_limit(self.des, 3))
        self.agi.trace("w", lambda *args: self.character_limit(self.agi, 3))

    # def get_name
    # 入力文字数制限
    def character_limit(self,entry_text, num):
        if len(entry_text.get()) > 0:
            entry_text.set(entry_text.get()[:num])
