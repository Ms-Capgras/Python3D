import tkinter as tk
from PIL import Image, ImageTk
from numpy import array, uint8
from typing import Union

root: Union[tk.Tk, tk.Toplevel, None] = None
MONITOR_WIDTH: int = 1920
MONITOR_HEIGHT: int = 1200

class Display:
    to_rgb = lambda hex_colour: (int(hex_colour[1:3], 16), int(hex_colour[3:5], 16), int(hex_colour[5::], 16))
    to_hex = lambda rgb_colour: ('#%02x%02x%02x' % tuple(rgb_colour))

    def __init__(self, title=" Python3D", width=MONITOR_WIDTH, height=MONITOR_HEIGHT, pixel_offset_x=0, pixel_offset_y=0, bgcolour="#ffffff", maximised=True) -> None:
        global root

        self.width = lambda: width
        self.height = lambda: height
        self._rgb_bg = Display.to_rgb(bgcolour)
        self.image = None
        
        if root is None:
            root = tk.Tk(className=title)
            self.window = root
        else:
            self.window = tk.Toplevel(root)
            self.window.title(title)
        self.window.configure(bg=bgcolour)
        self.window.geometry(f"{width}x{height}+{pixel_offset_x}+{pixel_offset_y}")
        if maximised: self.window.state("zoomed")
        
        self.bitmap = array([[self._rgb_bg for col in range(width)] for row in range(height)], dtype=uint8)
        self.canvas = tk.Canvas(self.window, width=width, height=height, bg=bgcolour)
        self.canvas.pack()
        self.update()
        self.canvas.create_image(0, 0, image=self.image, anchor=tk.NW)

    def set_pixel(self, x:int, y:int, colour:str) -> None:
        self.bitmap[y][x] = Display.to_rgb(colour)
    
    def get_pixel(self, x:int, y:int) -> str:
        return Display.to_hex(self.bitmap[y][x])

    def update(self) -> None:
        self.image = ImageTk.PhotoImage(Image.fromarray(self.bitmap, mode="RGB"))
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, image=self.image, anchor=tk.NW)
        self.window.update()

def mainloop() -> None:
    if root is None: raise RuntimeError("No displays have been created to begin the main loops of.")
    else: root.mainloop()