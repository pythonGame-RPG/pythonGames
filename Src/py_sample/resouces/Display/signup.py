from settings import *
from Sql import *
from validate import *
import random
import tkinter as tk
from turtle import *
import DTO.users as DTO
import DAO.usersDAO as DAO
import Base.basic_module as bs

class Signup(tk.Tk):
    def __init__(self,parent):
        self.parent = parent
        self.user = DTO.User()
        self._userDAO = DAO.UserDAO()
        self.name = tk.StringVar()
        self.user_id = tk.StringVar()
        self.password1 = tk.StringVar()
        self.password2 = tk.StringVar()

    def openDialog(self):
        # 子画面クラス
        self.window = tk.Toplevel(self.parent)
        # self.window.geometry('500x540')
        self.window.title("signup")
        
        self.createDisplay()
        
        # TODO:いらなくなったら消す
        self.parent.mainloop()

    def createDisplay(self):
        # ウィンドウを分ける
        self.entry_frame=tk.Frame(self.window, bg='cyan')
        self.entry_frame.pack(expand=True, fill = tk.BOTH, side="left")
        self.lblName = tk.Label(self.entry_frame,text = 'name')
        self.lblName.grid(row=0, column=0, padx=5, pady=2)
        self.entName = tk.Entry(self.entry_frame, textvariable=self.name)
        self.entName.grid(row=0, column=1, padx=5, pady=2)
        
        # ユーザID
        self.lblId = tk.Label(self.entry_frame, text = 'user_id')
        self.lblId.grid(row=2, column=0, padx=5, pady=2)
        self.entId = tk.Entry(self.entry_frame,textvariable=self.user_id)
        self.entId.grid(row=2, column=1, padx=5, pady=2)
        # パスワード1
        self.lblPass1 = tk.Label(self.entry_frame, text = 'password')
        self.lblPass1.grid(row=3, column=0, padx=5, pady=2)
        self.entPass1 = tk.Entry(self.entry_frame,textvariable=self.password1, show='*')
        self.entPass1.grid(row=3, column=1, padx=5, pady=2)
        # パスワード2
        self.lblPass2 = tk.Label(self.entry_frame, text = 'repeatPass')
        self.lblPass2.grid(row=4, column=0, padx=5, pady=2)
        self.entPass2 = tk.Entry(self.entry_frame,textvariable=self.password2, show='*')
        self.entPass2.grid(row=4, column=1, padx=5, pady=2)

        
        # ログインボタン
        self.btn = tk.Button(self.entry_frame, text='登録', command=self.submit)
        self.btn.grid(row=10, column=0, columnspan=2, padx=5, pady=2)
        
        self.running = True
        self.error = {}
        # 半角英数字エラー
        self.error['digit'] = {}
        # 文字列の長さエラー
        self.error['length'] = {}
        # パスワード一致エラー
        self.error['notMatch'] = ''
        # 辞書型データ('user_id':XXXX, 'password':XXXX)
        self.data = {}
        # エラー出力用
        self.error_output = {}
        self.users = None
        # 入力ロック判定用
        self.v_err = 0

    # ボタン押下後処理
    def submit(self):
        user_id = self.user_id.get()
        password1 = self.password1.get()
        password2 = self.password2.get()
        self.data = {'user_id':user_id, 'password1':password1, 'password2':password2 }
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
            # エラー文言セット
            self.lbl1 = tk.Label(self.entry_frame, foreground='#ff0000')
            self.lbl1.grid(row=1, column=0, padx=5, pady=2)
            self.lbl1['text'] = self.error_output['user_id']
            self.lblps1 = tk.Label(self.entry_frame, foreground='#ff0000')
            self.lblps1.grid(row=5, column=0, padx=5, pady=2)
            self.lblps1['text'] = self.error_output['password1']
            self.lblps2 = tk.Label(self.entry_frame, foreground='#ff0000')
            self.lblps2.grid(row=6, column=0, padx=5, pady=2)
            self.lblps2['text'] = self.error_output['password1']

        elif len(self.error['notMatch']) != 0:
            self.lblE4 = tk.Label(self.entry_frame, foreground='#ff0000')
            self.lblE4.grid(row=8, column=0, padx=5, pady=2)
            self.lblE4['text'] = self.error['notMatch']
        else:
            # ユーザ情報を取得
            self.user.init()
            self.user.user_id.set(self.user_id.get())
            self.user.password.set(self.password1.get())
            self.user.name.set(self.name.get())
            
            res = self._userDAO.insert_user(self.user)

            # 取得判定
            if res == 0:
                ++self.v_err
                self.lbl3 = tk.Label(self.entry_frame, foreground='#ff0000')
                self.lbl3.grid(row=7, column=0, padx=5, pady=2)
                self.lbl3['text'] = E0002
            else:
                # 登録完了ポップアップ表示
                bs.Popup.ShowInfo(self,E0002)
                self.destroy()
        if(self.v_err >= MAX_ERR):
            return


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
        
        if data['password1'] != data['password2']:
            self.error['notMatch'] = ERR_MESSAGE4
        return self.error
        
        # エラーの場合エラー文を返す

     
# import以外から呼び出された場合のみこのファイルを実行
# # if __name__ == '__main__':

root = tk.Tk()
c = Signup(root)
c.openDialog()