from PIL import Image, ImageTk
from tkinter import Tk, BOTH
import tkinter as tk
from tkinter.ttk import Frame, Label, Style

class BasicGui(Frame):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
      
        self.pack(fill=BOTH, expand=1)
        
        Style().configure("TFrame", background="#333")
        size = 600, 350
        car = Image.open("car.jpg")
        car = car.resize(size, Image.ANTIALIAS)
        carTk = ImageTk.PhotoImage(car)
        label1 = Label(self, image=carTk)
        label1.image = carTk
        label1.place(x=0, y=0)

        view = Image.open("selfdriving.jpg")
        view = view.resize(size, Image.ANTIALIAS)
        viewTk = ImageTk.PhotoImage(view)
        label2 = Label(self, image=viewTk)
        label2.image = viewTk
        label2.place(x=0, y=350)
