from mutagen.id3 import ID3 as id3
import mutagen
from copy import deepcopy

from constants import *
import lastfm

'''
Following are some tags for id3 (source: http://id3.org/id3v2.4.0-frames):

APIC Attached picture
COMM Comments
GEOB General encapsulated object
PRIV Private frame
TALB Album/Movie/Show title
TCOM Composer
TCON Content type
TDEN Encoding time
TDRC Recording time
TDRL Release time
TIT2 Title/songname/content description
TPE1 Lead performer(s)/Soloist(s)
TPE2 Band/orchestra/accompaniment
TPOS Part of a set
TRCK Track number/Position in set
TSOA Album sort order
TSOP Performer sort order
TSOT Title sort order
TRCK Software/Hardware and settings used for encoding
'''


def loadAllowedTags(name):
    f = open(name, 'r', encoding='utf-8')
    allowedTags = set(map(lambda x: x.strip(), f.readlines()))
    f.close()
    return allowedTags


def clearGarbageTags(file):
    allowedTags = loadAllowedTags('allowedTags.txt')
    audio = id3(SOURCE + file)

    for tag in list(audio.keys()):
        if tag not in allowedTags:
            audio.delall(tag)

    audio.save()


def addTags(file):
    track, album, artist = lastfm.searchInfo(file.strip('.mp3'))
    audio = id3(SOURCE + file)

    if track:
        try:
            audio['TIT2'].text = track
        except KeyError:
            audio.add(mutagen.id3.TIT2(encoding=3, text=track))
    if album:
        try:
            audio['TALB'].text = album
        except KeyError:
            audio.add(mutagen.id3.TALB(encoding=3, text=album))
    if artist:
        try:
            audio['TPE2'].text = artist
        except KeyError:
            audio.add(mutagen.id3.TPE2(encoding=3, text=artist))

    audio.save()
