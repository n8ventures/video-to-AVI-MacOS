from __version__ import __version__, __ffmpeg__
from packaging import version
import tkinter as tk
from tkinter import filedialog, ttk, PhotoImage
from tkinterdnd2 import TkinterDnD, DND_FILES
from tkmacosx import Button
from PIL import Image, ImageTk, ImageSequence
import os
import sys
import platform
import subprocess
import atexit
import threading
import re

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

    def on_closing():
        if switch == 1:
            popup.destroy()

    popup.protocol("WM_DELETE_WINDOW", on_closing)

    def noop_close():
        pass

    popup.bind("<Destroy>", lambda e: noop_close())

    if switch == 1:
        popup.bind("<FocusOut>", lambda e: popup.destroy())

    popup.grab_set()
    
    return popup

# popups
def about():
    geo_width = 370
    geo_len= 300

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

    close_button = Button(aboutmenu, text="Close", activebackground=('red'), command=aboutmenu.destroy)
    close_button.pack(pady=10)
    
def codec_popup():
    geo_width = 350
    geo_len= 400

    selected_codec = codec_combobox.get()
    codec_info, codec_description, codec_usage, codec_speed, codec_size, codec_quality = codec_dict.get(selected_codec, ("Unknown", "No information available.", "How did you break it???", 'tell me', 'nate@n8venures.dev', 'pls ty'))

    codec_menu = create_popup(root, f"Codec Info: {codec_info}", geo_width, geo_len, 1)
    make_non_resizable(codec_menu)

    codec_message = tk.Message(codec_menu, text=f"{selected_codec}\n[{codec_info}]\n\nINFO:\n{codec_description}\n\nUSAGE:\n{codec_usage}",justify='center')
    codec_message.pack(pady=10)
    
    codec_stat = tk.Label(codec_menu, text=f"QUALITY: {codec_quality}\n\nSPEED: {codec_speed}\n\nEST. SIZE: {codec_size}", justify='left')
    codec_stat.pack(pady=10)

    close_button = Button(codec_menu, text="Close", activebackground=('red'), command=codec_menu.destroy)
    close_button.pack(pady=10)

def notavideo():
    notavideo = create_popup(root, "Not a video!", 400, 100, 1)
    make_non_resizable(notavideo)

    errortext = (
        "Not a video! Please select a video file!"
    )

    about_label = tk.Label(notavideo, text=errortext, justify=tk.LEFT)
    about_label.pack(pady=10)

    close_button = Button(notavideo, text="Close", activebackground=('red'), command=notavideo.destroy)
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

def loading(texthere='', filenum=0, filestotal=0):
    global loading_screen, load_text_label
    
    if loading_event.is_set():
        if not loading_screen:  # Check if loading_screen is None
            loading_screen = create_popup(root, "Converting...", 350, 150, 0)
            make_non_resizable(loading_screen)
            load_text_label = tk.Label(loading_screen, text='Converting...\nPlease wait.')
            load_text_label.pack(pady=20)
            
            update_loading(texthere, filenum, filestotal)
            
            progress_bar = ttk.Progressbar(loading_screen, mode='indeterminate')
            progress_bar.pack(fill=tk.X, padx=10, pady=0)
            progress_bar.start()
            loading_screen.update_idletasks()
            print('starting loading popup')
    else:
        if loading_screen:  # Only destroy if it exists
            loading_screen.destroy()
            loading_screen = None  # Clear the reference
            print('loading popup dead')

def update_loading(texthere='', filenum=0, filestotal=0):
    if filenum == 0 and filestotal == 0 or filestotal == 1:
        load_text_label.config(text=f'{texthere}\n\nConverting...\nPlease wait.')
    else:
        load_text_label.config(text=f'({filenum}/{filestotal} Files)\n{texthere}\n\nConverting...\nPlease wait.')
    
    loading_screen.update_idletasks()

loading_event = threading.Event()

def loading_thread(texthere='', filenum=0, filestotal=0):
    loading_event.set()
    print('starting thread')
    loading(texthere, filenum, filestotal)
    
def loading_thread_switch(switch, texthere='', filenum=0, filestotal=0):
    if switch:
        threading.Thread(target=loading_thread, args=(texthere, filenum, filestotal), daemon=True).start()
        print('Thread Initialized.')
    else:
        print('killing loading popup')
        loading_event.clear()
        root.after(0, loading)
        
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

