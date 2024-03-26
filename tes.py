import tkinter as tk
from PIL import Image, ImageTk

root = tk.Tk()
root.geometry("400x300")

canvas = tk.Canvas(root, width=400, height=300)
canvas.pack()

# Create a new black image
black_image = Image.new("RGB", (100, 100), color="black")

# Convert the PIL image to a Tkinter-compatible image object
tk_image = ImageTk.PhotoImage(black_image)

# Add the image to the canvas
canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)

root.mainloop()
