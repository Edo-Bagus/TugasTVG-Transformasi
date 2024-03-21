import tkinter as tk

class PaintApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Paint App")

        self.canvas = tk.Canvas(root, width=600, height=400, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.canvas.bind("<B1-Motion>", self.draw)

        self.color = "black"

        clear_button = tk.Button(root, text="Clear", command=self.clear_canvas)
        clear_button.pack(side=tk.BOTTOM)

        black_button = tk.Button(root, text="Black", command=lambda: self.set_color("black"))
        black_button.pack(side=tk.BOTTOM)

        white_button = tk.Button(root, text="White", command=lambda: self.set_color("white"))
        white_button.pack(side=tk.BOTTOM)

        

    def draw(self, event):
        x1, y1 = (event.x - 1), (event.y - 1)
        x2, y2 = (event.x + 1), (event.y + 1)
        self.canvas.create_oval(x1, y1, x2, y2, fill=self.color, outline="")

    def set_color(self, color):
        self.color = color

    def clear_canvas(self):
        self.canvas.delete("all")

if __name__ == "__main__":
    root = tk.Tk()
    app = PaintApp(root)
    root.mainloop()
