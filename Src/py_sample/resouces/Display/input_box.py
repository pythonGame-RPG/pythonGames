import tkinter as tk

class FontSizer:
    def __init__(self, name='TkDefaultFont', size=12):
        self.name = name
        self.size = size

    def scale(self, sf):
        self.size *= sf

    @property
    def font(self):
        return self.name, int(self.size)

def zoomer(event):
    global font_sizer
    sf = 1.1 if event.delta > 0 else 0.9

    # 元に戻せるように逆数を保持
    global ini_size
    ini_size = ini_size / sf

    canvas.scale("all", 0, 0, sf, sf)
    font_sizer.scale(sf)
    canvas.itemconfigure('bangou', font=font_sizer.font)
    canvas.configure(scrollregion=canvas.bbox("all"))

def shoki_size():
    global font_sizer
    global ini_size
    canvas.scale("all", 0, 0, ini_size, ini_size)
    font_sizer.scale(ini_size)
    canvas.itemconfigure('bangou', font=font_sizer.font)
    canvas.configure(scrollregion=(0,0,500,500)) # 初期スクロール位置。適当に戻す

    ini_size = 1


window = tk.Tk()
window.title('サンプル')

frame1 = tk.Frame(window,bd=1,relief="ridge")
frame1.grid(row=1, column=0,sticky='news')

btn = tk.Button(frame1, text="元のサイズに戻す",command=shoki_size)
btn.grid(row=0, column=0,sticky="NEWS")

frame2 = tk.Frame(window,bd=1,relief="ridge")
frame2.grid(row=2, column=0,sticky='news')

canvas = tk.Canvas(frame2, height=500, width=500, bg='white',bd=1,relief="ridge")
canvas.grid(row=0, column=0,sticky='news')


canvas.create_oval(250-3, 250-3, 250+3, 250+3,fill='red',tag="en")
canvas.create_text(250, 250-8,text="1",tag="bangou",fill='red')

canvas.create_oval(250-3, 300-3, 250+3, 300+3,fill='red',tag="en")
canvas.create_text(250, 300-8,text="2",tag="bangou",fill='red')

canvas.create_oval(400-3, 400-3, 400+3, 400+3,fill='red',tag="en")
canvas.create_text(400, 400-8,text="2",tag="bangou",fill='red')


font_sizer = FontSizer(size=12)
canvas.itemconfigure('bangou', font=font_sizer.font)
canvas.bind("<MouseWheel>", zoomer)

ini_size = 1 # 初期倍率


frame2.grid_columnconfigure(0,weight=1)
frame2.grid_rowconfigure(0,weight=1)
window.grid_columnconfigure(0,weight=1)
window.grid_rowconfigure(2,weight=1)

window.mainloop()