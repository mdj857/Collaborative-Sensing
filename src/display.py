import Tkinter as tk
from time import sleep
from math import *
import numpy as np
import sys
from EKF_class import *
import threading
from planetDetector import *

rad = 200
class Desktop:

    def __init__(self, master):
        self.canvas = tk.Canvas(master, width=500, height=500)
        self.canvas.pack()
        self.ball_server = self.canvas.create_oval(0,0,20,20, fill='red', tags='id')
        self.ball_client = self.canvas.create_oval(0, 0, 20, 20, fill='blue', tags='id')
        self.ball_merge = self.canvas.create_oval(0, 0, 20, 20, fill='purple', tags='id')
        self.sun = self.canvas.create_oval(249-10, 249-10, 249 + 10, 249 + 10, fill='yellow', tags='id')
        self.rect = self.canvas.create_rectangle(5,5,500,500)


def convert(omega):
    #alpha = alpha * np.pi / 180
    alpha = -float(omega) % (2 * np.pi)
    x = 249 + rad * cos(alpha)
    y = 249 + - (rad * sin(alpha))
    return x, y

def update_label(root, server):
    def update():
        x, y = convert(server.rk.x[0])
        radius.set("Radius: " + str(rad))
        angle.set("Angle: " + str(float(server.rk.x[0]) % (2 * np.pi)))
        d.canvas.coords(d.ball_server, int(x)-10, int(y)-10, int(x)+10, int(y)+10)

        x, y = convert(server.omega_client)
        d.canvas.coords(d.ball_client, int(x) - 10, int(y) - 10, int(x) + 10, int(y) + 10)

        x, y = convert(server.omega)
        d.canvas.coords(d.ball_merge, int(x) - 10, int(y) - 10, int(x) + 10, int(y) + 10)

        root.after(100, update)
        
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
detector = PlanetDetector('../model/cascade.xml',2, False, False)
server = EKF_class(detector, "srv_transmit", "srv_recieve")
update_label(root, server)
button = tk.Button(root, text='Stop', width=25, command=root.destroy)
button.pack()
t = threading.Thread(target = ekf_thread)
t.start()
root.mainloop()
