import tkinter as tk
from tkinter import ttk

class FruitTree:
    def __init__(self,root):
        self.root = root
        self.iid=""
        self.rootiid=""
        self.frout_list = [
            {'id':1,'root_id':0,'name':'リンゴ'},
            {'id':2,'root_id':0,'name':'イチゴ'},
            {'id':101,'root_id':1,'name':'アップルパイ'},
            {'id':102,'root_id':1,'name':'リンゴジュース'},
            {'id':103,'root_id':2,'name':'イチゴ大福'},
        ]
        self.fruitRoot = {}
        self.fruitTree = {}

        # 画面表示
        self.createDisplay()
    
    def createDisplay(self):

        # フルーツフレーム
        self.pw_main = self.createTreeView(self.root)
        self.pw_main.pack(expand=True, fill = tk.BOTH, side="left")
    
    def createTreeView(self, pw_main):
        treeFrame = tk.Frame(pw_main, bg="cyan")
        # 検索したfruitをツリーに表示
        self.setSearchTree(treeFrame)
        return treeFrame
    
    def setSearchTree(self, treeFrame):
        self.tree = ttk.Treeview(treeFrame)
        # 選択イベント（必要であれば）
        # self.tree.bind("<<TreeviewSelect>>",self.targetFruit)
        # ツリー名
        self.tree.heading("#0",text="fruit_tree")
        self.tree.pack()
        # rootのiidを登録
        self.rootiid = self.tree.insert("","end",text="Home")
        self.iid = self.rootiid
        # 果物ツリー作成
        self.makeTree()

    # ツリー構成
    def makeTree(self):

        # 根となるfruitを取得
        initial_fruit = [fruit for fruit in self.frout_list if fruit['root_id'] == 0]
        
        # ツリーごとの果物要素を取得
        self.setFruitTree(initial_fruit,self.iid)
    
    # fruitのツリー構造を生成
    def setFruitTree(self,_addTree,_iid):

        # _addTree:アクティブツリーのノード
        for _fruit in _addTree:
            
            rootiid = self.tree.insert(_iid,"end",text=str(_fruit['id']) + ':' + _fruit['name'])
            iid = rootiid
            # 選択イベント用
            self.iid = iid
            # 選択果物を格納
            self.fruitRoot[iid] = _fruit

            # 進化先fruitを取得
            addFruit = [fruit for fruit in self.frout_list if _fruit['id'] == fruit['root_id']]

            # 進化先が存在する場合
            if len(addFruit) != 0:
                self.fruitTree[iid] = addFruit
                self.setFruitTree(addFruit,iid)

root = tk.Tk()
c = FruitTree(root)
root.mainloop()