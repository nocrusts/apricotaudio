# This file handles audio playback.
from pydub import AudioSegment
from pydub.playback import _play_with_simpleaudio

class PlaySound:
    def __init__(self, file):  # Used to initialize an audio object
        self.audio = AudioSegment.from_file(file)  # audiosegment object
        self.audio_length = len(self.audio)  # length of audio in ms
        self.audio_pos = 0  # not in use
        self.isPlaying = None  # is it playing?
        self.playback = None  # simpleaudio object

    def play(self):  # Used to play an audio object
        if self.isPlaying:
            self.stop()  # stops existing sound thread.
        if AudioSegment:
            self.playback = _play_with_simpleaudio(self.audio)
        self.isPlaying = True

    def stop(self):  # Used to stop an audio object
        self.playback.stop()
        self.isPlaying = False



