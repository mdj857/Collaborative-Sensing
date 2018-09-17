import tkinter as tk
from tkinter.ttk import Frame, Label, Style

import gui
# SET THESE BEFORE EXECUTION
canvas_w = 600
canvas_h = 660


class Moving_Ball(tk.Frame):
    global l3
    def __init__(self, parent, label3):
        tk.Frame.__init__(self, parent)
        l3 = label3
        # create a canvas
        self.canvas = tk.Canvas(width=canvas_w, height=canvas_h)

        
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Create>", self._create_grid)

        # this data is used to keep track of an 
        # item being dragged
        self._drag_data = {"x": 0, "y": 0, "item": None}


        # create a couple of movable objects
        self._create_grid((100, 100), "red", canvas_w, canvas_h)

        # add bindings for clicking, dragging and releasing over
        # any object with the "token" tag
        self.canvas.tag_bind("token", "<ButtonPress-1>", self.on_token_press)
        self.canvas.tag_bind("token", "<ButtonRelease-1>", self.on_token_release)
        self.canvas.tag_bind("token", "<B1-Motion>", self.on_token_motion)

    def _create_grid(self, coord, color, canvas_width, canvas_height):
        '''Create a token at the given coordinate in the given color'''


        (x,y) = coord
        circle = self.canvas.create_oval(x-25, y-25, x+25, y+25,
                                outline=color, fill=color, tags="token")
        self.canvas.create_line(0, 200, 399, 200, dash=(2,2))
        w = canvas_width
        h = canvas_height
        self.canvas.delete('grid_line') # Will only remove the grid_line

        # Creates all vertical lines at intevals of 100
        for i in range(0, w, 50):
            self.canvas.create_line(i, 0, i, h)

        #Creates all horizontal lines at intevals of 100
        for i in range(0, h, 50):
            self.canvas.create_line([(0, i), (w, i)], tag='grid_line')

        self.canvas.tag_raise(circle)
        
    def on_token_press(self, event):
        '''Begining drag of an object'''
        # record the item and its location
        self._drag_data["item"] = self.canvas.find_closest(event.x, event.y)[0]
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

    def on_token_release(self, event):
        '''End drag of an object'''
        # reset the drag information
        self._drag_data["item"] = None
        self._drag_data["x"] = 0
        self._drag_data["y"] = 0

    def on_token_motion(self, event):
        '''Handle dragging of an object'''
        # compute how much the mouse has moved
        delta_x = event.x - self._drag_data["x"]
        delta_y = event.y - self._drag_data["y"]
        # move the object the appropriate amount
        self.canvas.move(self._drag_data["item"], delta_x, delta_y)
        # record the new position
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y
        #label3 = Label(self, text=s)
        s = 'Coordinates: {} , {}'.format(self._drag_data["x"], self._drag_data["y"])
        print(s)
        #label3.place(x=25, y=630)