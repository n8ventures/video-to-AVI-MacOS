import tkinter as tk
from tkinter import ttk
import emoji

from __version__ import __version__
from modules.TkModules import make_non_resizable, center_window, Button

def notavideo(invalid_file, valid_file):
    from modules.rootTkSplashModule import root
    longest_invalid_length = max((len(file) for file in invalid_file if len(file) > 50), default=0)
    longest_valid_length = max((len(file) for file in valid_file if len(file) > 50), default=0)
    largest_length = max(longest_invalid_length, longest_valid_length)

    weight = (largest_length * 3) + 400
    height = (((len(invalid_file)+len(valid_file))*16)+150)
    
    if len(valid_file) != 0:
        height = height + 25
        
    print(f'{weight} x {height}')
    notavideo = create_popup(root, "Not A Video!", weight, height, 1, 1)
    make_non_resizable(notavideo)

    invalid_files_list = emoji.emojize(":cross_mark: ") + emoji.emojize("\n:cross_mark: ").join(invalid_file)
    button_text = 'Close'
    
    if len(valid_file) != 0:
        valid_files_list = emoji.emojize(":check_mark_button: ") + emoji.emojize("\n:check_mark_button: ").join(valid_file)
        valid_text = f"The following files will be processed:\n\n{valid_files_list}"
        button_text = 'Continue'
    else:
        valid_text = 'Please select valid video files!'

    errortext = (
        "The following files are not video files:\n\n"
        f"{invalid_files_list}\n\n"
        f"{valid_text}"
    )

    display_text_label = ttk.Label(notavideo, text=errortext,  anchor="center", justify="center")
    display_text_label.pack(pady=10)

    close_button = Button(notavideo, text=button_text, command=notavideo.destroy)
    close_button.pack(pady=10) 

def create_popup(root, title, width, height, switch, lift = 0):
    popup = tk.Toplevel(root)
    center_window(popup, width, height)
    popup.title(title)

    popup.attributes('-type', 'utility')

    if switch == 1:
        popup.bind("<FocusOut>", lambda e: popup.after(200, popup.destroy))
    if lift == 1:
        popup.lift()

    popup.grab_set()
    return popup

def codec_popup(root, codec_combobox, codec_dict):
    geo_width = 350
    geo_len= 450

    selected_codec = codec_combobox.get()
    codec_info, codec_description, codec_usage, codec_speed, codec_size, codec_quality = codec_dict.get(selected_codec, ("Unknown", "No information available.", "How did you break it???", 'tell me', 'nate@n8venures.dev', 'pls ty'))

    codec_menu = create_popup(root, f"Codec Info: {codec_info}", geo_width, geo_len, 1)
    make_non_resizable(codec_menu)

    codec_message = tk.Message(codec_menu, text=f"{selected_codec}\n[{codec_info}]\n\nINFO:\n{codec_description}\n\nUSAGE:\n{codec_usage}",justify='center')
    codec_message.pack(pady=10)
    
    codec_stat = tk.Label(codec_menu, text=f"QUALITY:\n{codec_quality}\n\nSPEED:\n{codec_speed}\n\nEST. SIZE:\n{codec_size}", justify='center')
    codec_stat.pack(pady=10)

    close_button = Button(codec_menu, text="Close", command=codec_menu.destroy)
    close_button.pack(pady=10)



