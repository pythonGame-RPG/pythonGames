from settings import *
import tkinter as tk
import tkinter.ttk as ttk
import datetime
from turtle import *

selected_d = ''

# カレンダーを作成するフレームクラス
class mycalendar():
    def __init__(self,parent):

        import datetime
        self.parent = parent
        self.dialog = None

        # 現在の日付を取得
        now = datetime.datetime.now()
        # 現在の年と月を属性に追加
        self.year = now.year
        self.month = now.month
        self.selected_d = tk.StringVar()

        # 追記 https://teratail.com/questions/234639#reply-355304
        global YEAR, MONTH
        YEAR = str(self.year)
        MONTH = str(self.month)

    def openDialog(self):        
       # 子画面クラス
        self.window = tk.Toplevel(self.parent)
        self.window.title("Calendar App")

        # エンターキーに更新処理をバインド
        self.window.bind('<Return>', self.change_month)

        # frame_top部分の作成
        frame_top = tk.Frame(self.window)
        frame_top.pack(pady=5)
        self.previous_month = tk.Label(frame_top, text = "<", font = ("",14))
        self.previous_month.bind("<1>",self.change_month)
        self.previous_month.pack(side = "left", padx = 10)

        # yearの出力→コンボボックスに変更?
        self.current_year = tk.Entry(frame_top, font = ("",18), width=4)
        self.current_year.delete(tk.END)
        self.current_year.insert(tk.END, self.year)
        self.current_year.pack(side = "left")
        # monthの出力→コンボボックスに変更
        self.current_month = tk.Label(frame_top, text = self.month, font = ("",18))
        self.current_month.pack(side = "left")

        self.next_month = tk.Label(frame_top, text = ">", font = ("",14))
        self.next_month.bind("<1>",self.change_month)
        self.next_month.pack(side = "left", padx = 10)

        # frame_week部分の作成
        frame_week = tk.Frame(self.window)
        frame_week.pack()
        button_mon = d_button(frame_week,  text = "Mon")
        button_mon.grid(column=0,row=0)
        button_tue = d_button(frame_week,  text = "Tue")
        button_tue.grid(column=1,row=0)
        button_wed = d_button(frame_week,  text = "Wed")
        button_wed.grid(column=2,row=0)
        button_thu = d_button(frame_week,  text = "Thu")
        button_thu.grid(column=3,row=0)
        button_fri = d_button(frame_week,  text = "Fri")
        button_fri.grid(column=4,row=0)
        button_sta = d_button(frame_week,  text = "Sat", fg = "blue")
        button_sta.grid(column=5,row=0)
        button_san = d_button(frame_week,  text = "Sun", fg = "red")
        button_san.grid(column=6,row=0)

        # frame_calendar部分の作成
        self.frame_calendar = tk.Frame(self.window)
        self.frame_calendar.pack()

        # 日付部分を作成するメソッドの呼び出し
        self.create_calendar(self.year,self.month)

          
    def create_calendar(self,year,month):
        "指定した年(year),月(month)のカレンダーウィジェットを作成する"

        # ボタンがある場合には削除する（初期化）
        try:
            for key,item in self.day.items():
                item.destroy()
        except:
            pass

        # calendarモジュールのインスタンスを作成
        import calendar
        cal = calendar.Calendar()
        # 指定した年月のカレンダーをリストで返す
        days = cal.monthdayscalendar(year,month)

        # 日付ボタンを格納する変数をdict型で作成
        self.day = {}
        # for文を用いて、日付ボタンを生成
        for i in range(0,42):
            c = i - (7 * int(i/7))
            r = int(i/7)
            try:
                # 日付が0でなかったら、ボタン作成
                if days[r][c] != 0:
                    self.day[i] = d_button(self.frame_calendar,text = days[r][c]) #,command=self.quit
                    self.day[i].configure(font=("",14),height=2, width=4, relief="flat")
                    self.day[i].bind('<Button-1>',self.quit_a)
                    self.day[i].grid(column=c,row=r)
            except:
                """
                月によっては、i=41まで日付がないため、日付がないiのエラー回避が必要
                """
                break

    def quit_a(self,event):
        selected_date = ''
        if event.widget['text'] not in ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']:
            selected_date += YEAR
            selected_date += convert_in2_2bytes(MONTH)
            selected_date += convert_in2_2bytes(str(event.widget['text']))
            from datetime import datetime as dt
            adt = dt.strptime(selected_date, '%Y%m%d')
            newstr = adt.strftime('%Y/%m/%d')
            self.parent.selected_date.set(newstr)

        # self.closeDialog()
        self.window.destroy()
        return "break"

    # textの内容のリセットself.yearに格納
    def change_month(self,event):
        # 入力されたyearをself.yearに格納datetime型に変換
        self.year = datetime.datetime.strptime(self.current_year.get(), '%Y').year

        # 押されたラベルを判定し、月の計算
        if event.widget["text"] == "<":
            self.month -= 1
        else:
            self.month += 1
        # 月が0、13になったときの処理
        if self.month == 0:
            self.year -= 1
            self.month = 12
        elif self.month == 13:
            self.year +=1
            self.month =1
        # frame_topにある年と月のラベルを変更する
        # labelではないのでカット。
        self.current_year["text"] = self.year
        self.current_month["text"] = self.month

        # 追記 https://teratail.com/questions/234639#reply-355304
        global YEAR, MONTH
        YEAR = str(self.year)
        MONTH = str(self.month)

        self.current_year.delete(0, tk.END) 
        self.current_year.insert(tk.END, self.year)
        # self.current_year.pack(side = "left")
        # 日付部分を作成するメソッドの呼び出し
        self.create_calendar(self.year,self.month)

# デフォルトのボタンクラス
# どーでもいいボタン、メインループあるのに何で別クラス？やりずらいんだが。
class d_button(tk.Button):
    def __init__(self,master=None,cnf={},**kw):
        tk.Button.__init__(self,master,cnf,**kw)
        self.selected_date = ''
        self.configure(font=("",14),height=2, width=4, relief="flat")
        # self.bind('<Button-1>',callback)# 追記 https://teratail.com/questions/234639
        self.bind('<Button-1>',callback)# 追記 https://teratail.com/questions/234639
        
def callback(event):
    selected_date = ''
    if event.widget['text'] not in ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']:
        selected_date += YEAR
        selected_date += convert_in2_2bytes(MONTH)
        selected_date += convert_in2_2bytes(str(event.widget['text']))
        select_d = selected_date

# 1桁の数字を2バイトに変換する関数
# 追記 https://teratail.com/questions/234639#reply-355304
def convert_in2_2bytes(str_number):
    if len(str_number) == 1:
        return '0' + str_number
    else:
        return str_number

"""
def get_birth():
    selected_date = 'a'
    m = mycalendar()
    # m.mainloop()
    selected_date = selected_d
    return selected_date
"""

# c = cal()
#m = mycalendar()
#m.mainloop()
