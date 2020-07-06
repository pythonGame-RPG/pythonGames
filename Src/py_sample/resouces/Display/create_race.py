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
        self.iid=""
        self.rootiid=""
        self.raceRoot = {}
        self.raceTree = {}
        self.s_race = []
        self.bs = bs.MyStack()

        # DBアクセス用
        self.ra = races.Race()
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


        #モード変更イベント
        #self.mode.trace("w", lambda *args: self.changeMode())


    def openDialog(self):        
       # 子画面クラス
        self.window = tk.Toplevel(self.parent)
        self.window.geometry('500x540')
        self.window.title("Race App")
        
        # ウィンドウを分ける
        pw_main = tk.PanedWindow(self.window, orient='horizontal')
        pw_main.pack(expand=True, fill = tk.BOTH, side="left")

        # self.window→pw_left（左画面ツリービュー）
        pw_left = self.createTreeView(pw_main)
        pw_main.add(pw_left)

        # self.window→pw_right（右画面ツリービュー）
        pw_right = tk.PanedWindow(pw_main, bg="yellow", orient='vertical')
        pw_main.add(pw_right)

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

        
        # TODO:いらなくなったら消す
        self.parent.mainloop()

    def createTreeView(self, pw_main):
        treeFrame = tk.PanedWindow(pw_main, bg="cyan", orient='vertical')
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
        return treeFrame

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
        self.entName = tk.Entry(pw_right_up3, textvariable=self.ra.race_name, width=16)
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
        self.lbl7 = tk.Label(pw_right_up2,text="HP(" + str(self.ra.p_HP.get()) + ")",width=9)
        self.lbl7.grid(row=2, column=0, padx=5, pady=2)
        self.ent7 = tk.Entry(pw_right_up2, textvariable=self.entry_ra.p_HP, width=6)
        self.ent7.grid(row=2, column=1, padx=5, pady=2)
        # MP
        self.lbl8 = tk.Label(pw_right_up2,text="MP(" + str(self.ra.p_MP.get()) + ")",width=9)
        self.lbl8.grid(row=2, column=2, padx=5, pady=2)
        self.ent8 = tk.Entry(pw_right_up2, textvariable=self.entry_ra.p_MP, width=6)
        self.ent8.grid(row=2, column=3, padx=5, pady=2)
        # sta
        self.lbl9 = tk.Label(pw_right_up2,text="sta(" + str(self.ra.p_sta.get()) + ")",width=9)
        self.lbl9.grid(row=3, column=0, padx=5, pady=2)
        self.ent9 = tk.Entry(pw_right_up2, textvariable=self.entry_ra.p_sta, width=6)
        self.ent9.grid(row=3, column=1, padx=5, pady=2)
        # atk
        self.lbl10 = tk.Label(pw_right_up2,text="atk(" + str(self.ra.p_atk.get()) + ")",width=9)
        self.lbl10.grid(row=3, column=2, padx=5, pady=2)
        self.ent10 = tk.Entry(pw_right_up2, textvariable=self.entry_ra.p_atk, width=6)
        self.ent10.grid(row=3, column=3, padx=5, pady=2)
        # vit
        self.lbl11 = tk.Label(pw_right_up2,text="vit(" + str(self.ra.p_vit.get()) + ")",width=9)
        self.lbl11.grid(row=4, column=0, padx=5, pady=2)
        self.ent11 = tk.Entry(pw_right_up2, textvariable=self.entry_ra.p_vit, width=6)
        self.ent11.grid(row=4, column=1, padx=5, pady=2)
        # mag
        self.lbl12 = tk.Label(pw_right_up2,text="mag(" + str(self.ra.p_mag.get()) + ")",width=9)
        self.lbl12.grid(row=4, column=2, padx=5, pady=2)
        self.ent12 = tk.Entry(pw_right_up2, textvariable=self.entry_ra.p_mag, width=6)
        self.ent12.grid(row=4, column=3, padx=5, pady=2)
        # des
        self.lbl13 = tk.Label(pw_right_up2,text="des(" + str(self.ra.p_des.get()) + ")",width=9)
        self.lbl13.grid(row=5, column=0, padx=5, pady=2)
        self.ent13 = tk.Entry(pw_right_up2, textvariable=self.entry_ra.p_des, width=6)
        self.ent13.grid(row=5, column=1, padx=5, pady=2)
        # agi
        self.lbl14 = tk.Label(pw_right_up2,text="agi(" + str(self.ra.p_agi.get()) + ")",width=9)
        self.lbl14.grid(row=5, column=2, padx=5, pady=2)
        self.ent14 = tk.Entry(pw_right_up2, textvariable=self.entry_ra.p_agi, width=6)
        self.ent14.grid(row=5, column=3, padx=5, pady=2)
        # total
        self.lbl16 = tk.Label(pw_right_up2,text="total(" + str(self.ra.total_pattern.get()) + ")",width=9)
        self.lbl16.grid(row=6, column=0, padx=5, pady=2)
        self.ent16 = tk.Entry(pw_right_up2, textvariable=self.entry_ra.total_pattern,  width=7)
        self.ent16.grid(row=6, column=1, padx=5, pady=2)
        self.ent16.configure(state = 'readonly')
        # rank
        self.lbl17 = tk.Label(pw_right_up2,text="rank(" + self.ra.r_rank.get() + ")",width=9)
        self.lbl17.grid(row=6, column=2, padx=5, pady=2)
        self.ent17 = tk.Entry(pw_right_up2, textvariable=self.entry_ra.r_rank,  width=7)
        self.ent17.grid(row=6, column=3, padx=5, pady=2)
        self.ent17.configure(state = 'readonly')

        # gene桁数制限
        self.ra.p_HP.trace("w", lambda *args: self.character_limit(self.ra.p_HP, 5))
        self.ra.p_MP.trace("w", lambda *args: self.character_limit(self.ra.p_MP, 5))
        self.ra.p_sta.trace("w", lambda *args: self.character_limit(self.ra.p_sta, 5))
        self.ra.p_atk.trace("w", lambda *args: self.character_limit(self.ra.p_atk, 5))
        self.ra.p_vit.trace("w", lambda *args: self.character_limit(self.ra.p_vit, 5))
        self.ra.p_mag.trace("w", lambda *args: self.character_limit(self.ra.p_mag, 5))
        self.ra.p_des.trace("w", lambda *args: self.character_limit(self.ra.p_des, 5))
        self.ra.p_agi.trace("w", lambda *args: self.character_limit(self.ra.p_agi, 5))

        return pw_right_up2

    def createButton(self, pw_right):
        pw_right_up4 = tk.PanedWindow(pw_right, bg="pink", orient='horizontal')
        # 登録ボタン
        self.btn1 = tk.Button(pw_right_up4, text='登録', width=10, command=self.entryRace)
        self.btn1.grid(row=4, column=0, padx=5, pady=4)
        # ランダムボタン
        self.btnRand = tk.Button(pw_right_up4, text='ランダム', width=10, command=self.randomNum)
        self.btnRand.grid(row=4, column=0, padx=5, pady=4)

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
        self.iid = self.tree.focus()

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
                self.mode.set(0)

            if self.mode.get() == 0:
                # 編集の場合、選択ツリーのraceを右画面に表示
                self.ra.set_select_race(race)

            elif self.mode.get() == 1:
                # 新規登録の場合、右画面の項目を初期化
                self.ra.init()

                # 進化元フラグOFF
                self.ra.initial_flg.set(0)
                self.ra.parent_race1_id == self.tree.item(self.iid,"text")

        else:
            # 編集不可
            self.rdoEdit.configure(state = 'disabled')
            self.mode.set(1)
            self.ra.init()

            # 進化元フラグON
            self.ra.initial_flg.set(1)
        
        self.entry_ra.p_HP.set(self.ra.p_HP.get())
        self.entry_ra.p_MP.set(self.ra.p_MP.get())
        self.entry_ra.p_sta.set(self.ra.p_sta.get())
        self.entry_ra.p_atk.set(self.ra.p_atk.get())
        self.entry_ra.p_vit.set(self.ra.p_vit.get())
        self.entry_ra.p_mag.set(self.ra.p_mag.get())
        self.entry_ra.p_des.set(self.ra.p_des.get())
        self.entry_ra.p_agi.set(self.ra.p_agi.get())
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
        
        return acquired_rank

    def getOneRank(self, total):
        
        rank = 'G'

        if total > 50000:
            rank = 'SSS'
        elif total > 20000:
            rank = 'SS'
        elif total > 10000:
            rank = 'S'
        elif total > 5000:
            rank = 'A'
        elif total > 2000:
            rank = 'B'
        elif total > 1000:
            rank = 'C'
        elif total > 500:
            rank = 'D'
        elif total > 200:
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

    # mode変更時の判定は必要ない
    """
    def changeMode(self):
        if self.mode.get() == 0:
            # 種族コンボボックス選択可
            self.cboChoice.configure(state = 'normal')
        else:
            # 種族コンボボックス選択不可
                self.cboChoice.configure(state = 'disabled')
    """

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
                self.ra.total_pattern.set(str(int(self.ra.p_HP.get())+int(self.ra.p_MP.get())
                +int(self.ra.p_sta.get())+int(self.ra.p_atk.get())+int(self.ra.p_vit.get())
                +int(self.ra.p_mag.get())+int(self.ra.p_des.get())+int(self.ra.p_agi.get())))   
            except:
                pass

    # 種族登録更新処理
    def entryRace(self):

        s_race = self.ra

        # 重複チェック実装
        res = [race for race in self.raceTree if s_race.race_name.get() == race.race_name 
                                             and s_race.r_rank.get() == race.r_rank ]
        if len(res) != 0:
            bs.Popup.ShowInfo(self,E0001)
            return

        # 登録確認ポップアップ表示
        bs.Popup.OKCancelPopup(self,Q0001)

        # 親種族の更新
        if self.mode.get() == 0:
            # 種族更新 
            self.ra_dao.update_race(s_race)
        else:
            # 種族登録 戻り値にInsertした種族を取得
            res = self.ra_dao.insert_race(s_race)
            # 子種族の更新
            if s_race.initial_flg == 0:
                self.ra_dao.update_child_race(s_race,res)

    # ランダム生成押下時
    def randomNum(self):
        # weight = 1.5 # 超レアガチャ
        # weight = 2   # 高レアガチャ
        # weight = 3   # レアガチャ
        weight = random.random() + 9.5   # ノーマルガチャ

        # 選択可能ランク
        acquired_rank = self.getRaceRank(self.ra.r_rank.get())

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

            while self.entry_ra.r_rank.get() not in acquired_rank and sum(reg_race.values()) < self.ra.total_pattern.get():

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

                weight -= 0.1
            
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
            
        elif self.mode.get() == 1:

            # geneをランダムで設定
            # self.ra.level.set(self.rand_num_hard(3,weight)

            while self.entry_ra.r_rank.get() in acquired_rank and sum(reg_race.values()) > self.ra.total_pattern.get():

                reg_race['r_hp'] = self.rand_num(5,weight)
                reg_race['r_mp'] = self.rand_num(5,weight)
                reg_race['r_sta'] = self.rand_num(5,weight)
                reg_race['r_atk'] = self.rand_num(5,weight)
                reg_race['r_vit'] = self.rand_num(5,weight)
                reg_race['r_mag'] = self.rand_num(5,weight)
                reg_race['r_des'] = self.rand_num(5,weight)
                reg_race['r_agi'] = self.rand_num(5,weight)

                weight -= 0.1
            
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


    def rand_num(self, num, weight):
        import numpy as np
        import matplotlib.pyplot as plt

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
