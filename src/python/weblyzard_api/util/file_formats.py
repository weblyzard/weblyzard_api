'''
Created on Nov 24, 2023

@author: max
'''
from dataclasses import dataclass


@dataclass
class FileFormat(object):
    ending: str
    label: str
    type: str


KNOWN_FORMATS = [
    FileFormat('mp4', 'MPEG-4 Part 14', 'video'),
    FileFormat('mov', '(QuickTime Movie', 'video'),
    FileFormat('avi', '(Audio Video Interleave', 'video'),
    FileFormat('wmv', '(Windows Media Video', 'video'),
    FileFormat('mkv', '(Matroska Video', 'video'),
    FileFormat('flv', 'Flash Video', 'video'),
    FileFormat('mpeg', 'MPEG-1/MPEG-2', 'video'),
    FileFormat('webm', '', 'video'),
    FileFormat('3gp', '3GPP Multimedia', 'video'),
    FileFormat('m4v', 'MPEG-4 Video File', 'video'),
    FileFormat('ts', 'MPEG Transport Stream', 'video'),
    FileFormat('mts', 'AVCHD Video File', 'video'),
    FileFormat('vob', 'DVD Video Object File', 'video'),
    FileFormat('mpg', 'MPEG Video File', 'video'),
    FileFormat('asf', 'Advanced Systems Format', 'video'),
    FileFormat('swf', 'Shockwave Flash Movie', 'video'),
    FileFormat('rm', 'RealMedia', 'video'),
    FileFormat('ogv', 'Ogg Video', 'video'),
    FileFormat('dv', 'Digital Video', 'video'),
    FileFormat('f4v', 'Flash Video', 'video'),
    FileFormat('ogg', 'Ogg Vorbis Video', 'video'),
    FileFormat('h264', 'H.264/MPEG-4 AVC', 'video'),
    FileFormat('hevc', 'High-Efficiency Video Coding', 'video'),
    FileFormat('xvid', 'Xvid Video', 'video'),
    FileFormat('divx', 'DivX Video', 'video'),
    FileFormat('jpeg', 'Joint Photographic Experts Group', 'image'),
    FileFormat('jpg', 'Joint Photographic Experts Group', 'image'),
    FileFormat('gif', 'Graphics Interchange Format', 'image'),
    FileFormat('png', 'Portable Network Graphics', 'image'),
    FileFormat('tiff', 'Tag Image File Format', 'image'),
    FileFormat('tif', 'Tag Image File Format', 'image'),
    FileFormat('bmp', 'Windows Bitmap', 'image'),
    FileFormat('svg', 'Scalable Vector Graphics', 'image'),
]


def get_file_type(ending: str) -> FileFormat:
    """Get the file type of ending (video/image/txt)
    :param ending: the file ending or a full filename/url to look up.
    """
    if ending is None or not isinstance(ending, str): return None
    if '.' in ending:
        ending = ending.split('.')[-1]
    for ff in KNOWN_FORMATS:
        if ending.lower() == ff.ending:
            return ff
    return None
