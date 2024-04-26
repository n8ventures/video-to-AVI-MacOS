from __version__ import __version__, __ffmpeg__
import tkinter as tk
from tkinter import filedialog, ttk, PhotoImage
from tkinterdnd2 import TkinterDnD, DND_FILES
from PIL import Image, ImageTk, ImageSequence
import os
import sys
import platform
import shutil
import subprocess
import atexit
import threading
import pywinctl as pwc 
from tkmacosx import Button

def is_running_from_bundle():
    # Check if the application is running from a bundled executable
    if getattr(sys, 'frozen', False):
        # For py2app bundles, use sys.executable to get the bundle path
        if hasattr(sys, '_MEIPASS'):
            return sys._MEIPASS
        else:
            current_dir = os.path.dirname(sys.executable)
            parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
            return os.path.join(parent_dir, "Resources")

    return False

ffmpeg = 'ffmpeg'

bundle_path = is_running_from_bundle()
if bundle_path:
    ffmpeg = os.path.join(bundle_path, ffmpeg)
else:
    MacOSbin = './bin/'
    ffmpeg = os.path.join(MacOSbin, ffmpeg)
    

# Create tkinter popup
def create_popup(root, title, width, height, switch):
    popup = tk.Toplevel(root)
    popup.title(title)
    popup.geometry(f"{width}x{height}")
    popup.iconphoto(True, icon)
    # popup.overrideredirect(True)
    popup.attributes('-type', 'utility')
    center_window(popup, width, height)
    
    if switch == 1:
        popup.bind("<FocusOut>", lambda e: popup.destroy())

    popup.grab_set()
    
    return popup

# popups
def about():
    geo_width = 370
    geo_len= 410

    aboutmenu = create_popup(root, "About Us!", geo_width, geo_len, 1)
    make_non_resizable(aboutmenu)

    ffmpeg_text = f"- FFmpeg (https://ffmpeg.org/)\nVersion: {__ffmpeg__}"
    copyright_text = (
    "This program is distributed under the MIT License.\n"
    "Copyright (c) 2024 John Nathaniel Calvara"
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

    close_button = ttk.Button(aboutmenu, text="Close", command=aboutmenu.destroy)
    close_button.pack(pady=10)

def notavideo():
    notavideo = create_popup(root, "Not a video!", 400, 100, 1)
    make_non_resizable(notavideo)

    errortext = (
        "Not a video! Please select a video file!"
    )

    about_label = tk.Label(notavideo, text=errortext, justify=tk.LEFT)
    about_label.pack(pady=10)

    close_button = ttk.Button(notavideo, text="Close", command=notavideo.destroy)
    close_button.pack(pady=10)

def clickable_link_labels(aboutmenu, text, link):
    mailto_label = tk.Label(aboutmenu, text=text, fg="blue", cursor="hand2")
    mailto_label.pack()
    mailto_label.bind("<Button-1>", lambda e: open_link(link))

def open_link(url):
    import webbrowser
    webbrowser.open(url)
    
# Tkinter stuff
def watermark_label(parent_window):
    
    menu_bar = tk.Menu(root)
    
    about_menu = tk.Menu (menu_bar, tearoff=0)
    about_menu.add_command(label="About Us", command=about)
    # about_menu.add_command(label="Check for Updates", command=CheckUpdates)
    menu_bar.add_cascade(label="Help", menu=about_menu)
    
    parent_window.config(menu=menu_bar)
    
    frame = tk.Frame(parent_window)
    frame.pack(side=tk.BOTTOM, fill=tk.X)

    separator_wm = ttk.Separator(frame, orient="horizontal")
    separator_wm.pack(side=tk.TOP, fill=tk.X)
    
    watermark_label = tk.Label(frame, text="by N8VENTURES", fg="gray")
    watermark_label.pack(side=tk.LEFT, anchor=tk.SW)
    
    version_label = tk.Label(frame, text=f"version: {__version__}", fg="gray")
    version_label.pack(side=tk.RIGHT, anchor=tk.SE)
    
    root.config(menu=menu_bar)

def make_non_resizable(window):
    window.resizable(False, False)

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window_width = width  
    window_height = height
    x_position = (screen_width - window_width) // 2
    y_position = (screen_height - window_height) // 2  
    window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position-35}")

# Loading functions
loading_screen = None

def loading():
    if loading_event.is_set():
        global loading_screen
        loading_screen = create_popup(root, "Converting...", 350, 120, 0)
        make_non_resizable(loading_screen)
        
        load_text_label = tk.Label(loading_screen, text='Converting...\nPlease wait.')
        load_text_label.pack(pady=20)

        progress_bar = ttk.Progressbar(loading_screen, mode='indeterminate')
        progress_bar.pack(fill=tk.X, padx=10, pady=0)
        progress_bar.start()
        root.update_idletasks()
        print('starting loading popup')
    else:
        loading_screen.destroy()
        print('loading popup dead')
        
loading_event = threading.Event()

def loading_thread():
    loading_event.set()
    print('starting thread')
    loading()
    
def loading_thread_switch(switch):
    if switch == True:
        threading.Thread(target=loading_thread, daemon=True).start()
    if switch == False:
        print('killing loading popup')
        loading_event.clear()
        loading()
        
# sys functions
def is_video_file(file_path):
    _, file_extension = os.path.splitext(file_path)
    return file_extension.lower() in video_extensions

