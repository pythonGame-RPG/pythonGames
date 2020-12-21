#!/usr/bin/env python
import tkinter

root = tkinter.Tk()
c = tkinter.Canvas(root, width = 600, height = 200)
c.create_polygon(85, 20, 150, 80, 120, 150, 50, 150, 20, 80, fill = 'pink')
c.create_polygon(285, 20, 250, 150, 350, 80, 220, 80, 320, 150, fill = 'aquamarine')
c.create_polygon(485, 20, 450, 80, 550, 150, 440, 150, 520, 80, fill = 'orange', smooth = True)
c.pack()

root.mainloop()