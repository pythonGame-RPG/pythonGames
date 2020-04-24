import tkinter as tk

class Gene:
    def __init__(self):
        self.gene_id = tk.IntVar()  
        self.personal_code = tk.IntVar()  
        self.s_HP = tk.IntVar()
        self.s_MP = tk.IntVar()
        self.s_sta = tk.IntVar()
        self.s_atk = tk.IntVar()
        self.s_bit = tk.IntVar()
        self.s_mag = tk.IntVar()
        self.s_des = tk.IntVar()
        self.s_agi = tk.IntVar()
        self.total_sense = tk.IntVar()
        self.gene_rank = tk.StringVar()
        self.ins_date = None
        self.ins_id = None
        self.upd_date = None
        self.upd_id = None

        self.bk_num = 0
        self.bk_total_sense = 0


        

    # def get_name
    # 入力文字数制限
    """
    def character_limit(self,entry_text, num):
        if len(str(entry_text.get())) > 0:
            entry_text.set(str(entry_text.get())[:num])
            self.total_sense.set(str(self.s_HP.get()+self.s_MP.get()+self.s_sta.get()
            +self.s_atk.get()+self.s_bit.get()+self.s_mag.get()+self.s_HP.get()
            +self.s_des.get()+self.s_agi.get()))
    """


