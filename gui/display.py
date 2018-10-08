import tkinter as tk
from time import sleep

index = 0
value = []


def update_label(root):
    def update():
        global index
        r, a = value[index]
        index = index + 1
        radius.set("Radius: " + str(r))
        angle.set("Angle: " + str(a))
        root.after(3000, update)

    update()


with open("test.txt") as f:
    for line in f:
        value.append(line.split())

root = tk.Tk()
radius = tk.StringVar()
angle = tk.StringVar()
root.title("Output Display")
r = tk.Label(root, fg="green", textvariable = radius)
r.pack()
a = tk.Label(root, fg="green", textvariable = angle)
a.pack()
update_label(root)
button = tk.Button(root, text='Stop', width=25, command=root.destroy)
button.pack()

root.mainloop()