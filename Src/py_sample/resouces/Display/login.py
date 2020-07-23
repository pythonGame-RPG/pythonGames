from settings import *
from Sql import *
from validate import *
import random
import tkinter as tk
import signup as sg
from turtle import *

# Login classes(GUIで実装)
class Login(tk.Tk):
    def __init__(self):
        self.root = tk.Tk.__init__(self)
        self.geometry('200x200')
        self.title('Enter password')
        # tkinterパーツを初期化
        #self.root = tk.Tk()
        # パーツ１：user_id入力
        self.ent1 = tk.Entry(self.root)
        self.ent1.pack()
        self.lbl1 = tk.Label(self.root, foreground='#ff0000')
        self.lbl1.pack()
        # パーツ２：password入力
        self.ent2 = tk.Entry(self.root, show='*')
        self.ent2.pack()
        self.lbl2 = tk.Label(self.root, foreground='#ff0000')
        self.lbl2.pack()
        self.lbl3 = tk.Label(self.root, foreground='#ff0000')
        self.lbl3.pack()
        # ログインボタン
        self.btn = tk.Button(self.root, text='Submit', command=self.submit)
        self.btn.pack()
        self.lbl3.pack()
        # アカウント作成ボタン
        self.btnAcount = tk.Button(self.root, text='Submit', command=self.makeAcount)
        self.btnAcount.pack()
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
            self.lbl1['text'] = self.error_output['user_id']
            self.lbl2['text'] = self.error_output['password']
        else:
            # ユーザ情報を取得
            self.user_data = self.select_user(self.data)

            # 取得判定
            if(len(self.user_data) == 0):
                ++self.v_err
                self.lbl3['text'] = ERR_MESSAGE3
            else:
                self.destroy()
                return self.user_data
        if(self.v_err >= MAX_ERR):
            return
        
    def makeAcount(self):
        s = sg.Signup(self)
        s.openDialog()
        
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
# # if __name__ == '__main__':
