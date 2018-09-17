import tkinter as tk
import gui
import move
import tegraCam
from tkinter.ttk import Label
import sys

if __name__ == '__main__':
    root = tk.Tk()
    root.geometry("1200x700")

    top_frame = tk.Frame(root)
    gui.BasicGui().pack(side=tk.LEFT, fill="both", expand=True)

    # bottom_frame = tk.Frame(root)
    # label3 = Label(root)
    # label3.place(x=650, y=670)
    #
    # move.Moving_Ball(bottom_frame, label3).pack(side=tk.RIGHT, fill="both", expand=True)
    cap = tegraCam.open_cam_usb(1, 1280, 720)
    if not cap.isOpened():
        sys.exit("Failed to open camera!")
    while True:
        label3 = Label(image = tegraCam.read_cam(cap))
        label3.place(x=650, y=670)

    cap.release()
    root.title(" Collaborative Sensing")

    root.mainloop()
