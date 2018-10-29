import tkinter as tk
from time import sleep

import sys

from planetDetector import *

index = 0
value = []

class Desktop:

    def __init__(self, master):
        self.canvas = tk.Canvas(master, width=500, height=500)
        self.canvas.pack()
        self.ball = self.canvas.create_oval(0,0,20,20, fill='red', tags='id')



def update_label(root):
    def update():
        global index
        r, a = value[index]
        index = (index + 1) % size
        print(index)
        radius.set("Radius: " + r)
        angle.set("Angle: " + a)
        d.canvas.coords(d.ball, int(r)-10, int(a)-10, int(r)+10, int(a)+10)
        root.after(1000, update)
        # line should be: R Theta
        for line in sys.stdin:
            value.append(line.split())
    update()


size = value.__len__()
root = tk.Tk()
radius = tk.StringVar()
angle = tk.StringVar()
d = Desktop(root)
root.title("Output Display")
r = tk.Label(root, fg="green", textvariable = radius)
r.pack()
a = tk.Label(root, fg="green", textvariable = angle)
a.pack()
update_label(root)
button = tk.Button(root, text='Stop', width=25, command=root.destroy)
button.pack()
detector = PlanetDetector('../old_models/model_4/cascade.xml', False, False)
root.mainloop()