def save_video(file_path, codec):
    output_dir = None
    
    if saveas_var.get():
        print("Save As Mode is enabled.")
        
        output_dir = filedialog.askdirectory(
            title="Select Folder to Save AVI File",
            initialdir=os.path.dirname(file_path[0])
        )
        
        print('Output Directory:', output_dir)
        if not output_dir:
            root.deiconify()
            return
    loading_thread_switch(True, os.path.basename(file_path[0]), 1, len(file_path))
    
    for filenum, file in enumerate(file_path, start=1):
        filename = os.path.basename(file)
        
        if saveas_var.get():
            output_file = os.path.join(output_dir, f"{os.path.splitext(filename)[0]}.avi")
        else:
            file_root = os.path.splitext(os.path.abspath(file))[0]
            output_file = f'{file_root}.avi'
            output_dir = os.path.dirname(file)
        
        if loading_screen:
            update_loading(filename, filenum, len(file_path))

        VidToAVI(file, output_file, codec)
    
    loading_thread_switch(False)
    print("Conversion complete!")
    root.deiconify()
    
    if output_dir:
        openOutputFolder(output_dir, output_file)

def choose_file(event):
    global file_path
    root.withdraw()
    file_path = filedialog.askopenfilenames(
        title="Select Video File",
        filetypes=(("Video files", "*" + " *".join(video_extensions)), ("All files", "*.*"))
    )
    if file_path:
        files_selected(file_path, codec_dict[codec_combobox.get()][0])
    else:
        root.deiconify()

def files_selected(file_path, codec):
    print('File Path: ', file_path)
    if file_path:
        for file in file_path:
            if not is_video_file(file):
                print(f'File "{file}" is not a supported video file.')
                root.deiconify()
                return
        threading.Thread(target= save_video, args=(file_path, codec ), daemon=True).start()
        print('Initializing Conversion...')
    elif file_path == '':
        root.deiconify()
        print('No video File dropped.')
    else:
        notavideo()

