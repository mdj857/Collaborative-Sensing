import tkinter as tk
import random

class Desktop:

    def __init__(self, master):
        self.canvas = tk.Canvas(master, width=400, height=400)
        self.canvas.pack()

        self.ball = self.canvas.create_oval(0,0,20,20, fill='red', tags='id')
        self.text_id = self.canvas.create_text(300, 300, anchor='se')
        self.canvas.tag_bind('id', '<B1-Motion>', self.move)
        self.canvas.tag_bind('id', '<ButtonRelease-1>', self.stop_move)

    def move(self, event):
        selected = event.widget.find_withtag("current")[0]
        self.canvas.coords(selected, event.x-10, event.y-10, event.x+10,event.y+10)

    def stop_move(self, event):
        selected = event.widget.find_withtag("current")[0]
        x1, y1, x2, y2 = self.canvas.coords(selected)
        self.canvas.itemconfig(
            self.text_id,
            text="Current location:({} {})".format(x, y)
        )

root = tk.Tk()
d = Desktop(root)
root.mainloop()