from tkinter import ttk
import tkinter as tk
import os
from idlelib.tooltip import Hovertip
import emoji

from modules.PopupModules import create_popup
from modules.TkModules import make_non_resizable, Button, clickable_link_labels
from modules.rootTkSplashModule import root
from modules.UpdaterModule import CheckUpdates

from __version__ import __version__, __ffmpeg__, __author__

def about():
    geo_width = 370
    geo_len= 250

    aboutmenu = create_popup(root, "About Us!", geo_width, geo_len, 1)
    make_non_resizable(aboutmenu)

    ffmpeg_text = f"- FFmpeg (https://ffmpeg.org/)\nVersion: {__ffmpeg__}"
    copyright_text = (
    "This program is distributed under the MIT License.\n"
    "Copyright (c) 2024-2025 John Nathaniel Calvara"
    )
    credits_text = (
        "\nCredits:\n"
        f"{ffmpeg_text}"
    )

    credits_label = tk.Label(aboutmenu, text=credits_text, justify=tk.LEFT)
    credits_label.pack(pady=10)

    copyright_label = tk.Label(aboutmenu, text=copyright_text, justify=tk.CENTER)
    copyright_label.pack(pady=5)

    clickable_link_labels(
        aboutmenu, "nate@n8ventures.dev", "mailto:nate@n8ventures.dev"
    )
    clickable_link_labels(  
        aboutmenu,
        "https://github.com/n8ventures",
        "https://github.com/n8ventures",
    )

    close_button = Button(aboutmenu, text="Close", command=aboutmenu.destroy)
    close_button.pack(pady=10)

def watermark_label(parent_window, debug = ''):
    menu_bar = tk.Menu(root)
    
    about_menu = tk.Menu(menu_bar, tearoff=0, name="apple")

    menu_bar.add_cascade(label="More", menu=about_menu)

    from modules.rootTkSplashModule import sv_ttk, darkdetect
    is_dark = True if darkdetect.theme() == "Dark" else False

    def toggle_theme():
        global is_dark
        if sv_ttk.get_theme() == "dark":
            sv_ttk.use_light_theme()
            is_dark = False
        elif sv_ttk.get_theme() == "light":
            sv_ttk.use_dark_theme()
            is_dark = True
            
        theme_label = emoji.emojize(f"{':crescent_moon:' if is_dark else ':sun_with_face:'} - Toggle Theme")
        about_menu.delete(0)
        about_menu.insert_command(0, label=theme_label, command=toggle_theme)

    about_menu.add_command(label=emoji.emojize(f"{':crescent_moon:' if is_dark else ':sun_with_face:'} - Toggle Theme"), command=toggle_theme)
    about_menu.add_separator()
    
    about_menu.add_command(label="About Me", command=about)
    about_menu.add_command(label="Check for Updates", command=CheckUpdates)
    
    parent_window.config(menu=menu_bar)
    
    frame = ttk.Frame(parent_window)
    frame.pack(side=tk.BOTTOM, fill=tk.X)

    separator_wm = ttk.Separator(frame, orient="horizontal")
    separator_wm.pack(side=tk.TOP, fill=tk.X)
    
    watermark_label = ttk.Label(frame, text=f" by {__author__}", style='WM.TLabel')
    watermark_label.pack(side=tk.LEFT, anchor=tk.SW)
    
    version_label = ttk.Label(frame, text=f"version: {__version__} {debug}", style='WM.TLabel')
    version_label.pack(side=tk.RIGHT, anchor=tk.SE)