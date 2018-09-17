import tkinter as tk
import gui
import move
from tkinter.ttk import Label

if __name__ == '__main__':
    root = tk.Tk()
    root.geometry("1200x700")

    top_frame = tk.Frame(root)
    gui.BasicGui().pack(side=tk.LEFT, fill="both", expand=True)

    bottom_frame = tk.Frame(root)
    label3 = Label(root)
    label3.place(x=650, y=670)

    move.Moving_Ball(bottom_frame, label3).pack(side=tk.RIGHT, fill="both", expand=True)

    root.title(" Collaborative Sensing")

    root.mainloop()