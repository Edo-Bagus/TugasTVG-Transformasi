import tkinter as tk
from tkinter import ttk
from tkinter import colorchooser
import math

class PaintApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Paint App")

        self.canvas = tk.Canvas(self.root, width=600, height=400, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.shapes = []  # To store drawn shapes
        self.selected_shape = None  # To store the currently selected shape

        # Toolbar
        self.toolbar = ttk.Frame(self.root)
        self.toolbar.pack(side=tk.LEFT, fill=tk.Y)

        ttk.Button(self.toolbar, text="Draw Line", command=self.draw_line).pack(fill=tk.X)
        ttk.Button(self.toolbar, text="Draw Rectangle", command=self.draw_rectangle).pack(fill=tk.X)
        
        ttk.Button(self.toolbar, text="Select", command=self.select).pack(fill=tk.X)
        
        translate_frame = ttk.Frame(self.toolbar)
        translate_frame.pack(fill=tk.X)
        ttk.Button(translate_frame, text="Translate", command=self.translate).pack(side=tk.LEFT)
        self.translation_entry = ttk.Entry(translate_frame)
        self.translation_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        rotate_frame = ttk.Frame(self.toolbar)
        rotate_frame.pack(fill=tk.X)
        ttk.Button(rotate_frame, text="Rotate", command=self.rotate).pack(side=tk.LEFT)
        self.rotation_entry = ttk.Entry(rotate_frame)
        self.rotation_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        scale_frame = ttk.Frame(self.toolbar)
        scale_frame.pack(fill=tk.X)
        ttk.Button(scale_frame, text="Scale", command=self.scale).pack(side=tk.LEFT)
        self.scale_entry = ttk.Entry(scale_frame)
        self.scale_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Event bindings
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

    # def draw(self, shape):
    #     self.canvas.unbind("<Button-1>")
    #     self.canvas.unbind("<B1-Motion>")
    #     self.canvas.unbind("<ButtonRelease-1>")
    #     self.canvas.bind("<B1-Motion>", self.on_draw)
    #     if shape == "line":
    #         # print(shape)
    #         self.canvas.bind("<Button-1>", self.start_draw_line)
    #     elif shape == "rectangle":
    #         # print("rect")
    #         self.canvas.bind("<Button-1>", self.start_draw_rectangle)

    def draw_line(self):
        self.canvas.unbind("<Button-1>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas.bind("<Button-1>", self.start_draw_line)
        self.canvas.bind("<B1-Motion>", self.on_draw)

    def draw_rectangle(self):
        self.canvas.unbind("<Button-1>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas.bind("<Button-1>", self.start_draw_rectangle)
        self.canvas.bind("<B1-Motion>", self.on_draw)

    def start_draw_line(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.current_shape = self.canvas.create_line(event.x, event.y, event.x, event.y)

    def start_draw_rectangle(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.current_shape = self.canvas.create_rectangle(event.x, event.y, event.x, event.y)

    def on_draw(self, event):
        # if self.current_shape:
        #     coords = self.canvas.coords(self.current_shape)
        #     if len(coords) == 4:  # Line or rectangle
            self.canvas.coords(self.current_shape, self.start_x, self.start_y, event.x, event.y)

    def select(self):
        print('tes')
        self.canvas.unbind("<Button-1>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas.bind("<Button-1>", self.on_select)

    def on_select(self, event):
        self.selected_shape = self.canvas.find_closest(event.x, event.y)[0]
        self.canvas.itemconfig(self.selected_shape, fill="red")

    def translate(self):
        if self.selected_shape:
            try:
                dx = int(self.translation_entry.get())
                dy = int(self.translation_entry.get())
                self.canvas.move(self.selected_shape, dx, dy)
            except ValueError:
                pass  # Handle invalid input

    def rotate_rectangle(self, x0, y0, x1, y1, angle):
        # Calculate center of the rectangle
        cx = (x0 + x1) / 2
        cy = (y0 + y1) / 2
        
        # Convert angle to radians
        radians = math.radians(angle)

        # Rotate each corner of the rectangle around the center
        x0_new = cx + math.cos(radians) * (x0 - cx) - math.sin(radians) * (y0 - cy)
        y0_new = cy + math.sin(radians) * (x0 - cx) + math.cos(radians) * (y0 - cy)
        x1_new = cx + math.cos(radians) * (x1 - cx) - math.sin(radians) * (y0 - cy)
        y1_new = cy + math.sin(radians) * (x1 - cx) + math.cos(radians) * (y0 - cy)
        x2_new = cx + math.cos(radians) * (x1 - cx) - math.sin(radians) * (y1 - cy)
        y2_new = cy + math.sin(radians) * (x1 - cx) + math.cos(radians) * (y1 - cy)
        x3_new = cx + math.cos(radians) * (x0 - cx) - math.sin(radians) * (y1 - cy)
        y3_new = cy + math.sin(radians) * (x0 - cx) + math.cos(radians) * (y1 - cy)
        
        return x0_new, y0_new, x1_new, y1_new, x2_new, y2_new, x3_new, y3_new

    def rotate(self):
        if self.selected_shape:
            try:
                angle = int(self.rotation_entry.get())  # Rotate by given angle
                x0, y0, x1, y1 = self.canvas.coords(self.selected_shape)
                x0, y0, x1, y1, x2, y2, x3, y3 = self.rotate_rectangle(x0, y0, x1, y1, angle)
                self.canvas.coords(self.selected_shape, x0, y0, x1, y1, x2, y2, x3, y3)
            except ValueError:
                pass  # Handle invalid input


    def scale(self):
        if self.selected_shape:
            try:
                scale_factor = float(self.scale_entry.get())  # Scale by given factor
                x0, y0, x1, y1 = self.canvas.coords(self.selected_shape)
                cx = (x0 + x1) / 2
                cy = (y0 + y1) / 2
                new_x0 = cx + scale_factor * (x0 - cx)
                new_y0 = cy + scale_factor * (y0 - cy)
                new_x1 = cx + scale_factor * (x1 - cx)
                new_y1 = cy + scale_factor * (y1 - cy)
                self.canvas.coords(self.selected_shape, new_x0, new_y0, new_x1, new_y1)
            except ValueError:
                pass  # Handle invalid input

    def on_click(self, event):
        pass

    def on_drag(self, event):
        pass

    def on_release(self, event):
        pass

root = tk.Tk()
app = PaintApp(root)
root.mainloop()
