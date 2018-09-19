import numpy as np
import cv2
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk

#Set up GUI
window = tk.Tk()  #Makes main window
window.wm_title("2 Cameras")
window.config(background="#FFFFFF")


#Capture video frames
lmain1 = tk.Label(master=window)
lmain2= tk.Label(master=window)
lmain1.pack(side=LEFT)
lmain2.pack(side=RIGHT)


cap1 = cv2.VideoCapture(0)
def show_frame1():
    showHelp = True
    showFullScreen = False
    helpText = "'Esc' to Quit, 'H' to Toggle Help, 'F' to Toggle Fullscreen"
    font = cv2.FONT_HERSHEY_PLAIN
    _, frame = cap1.read()
    if showHelp == True:
        cv2.putText(frame, helpText, (11, 20), font, 1.0, (32, 32, 32), 4, cv2.LINE_AA)
        cv2.putText(frame, helpText, (10, 20), font, 1.0, (240, 240, 240), 1, cv2.LINE_AA)
    # frame = cv2.flip(frame, 1)
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain1.imgtk = imgtk
    lmain1.configure(image=imgtk)
    lmain1.after(10, show_frame1)



cap2 = cv2.VideoCapture(1)
def show_frame2():
    _, frame = cap2.read()
    # frame = cv2.flip(frame, 1)
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain2.imgtk = imgtk
    lmain2.configure(image=imgtk)
    lmain2.after(10, show_frame2)


show_frame1()  #Display 2
show_frame2()
window.mainloop()