import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
import io
import numpy as np
from PIL import Image, ImageGrab

class PaintApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Paint App")

        self.canvas = tk.Canvas(root, width=600, height=600, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.canvas.bind("<B1-Motion>", self.draw)

        self.color = "black"

        self.brush_label = tk.Label(root, text="Brush Size: 0")
        self.brush_label.pack()
        self.brush = tk.Scale(root, from_=0, to=100, orient="horizontal", command=self.on_brush_changed, showvalue=False)
        self.brush.pack()

        draw_button = tk.Button(root, text="Draw", command=lambda: self.set_color("black"))
        draw_button.pack()

        erase_button = tk.Button(root, text="Erase", command=lambda: self.set_color("white"))
        erase_button.pack()

        select_button = tk.Button(root, text="Select", command=self.select_area)
        select_button.pack()

        clear_button = tk.Button(root, text="Clear", command=self.clear_canvas)
        clear_button.pack()

        self.transform_button = tk.Button(root, text="Transform", command=self.transform_canvas, state='disabled')
        self.transform_button.pack()

        

        

        

        self.root.resizable(False, False)

    def transform_canvas(self):
        new_window = tk.Toplevel(self.root)
        new_window.title("Print Preview")
        new_window.resizable(False, False)
        new_window.grab_set()
        self.translation_x_label = tk.Label(new_window, text="Translate X: 0")
        self.translation_x_label.pack()
        self.translation_x = tk.Scale(new_window, from_=-100, to=100, orient="horizontal", command=self.on_translation_x_changed, showvalue=False)
        self.translation_x.pack()
        self.translation_y_label = tk.Label(new_window, text="Translate Y: 0")
        self.translation_y_label.pack()
        self.translation_y = tk.Scale(new_window, from_=-100, to=100, orient="horizontal", command=self.on_translation_y_changed, showvalue=False)
        self.translation_y.pack()
        self.rotation_label = tk.Label(new_window, text="Rotation Degree: 0")
        self.rotation_label.pack()
        self.rotation = tk.Scale(new_window, from_=0, to=360, orient="horizontal", command=self.on_rotation_changed, showvalue=False, state='disabled')
        self.rotation.pack()
        self.scale_x_label = tk.Label(new_window, text="Scale X Degree: 0")
        self.scale_x_label.pack()
        self.scale_x = tk.Scale(new_window, from_=-100, to=100, orient="horizontal", command=self.on_scale_x_changed, showvalue=False, state='disabled')
        self.scale_x.pack()
        self.scale_y_label = tk.Label(new_window, text="Scale Y Degree: 0")
        self.scale_y_label.pack()
        self.scale_y = tk.Scale(new_window, from_=-100, to=100, orient="horizontal", command=self.on_scale_y_changed, showvalue=False, state='disabled')
        self.scale_y.pack()
        self.done = tk.Button(new_window, text="Done", command=transform)
        self.done.pack()

    def on_brush_changed(self, value):
        self.brush_label.config(text=f"Brush Size: {value}")

    def on_translation_x_changed(self, value):
        self.translation_x_label.config(text=f"Translation X: {value}")
        self.translate_x = self.translation_x.get()

    def on_translation_y_changed(self, value):
        self.translation_y_label.config(text=f"Translation y: {value}")
        self.translate_y = self.translation_y.get()

    def on_rotation_changed(self, value):
        self.rotation_label.config(text=f"Rotation: {value}")

    def on_scale_x_changed(self, value):
        self.scale_x_label.config(text=f"Scale X: {value}")

    def on_scale_y_changed(self, value):
        self.scale_y_label.config(text=f"Scale Y: {value}")

    def transform(self):
           

    def draw(self, event):
        size = self.brush.get()
        x1, y1 = (event.x - size), (event.y - size)
        x2, y2 = (event.x + size), (event.y + size)
        self.canvas.create_oval(x1, y1, x2, y2, fill=self.color, outline="")

    def set_color(self, color):
        self.color = color

    def clear_canvas(self):
        self.canvas.delete("all")

    def select_area(self): 
        self.canvas.bind("<ButtonPress-1>", self.start_selection)
        self.canvas.bind("<B1-Motion>", self.track_selection)
        self.canvas.bind("<ButtonRelease-1>", self.end_selection)
 
    def start_selection(self, event):
        self.start_x = event.x
        self.start_y = event.y

    def track_selection(self, event):
        self.end_x = event.x
        self.end_y = event.y
        self.canvas.delete("selection_rectangle")
        self.canvas.create_rectangle(self.start_x - 1, self.start_y -1, self.end_x + 1, self.end_y + 1, outline="black", tags="selection_rectangle")

    


    def end_selection(self, event):
        self.canvas.unbind("<ButtonPress-1>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas.delete("selection_rectangle")

        self.canvas.bind("<B1-Motion>", self.draw)
        
        x = min(self.start_x, self.end_x)
        y = min(self.start_y, self.end_y)
        x1 = max(self.start_x, self.end_x)
        y1 = max(self.start_y, self.end_y)

        self.transform_button.config(state='active')

        # Grab the selected area and convert it into an image
        self.selected_img = ImageGrab.grab(bbox=(self.root.winfo_rootx() + x, 
                                   self.root.winfo_rooty() + y, 
                                   self.root.winfo_rootx() + x1, 
                                   self.root.winfo_rooty() + y1))
        self.selected_img.save('canvas_image.png')

    def print_canvas(self):
        self.print_img = ImageTk.PhotoImage(Image.open('canvas_image.png'))
        self.canvas.create_image(10, 10, anchor=tk.NW, image=self.print_img)

    
if __name__ == "__main__":
    root = tk.Tk()
    app = PaintApp(root)
    root.mainloop()
