from settings import *
from Sql import *
from validate import *
import random
import DTO.character as chara
import DTO.genes as genes
import mycalendar as cal
import tkinter as tk
from tkinter import ttk
from turtle import *

# Login classes(GUIで実装)
class Signup(tk.Tk):
    def __init__(self):
        self.root = tk.Tk.__init__(self)
        #　子画面
        self.sub_root = cal.mycalendar(self)

        self.geometry('500x500')
        self.title('make character')
        self.chk_dangeonchar = tk.IntVar()

        self.selected_date = tk.StringVar()
        self.ch = chara.Character()
        self.ge = genes.Gene()

        # chara桁数制限
        self.ch.guild_rank.trace("w", lambda *args: self.character_limit(self.ch.guild_rank, 1))
        self.ch.level.trace("w", lambda *args: self.character_limit(self.ch.level, 3))
        self.ch.charisma.trace("w", lambda *args: self.character_limit(self.ch.charisma, 3))
        self.ch.karma.trace("w", lambda *args: self.character_limit(self.ch.karma, 3))
        self.ch.fortune.trace("w", lambda *args: self.character_limit(self.ch.fortune, 3))
        self.ch.intelligence.trace("w", lambda *args: self.character_limit(self.ch.intelligence, 3))
        # gene桁数制限
        self.ge.s_HP.trace("w", lambda *args: self.character_limit(self.ge.s_HP, 3))
        self.ge.s_MP.trace("w", lambda *args: self.character_limit(self.ge.s_MP, 3))
        self.ge.s_sta.trace("w", lambda *args: self.character_limit(self.ge.s_sta, 3))
        self.ge.s_atk.trace("w", lambda *args: self.character_limit(self.ge.s_atk, 3))
        self.ge.s_bit.trace("w", lambda *args: self.character_limit(self.ge.s_bit, 3))
        self.ge.s_mag.trace("w", lambda *args: self.character_limit(self.ge.s_mag, 3))
        self.ge.s_des.trace("w", lambda *args: self.character_limit(self.ge.s_des, 3))
        self.ge.s_agi.trace("w", lambda *args: self.character_limit(self.ge.s_agi, 3))

        self.total = tk.IntVar()
        self.ge.total_sense.trace("w", lambda *args: self.character_limit(self.total, 4))
        

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
        
        # group1_label
        self.lbl0 = tk.Label(fm_left_1,text = '基本データ')
        self.lbl0.grid(row=1, column=0,columnspan=5, padx=5, pady=2)
        # name
        self.lbl1 = tk.Label(fm_left_1,text = 'name')
        self.lbl1.grid(row=2, column=0, padx=5, pady=2)
        self.ent1 = tk.Entry(fm_left_1,textvariable=self.ch.name,width=10)
        self.ent1.grid(row=2, column=1, padx=5, pady=2)
        # sex
        self.lblsex = tk.Label(fm_left_1,text = 'sex')
        self.lblsex.grid(row=3, column=2, padx=5, pady=2)
        self.rdo1 = tk.Radiobutton(fm_left_1, value=0, variable=self.ch.sex, text='male')
        self.rdo1.grid(row=3, column=3, padx=5, pady=2)
        self.rdo2 = tk.Radiobutton(fm_left_1, value=1, variable=self.ch.sex, text='female')
        self.rdo2.grid(row=3, column=4, padx=5, pady=2)
        # location
        self.lblo = tk.Label(fm_left_1,text = 'location')
        self.lblo.grid(row=4, column=2, padx=5, pady=2)
        self.cboo = ttk.Combobox(fm_left_1, textvariable=self.ch.location_id,width=18)
        self.cboo['values']=('Foo', 'Bar', 'Baz')
        self.cboo.set("Foo")
        self.cboo.grid(row=4, column=3, columnspan=2, padx=5, pady=2)

        # dangeon_chara
        self.chk13 = tk.Checkbutton(fm_left_1, variable=int, var=self.chk_dangeonchar, text='dangeon_chara')
        self.chk13.grid(row=2, column=2,columnspan=2, padx=5, pady=2)
        # gene
        self.lbl2 = tk.Label(fm_left_1,text = 'gene')
        self.lbl2.grid(row=3, column=0, padx=5, pady=2)
        self.cbo2 = ttk.Combobox(fm_left_1, textvariable=self.ch.gene_id,width=10)
        self.cbo2['values']=('Foo', 'Bar', 'Baz')
        self.cbo2.set("Foo")
        self.cbo2.grid(row=3, column=1, padx=5, pady=2)
        # race
        self.lbl3 = tk.Label(fm_left_1,text = 'race')
        self.lbl3.grid(row=4, column=0, padx=5, pady=2)
        self.cbo3 = ttk.Combobox(fm_left_1, textvariable=self.ch.race_id,width=10)
        self.cbo3['values']=('Foo', 'Bar', 'Baz')
        self.cbo3.set("Foo")
        self.cbo3.grid(row=4, column=1, padx=5, pady=2)
        
        # birth
        self.lbl4 = tk.Label(fm_left_1,text = 'birth')
        self.lbl4.grid(row=5, column=2, padx=5, pady=2)
        self.ent4 = tk.Entry(fm_left_1, textvariable=self.selected_date,width=10)
        self.ent4.grid(row=5, column=3, padx=5, pady=2)
        # birthをDTOにセット
        self.ch.birth.set(self.ent4.get())

        # 日付選択アイコン
        self.i_birth = tk.Button(fm_left_1, text = "日付選択", font = ("",8),command=self.sub_root.openDialog)
        #self.i_birth.bind("<1>",self.select_birth)
        self.i_birth.grid(row=5, column=4, padx=5, pady=2)

        # birthplace
        self.lbl5a = tk.Label(fm_left_1,text = 'birthplace')
        self.lbl5a.grid(row=5, column=0, padx=5, pady=2)
        self.cbo5a = ttk.Combobox(fm_left_1, textvariable=self.ch.birthplace,width=10)
        self.cbo5a['values']=('Foo', 'Bar', 'Baz')
        self.cbo5a.set("Foo")
        self.cbo5a.grid(row=5, column=1, padx=5, pady=2)

        # ステータスフレーム
        fm_status = tk.Frame(pw_left, bd=2, relief="ridge")
        pw_left.add(fm_status)
        # group2_label
        self.lbl0 = tk.Label(fm_status,text = 'ステータス')
        self.lbl0.grid(row=0, column=0,columnspan=6, padx=5, pady=2)
        # RANK
        self.lbl5 = tk.Label(fm_status,text = 'G_rank')
        self.lbl5.grid(row=1, column=0, padx=5, pady=2)
        self.cbo2 = ttk.Combobox(fm_status, textvariable=self.ch.guild_rank,width=3)
        self.cbo2['values']=('G', 'F', 'E', 'D', 'C', 'B', 'A', 'S')
        self.cbo2.set("G")
        self.cbo2.grid(row=1, column=1, padx=5, pady=2)
        # LEVEL
        self.lbl6 = tk.Label(fm_status,text = 'level')
        self.lbl6.grid(row=1, column=2, padx=5, pady=2)
        self.ent6 = tk.Entry(fm_status, textvariable=self.ch.level, width=7)
        self.ent6.grid(row=1, column=3, padx=5, pady=2)
        # HP
        self.lbl7 = tk.Label(fm_status,text = 'HP')
        self.lbl7.grid(row=2, column=0, padx=5, pady=2)
        self.ent7 = tk.Entry(fm_status, textvariable=self.ge.s_HP, width=7)
        self.ent7.grid(row=2, column=1, padx=5, pady=2)
        # MP
        self.lbl8 = tk.Label(fm_status,text = 'MP')
        self.lbl8.grid(row=2, column=2, padx=5, pady=2)
        self.ent8 = tk.Entry(fm_status, textvariable=self.ge.s_MP, width=7)
        self.ent8.grid(row=2, column=3, padx=5, pady=2)
        # charisma
        self.lblcha = tk.Label(fm_status,text = 'charisma')
        self.lblcha.grid(row=2, column=4, padx=5, pady=2)
        self.entcha = tk.Entry(fm_status, textvariable=self.ch.charisma, width=7)
        self.entcha.grid(row=2, column=5, padx=5, pady=2)
        # sta
        self.lbl9 = tk.Label(fm_status,text = 'sta')
        self.lbl9.grid(row=3, column=0, padx=5, pady=2)
        self.ent9 = tk.Entry(fm_status, textvariable=self.ge.s_sta, width=7)
        self.ent9.grid(row=3, column=1, padx=5, pady=2)
        # atk
        self.lbl10 = tk.Label(fm_status,text = 'atk')
        self.lbl10.grid(row=3, column=2, padx=5, pady=2)
        self.ent10 = tk.Entry(fm_status, textvariable=self.ge.s_atk, width=7)
        self.ent10.grid(row=3, column=3, padx=5, pady=2)
        # karma
        self.lblka = tk.Label(fm_status,text = 'karma')
        self.lblka.grid(row=3, column=4, padx=5, pady=2)
        self.entka = tk.Entry(fm_status, textvariable=self.ch.karma, width=7)
        self.entka.grid(row=3, column=5, padx=5, pady=2)
        # bit
        self.lbl11 = tk.Label(fm_status,text = 'bit')
        self.lbl11.grid(row=4, column=0, padx=5, pady=2)
        self.ent11 = tk.Entry(fm_status, textvariable=self.ge.s_bit, width=7)
        self.ent11.grid(row=4, column=1, padx=5, pady=2)
        # mag
        self.lbl12 = tk.Label(fm_status,text = 'mag')
        self.lbl12.grid(row=4, column=2, padx=5, pady=2)
        self.ent12 = tk.Entry(fm_status, textvariable=self.ge.s_mag, width=7)
        self.ent12.grid(row=4, column=3, padx=5, pady=2)
        # fortune
        self.lblcha = tk.Label(fm_status,text = 'fortune')
        self.lblcha.grid(row=4, column=4, padx=5, pady=2)
        self.entcha = tk.Entry(fm_status, textvariable=self.ch.fortune, width=7)
        self.entcha.grid(row=4, column=5, padx=5, pady=2)
        # des
        self.lbl11 = tk.Label(fm_status,text = 'des')
        self.lbl11.grid(row=5, column=0, padx=5, pady=2)
        self.ent11 = tk.Entry(fm_status, textvariable=self.ge.s_des, width=7)
        self.ent11.grid(row=5, column=1, padx=5, pady=2)
        # agi
        self.lbl12 = tk.Label(fm_status,text = 'agi')
        self.lbl12.grid(row=5, column=2, padx=5, pady=2)
        self.ent12 = tk.Entry(fm_status, textvariable=self.ge.s_agi, width=7)
        self.ent12.grid(row=5, column=3, padx=5, pady=2)
        # intelligence
        self.lblcha = tk.Label(fm_status,text = 'intelligence')
        self.lblcha.grid(row=5, column=4, padx=5, pady=2)
        self.entcha = tk.Entry(fm_status, textvariable=self.ch.intelligence, width=7)
        self.entcha.grid(row=5, column=5, padx=5, pady=2)
        # total_sense
        self.lbl12 = tk.Label(fm_status,text = 'total_sense')
        self.lbl12.grid(row=6, column=2, padx=5, pady=2)
        self.ent12 = tk.Entry(fm_status, textvariable=self.ge.total_sense, width=7)
        self.ent12.grid(row=6, column=3, padx=5, pady=2)
        # total
        self.lbl12 = tk.Label(fm_status,text = 'total')
        self.lbl12.grid(row=6, column=4, padx=5, pady=2)
        self.ent12 = tk.Entry(fm_status, textvariable=self.total,  width=7)
        self.ent12.grid(row=6, column=5, padx=5, pady=2)
        # intelligence
        self.lblcha = tk.Label(fm_status,text = 'intelligence')
        self.lblcha.grid(row=5, column=4, padx=5, pady=2)
        self.entcha = tk.Entry(fm_status, textvariable=self.ch.intelligence, width=7)
        self.entcha.grid(row=5, column=5, padx=5, pady=2)
        
        # 特殊フレーム
        fm_specify = tk.Frame(pw_left, bd=2, relief="ridge")
        pw_left.add(fm_specify)
        # group3_label
        self.lbl_s = tk.Label(fm_specify,text = '特技')
        self.lbl_s.grid(row=0, column=0,columnspan=4, padx=5, pady=2)
        # Class1
        self.lbl13 = tk.Label(fm_specify,text = 'class')
        self.lbl13.grid(row=1, column=0, padx=5, pady=2)
        self.cbo2 = ttk.Combobox(fm_specify, textvariable=self.ch.class1 ,width=12)
        self.cbo2['values']=('無職', 'F', 'E', 'D', 'C', 'B', 'A', 'S')
        self.cbo2.set("無職")
        self.cbo2.grid(row=1, column=1, padx=5, pady=2)
        # Class2
        self.cbo2 = ttk.Combobox(fm_specify, textvariable=self.ch.class2 ,width=12)
        self.cbo2['values']=('ナイト', 'F', 'E', 'D', 'C', 'B', 'A', 'S')
        self.cbo2.set("")
        self.cbo2.grid(row=1, column=2, padx=5, pady=2)
        # Class3
        self.cbo2 = ttk.Combobox(fm_specify, textvariable=self.ch.class3 ,width=12)
        self.cbo2['values']=('ナイト', 'F', 'E', 'D', 'C', 'B', 'A', 'S')
        self.cbo2.set("")
        self.cbo2.grid(row=1, column=3, padx=5, pady=2)
        # talent1
        self.lbl16 = tk.Label(fm_specify,text = 'talent')
        self.lbl16.grid(row=2, column=0, padx=5, pady=2)
        self.cbo2 = ttk.Combobox(fm_specify, textvariable=self.ch.talent1 ,width=12)
        self.cbo2['values']=('なし', 'F', 'E', 'D', 'C', 'B', 'A', 'S')
        self.cbo2.set("なし")
        self.cbo2.grid(row=2, column=1, padx=5, pady=2)
        # talent2
        self.cbo2 = ttk.Combobox(fm_specify, textvariable=self.ch.talent2 ,width=12)
        self.cbo2['values']=('なし', 'F', 'E', 'D', 'C', 'B', 'A', 'S')
        self.cbo2.set("")
        self.cbo2.grid(row=2, column=2, padx=5, pady=2)
        # talent3
        self.cbo2 = ttk.Combobox(fm_specify, textvariable=self.ch.talent3 ,width=12)
        self.cbo2['values']=('なし', 'F', 'E', 'D', 'C', 'B', 'A', 'S')
        self.cbo2.set("")
        self.cbo2.grid(row=2, column=3, padx=5, pady=2)

        # 特殊フレーム
        fm_flg = tk.Frame(pw_left, bd=2, relief="ridge")
        pw_left.add(fm_flg)
        # group4_label
        self.lbl_f = tk.Label(fm_flg,text = 'フラグ')
        self.lbl_f.grid(row=0, column=1,columnspan=2, padx=5, pady=2)
        # dangeon
        self.chk13 = tk.Checkbutton(fm_flg, variable=int, var=self.ch.is_dangeon, text='is_dangeon')
        self.chk13.grid(row=1, column=0, padx=5, pady=2)
        # master
        self.chk14 = tk.Checkbutton(fm_flg, variable=int, var=self.ch.is_master, text='is_master')
        self.chk14.grid(row=1, column=1, padx=5, pady=2)
        # user
        self.chk15 = tk.Checkbutton(fm_flg, variable=int, var=self.ch.is_user, text='is_user')
        self.chk15.grid(row=1, column=2, padx=5, pady=2)
        # retire
        self.chk15 = tk.Checkbutton(fm_flg, variable=int, var=self.ch.is_retire, text='is_retire')
        self.chk15.grid(row=1, column=3, padx=5, pady=2)

        # ランダムボタン
        self.btn = tk.Button(fm_flg, text='ランダム生成', command=self.random_generate)
        self.btn.grid(row=7, column=0, columnspan=2, padx=5, pady=2)
        # 登録ボタン
        self.btn = tk.Button(fm_flg, text='登録', command=self.submit)
        self.btn.grid(row=7, column=2, columnspan=2, padx=5, pady=2)

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
        # self.after(10,self)

    def random_generate(self):
        pass
        # 最大3桁の数字を生成×12→関数でステータスに設定

        # 1～100までの数字生成（level用）→関数でステータスに設定
        # levelに応じた選択可能範囲の設定関数
        # 標準偏差関数（かなりきわどいやつ）を設定（標準化のため）
        # コンボボックス用マップ作成(id, name)→gene, race, g_rank, birthplace 
        # コンボボックス用マップ作成(id, name)→class, talent（LEVEL制限あり）
        # 日付生成ランダム→これどうやるの？
        # ランダムビット生成→1の確率ほぼ0
        # ランダムビット生成→50%、30%
        # 名前のランダム生成→人名、国、class、talent

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

    # 入力文字数制限
    def character_limit(self,entry_text, num):
        if len(str(entry_text.get())) > 0:
            entry_text.set(str(entry_text.get())[:num])
            # total_sense集計
            self.ge.total_sense.set(str(self.ge.s_HP.get()+self.ge.s_MP.get()+self.ge.s_sta.get()
            +self.ge.s_atk.get()+self.ge.s_bit.get()+self.ge.s_mag.get()+self.ge.s_HP.get()
            +self.ge.s_des.get()+self.ge.s_agi.get()))
            # total集計
            self.total.set(str(self.ge.total_sense.get()+self.ch.charisma.get()
            +self.ch.karma.get()+self.ch.fortune.get()+self.ch.intelligence.get()))

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