# Main function
def VidToAVI(file_path, output_path, codec):
    cmd = [
        ffmpeg,
        "-loglevel", "-8",
        '-y',
        '-i', file_path,
        "-vcodec", codec,
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
    icon = PhotoImage(file='./assets/ico.png')

root.iconphoto(True, icon)
root.wm_iconbitmap('icon.icns')

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
    global codec_dict, codec_combobox, saveas_var

    def on_drop(event):
        global file_path
        root.withdraw()
        file_path = re.findall(r'\{.*?\}|\S+', event.data)
        file_path = [re.sub(r'[{}]', '', file) for file in file_path]
        
        if file_path:
            files_selected(file_path, codec_dict[codec_combobox.get()][0])
        else:
            root.deiconify()
    
    # def on_check():
    #     if saveas_var.get():
    #         unbind_dnd(drop_label)
    #         unbind_dnd(canvas)
    #         unbind_dnd(saveas_box)
    #         unbind_dnd(codec_label)
    #         drop_label.config(text="Drag and Drop Disabled.\n\nPlease, Click this area to select file/s")
    #         root.update_idletasks()
    #     else:
    #         reg_dnd(drop_label)
    #         reg_dnd(canvas)
    #         reg_dnd(saveas_box)
    #         reg_dnd(codec_label)
    #         drop_label.config(text="Drag and Drop Video File Here\nor\nClick this area to select file/s")
    #         root.update_idletasks()

    def is_beta(version_str):
        ver = version.parse(version_str)
        return ver.is_prerelease or ver < version.parse("1.0.0")

    if is_beta(__version__):
        root.title(f"N8's Video to AVI (Beta) {__version__}")
    else:
        root.title(f"N8's Video to AVI {__version__}")

    geo_width= 400
    center_window(root, geo_width, 400)
    make_non_resizable(root)
    watermark_label(root)

    canvas = tk.Canvas(root, highlightthickness=0, bd=0)
    canvas.pack(expand=True, fill="both")
    
    codec_dict = {
        "Quick Convert (Remux)": 
            ("copy", 
            "Uses the video's built-in codec.\nNo re-encoding is processed.", 
            "For fast conversion without quality loss. Use this if you know the original codec used in the video.",
            "Very Fast", "Identical", "lossless"),

        "UT Video": 
            ("utvideo", 
            "Lossless codec with high compression ratios and speed. Supports various color spaces and is designed for high performance.", 
            "Ideal for video editing and archiving where lossless quality is required, especially for intermediate files.",
            "Fast", "Significantly Larger", "lossless"),

        "Raw Video": 
            ("rawvideo", 
            "Uncompressed video. Provides the highest quality but results in very large file sizes.\nThis is the equivalent of Adobe After Effect's 'None (Uncompressed)' codec on AVI.",
            "Used for video editing and archiving when quality is paramount.",
            "Fast", "Much Larger", "lossless"),

        "QuickTime Animation": 
            ("qtrle", 
            "RLE (Run-Length Encoding) based codec, typically used for animated content with low motion.", 
            "Best used for animations and simple graphics where compression efficiency is prioritized over high motion detail.",
            "Very Slow", "Significantly Larger", "lossless"),

        "Apple ProRes": 
            ("prores", 
            "A high-quality, lossy codec widely used in professional video production for its efficient balance between file size and quality.", 
            "Commonly used in post-production and broadcasting for its ease of editing and high visual fidelity.",
            "Fast", "Larger", "lossy"),

        "Huffyuv": 
            ("huffyuv", 
            "A lossless video codec that compresses RGB video data without losing quality.", 
            "Preferred for scenarios where lossless quality is essential but some file size reduction is beneficial.",
            "Fast", "Significantly Larger", "lossless"),

        "H.264": 
            ("libx264", 
            "A highly efficient video compression standard, widely used for streaming, video storage, and digital distribution.", 
            "The go-to codec for streaming, web video, and general video storage due to its high compression efficiency.",
            "Slow", "Much Smaller", "lossy"),

        "MPEG-4": 
            ("mpeg4", 
            "A widely used codec for internet video, digital distribution, and some portable media players.", 
            "Versatile for various video applications, though often replaced by H.264 and other modern codecs in new projects.",
            "Fast", "Smaller", "lossy"),

        "MJPEG": 
            ("mjpeg", 
            "A codec that encodes video as a series of JPEG images, often used in older video capture devices.", 
            "Common in video capture, surveillance, and devices with limited processing power where simplicity is key.",
            "Slow", "Larger", "lossy"),

        "CineForm": 
            ("cfhd", 
            "A high-quality, lossy codec optimized for video editing, balancing compression and quality.", 
            "Used in professional video editing workflows, especially for intermediate files during post-production.",
            "Fast", "Significantly Larger", "lossy"),
    }
    
    # Create a Label for the drop area
    drop_label = tk.Label(canvas, text="Drag and Drop Video File Here\nor\nClick this area to select video file/s")
    drop_label.pack(pady=50)
    
    # Create dropdown menu to select codecs
    codec_label = tk.Label(canvas, text="Select AVI Codec:")
    codec_label.pack(pady=(10, 5))
    
    codec_frame = tk.Frame(canvas)
    codec_frame.pack()
    
    codec_combobox = ttk.Combobox(codec_frame, values=list(codec_dict.keys()), state="readonly")
    if codec_dict:
        codec_combobox.set(list(codec_dict.keys())[0])

    codec_combobox.pack(side='left')

    moreinfo_button = Button(codec_frame, text='?', activebackground=('yellow','green'), width=25, height=25, borderless=1, command=codec_popup)
    moreinfo_button.pack(side='right')
    
    saveas_var = tk.IntVar()
    saveas_box = tk.Checkbutton(canvas, text="'Save As' Mode", variable=saveas_var)
    # saveas_box.config(command=on_check)
    saveas_box.pack(pady=10)

    # Bind the drop event to the on_drop function
    def reg_dnd(widget):
        widget.drop_target_register(DND_FILES)
        widget.dnd_bind('<<Drop>>', on_drop)
    
    def unbind_dnd(widget):
        widget.dnd_bind('<<Drop>>')

    reg_dnd(drop_label)
    reg_dnd(canvas)
    reg_dnd(saveas_box)
    reg_dnd(codec_label)
    codec_label.bind('<Button-1>', choose_file)
    drop_label.bind('<Button-1>', choose_file)
    canvas.bind('<Button-1>', choose_file)

    print("Current working directory:", os.getcwd())
    print("Executable path:", sys.executable)

    # logo on drop event area
    DnDLogo = 'icon_256x256.png' 
    if bundle_path:
        DnDLogo = os.path.join(bundle_path, DnDLogo)
    else:
        DnDLogo = './assets/icon_256x256.png'
    imgYPos = 350

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

splash_screen.after(1750, show_main)

root.mainloop()