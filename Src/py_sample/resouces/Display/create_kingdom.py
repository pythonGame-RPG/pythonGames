from settings import *
import tkinter as tk
import tkinter.ttk as ttk
from datetime import *
import random
import DAO.charactersDAO as _characters
import DTO.characters as characters
import DAO.fieldsDAO as _fields
import DTO.fields as fields
import DAO.locationsDAO as _locations
import DTO.locations as locations
import DAO.areasDAO as _areas
import DAO.spotsDAO as _spots
import DTO.fields as fields
import Base.basic_module as bs
import numpy as np
# import matplotlib.pyplot as plt
# import pyFAI
from concurrent import futures
import time
from tkinter import messagebox

# 軸の目盛り位置とラベル表示の調整用
from matplotlib.ticker import MultipleLocator, AutoMinorLocator
from matplotlib.ticker import StrMethodFormatter
# バルクイン用
import csv
import os
import sys
from pathlib import Path
import pprint

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
        self.rect_start_x = tk.IntVar()
        self.rect_start_y = tk.IntVar()
        self.rect_stop_x = tk.IntVar()
        self.rect_stop_y = tk.IntVar()
        self.start_x = 0
        self.start_y = 0
        self.stop_x = 0
        self.stop_y = 0
        # マップ座標データ：grid/grid_x/grid_y/horn_grid
        self.kingdom_grid = {}
        # 重複座標取得
        self.duplicate_grid = {}
        # 差集合（重複を省いた集合）
        self.setdiff_grid = set()
        # 重複データ（編集用）取得
        self.duplicate_area = {}
        # 上書きフラグ True：上書きを実施
        self.overWrite_flg = None
        self.rect = None
        self.evoLevel = tk.IntVar()
        self.choosedField = tk.StringVar()
        self.king_cbo = tk.StringVar()
        self.val = tk.DoubleVar()
        self.tilt = tk.DoubleVar()
        self.s_field = []
        self.bs = bs.MyStack()
        # フレーム
        self.pw_left = None
        self.pw_main = None
        self.root = os.path.dirname(__file__)
        sys.path.append(self.root + "/CSV")

        # ttkフレームの背景色
        s = ttk.Style()
        s.configure('new.TFrame', background='#7AC5CD')

        # 変更前
        self.civilization = 0
        self.power = 0
        self.technology = 0
        self.welfare = 0
        self.military = 0
        self.innovation = 0
        self.assets = 0
        self.total = 0
        self.dummy_num = 4000
        
        # 面積
        self._areas = tk.IntVar()

        # DBアクセス用
        self.ch = characters.Character()
        self.fi = fields.Field()
        self.lo = locations.Location()
        self.bk_ra = fields.Field()
        self.entry_fi = fields.Field()
        self.ch_dao = _characters.CharacterDAO()
        self.fi_dao = _fields.FieldDAO()
        self.lo_dao = _locations.LocationDAO()
        self.ar_dao = _areas.AreaDAO()
        self.sp_dao = _spots.SpotDAO()

        # ラベル用イベント
        #self.fi.population.trace("w", lambda *args: self.fi_status_set(self.fi.population,self.fi.population.get()))
        #self.fi.stress.trace("w", lambda *args: self.fi_status_set(self.fi.stress,self.fi.stress.get()))
        #self.fi.hate.trace("w", lambda *args: self.fi_status_set(self.fi.hate,self.fi.hate.get()))
        # 直結イベント
        self.fi.power.trace("w", lambda *args: self.fi_status_set(self.fi.power, self.fi.power.get(), self.dummy_num))
        self.fi.welfare.trace("w", lambda *args: self.fi_status_set(self.fi.welfare, self.fi.welfare.get(), self.dummy_num))
        self.fi.technology.trace("w", lambda *args: self.fi_status_set(self.fi.technology, self.fi.technology.get(), self.dummy_num))
        self.fi.military.trace("w", lambda *args: self.fi_status_set(self.fi.military, self.fi.military.get(), self.dummy_num))
        self.fi.civil_point.trace("w", lambda *args: self.fi_status_set(self.fi.civil_point, self.fi.civil_point.get(), self.dummy_num))
        self.fi.innovation.trace("w", lambda *args: self.fi_status_set(self.fi.innovation,self.fi.innovation.get(), self.dummy_num))
        self.fi.assets.trace("w", lambda *args: self.fi_status_set(self.fi.assets, self.fi.assets.get(), self.dummy_num))
        # レベルの上昇
        self.fi.civilization.trace("w", lambda *args: self.civilMultiply(self.fi.civilization.get()))
        # コンボボックス設定時
        self.king_cbo.trace("w", lambda *args: self.set_king_cbo())

        #モード変更イベント
        #self.rect_start_x.trace("w", lambda *args: self.changeMode())
    
    # param:civilization
    def civilMultiply(self, level):
        self.fi.strength.set(self.total * level)
    
    # コンボボックス選択時
    def set_king_cbo(self):
        # king_data
        res = self.ch_dao.pickup_character(self.king_cbo.get())
        self.ch.id.set(res['id'])
        self.ch.gene_id.set(res['gene_id'])


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
        self.pw_left = tk.PanedWindow(self.pw_main, bg="red", orient='vertical')
        self.pw_main.add(self.pw_left)

        # self.window→pw_right（右画面ツリービュー）
        pw_right = tk.PanedWindow(self.pw_main, bg="pink", orient='vertical')
        self.pw_main.add(pw_right)
        
        # self.window→pw_left_up（左上マップ表示）
        self.pw_left_up = self.createMap(self.pw_left)
        self.pw_left.add(self.pw_left_up)

        # self.window→pw_left_down（左下地方編集）
        pw_left_down = self.createLocation(self.pw_left)
        self.pw_left.add(pw_left_down)

        # self.window→pw_right_up（右上画面登録部）
        pw_right_up = self.createStatus(pw_right)
        pw_right.add(pw_right_up)
        pw_right_up2 = self.createButton(pw_right)
        pw_right.add(pw_right_up2)

        # self.window→pw_right_down（右下画面登録部）
        pw_right_down = self.createField(pw_right)
        pw_right.add(pw_right_down)

        # self.window→pw_right_up4（右下画面ボタン部）
        # pw_right_up4 = self.createButton(pw_right)
        # pw_right.add(pw_right_up4)

    def init(self):
        self.pw_map.delete("all")
        self.rect = None
        self.rect_start_x.set(0)
        self.rect_start_y.set(0)
        self.rect_stop_x.set(0)
        self.rect_stop_y.set(0)
        self.start_x = 0
        self.start_y = 0
        self.stop_x = 0
        self.stop_y = 0
        self.overWrite_flg = None
        self.duplicate_area = {}
        self.kingdom_grid = {}

    # マップ作製
    def createMap(self,pw_left):

        pw_left_up = tk.PanedWindow(pw_left, bg="pink", orient='horizontal')
        self.lblmap = tk.Label(pw_left_up,text = 'map')
        self.lblmap.grid(row=0, column=2, padx=5, pady=2)
        
        # マップ描画処理
        self.pw_map = tk.Canvas(pw_left_up, width=480, height=300,borderwidth=10) # , relief='sunken'
        self.pw_map.grid(row=1, column=2, padx=5, pady=2)
        self.pw_map.bind('<Button-1>', self.rect_start_pickup)
        self.pw_map.bind('<B1-Motion>', self.pickup_position)
        self.pw_map.bind('<ButtonRelease-1>', self.rect_stop_pickup)

        # マップデータ取得
        self.drawMap()
 
        # 新規作成用
        pw_new = ttk.Frame(pw_left_up, width=480, height=50,borderwidth=10, style="new.TFrame", relief='sunken')
        pw_new.grid(row=2, column=2, padx=5, pady=2)

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
    
    # ★再検索、マップ描画イベント
    def drawMap(self):

        area_data = self.ar_dao.select()

        for data in area_data:
            if data['field_id']  not in self.kingdom_grid:
                self.kingdom_grid[data['field_id']] = {'grid':set(), 'horn':[], 'grid_x':[], 'grid_y':[], 'data_list':[]}
            
            self.kingdom_grid[data['field_id']]['grid'].add((data['grid_x'], data['grid_y']))
            self.kingdom_grid[data['field_id']]['grid_x'].append(data['grid_x'])
            self.kingdom_grid[data['field_id']]['grid_y'].append(data['grid_y'])
            self.kingdom_grid[data['field_id']]['data_list'].append(data)
        
        # 色判別用
        color_cnt = 0

        # 外周取得処理
        for dkey, dval in self.kingdom_grid.items():
        
            # min値を取るためにわざわざ座標でなく辞書を選択
            min_x = min(dval['grid_x'])
            target_area = [_area for _area in dval['grid'] if _area[0] == min_x]
            min_y = min([_g[1] for _g in target_area])

            start_grid = (min_x, min_y)

            # 角areaは随時追加していく
            self.kingdom_grid[dkey]['horn'] = []
            self.kingdom_grid[dkey]['horn'].append(start_grid)

            # 進行方向0:東, 1:北, 2:西, 3:南
            next_cnt = 0
            focus_x = min_x
            focus_y = min_y
            # 初期座標、被らない座標を設定
            focus_area = (-1,-1)
            total_num = len(self.kingdom_grid[dkey]['grid'])

            # 角area作成、格納（長い）
            while focus_area != start_grid and len(self.kingdom_grid[dkey]['horn']) < total_num:
                # スタート地点を設定
                if focus_area == (-1, -1):
                    focus_area = start_grid
                # 東向きの場合
                if next_cnt == 0:
                    #focus_x = focus_x + 1
                    # 北に座標が存在する場合
                    if (focus_x, focus_y - 1) in dval['grid']:
                        # 角座標に格納
                        self.kingdom_grid[dkey]['horn'].append(focus_area)
                        # 北の座標をフォーカス設定
                        focus_y = focus_y - 1
                        focus_area = (focus_x, focus_y)
                        next_cnt = 1
                    # 東に進める場合
                    elif (focus_x + 1, focus_y) in dval['grid']:
                        focus_x = focus_x + 1
                        focus_area = (focus_x, focus_y)
                    # 南に座標が存在する場合
                    elif (focus_x, focus_y + 1) in dval['grid']:
                        # 角座標に格納
                        self.kingdom_grid[dkey]['horn'].append(focus_area)
                        # 南の座標をフォーカス設定
                        focus_y = focus_y + 1
                        focus_area = (focus_x, focus_y)
                        next_cnt = 3
                    # 西に座標が存在する場合（角ボタン状態）
                    elif (focus_x - 1, focus_y) in dval['grid']:
                        # 角座標に格納
                        self.kingdom_grid[dkey]['horn'].append(focus_area)
                        # 西の座標をフォーカス設定
                        focus_x = focus_x - 1
                        focus_area = (focus_x, focus_y)
                        next_cnt = 2
                # 北向きの場合
                elif next_cnt == 1:
                    #focus_y = focus_y - 1
                    # 西に座標が存在する場合
                    if (focus_x - 1, focus_y) in dval['grid']:
                        # 角座標に格納
                        self.kingdom_grid[dkey]['horn'].append(focus_area)
                        # 西の座標をフォーカス設定
                        focus_x = focus_x - 1
                        focus_area = (focus_x, focus_y)
                        next_cnt = 2
                    # 北に座標が存在する場合
                    elif (focus_x, focus_y - 1) in dval['grid']:
                        focus_y = focus_y - 1
                        focus_area = (focus_x, focus_y)
                    # 東に座標が存在する場合
                    elif (focus_x + 1, focus_y) in dval['grid']:
                        # 角座標に格納
                        self.kingdom_grid[dkey]['horn'].append(focus_area)
                        # 東の座標をフォーカス設定
                        focus_x = focus_x + 1
                        focus_area = (focus_x, focus_y)
                        next_cnt = 0
                    # 南に座標が存在する場合（角ボタン状態）
                    elif (focus_x, focus_y + 1) in dval['grid']:
                        # 角座標に格納
                        self.kingdom_grid[dkey]['horn'].append(focus_area)
                        # 南の座標をフォーカス設定
                        focus_y = focus_y + 1
                        focus_area = (focus_x, focus_y)
                        next_cnt = 3
                # 西向きの場合
                elif next_cnt == 2:
                    #focus_x = focus_x - 1
                    # 南に座標が存在する場合
                    if (focus_x, focus_y + 1) in dval['grid']:
                        # 角座標に格納
                        self.kingdom_grid[dkey]['horn'].append(focus_area)
                        # 南の座標をフォーカス設定
                        focus_y = focus_y + 1
                        focus_area = (focus_x, focus_y)
                        next_cnt = 3
                    # 西に座標が存在する場合
                    elif (focus_x - 1, focus_y) in dval['grid']:
                        focus_x = focus_x - 1
                        focus_area = (focus_x, focus_y)
                    # 北に座標が存在する場合
                    elif (focus_x, focus_y - 1) in dval['grid']:
                        # 角座標に格納
                        self.kingdom_grid[dkey]['horn'].append(focus_area)
                        # 北の座標をフォーカス設定
                        focus_y = focus_y - 1
                        focus_area = (focus_x, focus_y)
                        next_cnt = 1
                    # 東に座標が存在する場合（角ボタン状態）
                    elif (focus_x + 1, focus_y) in dval['grid']:
                        # 角座標に格納
                        self.kingdom_grid[dkey]['horn'].append(focus_area)
                        # 東の座標をフォーカス設定
                        focus_x = focus_x + 1
                        focus_area = (focus_x, focus_y)
                        next_cnt = 0
                # 南向きの場合
                elif next_cnt == 3:
                    #focus_y = focus_y + 1
                    # 東に座標が存在する場合
                    if (focus_x + 1, focus_y) in dval['grid']:
                        # 角座標に格納
                        self.kingdom_grid[dkey]['horn'].append(focus_area)
                        # 東の座標をフォーカス設定
                        focus_x = focus_x + 1
                        focus_area = (focus_x, focus_y)
                        next_cnt = 0
                    # 南に座標が存在する場合
                    elif (focus_x, focus_y + 1) in dval['grid']:
                        focus_y = focus_y + 1
                        focus_area = (focus_x, focus_y)
                    # 西に座標が存在する場合
                    elif (focus_x - 1, focus_y) in dval['grid']:
                        # 角座標に格納
                        self.kingdom_grid[dkey]['horn'].append(focus_area)
                        # 南の座標をフォーカス設定
                        focus_x = focus_x - 1
                        focus_area = (focus_x, focus_y)
                        next_cnt = 2
                    # 北に座標が存在する場合（角ボタン状態）
                    elif (focus_x, focus_y - 1) in dval['grid']:
                        # 角座標に格納
                        self.kingdom_grid[dkey]['horn'].append(focus_area)
                        # 南の座標をフォーカス設定
                        focus_y = focus_y - 1
                        focus_area = (focus_x, focus_y)
                        next_cnt = 1
            
            # 色分けして描画
            color = colorsCollection[color_cnt]
            self.pw_map.create_polygon(self.kingdom_grid[dkey]['horn'] ,fill = color,tags=dkey)

            color_cnt+=1
            if color_cnt >= len(colorsCollection):
                color_cnt = 0

        # fig, axes = plt.plot(1,4, figsize=(16,4))
        # axes[3].imshow(data10[2:8, 2:8], origin='lower', extent=[1.5, 7.5, 1.5, 7.5])

        # TODO:描画用座標取得

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
        self.lblarea = tk.Label(pw_point,text = 'areas:', bg="#7AC5CD")
        self.lblarea.grid(row=0, column=8, padx=5, pady=2)
        self.entarea = tk.Entry(pw_point, textvariable=self._areas, width = 9, state='readonly')
        self.entarea.grid(row=0, column=9, padx=5, pady=2)

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
        self.cboking = ttk.Combobox(pw_entry, textvariable=self.king_cbo, width=14)
        self.cboking.grid(row=1, column=3, padx=5, pady=2)
        #self.cboking['value'] = self.fi_dao.chooseCharacter(self.start_x,self.start_y,self.stop_x,self.stop_y)
        self.cboking['value'] = self.ch_dao.set_character()
        # capital
        self.lbl9 = tk.Label(pw_entry,text='capital',width=9, bg="#7AC5CD")
        self.lbl9.grid(row=1, column=4, padx=5, pady=2)
        self.ent8 = tk.Entry(pw_entry, textvariable=self.lo.location_id, width=12)
        self.ent8.grid(row=1, column=5, padx=5, pady=2)

        return pw_entry

    # 新規登録処理
    def entryNewKingdom(self):
        
        none_flg = True

        if self.rect_start_x.get() > 0 and self.rect_start_y.get() > 0 and self.rect_stop_x.get() > 0 and self.rect_stop_y.get() > 0:
            
            # 中心座標判定
            l_x = 0
            l_y = 0
            r_x = 0
            r_y = 0
            
            # TODO:面倒だから元結良い方法ないかな入れ替え処理
            if self.rect_start_x.get() <= self.rect_stop_x.get():
                r_x = self.rect_stop_x.get()
                l_x = self.rect_start_x.get()
            else:
                r_x = self.rect_start_x.get()
                l_x = self.rect_stop_x.get()

            if self.rect_start_y.get() < self.rect_stop_y.get():
                r_y = self.rect_stop_y.get()
                l_y = self.rect_start_y.get()
            else:
                r_y = self.rect_start_y.get()
                l_y = self.rect_stop_y.get()
        
            # 重複間引き
            # 新規登録座標取得
            new_area = set()
            new_list = set()

            # 新規座標を格納→短縮できるかも
            for i in range(int(l_x), int(r_x)):
                for j in range(int(l_y), int(r_y)):
                    new_area.add((i,j))
            
            import itertools
            
            # 差集合
            self.setdiff_grid = new_area
            
            # 差風豪、積集合取得
            for dkey, dval in self.kingdom_grid.items():
                
                # 積集合
                self.duplicate_grid[dkey] = new_area.intersection(dval['grid'])
                # 重複データ取得
                self.duplicate_area[dkey] = [data for data in dval['data_list'] if int(l_x) <= data['grid_x'] <= int(r_x) and int(l_y) <= data['grid_y'] <= int(r_y) ]

                # 差集合
                self.setdiff_grid = self.setdiff_grid ^ self.duplicate_grid[dkey]
                # 存在チェック
                if none_flg:
                    if len(self.duplicate_grid[dkey]):
                        none_flg = False
            
            # 重複が存在しない場合
            if none_flg:

                # 登録確認ポップアップ表示
                if bs.Popup.OKCancelPopup(self,Q0004) == False:
                    # いいえを選択した場合、描画した図形を削除
                    # self.init()
                    return
            else:
                # 上書きフラグONOFF
                self.overWrite_flg = bs.Popup.YesNoCancelPopup(self,Q0005)
                # キャンセルの場合
                if self.overWrite_flg == None:
                    return
            
            # ④登録用fieldsデータを作成(新規なのでほぼ③の数値(集計)となる)
            entry_field = self.newFields(l_x,l_y,r_x,r_y)
            # ③登録用locationsデータを作成→王都面積に比例、中心座標(①、②のデータの集計)
            entry_location = self.newLocations(l_x,l_y,r_x,r_y,entry_field[0])
            # ①登録用areasデータを作成
            # ②登録用spotsデータを作成(①のデータ件数×25)
            #future_list = []
            """
            with futures.ThreadPoolExecutor(max_workers=4) as executor:
                for i in range(l_x, r_x):
                    for j in range(l_y, r_y):
                        future = executor.submit(fn=self.newMapping, i_x=i, i_y=j)
                        future_list.append(future.result)
                _ = futures.as_completed(fs=future_list)

            # 中心座標エラー
            #bs.Popup.ShowInfo(self,E0004.format(X,Y))
            """
            print('complete!')
            # 初期化
            self.init()
            # 再検索
            self.drawMap()

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
        population = self.ch_dao.get_population(l_x,l_y,r_x,r_y)
        # 王国登録要素を表示
        entry_list = []
        entry_list.append(
            {
                "field_name":self.fi.field_name.get(),
                "f_rank":self.fi.f_rank.get(),
                "king_gene_id":self.ch.gene_id.get(),
                "character_id":self.ch.id.get(),
                "contract_id":self.fi.contract_id.get(),
                "is_war":self.fi.is_war.get(),
                "area":abs(r_x - l_x) * abs(r_y - l_y),
                "population":population,
                "p_density":int(population / ((r_x-l_x) * (r_y - l_y))),
                "stress":self.fi.stress.get(),
                "hate":self.fi.hate.get(),
                "power":self.fi.power.get(),
                "welfare":self.fi.welfare.get(),
                "technology":self.fi.technology.get(),
                "military":self.fi.military.get(),
                "civil_point":self.fi.civil_point.get(),
                "civilization":self.fi.civilization.get(),
                "innovation":self.fi.innovation.get(),
                "strength":self.fi.strength.get(),
                "assets":self.fi.assets.get(),
                "GDP":0,
                "tax":0,
                "disparity":0,
                "develop":0,
                "version":1,
                "is_deleted":0,
                "ins_date":datetime.now(),
                "ins_id":"dummy",
                "upd_date":datetime.now(),
                "upd_id":"dummy"
            }
        )

        return self.fi_dao.insert_field(entry_list)
        """
        try:
            self.fi_dao.insert_field(entry_list)
        except:
            # OKポップアップ
            messagebox.showinfo('警告', E0002)
        """

    # 王都作成
    def newLocations(self,l_x,l_y,r_x,r_y,field_data):

        # 王都作成
        capital_list = []
        capital_list.append(
            {
                # capitalの値も登録データからとってきた方がいいかも
                "field_id" : field_data['field_id'],
                "lord_gene_id" : field_data['king_gene_id'],
                "character_id" : field_data['character_id'],
                "location_name" : self.lo.location_name.get(),
                "l_rank" : self.lo.l_rank.get(),
                "is_battle" : self.lo.is_battle.get(),
                "area" : self.lo.area.get(),
                "population" : self.lo.population.get(),
                "p_density" : self.lo.p_density.get(),
                "stress":self.fi.stress.get(),
                "hate":self.fi.hate.get(),
                "power":self.fi.power.get(),
                "welfare":self.fi.welfare.get(),
                "technology":self.fi.technology.get(),
                "military":self.fi.military.get(),
                "civil_point":self.fi.civil_point.get(),
                "civilization":self.fi.civilization.get(),
                "innovation":self.fi.innovation.get(),
                "strength":self.fi.strength.get(),
                "assets":self.fi.assets.get(),
                "GDP" : self.fi.GDP.get(),
                "tax" : self.fi.tax.get(),
                "develop" : self.fi.develop.get(),
                "disparity" : self.fi.disparity.get(),
                "version":1,
                "is_deleted":0,
                "ins_date":datetime.now(),
                "ins_id":"dummy",
                "upd_date":datetime.now(),
                "upd_id":"dummy"
            }
        )
        # TODO:location_idを取ってくる
        imput_location = self.lo_dao.insert_location(capital_list)
        input_l = imput_location[0]
        
        # locations-areas
        future_list = []
        future2_list = []
        # loop要
        location_id = input_l["location_id"]
        field_id = input_l["field_id"]
        landlord_gene_id = input_l["lord_gene_id"]
        character_id = input_l["character_id"]
        
        """
        # バルクイン用csv作成
        # ★CSVは封印
        a_name = 'area_'+ datetime.now().strftime('%Y%m%d%H%M%S') + '.csv'
        s_name = 'spot_'+ datetime.now().strftime("%Y%m%d%H%M%S") + '.csv'
        a_path = Path(self.root + '/CSV/create_areas/' + a_name)
        s_path = Path(self.root + '/CSV/create_spots/' + s_name)
        a_file = open(a_path, 'w')
        s_file = open(s_path, 'w')
        a_writer = csv.writer(a_file)
        s_writer = csv.writer(s_file)
        """

        with futures.ThreadPoolExecutor(
            max_workers=4) as executor:
            # 王国の中心x,y1/5スケールで王都を作成
            l_k_x = int(l_x + abs(r_x - l_x) * 2 / 5)
            r_k_x = int(r_x - abs(r_x - l_x) * 2 / 5)
            l_k_y = int(l_y + abs(r_y - l_y) * 2 / 5)
            r_k_y = int(r_y - abs(r_y - l_y) * 2 / 5)

            print('map loading...')
            
            # 上書きを考慮した処理
            if self.overWrite_flg:

                entry_area = []
                entry_spot = []

                # データ編集
                print('start update')
                for dkey, dval in self.duplicate_area.items():

                    for data in dval:
                        
                        if int(l_k_x) <= data['grid_x'] <= int(r_k_x) and int(l_k_y) <= data['grid_y'] <= int(r_k_y):
                            data['field_id'] = field_id
                            data['location_id'] = location_id
                        else:
                            data['field_id'] = field_id

                        data['upd_id'] = "dummy"
                        data['upd_date'] = datetime.now()
                    
                        entry_area.append(data.values())
                
                # spot更新
                spots = self.sp_dao.select_data(l_x, r_x, l_y, r_y)

                # TODO:kingdom_grid使わない方が簡単じゃね？
                for data in spots:
                        
                    if int(l_k_x) <= data['grid_x'] <= int(r_k_x) and int(l_k_y) <= data['grid_y'] <= int(r_k_y):
                        data['field_id'] = field_id
                        data['location_id'] = location_id
                    else:
                        data['field_id'] = field_id

                    data['upd_id'] = "dummy"
                    data['upd_date'] = datetime.now()
                
                    entry_spot.append(data.values())

                # 削除処理
                self.ar_dao.dupplicate_delete(l_x, r_x, l_y, r_y)
                self.sp_dao.dupplicate_delete(l_x, r_x, l_y, r_y)
                # 登録処理
                self.ar_dao.bulk_insert_areas(entry_area)
                self.sp_dao.bulk_insert_spots(entry_spot)
                    
                #self.update_dupplicate(dkey, field_id, location_id, dval)
                print('end update')
                
            
            # 純粋データの登録
            for data in self.setdiff_grid:
                i = data[0]
                j = data[1]
                """
                future_list.append(
                    {
                        "grid_x":i,
                        "grid_y":j,
                        "location_id":location_id,
                        "field_id":field_id,
                        "is_maxHeight":0,
                        "height":0,
                        "is_river":0,
                        "depth":0,
                        "landlord_gene_id":landlord_gene_id,
                        "character_id":character_id,
                        "assets":0,
                        "civil_point":0,
                        "family":0,
                        "is_public":0,
                        "version":1,
                        "is_deleted":0,
                        "ins_date":datetime.now(),
                        "ins_id":"dummy",
                        "upd_date":datetime.now(),
                        "upd_id":"dummy"

                    }
                )
                """
                if (l_k_x <= i and i <= r_k_x) and (l_k_y <= j and j <= r_k_y):
                    future_list.append(
                        [ i, j, location_id, field_id, 0, 0, 0, 0, landlord_gene_id, character_id, 0, 0, 0, 0, 1, 0,None ,None ,None ,None ]
                    )
                else:
                    future_list.append(
                        [i, j, 0, field_id, 0, 0, 0, 0, 0, character_id, 0, 0, 0, 0, 1, 0,None ,None ,None ,None ]
                    )
                

                for i2 in range(0,4):
                    for j2 in range(0,4):
                        """
                        future2_list.append(
                            {
                                "sgrid_x":i2,
                                "sgrid_y":j2,
                                "location_id":location_id,
                                "field_id":field_id,
                                "grid_x":i,
                                "grid_y":j,
                                "building_id":0,
                                "assets":0,
                                "civil_point":0,
                                "f_count":0,
                                "is_public":0,
                                "version":1,
                                "is_deleted":0,
                                "ins_date":datetime.now(),
                                "ins_id":"dummy",
                                "upd_date":datetime.now(),
                                "upd_id":"dummy"
                            }
                        )
                        """
                        future2_list.append(
                            [str(i)+'-'+str(j)+'-'+str(i2)+'-'+str(j2), i2, j2, location_id, field_id, i, j, 0, 0, 0, 0, 0, 1, 0, None, None, None, None ]
                        )
            """
            # csv書き込み
            a_writer.writerows(future_list)
            s_writer.writerows(future2_list)
            a_file.close()
            s_file.close()
            """
            # areaバルクイン
            self.ar_dao.bulk_insert_areas(future_list)
            # spotバルクイン
            self.sp_dao.bulk_insert_spots(future2_list)
    
    # 重複データを更新
    def update_dupplicate(self,bk_kingdom_id, new_kingdom_id, new_location_id, target_grids):

        # select
        pass
        #self.ar_dao.updateArea(bk_kingdom_id, new_kingdom_id, new_location_id, target_grids)
        #self.sp_dao.updateSpot(bk_kingdom_id, new_kingdom_id, new_location_id, target_grids)
    
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


        self.lbl_title = tk.Label(pw_right_up,text="Country",width=9, bg="pink")
        self.lbl_title.grid(row=0, column=0, padx=5, pady=2, columnspan = 4)
        self.lbl_comment = tk.Label(pw_right_up,text="civilizationは0～25で入力してください", bg="pink")
        self.lbl_comment.grid(row=1, column=0, padx=5, pady=2, columnspan = 4)
        
        # civilization
        self.lblcivi = tk.Label(pw_right_up,text="civilization",width=9)
        self.lblcivi.grid(row=2, column=0, padx=5, pady=2)
        self.entcivi = tk.Entry(pw_right_up, textvariable=self.fi.civilization,  width=12)
        self.entcivi.grid(row=2, column=1, padx=5, pady=2)
        
        # rank
        self.lbl9 = tk.Label(pw_right_up,text="rank",width=9)
        self.lbl9.grid(row=2, column=2, padx=5, pady=2)
        self.ent9 = tk.Entry(pw_right_up, textvariable=self.fi.f_rank,  width=12)
        self.ent9.grid(row=2, column=3, padx=5, pady=2)
        self.ent9.configure(state = 'readonly')
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
        self.ent13.configure(state = 'disabled')
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
        # strength(合計値と同義)
        self.lbltotal = tk.Label(pw_right_up,text="strength",width=9)
        self.lbltotal.grid(row=6, column=2, padx=5, pady=2)
        self.enttotal = tk.Entry(pw_right_up, textvariable=self.fi.strength,  width=12)
        self.enttotal.grid(row=6, column=3, padx=5, pady=2)
        self.enttotal.configure(state = 'disabled')

        # 状態値
        self.lbl_st = tk.Label(pw_right_up,text="Status",width=9)
        self.lbl_st.grid(row=7, column=0, padx=5, pady=2, columnspan = 4)
        # stress
        self.lbl15 = tk.Label(pw_right_up,text="stress",width=9)
        self.lbl15.grid(row=8, column=0, padx=5, pady=2)
        self.ent15 = tk.Entry(pw_right_up, textvariable=self.fi.stress,  width=12)
        self.ent15.grid(row=8, column=1, padx=5, pady=2)
        # hate
        self.lbl16 = tk.Label(pw_right_up,text="hate",width=9)
        self.lbl16.grid(row=8, column=2, padx=5, pady=2)
        self.ent16 = tk.Entry(pw_right_up, textvariable=self.fi.hate,  width=12)
        self.ent16.grid(row=8, column=3, padx=5, pady=2)

        return pw_right_up

    def createButton(self, pw_right):
        pw_right_up4 = tk.PanedWindow(pw_right, bg="pink", orient='horizontal')

        # ランダム生成
        self.lbl17 = tk.Label(pw_right_up4,text="ランダム生成",width=9)
        self.lbl17.grid(row=0, column=0, columnspan=2, padx=5, pady=2)
        
        # 傾きラベル
        self.lblTlt = tk.Label(pw_right_up4,text="tilt",width=5)
        self.lblTlt.grid(row=1, column=0, padx=5, pady=2)
        
        # 傾きスケールの作成
        self.scTilt = ttk.Scale(
            pw_right_up4,
            variable=self.tilt,
            orient=tk.HORIZONTAL,
            length=250,
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
        self.lblWeight = tk.Label(pw_right_up4,text="weight",width=5)
        self.lblWeight.grid(row=2, column=0, padx=5, pady=2)

        # 重みスケールの作成
        self.scWeight = ttk.Scale(
            pw_right_up4,
            variable=self.val,
            orient=tk.HORIZONTAL,
            length=250,
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

    # 仮
    def set_f_rank(self,data):

        if int(data) > 500000000:
            self.fi.f_rank.set('SSS')
        elif int(data)  > 50000000:
            self.fi.f_rank.set('SS')
        elif int(data)  > 10000000:
            self.fi.f_rank.set('S')
        elif int(data)  > 2500000:
            self.fi.f_rank.set('A')
        elif int(data)  > 1000000:
            self.fi.f_rank.set('B')
        elif int(data)  > 450000:
            self.fi.f_rank.set('C')
        elif int(data)  > 150000:
            self.fi.f_rank.set('D')
        elif int(data)  > 62500:
            self.fi.f_rank.set('E')
        elif int(data)  > 12500:
            self.fi.f_rank.set('F')
        else:
            self.fi.f_rank.set('G')

        # self.ch_status_set(text_label,self.fi.f_rank.get())

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

    # 進化レベル設定（基準）
    def randomLevel(self):

        self.fi.civilization.set(random.randint(1,25))

    # 王国表示処理
    def entryField(self):

        # 登録完了ポップアップ表示
        bs.Popup.ShowInfo(self,I0002)
        
        # 再検索を実施
        self.init()
        self.drawMap()

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
        self.init()
        self.drawMap()

    # ランダム生成押下時
    def randomNum(self):
        # weight = 1.5 # 超レアガチャ
        # weight = 2   # 高レアガチャ
        # weight = 3   # レアガチャ
        # weight = random.random() + 100   # ノーマルガチャ

        # 選択可能ランク
        # TODO：チョイス可能に設定する
        # acquired_rank = self.getFieldRank(self.fi.civilization.get())
        
        # 重み付けローカル変数
        val = self.val.get()

        reg_field = {}
        reg_field['f_power'] = 1
        reg_field['f_welfare'] = 1
        reg_field['f_technology'] = 1
        reg_field['f_military'] = 1
        reg_field['f_assets'] = 1
        reg_field['f_innovation'] = 1
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
                reg_field['f_power'] = self.rand_num(5,weight)
                reg_field['f_welfare'] = self.rand_num(5,weight)
                reg_field['f_technology'] = self.rand_num(5,weight)
                reg_field['f_military'] = self.rand_num(5,weight)
                reg_field['f_assets'] = self.rand_num(5,weight)
                reg_field['f_innovation'] = self.rand_num(5,weight)

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
                reg_field['f_power'] = self.rand_num(5,weight)
                reg_field['f_welfare'] = self.rand_num(5,weight)
                reg_field['f_technology'] = self.rand_num(5,weight)
                reg_field['f_military'] = self.rand_num(5,weight)
                reg_field['f_assets'] = self.rand_num(5,weight)
                reg_field['f_innovation'] = self.rand_num(5,weight)

                # 新規の場合ブレーク条件
                # if self.getOneRank(sum(reg_field.values())) in acquired_rank and sum(reg_field.values()) > self.fi.civil_point.get():
                #     break

                # weight回復
                if sum(reg_field.values()) <= 0:
                    val = val + i*0.2
            
        self.fi.power.set(reg_field['f_power'])
        self.fi.welfare.set(reg_field['f_welfare'])
        self.fi.technology.set(reg_field['f_technology'])
        self.fi.military.set(reg_field['f_military'])
        self.fi.assets.set(reg_field['f_assets'])
        self.fi.innovation.set(reg_field['f_innovation'])
        self.fi.strength.set(sum(reg_field.values()))

        self.randomLevel()

        # totalからrankを設定
        self.set_f_rank(self.fi.civilization.get())
        # 旧ランク算出法
        # self.fi.f_rank.set(self.getOneRank(self.fi.strength.get()))

    def rand_num(self, num, weight):

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
    def fi_status_set(self,entry_text, input_num, num):
        if len(str(input_num)) > 0:
            # 不適切な値の場合は1に設定
            if not str(input_num).isdecimal():
                entry_text.set(1)
            if int(str(input_num)) <= 0:
                entry_text.set(1)
            # 100より大きい数字が入力されたら100に
            elif int(str(input_num)) > self._areas.get()*num:
                entry_text.set(self._areas.get()*num)
            entry_text.set(str(input_num)[:8])
            
            try:
                # strength
                self.fi.strength.set(str(int(self.fi.power.get())+int(self.fi.technology.get())
                +int(self.fi.welfare.get())+int(self.fi.military.get())+int(self.fi.innovation.get())
                +int(self.fi.assets.get())))

                self.total = self.fi.strength.get()
   
            except:
                pass

            self.set_f_rank(self.fi.strength.get()*self.fi.civilization.get())

    # マウスイベント
    def rect_start_pickup(self, event):
        self.rect_start_x.set(str(event.x))
        self.rect_start_y.set(str(event.y))
        self.start_x = event.x
        self.start_y = event.y

    # 正方形描画処理★
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

        l_x = 0
        l_y = 0
        r_x = 0
        r_y = 0
        
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
        
        self._areas.set(int((r_x - l_x) * (r_y - l_y)))

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
