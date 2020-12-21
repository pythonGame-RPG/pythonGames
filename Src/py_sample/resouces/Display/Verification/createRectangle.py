# 正方形描画処理★
import tkinter as tk
import tkinter.ttk as ttk

# ★追加
colorsCollection=['green yellow','yellow','orange','pink','medium purple','cyan','aquamarine']

class createRectangle():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('create_polygon')
        self.rect = None
        self.rect_start_x = tk.StringVar()
        self.rect_start_y = tk.StringVar()
        self.rect_stop_x = tk.StringVar()
        self.rect_stop_y = tk.StringVar()
        self.start_x = 0
        self.start_y = 0
        self.stop_x = 0
        self.stop_y = 0

        # ★追加
        self.areas = tk.StringVar()
        self.fields = []
        self.field_data = {'grid':set(), 'horn':[], 'grid_x':[], 'area':0}

        self.createDisplay()
        self.root.mainloop()
    
    # 画面を描画
    def createDisplay(self):
        # ウィンドウを分ける
        self.pw_main = tk.PanedWindow(self.root, orient='vertical')
        self.pw_main.pack(expand=True, fill = tk.BOTH, side="left")

        _pw = self.draw_rectangle(self.pw_main)
        self.pw_main.add(_pw)

        # 座標部
        _pw_grid = self.draw_point(self.pw_main)
        self.pw_main.add(_pw_grid)

        # 追加：面積
        _pw_grid = self.draw_area(self.pw_main)
        self.pw_main.add(_pw_grid)

        # 画面初期化
        # self.init()

    # 長方形を描画
    def draw_rectangle(self,_pw):

        _pw_up = tk.PanedWindow(_pw, bg="pink", orient='horizontal')
        
        self.lblmap = tk.Label(_pw_up,text = 'map')
        self.lblmap.grid(row=0, column=2, padx=5, pady=2)
        
        # マップ描画処理
        self.pw_map = tk.Canvas(_pw_up, width=480, height=300,borderwidth=10) # , relief='sunken'
        self.pw_map.grid(row=1, column=2, padx=5, pady=2)
        self.pw_map.bind('<Button-1>', self.rect_start_pickup)
        self.pw_map.bind('<B1-Motion>', self.pickup_position)
        self.pw_map.bind('<ButtonRelease-1>', self.rect_stop_pickup)

        return _pw_up
    
    # 座標を表示
    def draw_point(self,_pw_grid):

        pw_point = tk.PanedWindow(_pw_grid, bg="#7AC5CD", orient='horizontal')

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
        # 初期化ボタン
        self.btnReset = ttk.Button(pw_point, text='リセット', width=10, style='MyWidget.TButton', command=self.button_init)
        self.btnReset.grid(row=0, column=8, padx=5, pady=2)
        # ★追加：初期化ボタン
        self.btnReset = ttk.Button(pw_point, text='一つ削除', width=10, style='MyWidget.TButton', command=self.button_delete)
        self.btnReset.grid(row=0, column=9, padx=5, pady=2)

        return pw_point
    
    # 追加：描画図形面積表示
    def draw_area(self, _pw_area):
        
        _pw_area = tk.PanedWindow(_pw_area, bg="#7AC5CD", orient='horizontal')

        self.lbl_a = tk.Label(_pw_area, text="面積：", bg="#7AC5CD")
        self.lbl_a.grid(row=0, column=0, padx=5, pady=2)  
        self.txt_area = tk.Text(_pw_area, width = 60,height=3, bg="white")
        self.txt_area.grid(row=0, column=2, padx=5, pady=2)
        self.txt_area.insert('1.0',str(self.areas.get()))
        scroll = tk.Scrollbar(self.txt_area, orient=tk.VERTICAL)
        self.txt_area.configure(yscrollcommand = scroll.set)

        #, textvariable=self.areas
        return _pw_area

    # マウスイベント・開始
    def rect_start_pickup(self, event):
        self.rect_start_x.set(str(event.x))
        self.rect_start_y.set(str(event.y))
        self.start_x = event.x
        self.start_y = event.y

    # マウスイベント・ドラッグ中
    def pickup_position(self, event):
        self.rect_stop_x.set(str(event.x))
        self.rect_stop_y.set(str(event.y))

        if self.rect:
            self.pw_map.coords(self.rect,
                min(self.start_x, event.x), min(self.start_y, event.y),
                max(self.start_x, event.x), max(self.start_y, event.y))
        else:
            self.rect = self.pw_map.create_rectangle(self.start_x,
                self.start_y, event.x, event.y, outline='red')
    
    # マウスイベント・終了
    def rect_stop_pickup(self, event):
        
        self.rect_stop_x.set(str(event.x))
        self.rect_stop_y.set(str(event.y))

        # ★追加
        # 中心座標判定
        l_x = int(self.rect_start_x.get())
        l_y = int(self.rect_start_y.get())
        r_x = int(self.rect_stop_x.get())
        r_y = int(self.rect_stop_y.get())

        # 座標を追加
        for x in range(min(l_x,r_x), max(l_x,r_x)):
            for y in range(min(l_y,r_y), max(l_y,r_y)):
                self.field_data['grid'].add((x,y))
                # あとで使うのでx座標も追加
                self.field_data['grid_x'].append(x)
        
        # 座標数をカウント
        self.field_data['area'] = len(self.field_data['grid'])
        
        # 重複した場合上書き処理
        for dkey, dval in enumerate(self.fields):
            # 初期化
            self.fields[dkey] = {'grid':set(), 'horn':[], 'grid_x':[], 'area':0}
            # 重複した座標を取得
            dupplicate_fields = dval['grid'].intersection(self.field_data['grid'])
            self.fields[dkey]['grid'] = dval['grid'].difference(dupplicate_fields)
            self.fields[dkey]['grid_x'] = [d[0] for d in list(self.fields[dkey]['grid'])]
            self.fields[dkey]['area'] = len(self.fields[dkey]['grid'])
        
        # 面積が0のデータを除外
        self.fields = [data for data in self.fields if data['area'] > 0]
        self.fields.append(self.field_data)

        self.draw_datas()

    # ★追加
    def draw_datas(self):

        self.pw_map.delete("all")
        # 色判別用
        color_cnt = 0

        # 外周取得処理
        for data in self.fields:
            min_x = min(data['grid_x'])
            target_area = [_area for _area in list(data['grid']) if _area[0] == min_x]
            try:
                min_y = min([_g[1] for _g in target_area])
            except Exception as e:
                print('はみ出してますよ')

            start_grid = (min_x, min_y)

            # 角areaは随時追加していく
            data['horn'].append(start_grid)

            # 進行方向0:東, 1:北, 2:西, 3:南
            next_cnt = 0
            focus_x = min_x
            focus_y = min_y
            # 初期座標、被らない座標を設定
            focus_area = (-1,-1)

            while focus_area != start_grid:
                # スタート地点を設定
                if focus_area == (-1, -1):
                    focus_area = start_grid
                # 東向きの場合
                if next_cnt == 0:
                    #focus_x = focus_x + 1
                    # 北に座標が存在する場合
                    if (focus_x, focus_y - 1) in data['grid']:
                        # 角座標に格納
                        data['horn'].append(focus_area)
                        # 北の座標をフォーカス設定
                        focus_y = focus_y - 1
                        focus_area = (focus_x, focus_y)
                        next_cnt = 1
                    # 東に進める場合
                    elif (focus_x + 1, focus_y) in data['grid']:
                        focus_x = focus_x + 1
                        focus_area = (focus_x, focus_y)
                    # 南に座標が存在する場合
                    elif (focus_x, focus_y + 1) in data['grid']:
                        # 角座標に格納
                        data['horn'].append(focus_area)
                        # 南の座標をフォーカス設定
                        focus_y = focus_y + 1
                        focus_area = (focus_x, focus_y)
                        next_cnt = 3
                    # 西に座標が存在する場合（角ボタン状態）
                    elif (focus_x - 1, focus_y) in data['grid']:
                        # 角座標に格納
                        data['horn'].append(focus_area)
                        # 西の座標をフォーカス設定
                        focus_x = focus_x - 1
                        focus_area = (focus_x, focus_y)
                        next_cnt = 2
                # 北向きの場合
                elif next_cnt == 1:
                    #focus_y = focus_y - 1
                    # 西に座標が存在する場合
                    if (focus_x - 1, focus_y) in data['grid']:
                        # 角座標に格納
                        data['horn'].append(focus_area)
                        # 西の座標をフォーカス設定
                        focus_x = focus_x - 1
                        focus_area = (focus_x, focus_y)
                        next_cnt = 2
                    # 北に座標が存在する場合
                    elif (focus_x, focus_y - 1) in data['grid']:
                        focus_y = focus_y - 1
                        focus_area = (focus_x, focus_y)
                    # 東に座標が存在する場合
                    elif (focus_x + 1, focus_y) in data['grid']:
                        # 角座標に格納
                        data['horn'].append(focus_area)
                        # 東の座標をフォーカス設定
                        focus_x = focus_x + 1
                        focus_area = (focus_x, focus_y)
                        next_cnt = 0
                    # 南に座標が存在する場合（角ボタン状態）
                    elif (focus_x, focus_y + 1) in data['grid']:
                        # 角座標に格納
                        data['horn'].append(focus_area)
                        # 南の座標をフォーカス設定
                        focus_y = focus_y + 1
                        focus_area = (focus_x, focus_y)
                        next_cnt = 3
                # 西向きの場合
                elif next_cnt == 2:
                    #focus_x = focus_x - 1
                    # 南に座標が存在する場合
                    if (focus_x, focus_y + 1) in data['grid']:
                        # 角座標に格納
                        data['horn'].append(focus_area)
                        # 南の座標をフォーカス設定
                        focus_y = focus_y + 1
                        focus_area = (focus_x, focus_y)
                        next_cnt = 3
                    # 西に座標が存在する場合
                    elif (focus_x - 1, focus_y) in data['grid']:
                        focus_x = focus_x - 1
                        focus_area = (focus_x, focus_y)
                    # 北に座標が存在する場合
                    elif (focus_x, focus_y - 1) in data['grid']:
                        # 角座標に格納
                        data['horn'].append(focus_area)
                        # 北の座標をフォーカス設定
                        focus_y = focus_y - 1
                        focus_area = (focus_x, focus_y)
                        next_cnt = 1
                    # 東に座標が存在する場合（角ボタン状態）
                    elif (focus_x + 1, focus_y) in data['grid']:
                        # 角座標に格納
                        data['horn'].append(focus_area)
                        # 東の座標をフォーカス設定
                        focus_x = focus_x + 1
                        focus_area = (focus_x, focus_y)
                        next_cnt = 0
                # 南向きの場合
                elif next_cnt == 3:
                    #focus_y = focus_y + 1
                    # 東に座標が存在する場合
                    if (focus_x + 1, focus_y) in data['grid']:
                        # 角座標に格納
                        data['horn'].append(focus_area)
                        # 東の座標をフォーカス設定
                        focus_x = focus_x + 1
                        focus_area = (focus_x, focus_y)
                        next_cnt = 0
                    # 南に座標が存在する場合
                    elif (focus_x, focus_y + 1) in data['grid']:
                        focus_y = focus_y + 1
                        focus_area = (focus_x, focus_y)
                    # 西に座標が存在する場合
                    elif (focus_x - 1, focus_y) in data['grid']:
                        # 角座標に格納
                        data['horn'].append(focus_area)
                        # 南の座標をフォーカス設定
                        focus_x = focus_x - 1
                        focus_area = (focus_x, focus_y)
                        next_cnt = 2
                    # 北に座標が存在する場合（角ボタン状態）
                    elif (focus_x, focus_y - 1) in data['grid']:
                        # 角座標に格納
                        data['horn'].append(focus_area)
                        # 南の座標をフォーカス設定
                        focus_y = focus_y - 1
                        focus_area = (focus_x, focus_y)
                        next_cnt = 1
            
            # 色分けして描画
            color = colorsCollection[color_cnt]
            self.pw_map.create_polygon(data['horn'] ,fill = color)

            color_cnt+=1
            if color_cnt >= len(colorsCollection):
                color_cnt = 0
            
            self.init()
            
        # 面積を出力
        str_area = ''
        for dkey, dval in enumerate(self.fields):
            str_area = str_area + str(dkey+1) + '番目の図形：' + str(dval['area']) + ", "
        
        self.areas.set(str_area[:-2])
        self.txt_area.delete("1.0",tk.END)
        self.txt_area.insert("1.0",self.areas.get())
        
    # リセットボタン処理
    def init(self):
        self.pw_map.delete(self.rect)
        self.rect = None
        # ★追加
        self.field_data = {'grid':set(), 'horn':[], 'grid_x':[], 'area':0}
    
    # 追加
    def button_init(self):
        self.pw_map.delete("all")
        self.fields.clear()
        self.rect_start_x.set(0)
        self.rect_start_y.set(0)
        self.rect_stop_x.set(0)
        self.rect_stop_y.set(0)
        self.start_x = 0
        self.start_y = 0
        self.stop_x = 0
        self.stop_y = 0
        self.txt_area.delete("1.0",tk.END)
        self.init()
    
    # 一つ前を削除
    def button_delete(self):
        self.fields.pop(-1)
        self.draw_datas()

if __name__ == '__main__':
    c = createRectangle()