from tkinter import *
import tkinter.ttk as ttk

class TreeViewSampleInsert(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.create_widgets()
        self.pack()

    def create_widgets(self):
        insertButton = ttk.Button(self,text="insert",command=self.insertData)
        insertButton.pack()
        self.tree = ttk.Treeview(self)
        self.tree.pack()

    def insertData(self):
        iid = self.tree.insert("",index="end",text="testData")
        
        print(iid)


if __name__ == '__main__':
    master = Tk()
    master.title("TreeViewSampleInsert")
    master.geometry("300x250")
    TreeViewSampleInsert(master)
    master.mainloop()