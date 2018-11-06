import Tkinter as tk
from time import sleep
from math import *
import numpy as np
import sys
from EKF_class import *
import threading

rad = 200

class Desktop:

    def __init__(self, master):
        self.canvas = tk.Canvas(master, width=500, height=500)
        self.canvas.pack()
        self.ball = self.canvas.create_oval(0,0,20,20, fill='red', tags='id')
        self.sun = self.canvas.create_oval(249-10, 249-10, 249 + 10, 249 + 10, fill='yellow', tags='id')
        self.rect = self.canvas.create_rectangle(5,5,500,500)


def convert(alpha):
    #alpha = alpha * np.pi / 180
    x = 249 + rad * cos(alpha)
    y = 249 + - (rad * sin(alpha))
    return x, y

def update_label(root, server):
    def update():
        alpha = int(server.rk.x[0]) % (2 * np.pi)
        r, a = convert(alpha)
        radius.set("Radius: " + str(rad))
        angle.set("Angle: " + str(alpha))
        d.canvas.coords(d.ball, int(r)-10, int(a)-10, int(r)+10, int(a)+10)
        root.after(1000, update)
        
    update()

def ekf_thread():
	server.run_EKF()

root = tk.Tk()
radius = tk.StringVar()
angle = tk.StringVar()
d = Desktop(root)
root.title("Output Display")
r = tk.Label(root, fg="green", textvariable = radius)
r.pack()
a = tk.Label(root, fg="green", textvariable = angle)
a.pack()
server = EKF_class(0, "srv_transmit", "srv_recieve")
update_label(root, server)
button = tk.Button(root, text='Stop', width=25, command=root.destroy)
button.pack()
t = threading.Thread(target = ekf_thread)
t.start()
root.mainloop()
