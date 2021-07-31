# This file handles audio playback.


from pydub import AudioSegment
import simpleaudio
import io  # we don't want to make tempfiles for audiosegment to write to.
from pygame import mixer  # SIMPLEAUDIO DOESN'T WORK ! ARGH

class PlaySound:
    def __init__(self, file):  # Used to initialize an audio object
        self.audio = AudioSegment.from_file(file)  # audiosegment object
        self.audio_length = len(self.audio)  # length of audio in ms
        self.generateDisplaySongLength(self.audio_length)
        self.isPlaying = None  # is it playing?
        self.playback = None  # simpleaudio object
        self._buffer = io.BytesIO()
        mixer.init()

    def play(self, ms_position):  # Used to play an audio object
        # we need to convert all files into WAV first, as it seems simpleaudio is not always compatible.
        # raw_data = self.audio.raw_data
        if self.isPlaying:
            self.stop()  # stops existing sound thread.
        # if ms_position:  # this insanity because simpleaudio REQUIRES channels, bytes per sample, and sample rate
        # no longer necessary, we're just going to always convert.
        processed_data = self.audio[ms_position:]
        self._buffer = None
        self._buffer = io.BytesIO()
        processed_data.export(self._buffer, format="ogg")
        if self._buffer:
            mixer.music.load(self._buffer)
            mixer.music.play()

            # self.playback = simpleaudio.play_buffer(
            #     tempAudSeg.raw_data,
            #     num_channels=tempAudSeg.channels,
            #     bytes_per_sample=tempAudSeg.sample_width,
            #     sample_rate=tempAudSeg.frame_rate
            # )  # https://github.com/jiaaro/pydub/issues/160


        self.isPlaying = True

    def stop(self):  # Used to stop an audio object
        mixer.music.stop()
        self.isPlaying = False

    def generateDisplaySongLength(self, ms):
        #  1000ms is 1 second
        #  60 seconds is 1 minute
        #  60000 ms in 1 minute
        seconds = int((ms/1000) % 60)
        if seconds == 0:
            seconds = "00"
        minutes = int((ms/60000) % 60)
        #  maybe adding hours at some point, not right now.
        self.DisplaySongLength = str(minutes) + ":" + str(seconds)
        return self.DisplaySongLength

    def generateDisplaySongPosition(self, ms):
        seconds = int((ms/1000) % 60)
        if seconds == 0:
            seconds = "00"
        elif seconds < 10:
            seconds = "0" + str(seconds)
        minutes = int((ms/60000) % 60)
        self.DisplaySongPosition = str(minutes) + ":" + str(seconds) # not available until this function is called once
        return self.DisplaySongPosition

    def generateDisplayRemaining(self, ms):
        timeRemaining = self.audio_length - ms
        seconds = int((timeRemaining/1000) % 60)
        if seconds == 0:
            seconds = "00"
        elif seconds < 10:
            seconds = "0" + str(seconds)
        minutes = int((timeRemaining/60000) % 60)
        self.DisplayRemaining = str(minutes) + ":" + str(seconds)  # not available until this function is called once
        return self.DisplayRemaining

#  Workflow:
#  Create a new var = PlaySound("file") object.
#  Start audio with var.play()

