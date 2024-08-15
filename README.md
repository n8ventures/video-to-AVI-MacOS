# Video To AVI for MacOS

very simple GUI app for MacOS that converts videos into a .AVI container with various codecs to choose from using FFMPEG.

## Licenses

This software is distributed under the terms of the [MIT License](LICENSE).

Third-party components used in this software may have their own licenses. 
Please refer to the following for more information:

- [FFmpeg License](https://ffmpeg.org/legal.html)

## Downloadable Build
[Download Here](https://github.com/n8ventures/video-to-AVI-MacOS/releases/latest)

## Using Python
- Written with Python 3.12.3
- run `pip3 -r requirements.txt` to install the modules
- run `python main.py`

## How To Use

### 1. Before we import our videos, select our preferred codec!

![Selecting your codec](/assets/howto/Selecting_Codec.gif)

You can also learn more information about the codec you'll be implimenting!

![Codec Info](/assets/howto/Checking-codec-Info.gif)

### For more info about each codec here's a table:

Codec | Speed | Size | Lossless?
:---: | :---: | :---: | :---:
copy | Very Fast | Identical | ❓ (Depends on the codec of the video)
utvideo | Fast | Significantly Larger | ✅
rawvideo  | Fast | Much Larger | ✅
qtrle | Very Slow | Significantly Larger | ✅
prores | Fast | Larger | ❌
huffyuv | Fast | Significantly Larger | ✅
libx264 | Slow | Much Smaller | ❌
mpeg4 | Fast | Smaller | ❌
mjpeg | Slow | Larger | ❌
cfhd | Fast | Significantly Larger | ❌

- I used a 200MB h.264 video lasting about a minute and a half to convert and here's my results. Note that your experience may vary.

### The 'Save As' checkbox!

![Save As Checkbox](assets/howto/saveas_checkbox.gif)

 - Activating this will ask you which directory to save (not each file, since that would be *really* annoying).

### 2. Import your video file and wait for conversion!

- You may choose between clicking the area of the app or drag-and-drop it!

Drag-and-drop
![Drag-and-drop method](/assets/howto/Draganddrop.gif)

Click to import
![Click the area to import](/assets/howto/click-and-import.gif)