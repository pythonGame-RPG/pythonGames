from settings import *
import tkinter as tk
import tkinter.ttk as ttk
import datetime
# from turtle import *
import DAO.racesDAO as _races
import DTO.races as races

selected_d = ''

# カレンダーを作成するフレームクラス
class create_race():
    def __init__(self,parent):

        import datetime
        self.parent = parent
        self.dialog = None
        self.mode = tk.IntVar()
        self.iid=""
        self.rootiid=""
        self.raceTree = {}
        self.s_race = []

        # DBアクセス用
        self.ra = races.Race()
        self.ra_dao = _races.RaceDAO()

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

        # self.window→pw_right_down（右下画面ボタン部）
        pw_right_down = tk.PanedWindow(pw_right, bg="pink", orient='horizontal')
        pw_right.add(pw_right_down)
        
        # TODO:いらなくなったら消す
        self.parent.mainloop()

    def createTreeView(self, pw_main):
        treeFrame = tk.PanedWindow(pw_main, bg="cyan", orient='vertical')
        self.tree = ttk.Treeview(treeFrame)
        # ツリーの項目が選択されたら、選択された種族を表示する
        # self.tree.bind("<<TreeviewSelect>>",self.select_races)
        # 列名をつける
        self.tree.heading("#0",text="race_tree")
        self.tree.pack()
        # 種族ツリー作成
        self.makeTree()
        # rootのiidを登録
        self.rootiid = self.tree.insert("","end",text="Home")
        self.iid = self.rootiid
        return treeFrame

    def setMode(self,pw_right):

        pw_right_up1 = tk.PanedWindow(pw_right, bg="pink", orient='horizontal')
        # sex
        self.lblmode = tk.Label(pw_right_up1,text = 'mode')
        self.lblmode.grid(row=3, column=2, padx=5, pady=2)
        self.rdo1 = tk.Radiobutton(pw_right_up1, value=0, variable=self.mode, text='新規登録')
        self.rdo1.grid(row=3, column=3, padx=5, pady=2)
        self.rdo2 = tk.Radiobutton(pw_right_up1, value=1, variable=self.mode, text='編集')
        self.rdo2.grid(row=3, column=4, padx=5, pady=2)

        return pw_right_up1

    def createStatus(self, pw_right):

        pw_right_up2 = tk.PanedWindow(pw_right, bg="pink", orient='horizontal')

        self.lbl_title = tk.Label(pw_right_up2,text="status",width=9)
        self.lbl_title.grid(row=0, column=0, padx=5, pady=2, columnspan = 4)
        # HP
        self.lbl7 = tk.Label(pw_right_up2,text="HP",width=9)
        self.lbl7.grid(row=2, column=0, padx=5, pady=2)
        self.ent7 = tk.Entry(pw_right_up2, textvariable=self.ra.p_HP, width=6)
        self.ent7.grid(row=2, column=1, padx=5, pady=2)
        # MP
        self.lbl8 = tk.Label(pw_right_up2,text="MP",width=9)
        self.lbl8.grid(row=2, column=2, padx=5, pady=2)
        self.ent8 = tk.Entry(pw_right_up2, textvariable=self.ra.p_MP, width=6)
        self.ent8.grid(row=2, column=3, padx=5, pady=2)
        # sta
        self.lbl9 = tk.Label(pw_right_up2,text="sta",width=9)
        self.lbl9.grid(row=3, column=0, padx=5, pady=2)
        self.ent9 = tk.Entry(pw_right_up2, textvariable=self.ra.p_sta, width=6)
        self.ent9.grid(row=3, column=1, padx=5, pady=2)
        # atk
        self.lbl10 = tk.Label(pw_right_up2,text="atk",width=9)
        self.lbl10.grid(row=3, column=2, padx=5, pady=2)
        self.ent10 = tk.Entry(pw_right_up2, textvariable=self.ra.p_atk, width=6)
        self.ent10.grid(row=3, column=3, padx=5, pady=2)
        # vit
        self.lbl11 = tk.Label(pw_right_up2,text="vit",width=9)
        self.lbl11.grid(row=4, column=0, padx=5, pady=2)
        self.ent11 = tk.Entry(pw_right_up2, textvariable=self.ra.p_vit, width=6)
        self.ent11.grid(row=4, column=1, padx=5, pady=2)
        # mag
        self.lbl12 = tk.Label(pw_right_up2,text="mag",width=9)
        self.lbl12.grid(row=4, column=2, padx=5, pady=2)
        self.ent12 = tk.Entry(pw_right_up2, textvariable=self.ra.p_mag, width=6)
        self.ent12.grid(row=4, column=3, padx=5, pady=2)
        # des
        self.lbl13 = tk.Label(pw_right_up2,text="des",width=9)
        self.lbl13.grid(row=5, column=0, padx=5, pady=2)
        self.ent13 = tk.Entry(pw_right_up2, textvariable=self.ra.p_des, width=6)
        self.ent13.grid(row=5, column=1, padx=5, pady=2)
        # agi
        self.lbl14 = tk.Label(pw_right_up2,text="agi",width=9)
        self.lbl14.grid(row=5, column=2, padx=5, pady=2)
        self.ent14 = tk.Entry(pw_right_up2, textvariable=self.ra.p_agi, width=6)
        self.ent14.grid(row=5, column=3, padx=5, pady=2)

        return pw_right_up2

    # textの内容のリセットself.yearに格納
    def makeTree(self):

        # 選択したraceを取得
        self.s_race = self.ra_dao.select_races()
        initial_race = [race for race in s_race if race['initial_flg'] == 1]
        
        # ツリーごとの種族要素を取得
        self.setRaceTree(initial_race)

    # raceのツリー構造を生成
    def setRaceTree(self,_addTree):

        race_flg = True

        for _race in _addTree:
            
            addRace = [race for race in s_race if race['parent_race1_id'] == _race['race_id'] 
                or race['parent_race2_id'] == _race['race_id'] or race['parent_race3_id'] == _race['race_id']]

            if addRace is not None:
                self.insertRace(_race['race_id'], addRace)
                # None出ない場合子種族を件数分るループ
                setRaceTree(addTree)
            else:
                return
        


    #指定されたディレクトリに子階層を加える
    def insertRace(self, _race_iid, addRace):
        # ディレクトリ名がない場合は処理しない
        if addRace != "":

            """
            children = self.tree.get_children(_race_iid)
            
            # 同じ階層に同じ名前で作成は不可
            for child in children:
                childname = self.tree.item(child,"text")
                if childname == addRace:
                    messagebox.showerror("登録エラー","既に登録されています")
                    return
            """
            # addRaceを件数分ツリーに追加
            for child in addRace:
                self.tree.insert(_race_iid,"end",text=addRace['race_id'])
                # ツリーリストに追加
                self.raceTree[_race_iid] = addRace
            

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
