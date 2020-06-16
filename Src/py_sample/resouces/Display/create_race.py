from settings import *
import tkinter as tk
import tkinter.ttk as ttk
import datetime
from turtle import *
import DAO.racesDAO as _races
import DTO.races as races

selected_d = ''

# カレンダーを作成するフレームクラス
class create_race():
    def __init__(self,parent):

        import datetime
        self.parent = parent
        self.dialog = None

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
        pw_left = tk.PanedWindow(pw_main, bg="cyan", orient='vertical')
        pw_main.add(pw_left)
        pw_right = tk.PanedWindow(pw_main, bg="yellow", orient='vertical')
        pw_main.add(pw_right)
        # self.window→pw_right_up（右上画面登録部）
        pw_right_up = tk.PanedWindow(pw_right, bg="pink", orient='horizontal')
        pw_right.add(pw_right_up)
        # self.window→pw_right_down（右下画面ボタン部）
        pw_right_down = tk.PanedWindow(pw_right, bg="pink", orient='horizontal')
        pw_right.add(pw_right_down)

        # ステータスフレーム
        frame_top = tk.Frame(pw_left, bd=2, relief="ridge")
        
        # frame_top = tk.Frame(self.window)
        # rame_top.pack(pady=5)
        # HP
        self.lbl7 = tk.Label(pw_right_up,text="HP",width=9)
        self.lbl7.grid(row=2, column=0, padx=5, pady=2)
        self.ent7 = tk.Entry(frame_top, textvariable=self.ra.p_HP, width=4)
        self.ent7.grid(row=2, column=1, padx=5, pady=2)
        # MP
        self.lbl8 = tk.Label(pw_right_up,text="MP",width=9)
        self.lbl8.grid(row=2, column=2, padx=5, pady=2)
        self.ent8 = tk.Entry(frame_top, textvariable=self.ra.p_MP, width=4)
        self.ent8.grid(row=2, column=3, padx=5, pady=2)
        # sta
        self.lbl9 = tk.Label(pw_right_up,text="sta",width=9)
        self.lbl9.grid(row=3, column=0, padx=5, pady=2)
        self.ent9 = tk.Entry(frame_top, textvariable=self.ra.p_sta, width=4)
        self.ent9.grid(row=3, column=1, padx=5, pady=2)
        # atk
        self.lbl10 = tk.Label(pw_right_up,text="atk",width=9)
        self.lbl10.grid(row=3, column=2, padx=5, pady=2)
        self.ent10 = tk.Entry(frame_top, textvariable=self.ra.p_atk, width=4)
        self.ent10.grid(row=3, column=3, padx=5, pady=2)
        # vit
        self.lbl11 = tk.Label(pw_right_up,text="vit",width=9)
        self.lbl11.grid(row=4, column=0, padx=5, pady=2)
        self.ent11 = tk.Entry(frame_top, textvariable=self.ra.p_vit, width=4)
        self.ent11.grid(row=4, column=1, padx=5, pady=2)
        # mag
        self.lbl12 = tk.Label(pw_right_up,text="mag",width=9)
        self.lbl12.grid(row=4, column=2, padx=5, pady=2)
        self.ent12 = tk.Entry(frame_top, textvariable=self.ra.p_mag, width=4)
        self.ent12.grid(row=4, column=3, padx=5, pady=2)
        # des
        self.lbl13 = tk.Label(pw_right_up,text="des",width=9)
        self.lbl13.grid(row=5, column=0, padx=5, pady=2)
        self.ent13 = tk.Entry(frame_top, textvariable=self.ra.p_des, width=4)
        self.ent13.grid(row=5, column=1, padx=5, pady=2)
        # agi
        self.lbl14 = tk.Label(pw_right_up,text="agi",width=9)
        self.lbl14.grid(row=5, column=2, padx=5, pady=2)
        self.ent14 = tk.Entry(frame_top, textvariable=self.ra.p_agi, width=4)
        self.ent14.grid(row=5, column=3, padx=5, pady=2)

        # ツリービュー部
        self.tree=ttk.Treeview(master)

        mainloop()

          
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

    """
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
    """

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
         #self.bind('<Button-1>',callback)# 追記 https://teratail.com/questions/234639
"""        
def callback(event):
    selected_date = ''
    if event.widget['text'] not in ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']:
        selected_date += YEAR
        selected_date += convert_in2_2bytes(MONTH)
        selected_date += convert_in2_2bytes(str(event.widget['text']))
        select_d = selected_date
"""

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
