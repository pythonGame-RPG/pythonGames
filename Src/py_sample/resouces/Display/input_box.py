from tkinter import *
import tkinter.ttk as ttk
import tkinter.filedialog as filedialog
import os
import tkinter.messagebox as messagebox


# ディレクトリ構造をクラス化する
class Directory():

    # subDirs -> Directory List
    def __init__(self, dirPath,subDirs=None):
        self.dirPath = dirPath
        self.subDirs = subDirs

    def getSubDirs(self):
        return self.subDirs

    def getDirPath(self):
        return self.dirPath

#Directory作成ロジック
class MakeDirectoryLogic():

    def __init__(self,rootPath):
        self.setRootPath(rootPath)

    #Directoryの情報をもとに実際にフォルダを作成する
    def makeDirectory(self,rootPath,dirList):
        # パスが存在しない場合は即終了
        if os.path.exists(rootPath) ==False:
            return
        for dir in dirList:
            path = os.path.join(rootPath,dir.getDirPath())
            print("path",path)
            os.mkdir(path)
            # 子の階層を作成する
            children = dir.getSubDirs()
            if len(children) > 0:
                self.makeDirectory(path,children)
    # tree =ttk.Treeview
    # ツリーの情報からDirectoryリストを作成する
    def createDirectoryList(self,rootiid,tree,dirList):
        dirname = tree.item(rootiid,"text")
        children = tree.get_children(rootiid)
        childlist=[]
        dir = Directory(dirname,childlist)
        dirList.append(dir)
        if len(children)>0:
            for child in children:
                self.createDirectoryList(child,tree,childlist)
    # ルートパスを設定する
    def setRootPath(self,rootPath):
        self.rootPath = rootPath

    # GUIから呼び出すディレクトリ作成アクション
    def makeDirectoryAction(self,tree,rootiid):
        dirList=[]
        self.createDirectoryList(rootiid,tree,dirList)
        self.makeDirectory(self.rootPath,dirList)

class MakeDirectoryTools(ttk.Frame):

    def __init__(self,master):
        super().__init__(master)
        self.rootPath = StringVar()
        self.targetDir = StringVar()
        self.addDir = StringVar()
        self.iid=""
        self.rootiid=""
        self.logic = MakeDirectoryLogic(self.rootPath.get())
        self.create_widgets()

    def create_widgets(self):
        leftframe = self.createTreeView()
        leftframe.pack(side="left")
        rightframe= self.createInputPanel()
        rightframe.pack(side="right")
        self.pack()

    def createTreeView(self):
        treeFrame = ttk.Frame(self)
        self.tree = ttk.Treeview(treeFrame)
        # ツリーの項目が選択されたら指定されたを新しく階層を作るディレクトリ名を更新する
        self.tree.bind("<<TreeviewSelect>>",self.targetDirectory)
        # 列名をつける
        self.tree.heading("#0",text="Directory")
        self.tree.pack()
        # rootのiidを登録
        self.rootiid = self.tree.insert("","end",text="makedirectoryTools")
        self.iid = self.rootiid
        return treeFrame

    def createInputPanel(self):

        inputFrame = ttk.LabelFrame(self,text="InputParam")
        # 新しく作成するディレクトリのルート
        rootPathLabel = ttk.Label(inputFrame,text="RootPath")
        rootPathLabel.grid(column=0,row=0)
        rootpathEntry = ttk.Entry(inputFrame,textvariable=self.rootPath)
        rootpathEntry.grid(column=1,row=0)
        rootpathButton = ttk.Button(inputFrame,text="open",command=self.openFileDialog)
        rootpathButton.grid(column=2,row=0)

        #新しく階層を作るディレクトリを表示するWidget
        addPathLabel = ttk.Label(inputFrame,text="TargetDir")
        addPathLabel.grid(column=0,row=1)
        addpathEntry = ttk.Entry(inputFrame,state="readonly",textvariable=self.targetDir)
        addpathEntry.grid(column=1,row=1)
        addPathButton = ttk.Button(inputFrame,text="delete",command = self.deleteDirectory)
        addPathButton.grid(column=2,row=1)

        #追加するディレクトリを表示するWidget
        addNodeLabel = ttk.Label(inputFrame,text="AddDir")
        addNodeLabel.grid(column=0,row=2)
        addNodeEntry = ttk.Entry(inputFrame,textvariable=self.addDir)
        addNodeEntry.grid(column=1,row=2)
        addNodeButton = ttk.Button(inputFrame,text="add",command=self.insertDirectory)
        addNodeButton.grid(column=2,row=2)

        # 作成するボタン
        makeDirButton = ttk.Button(inputFrame,text="makeDirectory",command=self.makeDirectory)
        makeDirButton.grid(column=2,row=3)

        return inputFrame

    # ルートパスのディレクトリを決める
    def openFileDialog(self):
        folder  = filedialog.askdirectory();
        self.rootPath.set(folder)
        self.logic.setRootPath(folder)

    # 指定されたディレクトリを反映
    def targetDirectory(self,event):
        self.iid = self.tree.focus()
        if self.iid :
            self.targetDir.set(self.tree.item(self.iid,"text"))

    #指定されたディレクトリに子階層を加える
    def insertDirectory(self):
        addDir = self.addDir.get()
        # ディレクトリ名がない場合は処理しない
        if addDir != "":
            children = self.tree.get_children(self.iid)

            # 同じ階層に同じ名前で作成は不可
            for child in children:
                childname = self.tree.item(child,"text")
                if childname == addDir:
                    messagebox.showerror("登録エラー","既に登録されています")
                    return
            self.tree.insert(self.iid,"end",text=self.addDir.get())
    #ディレクトリを削除する
    def deleteDirectory(self):
        if self.iid == "" or self.iid == self.rootiid:
            messagebox.showerror("削除エラー","削除する階層を選択してください。\nmakedirectoryToolsディレクトリは削除できません。")
            return
        self.tree.delete(self.iid)

    # ディレクトリを作成する
    def makeDirectory(self):
        rootPath = self.rootPath.get()
        # ルートのパスが存在しない場合は作成できないのでエラーダイアログを出して終了
        if rootPath =="":
            messagebox.showerror("作成エラー","ディレクトリを作成するルートディレクトリを指定してください。")
            return
        elif os.path.exists(rootPath) == False:
            messagebox.showerror("作成エラー","ルートディレクトリが不正です。")
            return
        mkpath = os.path.join(rootPath,self.tree.item(self.rootiid,"text"))
        # 上書きを防ぐため、すでにこのツールで作成されたフォルダがある場合はエラーダイアログを出して終了
        if os.path.exists(mkpath):
            messagebox.showerror("作成エラー","既にmakedirectoryToolsディレクトリが作成されています")
            return
        # ロジックのディレクトリ作成アクションを呼び出す
        self.logic.makeDirectoryAction(self.tree,self.rootiid)



if __name__ == '__main__':
    master = Tk()
    master.title("MakeDirectory Tools")
    MakeDirectoryTools(master)
    master.mainloop()