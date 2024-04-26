from setuptools import setup
from __version__ import __versionMac__

if any(char.isalpha() for char in __versionMac__):
    icon = 'icoDev.icns'
else:
    icon = 'ico.icns'

APP = ['main-MacARM.py']
OPTIONS = {
    'iconfile': icon, 
    'packages':[
        'PIL',
        'tkinter',
        'tkinterdnd2',
        'subprocess', 
        'json',
        'urllib3', 
        'packaging', 
        'requests', 
        'pywinctl', 
        'tkmacosx',
        'colour',
        'charset_normalizer',
        'colorama',
        'tk',
        'typing_extensions',
        'threading',
        'shutil',
        'glob',
        'platform',
        'encodings',
        ],
    'includes':[
        'requests',
        'subprocess',
        'sys',
        'atexit',
        'tkinter',
        'os',
        'json',
        'shutil',
        'threading',
        'time',
        'math',
        'glob',
        'platform',
        ],
    'frameworks':[
        '/opt/homebrew/Cellar/tcl-tk/8.6.14/lib/libtk8.6.dylib',
        '/opt/homebrew/Cellar/tcl-tk/8.6.14/lib/libtcl8.6.dylib',
    ],
    'plist': {
        'NSHumanReadableCopyright': 
            'Copyright © 2024 John Nathaniel Calvara. This software is licensed under the MIT License.',
        'CFBundleIdentifier':
            "dev.n8ventures.N8VideoToAVI(Beta)",
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
        ]),
     ('../lib', ['/opt/homebrew/Cellar/tcl-tk/8.6.14/lib/']),
        ]
setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
    name='N8\'s Video To AVI (Beta)',
    version= __versionMac__,
    description='convert videos to AVI using FFMPEG.',
    author='John Nathaniel Calvara',
    author_email='nate@n8ventures.dev',
    url='https://github.com/n8ventures/video-to-gifski',
)
