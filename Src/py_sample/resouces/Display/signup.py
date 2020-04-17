from settings import *
from Sql import *
from validate import *
import random
import dbo.character as chara
import tkinter as tk
from tkinter import ttk
from turtle import *

# Login classes(GUIで実装)
class Signup(tk.Tk):
    def __init__(self):
        self.root = tk.Tk.__init__(self)
        self.geometry('500x400')
        self.title('make character')
        ch = chara.Character()
        id = None
        password = None
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
        
        # group_label
        self.lbl1 = tk.Label(fm_left_1,text = '基本データ')
        self.lbl1.grid(row=1, column=0,columnspan=2, padx=5, pady=2)
        # name
        self.lbl1 = tk.Label(fm_left_1,text = 'name')
        self.lbl1.grid(row=2, column=0, padx=5, pady=2)
        self.ent1 = tk.Entry(fm_left_1,textvariable=ch.name)
        self.ent1.grid(row=2, column=1, padx=5, pady=2)
        # gene
        self.lbl2 = tk.Label(fm_left_1,text = 'gene')
        self.lbl2.grid(row=3, column=0, padx=5, pady=2)
        self.cbo2 = ttk.Combobox(fm_left_1, textvariable=ch.gene_id)
        # self.cbo2.bind('<<ComboboxSelected>>', self.cbo2_selected)
        self.cbo2['values']=('Foo', 'Bar', 'Baz')
        self.cbo2.set("Foo")
        self.cbo2.grid(row=3, column=1, padx=5, pady=2)
        # race
        self.lbl3 = tk.Label(fm_left_1,text = 'race')
        self.lbl3.grid(row=4, column=0, padx=5, pady=2)
        self.cbo3 = ttk.Combobox(fm_left_1, textvariable=ch.race_id)
        # self.cbo3.bind('<<ComboboxSelected>>', self.cbo2_selected)
        self.cbo3['values']=('Foo', 'Bar', 'Baz')
        self.cbo3.set("Foo")
        self.cbo3.grid(row=4, column=1, padx=5, pady=2)
        # age
        self.lbl4 = tk.Label(fm_left_1,text = 'age')
        self.lbl4.grid(row=5, column=0, padx=5, pady=2)
        self.ent4 = tk.Entry(fm_left_1, textvariable=ch.age)
        self.ent4.grid(row=5, column=1, padx=5, pady=2)
        # birth
        self.lbl5 = tk.Label(fm_left_1,text = 'birth')
        self.lbl5.grid(row=6, column=0, padx=5, pady=2)
        self.ent5 = tk.Entry(fm_left_1, textvariable=ch.birth)
        self.ent5.grid(row=6, column=1, padx=5, pady=2)
        
        fm_status = tk.Frame(self.root, bd=2, relief="ridge")
        pw_left.add(fm_left_1)

        # 基本情報フレーム２
        fm_left_2 = tk.Frame(pw_left, bd=2, relief="ridge")
        pw_left.add(fm_left_2)
        
        fm_status = tk.Frame(pw_left, bd=2, relief="ridge")
        pw_left.add(fm_left_1)

        # ログインボタン
        self.btn = tk.Button(fm_left_1, text='Submit', command=self.submit)
        # self.btn.pack()
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

    # ボタン押下後処理
    def submit(self):
        self.user_id = self.ent1.get()
        self.passwd = self.ent2.get()
        self.data = {'user_id':self.user_id, 'password':self.passwd}
        # validateを実行
        self.error = self.valid(self.data)
        # エラーの場合エラー文を返す
        if(len(self.error['digit']) > 0 | len(self.error['length']) > 0):
            ++self.v_err
            # TODO:長いのでerrorを項目ごとにブレイクさせる処理に修正
            for dkey, dvalue in self.error.items():
                for dkey1, dvalue1 in dvalue.items():
                    try:
                        # 複数エラーの場合は改行をかませる
                        self.error_output[dkey1].join('/r/n' + dvalue1)
                    except KeyError:
                        self.error_output[dkey1] = dvalue1
            self.lbl_er1['text'] = self.error_output['user_id']
            self.lbl_er2['text'] = self.error_output['password']
        else:
            # ユーザ情報を取得
            self.user_data = self.select_user(self.data)

            # 取得判定
            if(len(self.user_data) == 0):
                ++self.v_err
                self.lbl_er3['text'] = ERR_MESSAGE3
            else:
                self.destroy()
                return self.user_data
        if(self.v_err >= MAX_ERR):
            return
        
        # 0407続きはここから

    # 入力チェック
    def valid(self, data):
        v = validate()
        # 入力値をループ
        for dkey, dvalue in data.items():
            # 半角英数字チェック
            if(v.isdigit(dvalue) == True):
                self.error['digit'].setdefault(dkey, ERR_MESSAGE1.format(dkey))
            # 文字数制限チェック
            if(v.v_length(dvalue, LOGIN_MAXNUM) == False):
                self.error['length'].setdefault(dkey, ERR_MESSAGE2.format(dkey, LOGIN_MAXNUM))
        return self.error

    # validate後データ入力された情報をもとにuser情報を取得
    def select_user(self, data):
        self.sql = sql_query()
        sql = self.sql.select(MST_USERS)
        sql = self.sql.where(sql,data)

        # sqlを実行してデータを取得
        user_data = self.sql.execute(sql)
        return user_data
        
        # エラーの場合エラー文を返す

     
# import以外から呼び出された場合のみこのファイルを実行
# if __name__ == '__main__':
s = Signup()
s.mainloop()
