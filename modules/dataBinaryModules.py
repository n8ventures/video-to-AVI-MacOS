import os

video_extensions = [
    # Common video formats
    '.mp4', '.m4v', '.mpeg', '.mpg', '.mp2', '.mpv', '.m4p', '.mpe', 
    '.avi', '.mov', '.qt', '.vob',  '.mkv',

    # High definition and other video formats
    '.m2ts', '.mts', '.m2v', '.ts', '.webm', '.wmv', '.yuv', 

    # Flash and streaming video formats
    '.flv', '.f4v', '.asf', '.rm', '.rmvb', '.nsv', '.roq', 

    # Animated image/video formats
    '.gif', '.gifv', '.mng', 

    # Less common video formats
    '.3g2', '.3gp', '.amv', '.drc', '.mpx', 

    # Open formats
    '.ogg', '.ogv', 

    # Professional video formats
    '.mxf', 

    # Additional formats
    '.svi'
]

codec_dict = {
        "Quick Convert (Remux)": 
            ("copy", 
            "Uses the video's built-in codec.\nNo re-encoding is processed.", 
            "For fast conversion without quality loss. Use this if you know the original codec used in the video.",
            "Very Fast", "Identical", "lossless* (depending on the original codec)"),

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

        "Apple ProRes (Not recommended)": 
            ("prores", 
            "A high-quality, lossy codec widely used in professional video production for its efficient balance between file size and quality.", 
            "Commonly used in post-production and broadcasting for its ease of editing and high visual fidelity. Not recommended as ProRes does not support AVI.",
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

def is_video_file(file_path):
    _, file_extension = os.path.splitext(file_path)
    return file_extension.lower() in video_extensions