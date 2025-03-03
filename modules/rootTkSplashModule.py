from tkinterdnd2 import TkinterDnD
from PIL import Image, ImageTk, ImageSequence
from tkinter import ttk, PhotoImage
import tkinter as tk
import os
import sys
import sv_ttk
import darkdetect

from modules.TkModules import center_window, widget_color
from modules.platformModules import bundle_path, icon

root = TkinterDnD.Tk()
root.withdraw()

print('TCL Library:', root.tk.exprstring('$tcl_library'))
print('Tk Library:',root.tk.exprstring('$tk_library'))


root.iconphoto(True, PhotoImage(file=icon))

sv_ttk.set_theme(darkdetect.theme())
print('sv_ttk.get_theme(): ', sv_ttk.get_theme())

style = ttk.Style()
style.configure("Alt.TLabel", foreground=widget_color[1])
style.configure("WM.TLabel", foreground='gray')
style.configure(
    "AltBox.TLabel",
    background="white", 
    relief="solid",      
    borderwidth=1,       
)
style.configure("Alt.TCheckbutton", foreground=widget_color[1])

# print(style.theme_names())  # List all themes
# print(style.layout("TLabel"))  # Display layout for 'TLabel'

splash_screen = tk.Toplevel(root)
splash_screen.overrideredirect(1) 
splash_screen.attributes('-topmost', True)  # Keep the window on top
splash_screen.attributes("-transparent", "true")
splash_geo_x = 350
splash_geo_y = 550
center_window(splash_screen, splash_geo_x, splash_geo_y)

gif_path = 'splash.gif'
if bundle_path:
    gif_path = os.path.join(bundle_path, gif_path)
else:
    gif_path = './/splash//splash.gif'


gif_img = Image.open(gif_path)
gif_frames_rgba = [frame.convert("RGBA") for frame in ImageSequence.Iterator(gif_img)]

splash_label = tk.Label(splash_screen, bg='white')
splash_label.pack()

def animate(frame_num, loop):
    frame = gif_frames_rgba[frame_num]
    photo = ImageTk.PhotoImage(frame)
    splash_label.config(image=photo, bg='white')
    splash_label.image = photo
    
    if loop:
        frame_num = (frame_num + 1) % len(gif_frames_rgba)
        splash_screen.after(25, animate, frame_num, True)
    elif frame_num < len(gif_frames_rgba) - 1:
        frame_num += 1
        splash_screen.after(25, animate, frame_num, False)