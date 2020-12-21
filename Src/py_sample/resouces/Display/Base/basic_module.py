from tkinter import messagebox

class MyStack:

    def __init__(self):
        self.stack = []
    def push(self, item):
        self.stack.append(item)
    def pop(self):
        result = self.stack[-1]  # 末尾の要素を変数に取り出す
        del self.stack[-1]  # リストから要素を削除する
        return result  # リスト末尾から取り出したデータを返送する

# ポップアップ表示
# param：出力文字列コード、
class Popup:

    def __init__(self):
        pass

    def OKCancelPopup(self, indata):
        # メッセージボックス（OK・キャンセル） 
        return messagebox.askokcancel('登録', indata)
        pass

    def YesNoCancelPopup(self, indata):
        # メッセージボックス（YES・NO・キャンセル） 
        return messagebox.askyesnocancel('登録', indata)

    def ShowInfo(self, indata):
        # メッセージボックス（情報） 
        return messagebox.showinfo('確認メッセージ', indata)