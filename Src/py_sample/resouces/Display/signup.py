from settings import *
from Sql import *
from validate import *
import random
import DTO.characters as chara
import DTO.genes as genes
import DTO.races as races
import DTO.classes as classes
import DTO.talents as talents
import DTO.locations as locations
# from DAO import * いつかはこっちのほうがいいかも
import DAO.charactersDAO as _chara
import DAO.genesDAO as _genes
import DAO.racesDAO as _races
import DAO.classesDAO as _classes
import DAO.talentsDAO as _talents
import DAO.fieldsDAO as _fields
import DAO.locationsDAO as _locations
import mycalendar as cal
import tkinter as tk
from tkinter import ttk
from turtle import *
from datetime import *

# Login classes(GUIで実装)
class Signup(tk.Tk):
    def __init__(self, user_id = None):
        self.root = tk.Tk.__init__(self)
        #　子画面
        self.sub_root = cal.mycalendar(self)

        self.geometry('500x500')
        self.title('make character')
        self.chk_dangeonchar = tk.IntVar()

        # 選択したコンボボックスの値を格納
        self.selected_date = tk.StringVar()
        self.cbo_gene_list = tk.StringVar()
        self.cbo_race_list = tk.StringVar()
        self.cbo_location_list = tk.StringVar()

        self.ch = chara.Character()
        self.ge = genes.Gene()
        self.ra = races.Race()
        self.cl = classes.Class()
        self.ta = talents.Talent()
        self.lo = locations.Location()
        self.ch_dao = _chara.CharacterDAO()
        self.ge_dao = _genes.GeneDAO()
        self.ra_dao = _races.RaceDAO()
        self.cl_dao = _classes.ClassDAO()
        self.ta_dao = _talents.TalentDAO()
        self.fi_dao = _fields.FieldDAO()
        self.lo_dao = _locations.LocationDAO()

        # 表示ラベル編集用
        self.HP = tk.StringVar()
        self.MP = tk.StringVar()
        self.sta = tk.StringVar()
        self.atk = tk.StringVar()
        self.vit = tk.StringVar()
        self.mag = tk.StringVar()
        self.des = tk.StringVar()
        self.agi = tk.StringVar()
        self.t_sense = tk.StringVar()
        self.s_total = tk.StringVar()

        self.HP_label = {'HP':self.HP}
        self.MP_label = {'MP':self.MP}
        self.sta_label = {'sta':self.sta}
        self.atk_label = {'atk':self.atk}
        self.vit_label = {'vit':self.vit}
        self.mag_label = {'mag':self.mag}
        self.des_label = {'des':self.des}
        self.agi_label = {'agi':self.agi}
        self.total_sense_label = {'total_sense':self.t_sense}
        self.total_label = {'total':self.s_total}

        # システム日付
        self.tdatetime = datetime.now()

        # 日付チェック
        self.selected_date.trace("w", lambda *args: self.date_limit(self.selected_date))

        # chara桁数制限
        # self.ch.guild_rank.trace("w", lambda *args: self.character_limit(self.ch.guild_rank, 1))
        self.ch.level.trace("w", lambda *args: self.level_limit(self.ch.level, 3))
        self.ch.charisma.trace("w", lambda *args: self.character_limit(self.ch.charisma, 4))
        self.ch.karma.trace("w", lambda *args: self.character_limit(self.ch.karma, 4))
        self.ch.fortune.trace("w", lambda *args: self.character_limit(self.ch.fortune, 4))
        self.ch.intelligence.trace("w", lambda *args: self.character_limit(self.ch.intelligence, 4))
        self.cbo_gene_list.trace("w", lambda *args: self.select_gene(self.cbo_gene_list))
        self.cbo_race_list.trace("w", lambda *args: self.select_race(self.cbo_race_list))
        # gene桁数制限
        self.ge.s_HP.trace("w", lambda *args: self.character_limit(self.ge.s_HP, 3, self.ch.HP, self.ra.p_HP))
        self.ge.s_MP.trace("w", lambda *args: self.character_limit(self.ge.s_MP, 3, self.ch.MP, self.ra.p_MP))
        self.ge.s_sta.trace("w", lambda *args: self.character_limit(self.ge.s_sta, 3, self.ch.sta, self.ra.p_sta))
        self.ge.s_atk.trace("w", lambda *args: self.character_limit(self.ge.s_atk, 3, self.ch.atk, self.ra.p_atk))
        self.ge.s_vit.trace("w", lambda *args: self.character_limit(self.ge.s_vit, 3, self.ch.vit, self.ra.p_vit))
        self.ge.s_mag.trace("w", lambda *args: self.character_limit(self.ge.s_mag, 3, self.ch.mag, self.ra.p_mag))
        self.ge.s_des.trace("w", lambda *args: self.character_limit(self.ge.s_des, 3, self.ch.des, self.ra.p_des))
        self.ge.s_agi.trace("w", lambda *args: self.character_limit(self.ge.s_agi, 3, self.ch.agi, self.ra.p_agi))
        
        # characterステータス設定
        self.ch.HP.trace("w", lambda *args: self.ch_status_set(self.HP_label,self.ch.HP.get()))
        self.ch.MP.trace("w", lambda *args: self.ch_status_set(self.MP_label,self.ch.MP.get()))
        self.ch.sta.trace("w", lambda *args: self.ch_status_set(self.sta_label,self.ch.sta.get()))
        self.ch.atk.trace("w", lambda *args: self.ch_status_set(self.atk_label,self.ch.atk.get()))
        self.ch.vit.trace("w", lambda *args: self.ch_status_set(self.vit_label,self.ch.vit.get()))
        self.ch.mag.trace("w", lambda *args: self.ch_status_set(self.mag_label,self.ch.mag.get()))
        self.ch.des.trace("w", lambda *args: self.ch_status_set(self.des_label,self.ch.des.get()))
        self.ch.agi.trace("w", lambda *args: self.ch_status_set(self.agi_label,self.ch.agi.get()))
        self.ch.total.trace("w", lambda *args: self.ch_status_set(self.total_label,self.ch.total.get()))
        self.ge.total_sense.trace("w", lambda *args: self.set_g_rank(self.total_sense_label,self.ge.total_sense.get()))

        # 合計
        self.ge.total_sense.trace("w", lambda *args: self.character_limit(self.ch.total, 4))

        # リスト取得
        self.class_list = self.cl_dao.set_class()
        self.talent_list = self.ta_dao.set_talent()

        # ウィンドウを分ける
        pw_main = tk.PanedWindow(self.root, orient='horizontal')
        pw_main.pack(expand=True, fill = tk.BOTH, side="left")

        # self.root→pw_left（左画面を扱う）
        pw_left = tk.PanedWindow(pw_main, bg="cyan", orient='vertical')
        pw_main.add(pw_left)
        pw_right = tk.PanedWindow(pw_main, bg="yellow", orient='vertical')
        pw_main.add(pw_right)

        # 基本情報フレーム１
        fm_left_1 = tk.Frame(pw_left, bd=2, relief="ridge")
        pw_left.add(fm_left_1)
        
        # group1_label
        self.lbl0 = tk.Label(fm_left_1,text = '基本データ')
        self.lbl0.grid(row=1, column=0,columnspan=5, padx=5, pady=2)
        # name
        self.lbl1 = tk.Label(fm_left_1,text = 'name')
        self.lbl1.grid(row=2, column=0, padx=5, pady=2)
        self.ent1 = tk.Entry(fm_left_1,textvariable=self.ch.name,width=10)
        self.ent1.grid(row=2, column=1, padx=5, pady=2)
        # sex
        self.lblsex = tk.Label(fm_left_1,text = 'sex')
        self.lblsex.grid(row=3, column=2, padx=5, pady=2)
        self.rdo1 = tk.Radiobutton(fm_left_1, value=0, variable=self.ch.sex, text='male')
        self.rdo1.grid(row=3, column=3, padx=5, pady=2)
        self.rdo2 = tk.Radiobutton(fm_left_1, value=1, variable=self.ch.sex, text='female')
        self.rdo2.grid(row=3, column=4, padx=5, pady=2)
        # location
        self.lblo = tk.Label(fm_left_1,text = 'location')
        self.lblo.grid(row=4, column=2, padx=5, pady=2)
        self.cboo = ttk.Combobox(fm_left_1, textvariable=self.cbo_location_list,width=18)
        self.cboo['values']=self.lo_dao.set_location()
        self.cboo.current(0)
        self.cboo.grid(row=4, column=3, columnspan=2, padx=5, pady=2)

        # dangeon_chara
        self.chk13 = tk.Checkbutton(fm_left_1, variable=int, var=self.chk_dangeonchar, text='dangeon_chara')
        self.chk13.grid(row=2, column=2,columnspan=2, padx=5, pady=2)
        # gene
        self.lbl2 = tk.Label(fm_left_1,text = 'gene')
        self.lbl2.grid(row=3, column=0, padx=5, pady=2)
        self.cbo2 = ttk.Combobox(fm_left_1, textvariable=self.cbo_gene_list,width=10)
        self.cbo2['values']=self.ge_dao.set_gene()
        self.cbo2.grid(row=3, column=1, padx=5, pady=2)
        # race
        self.lbl3 = tk.Label(fm_left_1,text = 'race')
        self.lbl3.grid(row=4, column=0, padx=5, pady=2)
        self.cbo3 = ttk.Combobox(fm_left_1, textvariable=self.cbo_race_list,width=10)
        self.cbo3['values']=self.ra_dao.set_race()
        self.cbo3.current(0)
        self.cbo3.grid(row=4, column=1, padx=5, pady=2)
        
        # birth
        self.lbl4 = tk.Label(fm_left_1,text = 'birth')
        self.lbl4.grid(row=5, column=2, padx=5, pady=2)
        self.ent4 = tk.Entry(fm_left_1, textvariable=self.ch.birth,width=10)
        self.ent4.grid(row=5, column=3, padx=5, pady=2)
        # birthをDTOにセット
        # self.ch.birth.set(self.ent4.get())

        # 日付選択アイコン
        self.i_birth = tk.Button(fm_left_1, text = "日付選択", font = ("",8),command=self.sub_root.openDialog)
        self.i_birth.grid(row=5, column=4, padx=5, pady=2)

        # birthplace
        self.lbl5a = tk.Label(fm_left_1,text = 'birthplace')
        self.lbl5a.grid(row=5, column=0, padx=5, pady=2)
        self.cbo5a = ttk.Combobox(fm_left_1, textvariable=self.ch.birthplace,width=10)
        self.cbo5a['values']=self.fi_dao.set_field()
        self.cbo5a.current(0)
        self.cbo5a.grid(row=5, column=1, padx=5, pady=2)

        # ステータスフレーム
        fm_status = tk.Frame(pw_left, bd=2, relief="ridge")

        pw_left.add(fm_status)
        # group2_label
        self.lbl0 = tk.Label(fm_status,text = 'ステータス')
        self.lbl0.grid(row=0, column=0,columnspan=6, padx=5, pady=2)
        # GUILD
        self.lbl5 = tk.Label(fm_status,text = 'GUILD')
        self.lbl5.grid(row=1, column=0, padx=5, pady=2)
        self.cbo2 = ttk.Combobox(fm_status, textvariable=self.ch.guild_rank,width=3)
        self.cbo2['values']=('G', 'F', 'E', 'D', 'C', 'B', 'A', 'S', 'SS', 'SSS')
        self.cbo2.set("G")
        self.cbo2.grid(row=1, column=1, padx=5, pady=2)
        # LEVEL
        self.lbl6 = tk.Label(fm_status,text = 'level')
        self.lbl6.grid(row=1, column=2, padx=5, pady=2)
        self.ent6 = tk.Entry(fm_status, textvariable=self.ch.level, width=4)
        self.ent6.grid(row=1, column=3, padx=5, pady=2)
        # is_gene_name
        self.chkgn = tk.Checkbutton(fm_status, variable=int, var=self.ge.is_gene_name, text='g_name')
        self.chkgn.grid(row=1, column=4, padx=5, pady=2)
        # gene_name
        self.entgn = tk.Entry(fm_status, textvariable=self.ge.gene_name, width=7)
        self.entgn.grid(row=1, column=5, padx=5, pady=2)
        # HP
        self.lbl7 = tk.Label(fm_status,textvariable=self.HP,width=9)
        self.lbl7.grid(row=2, column=0, padx=5, pady=2)
        self.ent7 = tk.Entry(fm_status, textvariable=self.ge.s_HP, width=4)
        self.ent7.grid(row=2, column=1, padx=5, pady=2)
        # MP
        self.lbl8 = tk.Label(fm_status,textvariable=self.MP,width=9)
        self.lbl8.grid(row=2, column=2, padx=5, pady=2)
        self.ent8 = tk.Entry(fm_status, textvariable=self.ge.s_MP, width=4)
        self.ent8.grid(row=2, column=3, padx=5, pady=2)
        # charisma
        self.lblcha = tk.Label(fm_status,text = 'charisma')
        self.lblcha.grid(row=2, column=4, padx=5, pady=2)
        self.entcha = tk.Entry(fm_status, textvariable=self.ch.charisma, width=7)
        self.entcha.grid(row=2, column=5, padx=5, pady=2)
        # sta
        self.lbl9 = tk.Label(fm_status,textvariable=self.sta,width=9)
        self.lbl9.grid(row=3, column=0, padx=5, pady=2)
        self.ent9 = tk.Entry(fm_status, textvariable=self.ge.s_sta, width=4)
        self.ent9.grid(row=3, column=1, padx=5, pady=2)
        # atk
        self.lbl10 = tk.Label(fm_status,textvariable=self.atk,width=9)
        self.lbl10.grid(row=3, column=2, padx=5, pady=2)
        self.ent10 = tk.Entry(fm_status, textvariable=self.ge.s_atk, width=4)
        self.ent10.grid(row=3, column=3, padx=5, pady=2)
        # karma
        self.lblka = tk.Label(fm_status,text = 'karma')
        self.lblka.grid(row=3, column=4, padx=5, pady=2)
        self.entka = tk.Entry(fm_status, textvariable=self.ch.karma, width=7)
        self.entka.grid(row=3, column=5, padx=5, pady=2)
        # vit
        self.lbl11 = tk.Label(fm_status,textvariable=self.vit,width=9)
        self.lbl11.grid(row=4, column=0, padx=5, pady=2)
        self.ent11 = tk.Entry(fm_status, textvariable=self.ge.s_vit, width=4)
        self.ent11.grid(row=4, column=1, padx=5, pady=2)
        # mag
        self.lbl12 = tk.Label(fm_status,textvariable=self.mag,width=9)
        self.lbl12.grid(row=4, column=2, padx=5, pady=2)
        self.ent12 = tk.Entry(fm_status, textvariable=self.ge.s_mag, width=4)
        self.ent12.grid(row=4, column=3, padx=5, pady=2)
        # fortune
        self.lblcha = tk.Label(fm_status,text = 'fortune')
        self.lblcha.grid(row=4, column=4, padx=5, pady=2)
        self.entcha = tk.Entry(fm_status, textvariable=self.ch.fortune, width=7)
        self.entcha.grid(row=4, column=5, padx=5, pady=2)
        # des
        self.lbl13 = tk.Label(fm_status,textvariable=self.des,width=9)
        self.lbl13.grid(row=5, column=0, padx=5, pady=2)
        self.ent13 = tk.Entry(fm_status, textvariable=self.ge.s_des, width=4)
        self.ent13.grid(row=5, column=1, padx=5, pady=2)
        # agi
        self.lbl14 = tk.Label(fm_status,textvariable=self.agi,width=9)
        self.lbl14.grid(row=5, column=2, padx=5, pady=2)
        self.ent14 = tk.Entry(fm_status, textvariable=self.ge.s_agi, width=4)
        self.ent14.grid(row=5, column=3, padx=5, pady=2)
        # intelligence
        self.lblcha = tk.Label(fm_status,text = 'intelligence')
        self.lblcha.grid(row=5, column=4, padx=5, pady=2)
        self.entcha = tk.Entry(fm_status, textvariable=self.ch.intelligence, width=7)
        self.entcha.grid(row=5, column=5, padx=5, pady=2)
        # total_sense
        self.lbl15 = tk.Label(fm_status,textvariable=self.t_sense)
        self.lbl15.grid(row=6, column=2, padx=5, pady=2)
        self.ent15 = tk.Entry(fm_status, textvariable=self.ge.total_sense, width=4)
        self.ent15.grid(row=6, column=3, padx=5, pady=2)
        self.ent15.configure(state = 'readonly')
        # total
        self.lbl16 = tk.Label(fm_status,textvariable=self.s_total,width=9)
        self.lbl16.grid(row=6, column=4, padx=5, pady=2)
        self.ent16 = tk.Entry(fm_status, textvariable=self.ch.total,  width=7)
        self.ent16.grid(row=6, column=5, padx=5, pady=2)
        self.ent16.configure(state = 'readonly')
        # intelligence
        self.lblcha = tk.Label(fm_status,text = 'intelligence')
        self.lblcha.grid(row=5, column=4, padx=5, pady=2)
        self.entcha = tk.Entry(fm_status, textvariable=self.ch.intelligence, width=7)
        self.entcha.grid(row=5, column=5, padx=5, pady=2)
        
        # 特殊フレーム
        fm_specify = tk.Frame(pw_left, bd=2, relief="ridge")
        pw_left.add(fm_specify)
        # group3_label
        self.lbl_s = tk.Label(fm_specify,text = '特技')
        self.lbl_s.grid(row=0, column=0,columnspan=4, padx=5, pady=2)
        # Class1
        self.lbl13 = tk.Label(fm_specify,text = 'class' )
        self.lbl13.grid(row=1, column=0, padx=5, pady=2)
        self.cbo13 = ttk.Combobox(fm_specify, textvariable=self.ch.class1 ,width=12)
        self.cbo13['values']=self.class_list
        try:
            self.cbo13.current(0)
        except:
            pass
        self.cbo13.grid(row=1, column=1, padx=5, pady=2)
        # Class2
        self.cbo14 = ttk.Combobox(fm_specify, textvariable=self.ch.class2 ,width=12)
        self.cbo14['values']=self.class_list
        self.cbo14.grid(row=1, column=2, padx=5, pady=2)
        # Class3
        self.cbo15 = ttk.Combobox(fm_specify, textvariable=self.ch.class3 ,width=12)
        self.cbo15['values']=self.class_list
        self.cbo15.grid(row=1, column=3, padx=5, pady=2)
        # talent1
        self.lbl16 = tk.Label(fm_specify,text = 'talent')
        self.lbl16.grid(row=2, column=0, padx=5, pady=2)
        self.cbo16 = ttk.Combobox(fm_specify, textvariable=self.ch.talent1 ,width=12)
        self.cbo16['values']=self.talent_list
        try:
            self.cbo16.current(0)
        except:
            pass
        self.cbo16.grid(row=2, column=1, padx=5, pady=2)
        # talent2
        self.cbo17 = ttk.Combobox(fm_specify, textvariable=self.ch.talent2 ,width=12)
        self.cbo17['values']=self.talent_list
        self.cbo17.grid(row=2, column=2, padx=5, pady=2)
        # talent3
        self.cbo18 = ttk.Combobox(fm_specify, textvariable=self.ch.talent3 ,width=12)
        self.cbo18['values']=self.talent_list
        self.cbo18.grid(row=2, column=3, padx=5, pady=2)

        # 特殊フレーム
        fm_flg = tk.Frame(pw_left, bd=2, relief="ridge")
        pw_left.add(fm_flg)
        # group4_label
        self.lbl_f = tk.Label(fm_flg,text = 'フラグ')
        self.lbl_f.grid(row=0, column=1,columnspan=2, padx=5, pady=2)
        # dangeon
        self.chk13 = tk.Checkbutton(fm_flg, variable=int, var=self.ch.is_dangeon, text='is_dangeon')
        self.chk13.grid(row=1, column=0, padx=5, pady=2)
        # master
        self.chk14 = tk.Checkbutton(fm_flg, variable=int, var=self.ch.is_master, text='is_master')
        self.chk14.grid(row=1, column=1, padx=5, pady=2)
        # user
        self.chk15 = tk.Checkbutton(fm_flg, variable=int, var=self.ch.is_user, text='is_user')
        self.chk15.grid(row=1, column=2, padx=5, pady=2)
        # retire
        self.chk16 = tk.Checkbutton(fm_flg, variable=int, var=self.ch.is_retire, text='is_retire')
        self.chk16.grid(row=1, column=3, padx=5, pady=2)

        

        # ランダムボタン
        self.btn1 = tk.Button(fm_flg, text='ランダム生成', command=self.random_generate)
        self.btn1.grid(row=7, column=0, padx=5, pady=2)

        # 登録ボタン
        self.btn2 = tk.Button(fm_flg, text='登録', command=self.submit)
        self.btn2.grid(row=7, column=1, padx=5, pady=2)

        # 連続登録ボタン
        self.btn3 = tk.Button(fm_flg, text='連続登録', command=self.continuous_submit)
        self.btn3.grid(row=7, column=2, padx=5, pady=2)

        # テキスト初期化
        self.ge.init()
        self.ra.init()
        self.ch.init(self.ge, self.ra)

        self.running = True
        self.user_id = None
        self.passwd = None
        self.error = {}
        # 半角英数字エラー
        self.error['digit'] = {}
        # 文字列の長さエラー
        self.error['length'] = {}
        # 辞書型データ('user_id':XXXX, 'password':XXXX)
        self.data = {}
        # エラー出力用
        self.error_output = {}
        self.users = None
        # 入力ロック判定用
        self.v_err = 0
        # self.after(10,self)

    def random_generate(self):
        weight = 8
        self.ch.birth.set(self.rand_date())
        self.ge.s_HP.set(self.rand_num(3,weight))
        self.ge.s_MP.set(self.rand_num(3,weight))
        self.ge.s_sta.set(self.rand_num(3,weight))
        self.ge.s_atk.set(self.rand_num(3,weight))
        self.ge.s_vit.set(self.rand_num(3,weight))
        self.ge.s_mag.set(self.rand_num(3,weight))
        self.ge.s_des.set(self.rand_num(3,weight))
        self.ge.s_agi.set(self.rand_num(3,weight))
        self.ch.charisma.set(self.rand_num(4,weight))
        self.ch.karma.set(self.rand_num(4,weight))
        self.ch.fortune.set(self.rand_num(4,weight))
        self.ch.intelligence.set(self.rand_num(4,weight))
        self.ch.set_status_all(self.ge, self.ra)

        self.set_g_rank()

    def set_g_rank(self,text_label,data):

        if int(data) > 700:
            self.ge.g_rank.set('SSS')
        elif int(data)  > 600:
            self.ge.g_rank.set('SS')
        elif int(data)  > 500:
            self.ge.g_rank.set('S')
        elif int(data)  > 400:
            self.ge.g_rank.set('A')
        elif int(data)  > 300:
            self.ge.g_rank.set('B')
        elif int(data)  > 200:
            self.ge.g_rank.set('C')
        elif int(data)  > 100:
            self.ge.g_rank.set('D')
        elif int(data)  > 50:
            self.ge.g_rank.set('E')
        else:
            self.ge.g_rank.set('F')

        self.ch_status_set(text_label,self.ge.g_rank.get())

             
    def rand_num(self, num, weight):
        import numpy as np
        import matplotlib.pyplot as plt

        # weight=3:強者が出やすくなる
        a = np.arange(0,weight,0.1)
        exp_a = np.exp(a)
        sum_exp_a = np.sum(exp_a)
        y = exp_a / sum_exp_a
        rn_int = int(random.choice(y)*10**num)
        if rn_int > 10**(num-1):
            rn_int = 10**(num-1)
        if rn_int == 0:
            rn_int = random.randint(1,10**(num-2))
        # plt.plot(a,y)
        # plt.show()
        # rad_int = random.randint(1,10**(num-1))

        return rn_int

    def rand_date(self):
        rand_d = None
        import calendar
        cal = calendar.Calendar()
        year = random.randint(1950,date.today().year)
        month = self.convert_in2_2bytes(str(random.randint(1,12)))
        # 指定した年月のカレンダーをリストで返す
        days = cal.itermonthdates(year,month)
        day = random.choice([date for date in days if date.month == month])
        day = self.convert_in2_2bytes(str(day.day))
        rand_d = str(year) + '/' + str(month) + '/' + str(day)
        return rand_d
        
        # コンボボックス用マップ作成(id, name)→gene, race, g_rank, birthplace 
        # コンボボックス用マップ作成(id, name)→class, talent（LEVEL制限あり）
        # 日付生成ランダム→これどうやるの？
        # ランダムビット生成→1の確率ほぼ0
        # ランダムビット生成→50%、30%
        # 名前のランダム生成→人名、国、class、talent

    # コンボボックスの取得
    def get_combo(self):
        pass

    # ボタン押下後処理
    def submit(self):
        # gene登録
        if len(self.ch.gene_id.get()) > 0:
            pass
        else:
            self.ge_dao.insert_gene(self.ge)
        
        # 年齢設定
        d_today = date(self.tdatetime.year, self.tdatetime.month, self.tdatetime.day)
        b_birth = datetime.strptime(self.ch.birth.get(),'%Y/%m/%d')
        d_birth = date(b_birth.year, b_birth.month, b_birth.day)
        self.ch.age.set((d_today - d_birth).years)
        
    def continuous_submit(self):
        pass

    # birthdayチェック
    def date_limit(self, entry_text):
        
        tstr = self.tdatetime.strftime('%Y/%m/%d')
        # 未来日の場合、システム日付を設定
        if str(entry_text.get()) > str(tstr):
            self.ent4.delete(0, tk.END)
            self.ent4.insert(0, str(tstr))
            self.selected_date.set(str(tstr))
        self.ch.birth.set(self.selected_date.get())
        

    # geneが選択された場合
    def select_gene(self, select_gene):
        # 対象をロック、空の場合は解除
        if len(select_gene.get()) > 0:
            self.ent7.configure(state = 'readonly')
            self.ent8.configure(state = 'readonly')
            self.ent9.configure(state = 'readonly')
            self.ent10.configure(state = 'readonly')
            self.ent11.configure(state = 'readonly')
            self.ent12.configure(state = 'readonly')
            self.ent13.configure(state = 'readonly')
            self.ent14.configure(state = 'readonly')
            self.entgn.configure(state = 'readonly')
            self.chkgn.configure(state = 'disable')
            # 選択したgeneを取得
            s_gene = self.ge_dao.pickup_gene(self.cbo_gene_list.get())

            # 対象に選択したgeneの値を反映
            self.ge.set_select_gene(s_gene)

            # gene_idを設定
            self.ch.gene_id = s_gene['gene_id']
        else:
            self.ge.init()
            self.ch.init(self.ge, self.ra)
            self.ent7.configure(state = 'normal')
            self.ent8.configure(state = 'normal')
            self.ent9.configure(state = 'normal')
            self.ent10.configure(state = 'normal')
            self.ent11.configure(state = 'normal')
            self.ent12.configure(state = 'normal')
            self.ent13.configure(state = 'normal')
            self.ent14.configure(state = 'normal')
            self.entgn.configure(state = 'normal')
            self.chkgn.configure(state = 'active')
    
    # raceが選択された場合
    def select_race(self, select_race):
        # 選択したraceを取得
        s_race = self.ra_dao.pickup_race(self.cbo_race_list.get())

        # 対象に選択したraceの値を反映
        self.ra.set_select_race(s_race)

        # race_idを設定
        self.ch.race_id = s_race['race_id']
        # characterに反映
        self.ch.set_status(self.ge, self.ra)
    
    # locationが選択された場合
    def select_location(self, select_location):
        # 選択したlocationを取得
        s_location = self.ge_dao.pickup_location(self.cbo_location_list.get())

        # 対象に選択したlocationの値を反映
        self.lo.set_select_location(s_location)

        # location_idを設定
        self.ch.location_id = s_location['location_id']

    # 入力文字数制限
    def character_limit(self,entry_text, num, ch_text=None, ra_text=None):
        if len(str(entry_text.get())) > 0:
            # 不適切な値の場合は1に設定
            if not str(entry_text.get()).isdecimal():
                entry_text.set(1)
            if int(str(entry_text.get())) <= 0:
                entry_text.set(1)
            # 100より大きい数字が入力されたら100に
            elif int(str(entry_text.get())) > 10**(num-1):
                entry_text.set(10**(num-1))
            entry_text.set(str(entry_text.get())[:num])
            
            if ch_text is not None:
                self.ch.set_status(ch_text,entry_text.get(),ra_text.get())
                try:
                    # total_sense集計
                    self.ge.total_sense.set(str(int(self.ge.s_HP.get())+int(self.ge.s_MP.get())
                    +int(self.ge.s_sta.get())+int(self.ge.s_atk.get())+int(self.ge.s_vit.get())
                    +int(self.ge.s_mag.get())+int(self.ge.s_des.get())+int(self.ge.s_agi.get())))
                    # total集計   
                    self.ch.calculate_total(self.ge, self.ra)     
                except:
                    pass
        # self.ch.set_status(entry_text.get(), ra_text.get())
    
    # レベル制限導入
    def level_limit(self,entry_text, num, ch_text=None, ra_text=None):
        if len(str(entry_text.get())) > 0:
            # 不適切な値の場合は1に設定
            if not str(entry_text.get()).isdecimal():
                entry_text.set(1)
            if int(str(entry_text.get())) <= 0:
                entry_text.set(1)
            # クラス、タレント選択制限
            if int(str(entry_text.get())) < 60:
                self.cbo15.set("")
                self.cbo15.configure(state = "disabled")
            if int(str(entry_text.get())) < 50:
                self.cbo18.set("")
                self.cbo18.configure(state = "disabled")
            if int(str(entry_text.get())) < 30:
                self.cbo14.set("")
                self.cbo14.configure(state = "disabled")
            if int(str(entry_text.get())) < 20:
                self.cbo17.set("")
                self.cbo17.configure(state = "disabled")
            if int(str(entry_text.get())) >= 60:
                self.cbo15.current(0)
                self.cbo15.configure(state = "normal")
            if int(str(entry_text.get())) >= 50:
                self.cbo18.current(0)
                self.cbo18.configure(state = "normal")
            if int(str(entry_text.get())) >= 30:
                self.cbo14.current(0)
                self.cbo14.configure(state = "normal")
            if int(str(entry_text.get())) >= 20:
                self.cbo17.current(0)
                self.cbo17.configure(state = "normal")
            # 100より大きい数字が入力されたら100に
            if int(str(entry_text.get())) > 100:
                entry_text.set(100)
            entry_text.set(str(entry_text.get())[:num])
        self.ch.set_status_all(self.ge, self.ra)


    # ラベル編集
    def ch_status_set(self,label_text,input_num):
        for dkey, dval in label_text.items():
            dval.set(dkey + '（{}）'.format(input_num))

    def convert_in2_2bytes(self,str_number):
        if len(str_number) == 1:
            return int('0' + str_number)
        else:
            return int(str_number)

     
# import以外から呼び出された場合のみこのファイルを実行
# if __name__ == '__main__':
s = Signup()
s.mainloop()
