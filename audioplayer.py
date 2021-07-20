# This file handles audio playback.

from pydub import AudioSegment
from pydub.playback import play


class Audio:
    def __init__(self, file, filetype):
        # self.name = filename # somehow get filename from file object, we'll figure this out when gtk is done.
        self.type = filetype
        self.sound = AudioSegment.from_file(file)




