from settings import *
import tkinter as tk
import tkinter.ttk as ttk
import datetime
import random
import DAO.racesDAO as _races
import DTO.races as races
import Base.basic_module as bs

selected_d = ''

# カレンダーを作成するフレームクラス
class create_race():
    def __init__(self,parent):

        import datetime
        self.parent = parent
        self.dialog = None
        self.targetRa = tk.StringVar()
        self.mode = tk.IntVar()
        self.evoLevel = tk.IntVar()
        self.choosedRace = tk.StringVar()
        self.val = tk.DoubleVar()
        self.tilt = tk.DoubleVar()
        self.iid=""
        self.bk_iid=""
        self.rootiid=""
        self.raceRoot = {}
        self.raceTree = {}
        self.s_race = []
        self.bs = bs.MyStack()
        # フレーム
        self.pw_left = None
        self.pw_main = None

        # 表示ラベル編集用
        self.HP = tk.StringVar()
        self.MP = tk.StringVar()
        self.sta = tk.StringVar()
        self.atk = tk.StringVar()
        self.vit = tk.StringVar()
        self.mag = tk.StringVar()
        self.des = tk.StringVar()
        self.agi = tk.StringVar()
        self.p_total = tk.StringVar()
        self.r_rank = tk.StringVar()
        self.HP.set('HP')
        self.MP.set('MP')
        self.sta.set('sta')
        self.atk.set('atk')
        self.vit.set('vit')
        self.mag.set('mag')
        self.des.set('des')
        self.agi.set('agi')
        self.p_total.set('total')
        self.r_rank.set('rank')
        self.HP_label = {'HP':self.HP}
        self.MP_label = {'MP':self.MP}
        self.sta_label = {'sta':self.sta}
        self.atk_label = {'atk':self.atk}
        self.vit_label = {'vit':self.vit}
        self.mag_label = {'mag':self.mag}
        self.des_label = {'des':self.des}
        self.agi_label = {'agi':self.agi}
        self.total_label = {'total':self.p_total}
        self.rank_label = {'total':self.r_rank}

        # DBアクセス用
        self.ra = races.Race()
        self.bk_ra = races.Race()
        self.entry_ra = races.Race()
        self.ra_dao = _races.RaceDAO()

        self.entry_ra.p_HP.trace("w", lambda *args: self.character_limit(self.entry_ra.p_HP, 5))
        self.entry_ra.p_MP.trace("w", lambda *args: self.character_limit(self.entry_ra.p_MP, 5))
        self.entry_ra.p_sta.trace("w", lambda *args: self.character_limit(self.entry_ra.p_sta, 5))
        self.entry_ra.p_atk.trace("w", lambda *args: self.character_limit(self.entry_ra.p_atk, 5))
        self.entry_ra.p_vit.trace("w", lambda *args: self.character_limit(self.entry_ra.p_vit, 5))
        self.entry_ra.p_mag.trace("w", lambda *args: self.character_limit(self.entry_ra.p_mag, 5))
        self.entry_ra.p_des.trace("w", lambda *args: self.character_limit(self.entry_ra.p_des, 5))
        self.entry_ra.p_agi.trace("w", lambda *args: self.character_limit(self.entry_ra.p_agi, 5))

        # ラベル用イベント
        self.ra.p_HP.trace("w", lambda *args: self.ch_status_set(self.HP_label,self.ra.p_HP.get()))
        self.ra.p_MP.trace("w", lambda *args: self.ch_status_set(self.MP_label,self.ra.p_MP.get()))
        self.ra.p_sta.trace("w", lambda *args: self.ch_status_set(self.sta_label,self.ra.p_sta.get()))
        self.ra.p_atk.trace("w", lambda *args: self.ch_status_set(self.atk_label,self.ra.p_atk.get()))
        self.ra.p_vit.trace("w", lambda *args: self.ch_status_set(self.vit_label,self.ra.p_vit.get()))
        self.ra.p_mag.trace("w", lambda *args: self.ch_status_set(self.mag_label,self.ra.p_mag.get()))
        self.ra.p_des.trace("w", lambda *args: self.ch_status_set(self.des_label,self.ra.p_des.get()))
        self.ra.p_agi.trace("w", lambda *args: self.ch_status_set(self.agi_label,self.ra.p_agi.get()))
        self.ra.total_pattern.trace("w", lambda *args: self.ch_status_set(self.total_label,self.ra.total_pattern.get()))
        self.ra.r_rank.trace("w", lambda *args: self.ch_status_set(self.rank_label,self.ra.r_rank.get()))

        #モード変更イベント
        #self.mode.trace("w", lambda *args: self.changeMode())


    def openDialog(self):        
       # 子画面クラス
        self.window = tk.Toplevel(self.parent)
        self.window.geometry('500x540')
        self.window.title("Race App")
        
        self.createDisplay()
        
        # TODO:いらなくなったら消す
        self.parent.mainloop()
    
    def createDisplay(self):
        # ウィンドウを分ける
        self.pw_main = tk.PanedWindow(self.window, orient='horizontal')
        self.pw_main.pack(expand=True, fill = tk.BOTH, side="left")

        # self.window→pw_left（左画面ツリービュー）
        self.pw_left = self.createTreeView(self.pw_main)
        self.pw_main.add(self.pw_left)

        # self.window→pw_right（右画面ツリービュー）
        pw_right = tk.PanedWindow(self.pw_main, bg="yellow", orient='vertical')
        self.pw_main.add(pw_right)

        # self.window→pw_right_up1（右上画面モード選択）
        pw_right_up1 = self.setMode(pw_right)
        pw_right.add(pw_right_up1)

        # self.window→pw_right_up2（右上画面登録部）
        pw_right_up2 = self.createStatus(pw_right)
        pw_right.add(pw_right_up2)

        # self.window→pw_right_up3（右下画面登録部）
        pw_right_up3 = self.createRace(pw_right)
        pw_right.add(pw_right_up3)

        # self.window→pw_right_up4（右下画面ボタン部）
        pw_right_up4 = self.createButton(pw_right)
        pw_right.add(pw_right_up4)

    def createTreeView(self, pw_main):
        treeFrame = tk.PanedWindow(pw_main, bg="cyan", orient='vertical')
        # 検索したraceをツリーに表示
        self.setSearchTree(treeFrame)
        return treeFrame

    # ツリーデータ検索
    def setSearchTree(self, treeFrame):
        self.tree = ttk.Treeview(treeFrame)
        # ツリーの項目が選択されたら、選択された種族を表示する
        self.tree.bind("<<TreeviewSelect>>",self.targetRace)
        # 列名をつける
        self.tree.heading("#0",text="race_tree")
        self.tree.pack()
        # rootのiidを登録
        self.rootiid = self.tree.insert("","end",text="Home")
        self.iid = self.rootiid
        # 種族ツリー作成
        self.makeTree()

    def setMode(self,pw_right):

        pw_right_up1 = tk.PanedWindow(pw_right, bg="pink", orient='horizontal')
        # sex
        self.lblmode = tk.Label(pw_right_up1,text = 'mode')
        self.lblmode.grid(row=3, column=2, padx=5, pady=2)
        self.rdoEdit = tk.Radiobutton(pw_right_up1, value=0, variable=self.mode, text='編集')
        self.rdoEdit.grid(row=3, column=3, padx=5, pady=2)
        self.rdoNew = tk.Radiobutton(pw_right_up1, value=1, variable=self.mode, text='新規登録')
        self.rdoNew.grid(row=3, column=4, padx=5, pady=2)

        return pw_right_up1

    # 名前部作成
    def createRace(self,pw_right):
        pw_right_up3 = tk.PanedWindow(pw_right, bg="pink", orient='horizontal')

        self.lbl_titleName = tk.Label(pw_right_up3,text="name",width=9)
        self.lbl_titleName.grid(row=0, column=0, padx=5, pady=2, columnspan = 4)

        # 種族選択
        self.lblChoice = tk.Label(pw_right_up3,text="種族選択",width=9)
        self.lblChoice.grid(row=1, column=0, padx=5, pady=2)
        self.cboChoice = ttk.Combobox(pw_right_up3, textvariable=self.choosedRace, width=14)
        self.cboChoice.grid(row=1, column=1, padx=5, pady=2)
        
        # 種族名
        self.lblName = tk.Label(pw_right_up3,text="種族名",width=9)
        self.lblName.grid(row=2, column=0, padx=5, pady=2)
        self.entName = tk.Entry(pw_right_up3, textvariable=self.entry_ra.race_name, width=16)
        self.entName.grid(row=2, column=1, padx=5, pady=2)
        # 進化レベル
        self.lblLevel = tk.Label(pw_right_up3,text="進化レベル",width=9)
        self.lblLevel.grid(row=4, column=0, padx=5, pady=2)
        self.entLevel = tk.Entry(pw_right_up3, textvariable=self.evoLevel, width=6)
        self.entLevel.grid(row=4, column=1, padx=5, pady=2)

        # 種族選択イベント
        self.choosedRace.trace("w", lambda *args: self.select_race(self.choosedRace))

        return pw_right_up3

    # ステータス部作成
    def createStatus(self, pw_right):

        pw_right_up2 = tk.PanedWindow(pw_right, bg="pink", orient='horizontal')

        self.lbl_title = tk.Label(pw_right_up2,text="status",width=9)
        self.lbl_title.grid(row=0, column=0, padx=5, pady=2, columnspan = 4)
        # HP
        self.lbl7 = tk.Label(pw_right_up2,textvariable=self.HP,width=9)
        self.lbl7.grid(row=2, column=0, padx=5, pady=2)
        self.ent7 = tk.Entry(pw_right_up2, textvariable=self.entry_ra.p_HP, width=6)
        self.ent7.grid(row=2, column=1, padx=5, pady=2)
        # MP
        self.lbl8 = tk.Label(pw_right_up2,textvariable=self.MP,width=9)
        self.lbl8.grid(row=2, column=2, padx=5, pady=2)
        self.ent8 = tk.Entry(pw_right_up2, textvariable=self.entry_ra.p_MP, width=6)
        self.ent8.grid(row=2, column=3, padx=5, pady=2)
        # sta
        self.lbl9 = tk.Label(pw_right_up2,textvariable=self.sta,width=9)
        self.lbl9.grid(row=3, column=0, padx=5, pady=2)
        self.ent9 = tk.Entry(pw_right_up2, textvariable=self.entry_ra.p_sta, width=6)
        self.ent9.grid(row=3, column=1, padx=5, pady=2)
        # atk
        self.lbl10 = tk.Label(pw_right_up2,textvariable=self.atk,width=9)
        self.lbl10.grid(row=3, column=2, padx=5, pady=2)
        self.ent10 = tk.Entry(pw_right_up2, textvariable=self.entry_ra.p_atk, width=6)
        self.ent10.grid(row=3, column=3, padx=5, pady=2)
        # vit
        self.lbl11 = tk.Label(pw_right_up2,textvariable=self.vit,width=9)
        self.lbl11.grid(row=4, column=0, padx=5, pady=2)
        self.ent11 = tk.Entry(pw_right_up2, textvariable=self.entry_ra.p_vit, width=6)
        self.ent11.grid(row=4, column=1, padx=5, pady=2)
        # mag
        self.lbl12 = tk.Label(pw_right_up2,textvariable=self.mag,width=9)
        self.lbl12.grid(row=4, column=2, padx=5, pady=2)
        self.ent12 = tk.Entry(pw_right_up2, textvariable=self.entry_ra.p_mag, width=6)
        self.ent12.grid(row=4, column=3, padx=5, pady=2)
        # des
        self.lbl13 = tk.Label(pw_right_up2,textvariable=self.des,width=9)
        self.lbl13.grid(row=5, column=0, padx=5, pady=2)
        self.ent13 = tk.Entry(pw_right_up2, textvariable=self.entry_ra.p_des, width=6)
        self.ent13.grid(row=5, column=1, padx=5, pady=2)
        # agi
        self.lbl14 = tk.Label(pw_right_up2,textvariable=self.agi,width=9)
        self.lbl14.grid(row=5, column=2, padx=5, pady=2)
        self.ent14 = tk.Entry(pw_right_up2, textvariable=self.entry_ra.p_agi, width=6)
        self.ent14.grid(row=5, column=3, padx=5, pady=2)
        # total
        self.lbl16 = tk.Label(pw_right_up2,textvariable=self.p_total,width=9)
        self.lbl16.grid(row=6, column=0, padx=5, pady=2)
        self.ent16 = tk.Entry(pw_right_up2, textvariable=self.entry_ra.total_pattern,  width=7)
        self.ent16.grid(row=6, column=1, padx=5, pady=2)
        self.ent16.configure(state = 'readonly')
        # rank
        self.lbl17 = tk.Label(pw_right_up2,textvariable=self.r_rank,width=9)
        self.lbl17.grid(row=6, column=2, padx=5, pady=2)
        self.ent17 = tk.Entry(pw_right_up2, textvariable=self.entry_ra.r_rank,  width=7)
        self.ent17.grid(row=6, column=3, padx=5, pady=2)
        self.ent17.configure(state = 'readonly')

        # gene桁数制限
        """とってくるだけのデータなのでカット
        self.ra.p_HP.trace("w", lambda *args: self.character_limit(self.ra.p_HP, 5))
        self.ra.p_MP.trace("w", lambda *args: self.character_limit(self.ra.p_MP, 5))
        self.ra.p_sta.trace("w", lambda *args: self.character_limit(self.ra.p_sta, 5))
        self.ra.p_atk.trace("w", lambda *args: self.character_limit(self.ra.p_atk, 5))
        self.ra.p_vit.trace("w", lambda *args: self.character_limit(self.ra.p_vit, 5))
        self.ra.p_mag.trace("w", lambda *args: self.character_limit(self.ra.p_mag, 5))
        self.ra.p_des.trace("w", lambda *args: self.character_limit(self.ra.p_des, 5))
        self.ra.p_agi.trace("w", lambda *args: self.character_limit(self.ra.p_agi, 5))
        """

        return pw_right_up2

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
        self.btnEntry = tk.Button(pw_right_up4, text='登録', width=10, command=self.entryRace)
        self.btnEntry.grid(row=5, column=0, columnspan=2, padx=5, pady=4)

        # 削除ボタン
        self.btnEntry = tk.Button(pw_right_up4, text='削除', width=10, command=self.deleteRace)
        self.btnEntry.grid(row=6, column=0, columnspan=2, padx=5, pady=4)

        return pw_right_up4


    # textの内容のリセットself.yearに格納
    def makeTree(self):

        # 選択したraceを取得
        self.s_race = self.ra_dao.select_races()
        initial_race = [race for race in self.s_race if race['initial_flg'] == 1]
        
        # ツリーごとの種族要素を取得
        self.setRaceTree(initial_race,self.iid)

    # raceのツリー構造を生成
    def setRaceTree(self,_addTree,_iid):

        # _addTree:アクティブツリーのノード
        for _race in _addTree:
            
            rootiid = self.tree.insert(_iid,"end",text=str(_race['race_id']) + ':' + _race['race_name'])
            iid = rootiid
            # 選択イベント用
            self.iid = iid
            # 選択種族を格納
            self.raceRoot[iid] = _race

            # 進化先raceを取得
            addRace = [race for race in self.s_race if _race['parent_race1_id'] == race['race_id'] 
                or _race['parent_race2_id'] == race['race_id'] or _race['parent_race3_id'] == race['race_id']]

            # 進化先が存在する場合
            if len(addRace) != 0:
                self.raceTree[iid] = addRace
                self.setRaceTree(addRace,iid)

    # 種族選択時
    def targetRace(self,event):
        # 初期化
        self.ra.init()
        # 前フォーカスIDをセット
        self.iid = self.tree.focus()
        self.bk_iid = self.tree.parent(self.iid)

        # 種族選択コンボボックス編集
        self.cboChoice['values'] = self.getRaceValue()

        # ホームでない場合
        if self.iid != 'I001':

            # 編集：アクティブ
            self.rdoEdit.configure(state = 'normal')
            
            #race:選択ツリー
            race = self.raceRoot[self.iid]

            # 進化先がすべて埋まっている場合→新規登録不可
            if race['parent_race1_id'] != None and race['parent_race2_id'] != None and race['parent_race3_id'] != None:
                self.rdoNew.configure(state = 'disabled')
                self.mode.set(0)
            elif race['r_rank'] == 'SSS':
                self.rdoNew.configure(state = 'disabled')
                self.mode.set(0)
            else:
                self.rdoNew.configure(state = 'normal')
                self.rdoEdit.configure(state = 'normal')

            if self.mode.get() == 0:
                # 編集の場合、選択ツリーのraceを右画面に表示
                self.ra.set_select_race(race)

            elif self.mode.get() == 1:
                # 新規登録の場合、右画面の項目を初期化
                self.ra.set_select_race(race)

                self.ra.parent_race1_id == self.tree.item(self.iid,"text")
            
            if self.bk_iid != 'I001':
                # 一つ前のraceをセット
                self.bk_ra.set_select_race(self.raceRoot[self.bk_iid])
            else:
                # 初期化
                self.bk_ra.init()

        else:
            # 編集不可
            self.rdoEdit.configure(state = 'disabled')
            self.mode.set(1)
            self.ra.init()
            self.bk_ra.init()

            # 進化元フラグON
            self.entry_ra.initial_flg.set(1)

        self.setRaceSelected()


    # 選択したraceを登録用メンバにセット
    def setRaceSelected(self):
        
        self.entry_ra.race_name.set(self.ra.race_name.get())
        self.entry_ra.race_id.set(self.ra.race_id.get())
        self.entry_ra.p_HP.set(self.ra.p_HP.get())
        self.entry_ra.p_MP.set(self.ra.p_MP.get())
        self.entry_ra.p_sta.set(self.ra.p_sta.get())
        self.entry_ra.p_atk.set(self.ra.p_atk.get())
        self.entry_ra.p_vit.set(self.ra.p_vit.get())
        self.entry_ra.p_mag.set(self.ra.p_mag.get())
        self.entry_ra.p_des.set(self.ra.p_des.get())
        self.entry_ra.p_agi.set(self.ra.p_agi.get())
        self.entry_ra.parent_race1_id.set(self.ra.parent_race1_id.get())
        self.entry_ra.evolution1_level.set(self.ra.evolution1_level.get())
        self.entry_ra.parent_race2_id.set(self.ra.parent_race2_id.get())
        self.entry_ra.evolution2_level.set(self.ra.evolution2_level.get())
        self.entry_ra.parent_race3_id.set(self.ra.parent_race3_id.get())
        self.entry_ra.evolution3_level.set(self.ra.evolution3_level.get())
        self.entry_ra.r_rank.set(self.ra.r_rank.get())
        self.entry_ra.total_pattern.set(self.ra.total_pattern.get())

    # 上位ランクデータ取得
    def getRaceValue(self):
        raceList = {}
        try:
            acquired_rank = self.getRaceRank(self.raceRoot[self.iid]['r_rank'])
            self.cboChoice.configure(state = 'normal')
        except:
            acquired_rank = []
            self.cboChoice.configure(state = 'disabled')


        for data in self.raceRoot.values():
            if data['r_rank'] in acquired_rank:
                raceList[data['race_id']] = data['r_rank'] + ':' + data['race_name']
        
        return list(raceList.values())

    # 選択可能ランクリスト取得
    # 0:編集の場合は自身のランクも選択可能に設定
    def getRaceRank(self, r_rank):
        acquired_rank = []
        if r_rank == 'SS':
            acquired_rank = ['SSS']
        if r_rank == 'S':
            acquired_rank = ['SSS','SS']
        if r_rank == 'A':
            acquired_rank = ['SSS','SS','S']
        if r_rank == 'B':
            acquired_rank = ['SSS','SS','S','A']
        if r_rank == 'C':
            acquired_rank = ['SSS','SS','S','A','B']
        if r_rank == 'D':
            acquired_rank = ['SSS','SS','S','A','B','C']
        if r_rank == 'E':
            acquired_rank = ['SSS','SS','S','A','B','C','D']
        if r_rank == 'F':
            acquired_rank = ['SSS','SS','S','A','B','C','D','E']
        if r_rank == 'G':
            acquired_rank = ['SSS','SS','S','A','B','C','D','E','F']

        if self.mode.get() == 0:
            acquired_rank.append(r_rank)
        
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
            
    # raceが選択された場合
    def select_race(self, _race):

        # 選択したraceを取得
        s_race = self.ra_dao.pickup_race(_race.get())

        # コンボボックスの種族が存在しない場合初期化
        try:
            # 対象に選択したraceの値を反映
            self.ra.set_select_race(s_race)
        except:
            self.ra.init()

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
                # total_pattern集計
                self.entry_ra.total_pattern.set(str(int(self.entry_ra.p_HP.get())+int(self.entry_ra.p_MP.get())
                +int(self.entry_ra.p_sta.get())+int(self.entry_ra.p_atk.get())+int(self.entry_ra.p_vit.get())
                +int(self.entry_ra.p_mag.get())+int(self.entry_ra.p_des.get())+int(self.entry_ra.p_agi.get())))   
            except:
                pass

            self.entry_ra.r_rank.set(self.getOneRank(self.entry_ra.total_pattern.get()))


    # 進化レベル設定（基準）
    def randomLevel(self,r_rank):
        if r_rank == 'SS"':
            self.evoLevel.set(random.randint(60,99))
        if r_rank == 'SS':
            self.evoLevel.set(random.randint(45,70))
        if r_rank == 'S':
            self.evoLevel.set(random.randint(40,65))
        if r_rank == 'A':
            self.evoLevel.set(random.randint(35,60))
        if r_rank == 'B':
            self.evoLevel.set(random.randint(30,55))
        if r_rank == 'C':
            self.evoLevel.set(random.randint(25,50))
        if r_rank == 'D':
            self.evoLevel.set(random.randint(20,40))
        if r_rank == 'E':
            self.evoLevel.set(random.randint(10,30))
        if r_rank == 'F':
            self.evoLevel.set(random.randint(5,20))
        if r_rank == 'G':
            self.evoLevel.set(random.randint(1,5))
        

    # 種族登録更新処理
    def entryRace(self):

        s_race = self.entry_ra

        # 重複チェック実装
        res = [race for race in list(self.raceTree.values()) if s_race.race_name.get() == race[0]['race_name'] and s_race.r_rank.get() == race[0]['r_rank'] ]
        
        if len(res) != 0:
            bs.Popup.ShowInfo(self,E0001)
            return
        
        # initial_flg設定
        if self.iid == 'I001':
            self.entry_ra.initial_flg.set(1)
        else:
            if self.mode.get() == 0 and self.bk_iid == 'I001':
                self.entry_ra.initial_flg.set(1)
            elif self.mode.get() == 0:
                self.entry_ra.initial_flg.set(0)
            else:
                self.entry_ra.initial_flg.set(0)

        # 登録確認ポップアップ表示
        if bs.Popup.OKCancelPopup(self,Q0001) == False:
            return

        try:
            # 親種族の更新
            if self.mode.get() == 0:
                # 種族更新 
                self.ra_dao.update_race(s_race)
                # TODO:進化前更新
            else:
                # 種族登録 戻り値にInsertした種族を取得
                res_id = self.ra_dao.insert_race(s_race)
                # 子種族の更新
                if self.iid != 'I001':
                    self.ra_dao.update_child_race(self.ra,res_id,self.evoLevel.get())
        except:
            # 登録完了ポップアップ表示
            bs.Popup.ShowInfo(self,E0002)
            return

        # 登録完了ポップアップ表示
        bs.Popup.ShowInfo(self,I0002)
        
        # 再検索を実施
        self.pw_main.destroy()
        self.createDisplay()

    # 削除処理
    def deleteRace(self):

        # 登録確認ポップアップ表示
        if bs.Popup.OKCancelPopup(self,Q0002) == False:
            return
        
        if self.ra_dao.delete_race(self.ra) == False:
            bs.Popup.ShowInfo(self,E0002)
            return
        if self.ra_dao.update_else(self.ra) == False:
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
        self.setRaceSelected()

        # 選択可能ランク
        # TODO：チョイス可能に設定する
        acquired_rank = self.getRaceRank(self.entry_ra.r_rank.get())
        
        # 重み付けローカル変数
        val = self.val.get()

        reg_race = {}
        reg_race['r_hp'] = 1
        reg_race['r_mp'] = 1
        reg_race['r_sta'] = 1
        reg_race['r_atk'] = 1
        reg_race['r_vit'] = 1
        reg_race['r_mag'] = 1
        reg_race['r_des'] = 1
        reg_race['r_agi'] = 1

        # 登録用
        
        # 新規、編集ランク制限
        if self.mode.get() == 0:

            for i in range(1000):

                # 重み付けF-C安定
                # あたり
                # weight = 70

                weight = val + 1 - i*0.1

                # geneをランダムで設定
                # self.ra.level.set(self.rand_num_hard(3,weight))
                reg_race['r_hp'] = self.rand_num(5,weight)
                reg_race['r_mp'] = self.rand_num(5,weight)
                reg_race['r_sta'] = self.rand_num(5,weight)
                reg_race['r_atk'] = self.rand_num(5,weight)
                reg_race['r_vit'] = self.rand_num(5,weight)
                reg_race['r_mag'] = self.rand_num(5,weight)
                reg_race['r_des'] = self.rand_num(5,weight)
                reg_race['r_agi'] = self.rand_num(5,weight)

                # 編集の場合：ブレーク条件
                if self.getOneRank(sum(reg_race.values())) in acquired_rank:
                    break

                # weight回復
                if sum(reg_race.values()) <= 0:
                    val = val + i*0.2

        elif self.mode.get() == 1:

            # geneをランダムで設定
            # self.ra.level.set(self.rand_num_hard(3,weight)

            for i in range(1000):

                # 重み付けF-C安定
                # あたり
                # weight = 70

                weight = val + 1 - i*0.1

                # geneをランダムで設定
                # self.ra.level.set(self.rand_num_hard(3,weight))
                reg_race['r_hp'] = self.rand_num(5,weight)
                reg_race['r_mp'] = self.rand_num(5,weight)
                reg_race['r_sta'] = self.rand_num(5,weight)
                reg_race['r_atk'] = self.rand_num(5,weight)
                reg_race['r_vit'] = self.rand_num(5,weight)
                reg_race['r_mag'] = self.rand_num(5,weight)
                reg_race['r_des'] = self.rand_num(5,weight)
                reg_race['r_agi'] = self.rand_num(5,weight)

                # 新規の場合ブレーク条件
                if self.getOneRank(sum(reg_race.values())) in acquired_rank and sum(reg_race.values()) > self.ra.total_pattern.get():
                    break

                # weight回復
                if sum(reg_race.values()) <= 0:
                    val = val + i*0.2
            
        self.entry_ra.p_HP.set(reg_race['r_hp'])
        self.entry_ra.p_MP.set(reg_race['r_mp'])
        self.entry_ra.p_sta.set(reg_race['r_sta'])
        self.entry_ra.p_atk.set(reg_race['r_atk'])
        self.entry_ra.p_vit.set(reg_race['r_vit'])
        self.entry_ra.p_mag.set(reg_race['r_mag'])
        self.entry_ra.p_des.set(reg_race['r_des'])
        self.entry_ra.p_agi.set(reg_race['r_agi'])
        self.entry_ra.total_pattern.set(sum(reg_race.values()))

        # totalからrankを設定
        self.entry_ra.r_rank.set(self.getOneRank(self.entry_ra.total_pattern.get()))

        # 進化レベル設定
        self.randomLevel(self.entry_ra.r_rank.get())

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
    def ch_status_set(self,label_text,input_num):
        for dkey, dval in label_text.items():
            dval.set(dkey + '（{}）'.format(input_num))

# 1桁の数字を2バイトに変換する関数
# 追記 https://teratail.com/questions/234639#reply-355304
def convert_in2_2bytes(str_number):
    if len(str_number) == 1:
        return '0' + str_number
    else:
        return str_number

root = tk.Tk()
c = create_race(root)
c.openDialog()
