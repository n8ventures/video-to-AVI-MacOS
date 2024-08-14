from setuptools import setup
from __version__ import __version__
import packaging.version

def is_beta(version_str):
    ver = packaging.version.parse(version_str)
    return ver.is_prerelease or ver < packaging.version.parse("1.0.0")

if is_beta(__version__):
    appname = "N8's Video To AVI (Beta)"
    icon = 'iconDev.icns'
else:
    appname = "N8's Video To AVI"
    icon = 'icon.icns'

APP = ['main.py']
OPTIONS = {
    'iconfile': icon, 
    'packages':[
        'PIL',
        'tkinter',
        'tkinterdnd2',
        'packaging', 
        'tkmacosx',
        'tk',
        ],
    'includes':[
        'subprocess',
        'sys',
        'atexit',
        'os',
        'shutil',
        'threading',
        'platform',
        're',
        ],
        'excludes': [
        'PyInstaller', #this is due to the packaging module
        ],
    'frameworks':[
        '/opt/homebrew/Cellar/tcl-tk/8.6.14/lib/libtk8.6.dylib',
        '/opt/homebrew/Cellar/tcl-tk/8.6.14/lib/libtcl8.6.dylib',
    ],
    'plist': {
        'NSHumanReadableCopyright': 
            'Copyright © 2024 John Nathaniel Calvara. This software is licensed under the MIT License.',
        'CFBundleIdentifier':
            "dev.n8ventures.N8VideoToAVI",
        'NSAppleScriptEnabled':
            True,
        'CFBundleGetInfoString':
            'Convert Video To AVI with FFmpeg.',
        }
}
DATA_FILES=[   
    ('.', [
        './bin/ffmpeg',
        'icon.icns',
        'iconDev.icns',
        './splash/splash.gif',
        './assets/ico.png',
        './assets/icondev.png',
        './assets/icon_256x256.png'
        ]),
     ('../lib', ['/opt/homebrew/Cellar/tcl-tk/8.6.14/lib/']),
        ]
setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
    name=appname,
    version= __version__,
    description='convert videos to AVI using FFMPEG.',
    author='John Nathaniel Calvara',
    author_email='nate@n8ventures.dev',
    url='https://github.com/n8ventures/video-to-AVI-MacOS',
)
