from settings import *
import tkinter as tk
import tkinter.ttk as ttk
import datetime
import random
import DAO.fieldsDAO as _fields
import DTO.fields as fields
import DAO.locationsDAO as _locations
import DTO.locations as locations
import DAO.areasDAO as _areas
import DTO.fields as fields
import Base.basic_module as bs
# import numpy as np
# import matplotlib.pyplot as plt
# import pyFAI
from concurrent import futures
import time
from tkinter import messagebox

# 軸の目盛り位置とラベル表示の調整用
from matplotlib.ticker import MultipleLocator, AutoMinorLocator
from matplotlib.ticker import StrMethodFormatter

# map範囲
X = 1440
Y = 900

# カレンダーを作成するフレームクラス
class create_kingdom():
    def __init__(self,parent):

        import datetime
        self.parent = parent
        self.dialog = None
        self.targetRa = tk.StringVar()
        self.rect_start_x = tk.StringVar()
        self.rect_start_y = tk.StringVar()
        self.rect_stop_x = tk.StringVar()
        self.rect_stop_y = tk.StringVar()
        self.start_x = 0
        self.start_y = 0
        self.stop_x = 0
        self.stop_y = 0
        self.rect = None
        self.evoLevel = tk.IntVar()
        self.choosedField = tk.StringVar()
        self.val = tk.DoubleVar()
        self.tilt = tk.DoubleVar()
        self.s_field = []
        self.bs = bs.MyStack()
        # フレーム
        self.pw_left = None
        self.pw_main = None

        # ttkフレームの背景色
        s = ttk.Style()
        s.configure('new.TFrame', background='#7AC5CD')

        # 表示ラベル編集用
        self.HP = tk.StringVar()
        self.MP = tk.StringVar()
        self.sta = tk.StringVar()
        self.atk = tk.StringVar()
        self.vit = tk.StringVar()
        self.mag = tk.StringVar()
        self.des = tk.StringVar()
        self.agi = tk.StringVar()

        # DBアクセス用
        self.fi = fields.Field()
        self.lo = locations.Location()
        self.bk_ra = fields.Field()
        self.entry_fi = fields.Field()
        self.fi_dao = _fields.FieldDAO()
        self.lo_dao = _locations.LocationDAO()
        self.ar_dao = _areas.AreaDAO()

        # ラベル用イベント
        self.fi.population.trace("w", lambda *args: self.fi_status_set(self.fi.population.get()))
        self.fi.stress.trace("w", lambda *args: self.fi_status_set(self.fi.stress.get()))
        self.fi.hate.trace("w", lambda *args: self.fi_status_set(self.fi.hate.get()))
        self.fi.power.trace("w", lambda *args: self.fi_status_set(self.fi.power.get()))
        self.fi.welfare.trace("w", lambda *args: self.fi_status_set(self.fi.welfare.get()))
        self.fi.technology.trace("w", lambda *args: self.fi_status_set(self.fi.technology.get()))
        self.fi.military.trace("w", lambda *args: self.fi_status_set(self.fi.military.get()))
        self.fi.civil_point.trace("w", lambda *args: self.fi_status_set(self.fi.civil_point.get()))
        self.fi.civilization.trace("w", lambda *args: self.fi_status_set(self.fi.civilization.get()))
        self.fi.innovation.trace("w", lambda *args: self.fi_status_set(self.fi.innovation.get()))
        self.fi.strength.trace("w", lambda *args: self.fi_status_set(self.fi.strength.get()))
        self.fi.assets.trace("w", lambda *args: self.fi_status_set(self.fi.assets.get()))

        #モード変更イベント
        #self.rect_start_x.trace("w", lambda *args: self.changeMode())

    def openDialog(self):        
        # 子画面クラス
        self.window = tk.Toplevel(self.parent)
        self.window.geometry('960x720')
        self.window.title("Kingdom App")
        
        self.createDisplay()
        
        # TODO:いらなくなったら消す
        self.parent.mainloop()
    
    def createDisplay(self):
        # ウィンドウを分ける
        self.pw_main = tk.PanedWindow(self.window, orient='horizontal')
        self.pw_main.pack(expand=True, fill = tk.BOTH, side="left")

        # self.window→pw_left（左画面ツリービュー）
        pw_left = tk.PanedWindow(self.pw_main, bg="red", orient='vertical')
        self.pw_main.add(pw_left)

        # self.window→pw_right（右画面ツリービュー）
        pw_right = tk.PanedWindow(self.pw_main, bg="pink", orient='vertical')
        self.pw_main.add(pw_right)
        
        # self.window→pw_left_up（左上マップ表示）
        pw_left_up = self.createMap(pw_left)
        pw_left.add(pw_left_up)

        # self.window→pw_left_down（左下地方編集）
        pw_left_down = self.createLocation(pw_left)
        pw_left.add(pw_left_down)

        # self.window→pw_right_up（右上画面登録部）
        pw_right_up = self.createStatus(pw_right)
        pw_right.add(pw_right_up)
        pw_right_up2 = self.createButton(pw_right)
        pw_right.add(pw_right_up2)

        # self.window→pw_right_down（右下画面登録部）
        pw_right_down = self.createField(pw_right)
        pw_right.add(pw_right_down)

        # 画面初期化
        self.init()

        # self.window→pw_right_up4（右下画面ボタン部）
        # pw_right_up4 = self.createButton(pw_right)
        # pw_right.add(pw_right_up4)

    def init(self):
        self.rect = None
        self.pw_map.delete()
        self.rect_start_x.set(0)
        self.rect_start_y.set(0)
        self.rect_stop_x.set(0)
        self.rect_stop_y.set(0)
        self.start_x = 0
        self.start_y = 0
        self.stop_x = 0
        self.stop_y = 0

    def createMap(self,pw_left):

        pw_left_up = tk.PanedWindow(pw_left, bg="pink", orient='horizontal')
        self.lblmap = tk.Label(pw_left_up,text = 'map')
        self.lblmap.grid(row=0, column=2, padx=5, pady=2)
        
        self.pw_map = tk.Canvas(pw_left_up, width=480, height=300,borderwidth=10) # , relief='sunken'
        self.pw_map.grid(row=1, column=2, padx=5, pady=2)
        self.pw_map.bind('<Button-1>', self.rect_start_pickup)
        self.pw_map.bind('<B1-Motion>', self.pickup_position)
        self.pw_map.bind('<ButtonRelease-1>', self.rect_stop_pickup)

 
        # 新規作成用
        pw_new = ttk.Frame(pw_left_up, width=480, height=50,borderwidth=10, style="new.TFrame", relief='sunken')
        pw_new.grid(row=2, column=2, padx=5, pady=2)

        # {kingdom_id : [座標リスト] }を取得

        kingdom_grid = {}
        # areasを取得
        area_data = self.ar_dao.select()

        for data in area_data:
            if data['field_id'] in kingdom_grid:
                kingdom_grid[data['field_id']].append((data['grid_x'], data['grid_y']))
            else:
                kingdom_grid[data['field_id']] = []
                kingdom_grid[data['field_id']].append((data['grid_x'], data['grid_y']))
            
        # fig, axes = plt.plot(1,4, figsize=(16,4))
        # axes[3].imshow(data10[2:8, 2:8], origin='lower', extent=[1.5, 7.5, 1.5, 7.5])

        # 色判別用
        i = 0
        # マッピング処理
        for dkey, dval in kingdom_grid.items():

            color = colorsCollection[i]
            for d in dval:
                self.pw_map.create_rectangle(*d,1,1,fill = color,tags=dkey)
            ++i
            if i >= len(colorsCollection):
                i = 0
        # 座標部
        pw_point = self.drawPoint(pw_new)
        pw_point.grid(row=2, column=3, padx=5, pady=2,sticky=tk.W)

         # 新規作成ボタン部
        pw_button = self.drawButton(pw_new)
        pw_button.grid(row=2, column=4, padx=5, pady=2,sticky=tk.E)

        # 登録部
        pw_entry = self.drawEntry(pw_new)
        pw_entry.grid(row=3, column=3,columnspan=2, padx=5, pady=2,sticky=tk.W)

        return pw_left_up

    # 座標を描画
    def drawPoint(self, pw_new):

        pw_point = tk.PanedWindow(pw_new, bg="#7AC5CD", orient='horizontal')

        # 座標表示ウィジェット→読み取り専用？？
        self.lblx = tk.Label(pw_point,text = 'x1:', bg="#7AC5CD")
        self.lblx.grid(row=0, column=0, padx=5, pady=2)
        self.textx = tk.Entry(pw_point, textvariable=self.rect_start_x, width = 4, state='readonly')
        self.textx.grid(row=0, column=1, padx=5, pady=2)
        self.lbly = tk.Label(pw_point,text = 'y1:', bg="#7AC5CD")
        self.lbly.grid(row=0, column=2, padx=5, pady=2)
        self.texty = tk.Entry(pw_point, textvariable=self.rect_start_y, width = 4, state='readonly')
        self.texty.grid(row=0, column=3, padx=5, pady=2)
        self.lblvert = tk.Label(pw_point,text = 'x2:', bg="#7AC5CD")
        self.lblvert.grid(row=0, column=4, padx=5, pady=2)
        self.entvert = tk.Entry(pw_point, textvariable=self.rect_stop_x, width = 4, state='readonly')
        self.entvert.grid(row=0, column=5, padx=5, pady=2)
        self.lblhori = tk.Label(pw_point,text = 'y2:', bg="#7AC5CD")
        self.lblhori.grid(row=0, column=6, padx=5, pady=2)
        self.enthori = tk.Entry(pw_point, textvariable=self.rect_stop_y, width = 4, state='readonly')
        self.enthori.grid(row=0, column=7, padx=5, pady=2)

        return pw_point
    
    def drawButton(self, pw_new):

        pw_button = tk.PanedWindow(pw_new, bg="#7AC5CD", orient='horizontal')

        # 新規登録ボタン
        self.btnnew = tk.Button(pw_button, text='新規登録', width=10, command=self.entryNewKingdom)
        self.btnnew.grid(row=0, column=8, padx=5, pady=4)

        return pw_button

    def drawEntry(self,pw_new):

        pw_entry = tk.PanedWindow(pw_new, bg="#7AC5CD", orient='horizontal')

        # kingdom
        self.lbl7 = tk.Label(pw_entry,text='kingdom',width=9, bg="#7AC5CD")
        self.lbl7.grid(row=1, column=0, padx=5, pady=2)
        self.ent7 = tk.Entry(pw_entry, textvariable=self.fi.king_gene_id, width=12)
        self.ent7.grid(row=1, column=1, padx=5, pady=2)
        # characterを選択
        # TODO:条件→王家でない、領主or勇者である、家名持ち
        # king
        self.lbl8 = tk.Label(pw_entry,text='king',width=9, bg="#7AC5CD")
        self.lbl8.grid(row=1, column=2, padx=5, pady=2)
        self.cboking = ttk.Combobox(pw_entry, textvariable=self.fi.character_id, width=14)
        self.cboking.grid(row=1, column=3, padx=5, pady=2)
        self.cboking['value'] = self.fi_dao.chooseCharacter(self.start_x,self.start_y,self.stop_x,self.stop_y)
        # capital
        self.lbl9 = tk.Label(pw_entry,text='capital',width=9, bg="#7AC5CD")
        self.lbl9.grid(row=1, column=4, padx=5, pady=2)
        self.ent8 = tk.Entry(pw_entry, textvariable=self.lo.location_id, width=12)
        self.ent8.grid(row=1, column=5, padx=5, pady=2)

        return pw_entry

    def entryNewKingdom(self):
        # 登録確認ポップアップ表示
        if bs.Popup.OKCancelPopup(self,Q0004) == False:
            # いいえを選択した場合、描画した図形を削除
            # self.init()
            return

        if len(self.rect_start_x.get()) > 0 and len(self.rect_start_y.get()) > 0 and len(self.rect_stop_x.get()) > 0 and len(self.rect_stop_y.get()) > 0:
            # 中心座標判定
            l_x = 0
            l_y = 0
            r_x = 0
            r_y = 0
            
            # TODO:面倒だから元結良い方法ないかな入れ替え処理
            if self.rect_start_x.get() < self.rect_stop_x.get():
                l_x = self.rect_stop_x.get()
                r_x = self.rect_start_x.get()
            else:
                l_x = self.rect_start_x.get()
                r_x = self.rect_stop_x.get()

            if self.rect_start_y.get() < self.rect_stop_y.get():
                l_y = self.rect_stop_y.get()
                r_y = self.rect_start_y.get()
            else:
                l_y = self.rect_start_y.get()
                r_y = self.rect_stop_y.get()


            # ④登録用fieldsデータを作成(新規なのでほぼ③の数値(集計)となる)
            entry_field = self.newFields(l_x,l_y,r_x,r_y)
            # ③登録用locationsデータを作成→王都面積に比例、中心座標(①、②のデータの集計)
            entry_location = self.newLocations(l_x,l_y,r_x,r_y,entry_field)
            # ①登録用areasデータを作成
            # ②登録用spotsデータを作成(①のデータ件数×25)
            future_list = []
            with futures.ThreadPoolExecutor(max_workers=4) as executor:
                for i in range(l_x, r_x):
                    for j in range(l_y, r_y):
                        future = executor.submit(fn=self.newMapping, i_x=i, i_y=j)
                        future_list.append(future.result)
                _ = futures.as_completed(fs=future_list)

            # 中心座標エラー
            #bs.Popup.ShowInfo(self,E0004.format(X,Y))

        else:
            # 登録エラーポップアップ表示
            bs.Popup.ShowInfo(self,E0003)
    
    # エリア、建物作成(ランダムテンプレート)
    def newMapping(self, i_x, i_y):
        area = self.areas
        area.grid_x = i_x
        area.grid_y = i_y
        # 先にfields、locations登録してidを格納

    # 王国作成
    def newFields(self,l_x,l_y,r_x,r_y):
        # 範囲内に孫沿いする人口を取得
        # 初期化状態で登録
        population = self.fi_dao.get_population(l_x,l_y,r_x,r_y)
        # 王国登録要素を表示
        entry_list = []
        entry_list.append(
            {
                "field_name":self.fi.field_name.get(),
                "f_rank":self.fi.f_rank.get(),
                "king_gene_id":self.fi_dao.pickup_field(self.cboChoice.get()),
                "character_id":self.fi.character_id.get(),
                "contract_id":self.fi.contract_id.get(),
                "is_war":"0",
                "area":abs(r_x - l_x) * abs(r_y - l_y),
                "population":population,
                "p_density":int(population / ((r_x-l_x) * (r_y - l_y))),
                "stress":0,
                "hate":0,
                "power":0,
                "welfare":0,
                "technology":0,
                "military":0,
                "civil_point":0,
                "civilization":0,
                "innovation":0,
                "strength":0,
                "assets":0,
                "GDP":0,
                "tax":0,
                "develop":0,
                "version":1,
                "is_deleted":0,
                "ins_date":datetime.now(),
                "ins_id":"dummy",
                "upd_date":datetime.now(),
                "upd_id":"dummy"
            }
        )

        try:
            self.fi_dao.insert_field(entry_list)
        except:
            # OKポップアップ
            messagebox.showinfo('警告', E0002)

    # 王都作成
    def newLocations(self,l_x,l_y,r_x,r_y,field_data):

        # 王都作成
        capital_list = []
        capital_list.append(
            {
                "field_id" : field_data['field_id'],
                "lord_gene_id" : field_data['king_gene_id'],
                "character_id" : field_data['character_id'],
                "location_name" : self.lo.insert_location,
                "l_rank" : self.lo.l_rank.get(),
                "is_battle" : self.lo.is_battle.get(),
                "area" : self.lo.area.get(),
                "population" : self.lo.population.get(),
                "p_density" : self.lo.p_density.get(),
                "stress" : self.lo.stress.get(),
                "hate" : self.lo.hate.get(),
                "power" : self.lo.power.get(),
                "welfare" : self.lo.welfare.get(),
                "technology" : self.lo.technology.get(),
                "military" : self.lo.military.get(),
                "civil_point" : self.lo.civil_point.get(),
                "civilization" : self.lo.civilization.get(),
                "innovation" : self.lo.innovation.get(),
                "strength" : self.lo.strength.get(),
                "assets" : self.lo.assets.get(),
                "GDP" : self.lo.GDP.get(),
                "tax" : self.lo.tax.get(),
                "develop" : self.lo.develop.get(),
                "disparity" : self.lo.disparity.get(),
                "version":1,
                "is_deleted":0,
                "ins_date":datetime.now(),
                "ins_id":"dummy",
                "upd_date":datetime.now(),
                "upd_id":"dummy"
            }
        )
        # locations-areas
        future_list = []
        with futures.ThreadPoolExecutor(max_workers=4) as executor:
            # 王国の中心x,y1/5スケールで王都を作成
            for i in range(int(l_x + abs(r_x - l_x) * 2 / 5), int(r_x - abs(r_x - l_x) * 2 / 5)):
                for j in range(int(l_y + abs(r_y - l_y) * 2 / 5), int(r_y - abs(r_y - l_y) * 2 / 5)):
                    future_list.append(
                        {
                            "grid_x":i,
                            "grid_y":j,
                            "field_id" : "dummy",
                            "lord_gene_id" : "dummy",
                            "character_id" : "dummy",
                            "location_name" : "dummy",
                            "l_rank" : "dummy",
                            "is_battle" : "dummy",
                            "power" : "dummy",
                            "welfare" : "dummy",
                            "technology" : "dummy",
                            "military" : "dummy",
                            "disparity" : "dummy",
                            "stress" : "dummy",
                            "civil_point" : "dummy",
                            "civilization" : "dummy",
                            "population" : "dummy",
                            "assets" : "dummy",
                            "GDP" : "dummy",
                            "tax" : "dummy",
                            "develop" : "dummy",
                            "version" : "dummy",
                            "is_deleted" : "dummy",
                            "ins_date" : "dummy",
                            "ins_id" : "dummy",
                            "upd_date" : "dummy",
                            "upd_id" : "dummy"
                        }
                    )
    
    def createLocation(self, pw_left):

        pw_left_down = tk.PanedWindow(pw_left, bg="pink", orient='horizontal')
        self.lbllocation = tk.Label(pw_left_down,text = 'location')
        self.lbllocation.grid(row=0, column=2, padx=5, pady=2)
        
        pw_location = ttk.Frame(pw_left_down, width=480, height=300,borderwidth=10, relief='sunken')
        pw_location.grid(row=2, column=2, padx=5, pady=2)

        return pw_left_down

    # 名前部作成
    def createField(self,pw_right):
        pw_right_down = tk.PanedWindow(pw_right, bg="pink", orient='horizontal')

        self.lbl_titleName = tk.Label(pw_right_down,text="name",width=9)
        self.lbl_titleName.grid(row=0, column=0, padx=5, pady=2, columnspan = 4)

        

        return pw_right_down

    # ステータス部作成
    def createStatus(self, pw_right):

        pw_right_up = tk.PanedWindow(pw_right, bg="pink", orient='horizontal')

        self.lbl_title = tk.Label(pw_right_up,text="Country",width=9)
        self.lbl_title.grid(row=0, column=0, padx=5, pady=2, columnspan = 4)
        # civilization
        self.lbl14 = tk.Label(pw_right_up,text="civilization",width=9)
        self.lbl14.grid(row=1, column=0, padx=5, pady=2)
        self.ent14 = tk.Entry(pw_right_up, textvariable=self.fi.civilization,  width=12)
        self.ent14.grid(row=1, column=1, padx=5, pady=2)
        # rank
        self.lbl16 = tk.Label(pw_right_up,text="rank",width=9)
        self.lbl16.grid(row=1, column=2, padx=5, pady=2)
        self.ent16 = tk.Entry(pw_right_up, textvariable=self.fi.f_rank,  width=12)
        self.ent16.grid(row=1, column=3, padx=5, pady=2)
        self.ent16.configure(state = 'readonly')
        # power
        self.lbl10 = tk.Label(pw_right_up,text="power",width=9)
        self.lbl10.grid(row=3, column=0, padx=5, pady=2)
        self.ent10 = tk.Entry(pw_right_up, textvariable=self.fi.power,  width=12)
        self.ent10.grid(row=3, column=1, padx=5, pady=2)
        # welfare
        self.lbl11 = tk.Label(pw_right_up,text="welfare",width=9)
        self.lbl11.grid(row=3, column=2, padx=5, pady=2)
        self.ent11 = tk.Entry(pw_right_up, textvariable=self.fi.welfare,  width=12)
        self.ent11.grid(row=3, column=3, padx=5, pady=2)
        # technology
        self.lbl12 = tk.Label(pw_right_up,text="technology",width=9)
        self.lbl12.grid(row=4, column=0, padx=5, pady=2)
        self.ent12 = tk.Entry(pw_right_up, textvariable=self.fi.technology,  width=12)
        self.ent12.grid(row=4, column=1, padx=5, pady=2)
        # military
        self.lbl13 = tk.Label(pw_right_up,text="military",width=9)
        self.lbl13.grid(row=4, column=2, padx=5, pady=2)
        self.ent13 = tk.Entry(pw_right_up, textvariable=self.fi.military,  width=12)
        self.ent13.grid(row=4, column=3, padx=5, pady=2)
        # innovation
        self.lbl14 = tk.Label(pw_right_up,text="innovation",width=9)
        self.lbl14.grid(row=5, column=0, padx=5, pady=2)
        self.ent14 = tk.Entry(pw_right_up, textvariable=self.fi.innovation,  width=12)
        self.ent14.grid(row=5, column=1, padx=5, pady=2)
        # assets
        self.lbl14 = tk.Label(pw_right_up,text="assets",width=9)
        self.lbl14.grid(row=5, column=2, padx=5, pady=2)
        self.ent14 = tk.Entry(pw_right_up, textvariable=self.fi.assets,  width=12)
        self.ent14.grid(row=5, column=3, padx=5, pady=2)

        # 状態値
        self.lbl_st = tk.Label(pw_right_up,text="Status",width=9)
        self.lbl_st.grid(row=6, column=0, padx=5, pady=2, columnspan = 4)
        # stress
        self.lbl15 = tk.Label(pw_right_up,text="stress",width=9)
        self.lbl15.grid(row=7, column=0, padx=5, pady=2)
        self.ent15 = tk.Entry(pw_right_up, textvariable=self.fi.stress,  width=12)
        self.ent15.grid(row=7, column=1, padx=5, pady=2)
        # hate
        self.lbl16 = tk.Label(pw_right_up,text="hate",width=9)
        self.lbl16.grid(row=7, column=2, padx=5, pady=2)
        self.ent16 = tk.Entry(pw_right_up, textvariable=self.fi.hate,  width=12)
        self.ent16.grid(row=7, column=3, padx=5, pady=2)

        return pw_right_up

    def createButton(self, pw_right):
        pw_right_up4 = tk.PanedWindow(pw_right, bg="pink", orient='horizontal')

        # ランダム生成
        self.lbl17 = tk.Label(pw_right_up4,text="ランダム生成",width=9)
        self.lbl17.grid(row=0, column=0, columnspan=2, padx=5, pady=2)
        
        # 傾きラベル
        self.lblTlt = tk.Label(pw_right_up4,text="傾き",width=5)
        self.lblTlt.grid(row=1, column=0, padx=5, pady=2)
        
        # 傾きスケールの作成
        self.scTilt = ttk.Scale(
            pw_right_up4,
            variable=self.tilt,
            orient=tk.HORIZONTAL,
            length=150,
            from_=0,
            to=10
            # , command=lambda e: print('val:%4d' % self.val.get())
            )
        self.scTilt.grid(row=1, column=1, sticky=(tk.N, tk.E, tk.S, tk.W), padx=5, pady=2)

        # tilt出力
        self.entTilt = tk.Entry(pw_right_up4, textvariable=self.tilt,  width=7)
        self.entTilt.grid(row=1, column=2, padx=5, pady=2)
        # self.entTilt.configure(state = 'readonly')
        
        # 傾きラベル
        self.lblWeight = tk.Label(pw_right_up4,text="重み",width=5)
        self.lblWeight.grid(row=2, column=0, padx=5, pady=2)

        # 重みスケールの作成
        self.scWeight = ttk.Scale(
            pw_right_up4,
            variable=self.val,
            orient=tk.HORIZONTAL,
            length=150,
            from_=0,
            to=100
            # , command=lambda e: print('val:%4d' % self.val.get())
            )
        self.scWeight.grid(row=2, column=1, sticky=(tk.N, tk.E, tk.S, tk.W), padx=5, pady=2)

        # weight出力
        self.entWeight = tk.Entry(pw_right_up4, textvariable=self.val,  width=7)
        self.entWeight.grid(row=2, column=2, padx=5, pady=2)
        # self.entWeight.configure(state = 'readonly')

        # ランダムボタン
        self.btnRand = tk.Button(pw_right_up4, text='ランダム', width=10, command=self.randomNum)
        self.btnRand.grid(row=4, column=0, columnspan=2, padx=5, pady=4)

        # 登録ボタン
        self.btnEntry = tk.Button(pw_right_up4, text='登録', width=10, command=self.entryField)
        self.btnEntry.grid(row=5, column=0, columnspan=2, padx=5, pady=4)

        return pw_right_up4


    # textの内容のリセットself.yearに格納
    def set_f_rank(self,text_label,data):

        if int(data) > 5000000000000:
            self.fi.f_rank.set('SSS')
        elif int(data)  > 200000000000:
            self.fi.f_rank.set('SS')
        elif int(data)  > 10000000000:
            self.fi.f_rank.set('S')
        elif int(data)  > 5000000000:
            self.fi.f_rank.set('A')
        elif int(data)  > 250000000:
            self.fi.f_rank.set('B')
        elif int(data)  > 12500000:
            self.fi.f_rank.set('C')
        elif int(data)  > 1000000:
            self.fi.f_rank.set('D')
        elif int(data)  > 62500:
            self.fi.f_rank.set('E')
        elif int(data)  > 12500:
            self.fi.f_rank.set('F')
        else:
            self.fi.f_rank.set('G')

        # self.ch_status_set(text_label,self.fi.f_rank.get())

    # 選択したfieldを登録用メンバにセット
    def setFieldSelected(self):
        
        # self.fi.field_name.set(self.fi.field_name.get())
        self.fi.field_id.set(self.fi.field_id.get())
        self.fi.king_gene_id.set(self.fi.king_gene_id.get())
        self.fi.character_id.set(self.fi.character_id.get())
        self.fi.contract_id.set(self.fi.contract_id.get())
        self.fi.castle.set(self.fi.castle.get())
        self.fi.area.set(self.fi.area.get())
        self.fi.population.set(self.fi.population.get())
        self.fi.stress.set(self.fi.stress.get())
        self.fi.hate.set(self.fi.hate.get())
        self.fi.parent_field1_id.set(self.fi.parent_field1_id.get())
        self.fi.evolution1_level.set(self.fi.evolution1_level.get())
        self.fi.parent_field2_id.set(self.fi.parent_field2_id.get())
        self.fi.evolution2_level.set(self.fi.evolution2_level.get())
        self.fi.parent_field3_id.set(self.fi.parent_field3_id.get())
        self.fi.evolution3_level.set(self.fi.evolution3_level.get())
        self.fi.civilization.set(self.fi.civilization.get())
        self.fi.civil_point.set(self.fi.civil_point.get())

    # 上位ランクデータ取得
    def getFieldValue(self):
        fieldList = {}
        try:
            acquired_rank = self.getFieldRank(self.fieldRoot[self.iid]['civilization'])
            self.cboChoice.configure(state = 'normal')
        except:
            acquired_rank = []
            self.cboChoice.configure(state = 'disabled')

        for data in self.fieldRoot.values():
            # ランクが選択可能ランク以上、かつ進化先と重複しない
            if (data['civilization'] in acquired_rank and str(data['field_id']) != self.fi.field_id.get()):
                try:
                    # fieldTree = Noneの場合を考慮
                    if data['field_id'] not in [field['field_id'] for field in self.fieldTree[self.iid]]:
                        fieldList[data['field_id']] = data['civilization'] + ':' + data['field_name']
                except:
                    fieldList[data['field_id']] = data['civilization'] + ':' + data['field_name']
        
        return list(fieldList.values())

    # 選択可能ランクリスト取得
    # 0:編集の場合は自身のランクも選択可能に設定
    def getFieldRank(self, civilization):
        acquired_rank = []
        if civilization == 'SS':
            acquired_rank = ['SSS']
        if civilization == 'S':
            acquired_rank = ['SSS','SS']
        if civilization == 'A':
            acquired_rank = ['SSS','SS','S']
        if civilization == 'B':
            acquired_rank = ['SSS','SS','S','A']
        if civilization == 'C':
            acquired_rank = ['SSS','SS','S','A','B']
        if civilization == 'D':
            acquired_rank = ['SSS','SS','S','A','B','C']
        if civilization == 'E':
            acquired_rank = ['SSS','SS','S','A','B','C','D']
        if civilization == 'F':
            acquired_rank = ['SSS','SS','S','A','B','C','D','E']
        if civilization == 'G':
            acquired_rank = ['SSS','SS','S','A','B','C','D','E','F']

        # ホームの場合は初期ランク'G'を追加
        if self.iid == 'I001':
            acquired_rank.append('G')
        
        return acquired_rank

    # totalからランクを設定
    def getOneRank(self, total):
        
        rank = 'G'

        if total > 50000:
            rank = 'SSS'
        elif total > 30000:
            rank = 'SS'
        elif total > 15000:
            rank = 'S'
        elif total > 10000:
            rank = 'A'
        elif total > 7500:
            rank = 'B'
        elif total > 5000:
            rank = 'C'
        elif total > 3000:
            rank = 'D'
        elif total > 1500:
            rank = 'F'
        
        return rank
            
    # fieldが選択された場合
    def select_field(self, _field):

        # コンボボックスの種族が存在しない場合初期化
        try:
            # 選択したfieldを取得
            s_field = self.fi_dao.pickup_field(_field.get())
            # 対象に選択したfieldの値を反映
            self.fi.set_select_field(s_field)
        except:
            _field.set('')
            self.setFieldSelected()
            return

    # 入力文字数制限NOTE:entry_text:gene,num:桁数
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
        
            try:
                # civil_point集計
                self.fi.civil_point.set(str(int(self.fi.king_gene_id.get())+int(self.fi.character_id.get())
                +int(self.fi.contract_id.get())+int(self.fi.castle.get())+int(self.fi.area.get())
                +int(self.fi.population.get())+int(self.fi.stress.get())+int(self.fi.hate.get())))   
            except:
                pass

            # self.fi.civilization.set(self.getOneRank(self.fi.civil_point.get()))


    # 入力文字数制限NOTE:entry_text:gene,num:桁数
    def character_limit_move(self,entry_text, num, ch_text=None, ra_text=None):
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
        
        # TODO:ナニコレ
        # tk.Canvas.coords(self.new_kingdom, x0, y0, x1, y1)

            # self.fi.civilization.set(self.getOneRank(self.fi.civil_point.get()))

    # 進化レベル設定（基準）
    def randomLevel(self,civilization):
        if civilization == 'SSS':
            self.evoLevel.set(random.randint(60,99))
        if civilization == 'SS':
            self.evoLevel.set(random.randint(45,70))
        if civilization == 'S':
            self.evoLevel.set(random.randint(40,65))
        if civilization == 'A':
            self.evoLevel.set(random.randint(35,60))
        if civilization == 'B':
            self.evoLevel.set(random.randint(30,55))
        if civilization == 'C':
            self.evoLevel.set(random.randint(25,50))
        if civilization == 'D':
            self.evoLevel.set(random.randint(20,40))
        if civilization == 'E':
            self.evoLevel.set(random.randint(10,30))
        if civilization == 'F':
            self.evoLevel.set(random.randint(5,20))
        if civilization == 'G':
            self.evoLevel.set(random.randint(1,5))
        

    # 王国表示処理
    def entryField(self):

        # プルダウンで設定した場合
        if len(self.choosedField.get()) != 0:
            # 登録確認ポップアップ表示
            if bs.Popup.OKCancelPopup(self,Q0003) == False:
                return
            # 進化先に選択種族を設定する
            try:
                self.fi_dao.update_child_field(self.fi, self.fi.field_id.get(), self.evoLevel.get())
            except:
                # 登録エラーポップアップ表示
                bs.Popup.ShowInfo(self,E0002)
                return
        else:
            # プルダウンで設定されていない場合
            self.displayEntry()

        # 登録完了ポップアップ表示
        bs.Popup.ShowInfo(self,I0002)
        
        # 再検索を実施
        self.pw_main.destroy()
        self.createDisplay()
    
    # 画面内容登録
    def displayEntry(self):
        s_field = self.entry_fi

        # 重複チェック実装
        res = [field for field in list(self.fieldTree.values()) if s_field.field_name.get() == field[0]['field_name'] and s_field.civilization.get() == field[0]['civilization'] ]
        
        if len(res) != 0:
            bs.Popup.ShowInfo(self,E0001)
            return
        
        # initial_flg設定
        if self.iid == 'I001':
            self.fi.initial_flg.set(1)
        else:
            pass

        # 登録確認ポップアップ表示
        if bs.Popup.OKCancelPopup(self,Q0001) == False:
            return

        try:
            # 親種族の更新
            if self.rect_start_x.get() == 0:
                # 種族更新 
                self.fi_dao.update_field(s_field)
                # TODO:進化前更新
            else:
                # 種族登録 戻り値にInsertした種族を取得
                res_id = self.fi_dao.insert_field(s_field)
                # 子種族の更新
                if self.iid != 'I001':
                    self.fi_dao.update_child_field(self.fi,res_id,self.evoLevel.get())
        except:
            # 登録エラーポップアップ表示
            bs.Popup.ShowInfo(self,E0002)
            return

    # 削除処理
    def deleteField(self):

        # 削除確認ポップアップ表示
        if bs.Popup.OKCancelPopup(self,Q0002) == False:
            return
        
        if self.fi_dao.delete_field(self.fi) == False:
            bs.Popup.ShowInfo(self,E0002)
            return
        if self.fi_dao.update_else(self.fi, self.bk_ra) == False:
            bs.Popup.ShowInfo(self,E0002)
            return
    
        # 削除完了ポップアップ表示
        bs.Popup.ShowInfo(self,I0002)

        # 再検索を実施
        self.pw_main.destroy()
        self.createDisplay()

    # ランダム生成押下時
    def randomNum(self):
        # weight = 1.5 # 超レアガチャ
        # weight = 2   # 高レアガチャ
        # weight = 3   # レアガチャ
        # weight = random.random() + 100   # ノーマルガチャ
        
        # 表示用種族をセットする（連打対応）
        self.setFieldSelected()

        # 選択可能ランク
        # TODO：チョイス可能に設定する
        acquired_rank = self.getFieldRank(self.fi.civilization.get())
        
        # 重み付けローカル変数
        val = self.val.get()

        reg_field = {}
        reg_field['r_hp'] = 1
        reg_field['r_mp'] = 1
        reg_field['r_sta'] = 1
        reg_field['r_atk'] = 1
        reg_field['r_vit'] = 1
        reg_field['r_mag'] = 1
        reg_field['r_des'] = 1
        reg_field['r_agi'] = 1

        # 登録用
        
        # 新規、編集ランク制限
        if self.rect_start_x.get() == 0:

            for i in range(1000):

                # 重み付けF-C安定
                # あたり
                # weight = 70

                weight = val + 1 - i*0.1

                # geneをランダムで設定
                # self.fi.level.set(self.rand_num_hard(3,weight))
                reg_field['r_hp'] = self.rand_num(5,weight)
                reg_field['r_mp'] = self.rand_num(5,weight)
                reg_field['r_sta'] = self.rand_num(5,weight)
                reg_field['r_atk'] = self.rand_num(5,weight)
                reg_field['r_vit'] = self.rand_num(5,weight)
                reg_field['r_mag'] = self.rand_num(5,weight)
                reg_field['r_des'] = self.rand_num(5,weight)
                reg_field['r_agi'] = self.rand_num(5,weight)

                # 編集の場合：ブレーク条件
                # if self.getOneRank(sum(reg_field.values())) in acquired_rank:
                #     break

                # weight回復
                if sum(reg_field.values()) <= 0:
                    val = val + i*0.2

        elif self.rect_start_x.get() == 1:

            # geneをランダムで設定
            # self.fi.level.set(self.rand_num_hard(3,weight)

            for i in range(1000):

                # 重み付けF-C安定
                # あたり
                # weight = 70

                weight = val + 1 - i*0.1

                # geneをランダムで設定
                # self.fi.level.set(self.rand_num_hard(3,weight))
                reg_field['r_hp'] = self.rand_num(5,weight)
                reg_field['r_mp'] = self.rand_num(5,weight)
                reg_field['r_sta'] = self.rand_num(5,weight)
                reg_field['r_atk'] = self.rand_num(5,weight)
                reg_field['r_vit'] = self.rand_num(5,weight)
                reg_field['r_mag'] = self.rand_num(5,weight)
                reg_field['r_des'] = self.rand_num(5,weight)
                reg_field['r_agi'] = self.rand_num(5,weight)

                # 新規の場合ブレーク条件
                # if self.getOneRank(sum(reg_field.values())) in acquired_rank and sum(reg_field.values()) > self.fi.civil_point.get():
                #     break

                # weight回復
                if sum(reg_field.values()) <= 0:
                    val = val + i*0.2
            
        self.fi.king_gene_id.set(reg_field['r_hp'])
        self.fi.character_id.set(reg_field['r_mp'])
        self.fi.contract_id.set(reg_field['r_sta'])
        self.fi.castle.set(reg_field['r_atk'])
        self.fi.area.set(reg_field['r_vit'])
        self.fi.population.set(reg_field['r_mag'])
        self.fi.stress.set(reg_field['r_des'])
        self.fi.hate.set(reg_field['r_agi'])
        self.fi.civil_point.set(sum(reg_field.values()))

        # totalからrankを設定
        self.fi.civilization.set(self.getOneRank(self.fi.civil_point.get()))

        # 進化レベル設定
        self.randomLevel(self.fi.civilization.get())

    def rand_num(self, num, weight):
        import numpy as np
        import matplotlib.pyplot as plt

        a = np.arange(0,self.tilt.get()+1,0.1)
        exp_a = np.exp(a)
        sum_exp_a = np.sum(exp_a)
        y = exp_a / sum_exp_a
        rn_int = int(random.choice(y)*(10**num)*weight/(weight+80))
        if rn_int > 10**(num-1):
            rn_int = 10**(num-1)
        if rn_int == 0:
            rn_int = random.randint(1,10**(num-2))
        # plt.plot(a,y)
        # plt.show()
        # rad_int = random.randint(1,10**(num-1))
        return rn_int
    
    # ラベル編集
    def fi_status_set(self,label_text,input_num):
        for dkey, dval in label_text.items():
            dval.set(dkey + '（{}）'.format(input_num))
    
    # マウスイベント
    def rect_start_pickup(self, event):
        self.rect_start_x.set(str(event.x))
        self.rect_start_y.set(str(event.y))
        self.start_x = event.x
        self.start_y = event.y

    def pickup_position(self, event):
        
        if 0 <= event.x <= X and 0 <= event.y <= Y:
            self.rect_stop_x.set(str(event.x))
            self.rect_stop_y.set(str(event.y))
            # self.stop_x = event.x
            # self.stop_y = event.y

            if self.rect:
                self.pw_map.coords(self.rect,
                    min(self.start_x, event.x), min(self.start_y, event.y),
                    max(self.start_x, event.x), max(self.start_y, event.y))
            else:
                self.rect = self.pw_map.create_rectangle(self.start_x,
                    self.start_y, event.x, event.y, outline='red')

    def rect_stop_pickup(self, event):
        self.rect_stop_x.set(str(event.x))
        self.rect_stop_y.set(str(event.y))

# 1桁の数字を2バイトに変換する関数
# 追記 https://teratail.com/questions/234639#reply-355304
def convert_in2_2bytes(str_number):
    if len(str_number) == 1:
        return '0' + str_number
    else:
        return str_number

root = tk.Tk()
c = create_kingdom(root)
c.openDialog()
