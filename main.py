import packaging.version
import tkinter as tk
from tkinter import filedialog, ttk
from tkinterdnd2 import DND_FILES
import os
import sys
import subprocess
import atexit
import threading
import re

# version info
from __version__ import __version__, __ffmpeg__

# splash screen module
from modules.rootTkSplashModule import (
    root,
    splash_screen,
    animate
)

# tk popups and settings
from modules.PopupModules import (
    create_popup, 
    notavideo,
    codec_popup
    )
from modules.TkModules import (
    make_non_resizable, center_window,
    Button
    )

# platform modules
from modules.platformModules import (
    bundle_path,
    ffmpeg,
    openOutputFolder
    )

# info module
from modules.infoModules import watermark_label

# data module
from modules.dataBinaryModules import (
    video_extensions, codec_dict,
    is_video_file
    )

from modules.UpdaterModule import autoChecker

# Loading functions
loading_screen = None

def loading(root, texthere='', filenum=0, filestotal=0):
    global loading_screen, load_text_label

    if loading_event.is_set():
        if not loading_screen: 
            loading_screen = create_popup(root, "Converting...", 380, 150, 0)
            make_non_resizable(loading_screen)
            
            load_text_label = ttk.Label(loading_screen, text='Converting...\nPlease wait.', anchor="center", justify="center")
            load_text_label.pack(pady=20)

            update_loading(texthere, filenum, filestotal)

            progress_bar = ttk.Progressbar(loading_screen, mode='indeterminate')
            progress_bar.pack(fill=tk.X, padx=10, pady=0)
            progress_bar.start()
            loading_screen.update_idletasks()
            print('starting loading popup')
    else:
        if loading_screen:  
            loading_screen.destroy()
            loading_screen = None 
            print('loading popup dead')

def update_loading(texthere='', filenum=0, filestotal=0):
    if filenum == 0 and filestotal == 0 or filestotal == 1:
        load_text_label.config(text=f'{texthere}\n\nConverting...\nPlease wait.')
    else:
        load_text_label.config(text=f'({filenum}/{filestotal} Files)\n{texthere}\n\nConverting...\nPlease wait.')
    
    loading_screen.update_idletasks()

loading_event = threading.Event()

def loading_thread(root, texthere='', filenum=0, filestotal=0):
    loading_event.set()
    print('starting thread')
    loading(root, texthere, filenum, filestotal)

def loading_thread_switch(root, switch, texthere='', filenum=0, filestotal=0):
    if switch:
        threading.Thread(target=loading_thread, args=(root, texthere, filenum, filestotal), daemon=True).start()
        print('Thread Initialized.')
    else:
        print('killing loading popup')
        loading_event.clear()
        root.after(0, loading(root))

def save_video(file_path, codec):
    output_dir = None
    
    if saveas_var.get():
        print("Save As Mode is enabled.")
        
        output_dir = filedialog.askdirectory(
            title="Select Folder to Save AVI File",
            initialdir=os.path.dirname(file_path[0][1])
        )
        
        print('Output Directory:', output_dir)
        if not output_dir:
            root.deiconify()
            return

    loading_thread_switch(root, True, file_path[0][0], 1, len(file_path))
    
    for filenum, (file, full_path) in enumerate(file_path, start=1):
        
        if saveas_var.get():
            output_file = os.path.join(output_dir, f"{os.path.splitext(file)[0]}.avi")
        else:
            file_root = os.path.splitext(os.path.abspath(full_path))[0]
            output_file = f'{file_root}.avi'
            output_dir = os.path.dirname(full_path)
        
        if loading_screen:
            update_loading(file, filenum, len(file_path))
        
        VidToAVI(full_path, output_file, codec)
    
    loading_thread_switch(root, False)
    print("Conversion complete!")
    root.deiconify()
    
    try:
        openOutputFolder(output_dir, output_file)
    except OSError as e:
        print(f"Error: {e}")

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
    global valid_files
    invalid_files = []
    valid_files = []

    print('File Path: ', file_path)

    if file_path == '':
        root.deiconify()
        print('No video File dropped.')
        return

    for file in file_path:
        if not is_video_file(file):
            print(f'File "{file}" is not a supported video file.')
            invalid_files.append(os.path.basename(file))
            continue

        valid_files.append((os.path.basename(file), file))

    if invalid_files and len(valid_files) == 0:
        root.deiconify()
        notavideo(invalid_files,[f[0] for f in valid_files])

    if valid_files:
        threading.Thread(target=save_video, args=(valid_files, codec), daemon=True).start()
        print('Initializing Conversion...')

# Main function
def VidToAVI(file_path, output_path, codec):
    cmd = [
        ffmpeg,
        "-loglevel", "quiet",
        '-y',
        '-i', file_path,
        "-vcodec", codec,
        "-acodec","copy",
        output_path,
    ]
    print('converting to AVI...')
    print('Codec: ', codec)
    print('File path: ', file_path)
    print('Output path: ', output_path)
    subprocess.run(cmd)

# main root
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
        ver = packaging.version.parse(version_str)
        return ver.is_prerelease or ver < packaging.version.parse("1.0.0")

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

    moreinfo_button = Button(codec_frame, text='?', command=lambda:codec_popup(root, codec_combobox, codec_dict))
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
    reg_dnd(codec_frame)
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

    root.update_idletasks()
    splash_screen.destroy()
    root.deiconify()

    threading.Thread(target=autoChecker, daemon=True).start()    

def on_closing():
    print("Closing the application.")
    
    atexit.unregister(on_closing)  # Unregister the atexit callback
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)
atexit.register(on_closing)

splash_screen.after(1750, show_main)

root.mainloop()