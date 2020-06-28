import tkinter as tk
import tkinter.ttk as ttk

# 種族選択画面を作成するフレームクラス
class create_kind():
    def __init__(self,parent):

        self.parent = parent
        self.dialog = None
        self.iid=""
        self.rootiid=""
        self.kindRoot = {}
        self.kindTree = {}
        self.s_kind = []

    def openDialog(self):        
       # 子画面クラス
        self.window = tk.Toplevel(self.parent)
        self.window.geometry('200x300')
        self.window.title("kind App")
        
        # ウィンドウを分ける
        pw_main = tk.PanedWindow(self.window, orient='horizontal')
        pw_main.pack(expand=True, fill = tk.BOTH, side="left")

        pw_left = tk.PanedWindow(pw_main, bg="cyan", orient='vertical')
        self.tree = ttk.Treeview(pw_left)

        self.tree.heading("#0",text="kind_tree")
        self.tree.pack()

        self.rootiid = self.tree.insert("","end",text="Home")
        self.iid = self.rootiid

        pw_main.add(pw_left)

        self.parent.mainloop()

root = tk.Tk()
c = create_kind(root)
c.openDialog()