def is_folder_open(path):
    folder_name = os.path.basename(path)
    if platform.system() == 'Darwin':  # macOS
        # Use AppleScript to check if Finder window is open with the specified folder
        script = f'''
            tell application "System Events"
                set openWindows to name of every window of application process "Finder"
            end tell
            if "{folder_name}" is in openWindows then
                return true
            else
                return false
            end if
        ''' 
        open_windows = subprocess.check_output(['osascript', '-e', script]).decode('utf-8').strip()
        return open_windows == 'true'
    else:
        raise OSError("Unsupported operating system")

video_extensions = [
'.3g2', '.3gp', '.amv', '.asf', '.avi', '.drc', '.f4v', '.flv', '.gif', '.gifv', '.m2ts', 
'.m2v', '.m4p', '.m4v', '.mkv', '.mng', '.mov', '.mp2', '.mp4', '.mpe', '.mpeg', '.mpg', 
'.mpv', '.mts', '.mxf', '.nsv', '.ogg', '.ogv', '.qt', '.rm', '.rmvb', '.roq', '.svi', 
'.ts', '.vob', '.webm', '.wmv', '.yuv'
]

def openOutputFolder(path, path2):
    print('checking if window is open...')
    if not is_folder_open(path):
        subprocess.run(['open', '-R', path2])
    else:
        print('window found!')
        subprocess.run(['open', '-R', path2])

def save_video(file_path):
    print(f"File: {file_path}")
    
    if file_path and is_video_file(file_path):
        output_file = filedialog.asksaveasfile(
        defaultextension=".avi",
        initialfile=f"{os.path.splitext(os.path.basename(file_path))[0]}.avi",
        filetypes=[("AVI video", "*.avi")],
        )
        if output_file:
            output_file.close()
            output_folder = os.path.abspath(output_file.name)
            output_dir = os.path.dirname(output_file.name)

            loading_thread_switch(True)
            VidToAVI(file_path, output_folder)
            loading_thread_switch(False)

            print("Conversion complete!")
            root.deiconify()
            openOutputFolder(output_dir, output_folder)
        else:
            root.deiconify()
    elif file_path == '':
        root.deiconify()
        print('No video File dropped.')
    else:
        notavideo()

def choose_file():
    global file_path
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Select Video File",
        filetypes=(("Video files", "*" + " *".join(video_extensions)), ("All files", "*.*"))
    )
    
    threading.Thread(target= save_video, args=(file_path, ), daemon=True).start()

# Main function
def VidToAVI(file_path, output_path):
    cmd = [
        ffmpeg,
        "-loglevel", "-8",
        '-y',
        '-i', file_path,
        "-vcodec", "copy",
        "-acodec","copy",
        output_path,
    ]
    print('converting to AVI...')
    print('File path: ', file_path)
    print('Output path: ', output_path)
    subprocess.run(cmd)

# main root
root = TkinterDnD.Tk()
if bundle_path:
    icon =  PhotoImage(file=os.path.join(bundle_path, 'ico.png'))
else:
    icon = PhotoImage(file='./ico/ico.png')
    
root.withdraw()

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
    gif_path = './splash/splash.gif'


gif_img = Image.open(gif_path)
gif_frames_rgba = [frame.convert("RGBA") for frame in ImageSequence.Iterator(gif_img)]

splash_label = tk.Label(splash_screen, bg='white')
splash_label.pack()

# Function to animate GIF frames
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

animate(0, False)

def show_main():
    def on_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
        
    def drag_enter(event):
        drop_label.config
        label.config

    def drag_leave(event):
        drop_label.config
        label.config
        
    def on_drop(event):
        global file_path
        drop_label.config
        label.config
        file_path = event.data.strip('{}')
        root.withdraw()
        save_video(file_path)

    if any(char.isalpha() for char in __version__):
        root.title(f"N8's Video to AVI Early Access {__version__}")
        
    else:
        root.title(f"N8's Video to AVI {__version__}")

    geo_width= 400
    center_window(root, geo_width, 300)
    root.iconphoto(True, icon)
    root.wm_iconbitmap('icon.icns')
    make_non_resizable(root)
    watermark_label(root)

    canvas = tk.Canvas(root)
    canvas.pack(expand=True, fill="both")

    # Create a button to choose a file
    choose_button = Button(canvas, text="Choose Video File", command=choose_file)
    choose_button.pack(side=tk.TOP, pady=50)

    # Create a Label for the drop area
    drop_label = tk.Label(canvas, text="Or Drag and Drop Video File Here")
    drop_label.pack() 

    # Bind the drop event to the on_drop function
    drop_label.bind("<Enter>", drag_enter)
    drop_label.bind("<Leave>", drag_leave)
    drop_label.drop_target_register(DND_FILES)
    drop_label.dnd_bind('<<Drop>>', on_drop)
    canvas.bind("<Enter>", drag_enter)
    canvas.bind("<Leave>", drag_leave)
    canvas.dnd_bind('<<Drop>>', on_drop)
    canvas.drop_target_register(DND_FILES)

    print("Current working directory:", os.getcwd())
    print("Executable path:", sys.executable)

    # logo on drop event area
    DnDLogo = 'icon_256x256.png' 
    if bundle_path:
        DnDLogo = os.path.join(bundle_path, DnDLogo)
    else:
        DnDLogo = './ico/icon_256x256.png'
    imgYPos = 250

    image = tk.PhotoImage(file=DnDLogo)
    resized_image = image.subsample(2)
    label = tk.Label(canvas, image=resized_image, bd=0)
    label.image = resized_image
    label.place(x=geo_width / 2, y=imgYPos, anchor=tk.CENTER)
    
    splash_screen.destroy()
    root.deiconify()

def on_closing():
    print("Closing the application.")
    
    atexit.unregister(on_closing)  # Unregister the atexit callback
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)
atexit.register(on_closing)

splash_screen.after(3500, show_main)

root.mainloop()