# This file handles audio playback.
# TODO: Fix MASSIVE corruption effect when playing audio(m4a only?) files.
from pydub import AudioSegment
import simpleaudio
from pydub.playback import _play_with_simpleaudio


class PlaySound:
    def __init__(self, file):  # Used to initialize an audio object
        self.audio = AudioSegment.from_file(file)  # audiosegment object
        self.audio_length = len(self.audio)  # length of audio in ms
        self._generateDisplaySongLength(self.audio_length)
        self.audio_pos = 0  # not in use
        self.isPlaying = None  # is it playing?
        self.playback = None  # simpleaudio object
        self.DisplaySongLength  # the M:SS display
        self.ms_elapsed = 0

    def play(self):  # Used to play an audio object
        if self.isPlaying:
            self.stop()  # stops existing sound thread.
        if AudioSegment:
            self.playback = simpleaudio.play_buffer(
                self.audio.raw_data,
                num_channels=self.audio.channels,
                bytes_per_sample=self.audio.sample_width,
                sample_rate=self.audio.frame_rate
            ) # https://github.com/jiaaro/pydub/issues/160
        self.isPlaying = True

    def stop(self):  # Used to stop an audio object
        self.playback.stop()
        self.isPlaying = False

    def _generateDisplaySongLength(self, ms):
        #  1000ms is 1 second
        #  60 seconds is 1 minute
        #  60000 ms in 1 minute
        seconds = int((ms/1000) % 60)
        if seconds == 0:
            seconds = "00"
        minutes = int((ms/60000) % 60)
        #  maybe adding hours at some point, not right now.
        self.DisplaySongLength = str(minutes) + ":" + str(seconds)

    #def _generateRemainingTime(self, ms_elapsed):
    #
    #
    #def _generateElapsedTime(self, ms_elapsed):


#  Workflow:
#  Create a new var = PlaySound("file") object.
#  Start audio with var.play()

