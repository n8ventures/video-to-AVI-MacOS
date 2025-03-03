import os
import sys
import platform
import subprocess
import tkinter as tk
from __version__ import __version__

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


bundle_path = is_running_from_bundle()
ffmpeg = 'ffmpeg'
icon = None

if any(char.isalpha() for char in __version__):
    icon = os.path.join(bundle_path or '', 'icondev.png') if bundle_path else './assets/icondev.png'
else:
    icon = os.path.join(bundle_path or '', 'ico.png') if bundle_path else './assets/ico.png'

bundle_path = is_running_from_bundle()
if bundle_path:
    ffmpeg = os.path.join(bundle_path, ffmpeg)
else:
    MacOSbin = './bin/'
    ffmpeg = os.path.join(MacOSbin, ffmpeg)

def is_folder_open(path):
    """
    Checks if the folder is currently open in Finder (macOS only).
    """
    if platform.system() != 'Darwin':  # Ensure this only runs on macOS
        raise OSError("is_folder_open is only supported on macOS.")

    folder_name = os.path.basename(path)

    # AppleScript to check Finder windows
    script = '''
        tell application "System Events"
            set openWindows to name of every window of application process "Finder"
        end tell
        return openWindows
    '''

    try:
        open_windows = subprocess.check_output(['osascript', '-e', script]).decode('utf-8').strip().split(", ")
        # Check if folder name is in the list of open windows
        return folder_name in open_windows
    except subprocess.CalledProcessError as e:
        print(f"Error checking Finder windows: {e}")
        return False
    
def openOutputFolder(path, path2):
    """
    Opens the specified folder or reveals a file in Finder (macOS only).
    """
    if platform.system() != 'Darwin':  # Ensure this only runs on macOS
        raise OSError("openOutputFolder is only supported on macOS.")

    print('Checking if folder is open...')
    if not is_folder_open(path):
        print('Folder not found in Finder. Opening folder...')
    else:
        print('Folder is already open in Finder.')

    # Reveal the file or folder in Finder
    try:
        subprocess.run(['open', '-R', path2], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error opening folder in Finder: {e}")
