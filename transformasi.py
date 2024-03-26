import tkinter as tk
from tkinter import ttk
from tkinter import colorchooser
import math
import numpy as np

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

        ttk.Button(self.toolbar, text="Draw Polygon", command=self.draw_line).pack(fill=tk.X)
        
        ttk.Button(self.toolbar, text="Select", command=self.select).pack(fill=tk.X)
        
        translate_frame = ttk.Frame(self.toolbar)
        translate_frame.pack(fill=tk.X)
        ttk.Button(translate_frame, text="Translate", command=self.translate).pack(side=tk.LEFT)
        translation_x_label = ttk.Label(translate_frame, text="X")
        translation_x_label.pack(side=tk.LEFT)
        self.translation_x_entry = ttk.Entry(translate_frame)
        self.translation_x_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        translation_y_label = ttk.Label(translate_frame, text="Y")
        translation_y_label.pack(side=tk.LEFT)
        self.translation_y_entry = ttk.Entry(translate_frame)
        self.translation_y_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        rotate_frame = ttk.Frame(self.toolbar)
        rotate_frame.pack(fill=tk.X)
        ttk.Button(rotate_frame, text="Rotate", command=self.rotate).pack(side=tk.LEFT)
        self.rotation_entry = ttk.Entry(rotate_frame)
        self.rotation_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        scale_frame = ttk.Frame(self.toolbar)
        scale_frame.pack(fill=tk.X)
        ttk.Button(scale_frame, text="Scale", command=self.scale).pack(side=tk.LEFT)
        scale_x_label = ttk.Label(scale_frame, text="X")
        scale_x_label.pack(side=tk.LEFT)
        self.scale_entry_x = ttk.Entry(scale_frame)
        self.scale_entry_x.pack(side=tk.LEFT, fill=tk.X, expand=True)
        scale_y_label = ttk.Label(scale_frame, text="Y")
        scale_y_label.pack(side=tk.LEFT)
        self.scale_entry_y = ttk.Entry(scale_frame)
        self.scale_entry_y.pack(side=tk.LEFT, fill=tk.X, expand=True)

        combined_framed = ttk.Frame(self.toolbar)
        combined_framed.pack(fill=tk.X)
        ttk.Button(combined_framed, text="Combined Transformation", command=self.combined).pack(side=tk.LEFT)

        # Event bindings
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

    def draw_line(self):
        self.canvas.unbind("<Button-1>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas.bind("<Button-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.on_draw)

    def start_draw(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.points = [event.x, event.y]
        self.current_shape = self.canvas.create_polygon(self.points, fill='', outline='black')

    def on_draw(self, event):
        self.points.extend([event.x, event.y])
        self.canvas.coords(self.current_shape, *self.points)

    def select(self):
        self.canvas.unbind("<Button-1>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas.bind("<Button-1>", self.on_select)

    def on_select(self, event):
        if self.selected_shape != None:
            self.canvas.itemconfig(self.selected_shape, outline="black")
            self.selected_shape = self.canvas.find_closest(event.x, event.y)[0]
            self.points = []
            self.points = self.canvas.coords(self.selected_shape)
            self.canvas.itemconfig(self.selected_shape, outline="red")
        else:
            self.selected_shape = self.canvas.find_closest(event.x, event.y)[0]
            self.canvas.itemconfig(self.selected_shape, outline="red")

    def translate(self):
        if self.selected_shape:
            try:
                result = []
                for i in range(0, len(self.points), 2):
                    x = self.points[i]
                    y = self.points[i+1]
                    new_x = x + float(self.translation_x_entry.get())
                    new_y = y + float(self.translation_y_entry.get())
                    result_point = [int(new_x), int(new_y)]
                    result = np.append(result, result_point)
                    result_list = result.tolist()

                    self.canvas.coords(self.selected_shape, result_list)
                    
                    self.points[i] = int(new_x)
                    self.points[i+1] = int(new_y)
                    
            except ValueError:
                pass  # Handle invalid input

    def rotate(self):
        if self.selected_shape: # Your array of points
            try:
                result = np.array([])
                x0, y0, x1, y1 = self.canvas.bbox(self.selected_shape)
                cx = (x0 + x1) / 2
                cy = (y0 + y1) / 2
                for i in range(0, len(self.points), 2):
                    x = self.points[i]
                    y = self.points[i+1]
                    angle = math.radians(float(self.rotation_entry.get()))
                    new_x = cx + math.cos(angle) * (x - cx) - math.sin(angle) * (y - cy)
                    new_y = cy + math.sin(angle) * (x - cx) + math.cos(angle) * (y - cy)
                    result_point = [int(new_x), int(new_y)]
                    result = np.append(result, result_point)
                    result_list = result.tolist()

                    self.canvas.coords(self.selected_shape, result_list)

                    self.points[i] = int(new_x)
                    self.points[i+1] = int(new_y)
    # Perform operations on each point her 
            except ValueError:
                pass  # Handle invalid input


    def scale(self):
        if self.selected_shape:
            try:
                result = np.array([])
                x0, y0, x1, y1 = self.canvas.bbox(self.selected_shape)
                cx = (x0 + x1) / 2
                cy = (y0 + y1) / 2
                for i in range(0, len(self.points), 2):
                    x = self.points[i]
                    y = self.points[i+1]
                    scale_factor_x = float(self.scale_entry_x.get())
                    scale_factor_y = float(self.scale_entry_y.get())
                    new_x = cx + scale_factor_x * (x - cx)
                    new_y = cy + scale_factor_y * (y - cy)
                    result_point = [int(new_x), int(new_y)]
                    result = np.append(result, result_point)
                    result_list = result.tolist()

                    self.canvas.coords(self.selected_shape, result_list)

                    self.points[i] = int(new_x)
                    self.points[i+1] = int(new_y)

            except ValueError:
                pass  # Handle invalid input

    def combined(self):
        if self.selected_shape:
            try:
                self.translate()
                self.rotate()
                self.scale()

            except ValueError:
                pass 

    def on_click(self, event):
        pass

    def on_drag(self, event):
        pass

    def on_release(self, event):
        pass

root = tk.Tk()
app = PaintApp(root)
root.mainloop()
