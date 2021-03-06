import audioplayer
import gi
import time

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import GLib

class Handler:
    def __init__(self):
        self.PlayButtonMode = 0  # 0 is paused, 1 is playing
        self.Audio = None  # tracks filename of audio file
        self.sound = None  # audioplayer object
        self.sliderPos = 0  # slider's position
        self.s_elapsed = 0  # tracks seconds elapsed according to the slider position.
        self._song_finished = False
        self._timer_id = None

    def onDestroy(self, *args):  # used for closing window
        Gtk.main_quit()

    def fileChosen(self, widget):  # when file chooser selects a file

        self.Audio = widget.get_filename()

        if self.sound is None:
            self.sound = audioplayer.PlaySound(self.Audio)
        else:
            try:
                self.sound.stop()
                self.sound = None  # not sure if this is needed or if python can handle this GC
            except AttributeError:
                print("Previous song was never played, catching exception.")
            self.sound = audioplayer.PlaySound(self.Audio)
            self.PlayButtonMode = 0
            self.sliderPos = 0
            self.s_elapsed = 0
            slider_val.set_value(0)
            stop_start.set_label("gtk-media-play")

        print("Song path: " + str(self.Audio))
        print("Song Length in ms: " + str(self.sound.audio_length))  # pydub uses ms
        slider_val.set_value(0)  # reset slider to 0
        STElapsed.set_text("0:00 / " + str(self.sound.DisplaySongLength))

    def playClicked(self, widget):
        if self.sound:  # ensure that self.sound exists first, otherwise we get an error.
            if self.PlayButtonMode == 0:
                print("Starting Sound.")
                if self._timer_id:
                    GLib.source_remove(self._timer_id)
                self._timer_id = GLib.timeout_add(interval=1000, function=self.timeTracker)  # start timer
                if not self._song_finished:
                    self.sound.play(int((self.sliderPos / 100) * self.sound.audio_length))
                else:
                    self.sound.play(0)
                widget.set_label("gtk-media-pause")
                self.PlayButtonMode = 1
            else:
                self.sound.stop()
                print("Stopped Sound.")
                self.PlayButtonMode = 0
                widget.set_label("gtk-media-play")

    def sliderMoved(self, gtkRange, scroll, value):
        self.sliderMoving = 1
        self.sliderPos = (max(min(int(value), 100), 0))
        self.timeTracker()

    def sliderReleased(self, widget, event):
        if self.sound:
            self.sliderMoving = 0
            if not self.sliderPos == 100:
                if self._timer_id:
                    GLib.source_remove(self._timer_id)
                self._timer_id = GLib.timeout_add(interval=1000, function=self.timeTracker)  # start timer
                self.sound.play(int((self.sliderPos / 100) * self.sound.audio_length))  # sound.play is in ms
                stop_start.set_label("gtk-media-pause")
                self.PlayButtonMode = 1

    def sliderPressed(self, widget, event):
        if self.PlayButtonMode == 1:
            self.sound.stop()
            stop_start.set_label("gtk-media-play")
            self.PlayButtonMode = 0

    def timeTracker(self):
        songPosition = int((self.sliderPos / 100) * self.sound.audio_length) + (self.s_elapsed * 1000)
        if self._song_finished:
            self.sliderPos = 0
            self.s_elapsed = 0
            songPosition = 0
            self._song_finished = False
        self.s_elapsed += 1
        # Formula: percentage of slider completed * audio length = slider's position in ms
        # slider's position in ms + time elapsed in ms = final time
        # songPositionSec = round(songPosition / 1000, 2) # rough estimate (unused for now)

        if songPosition >= self.sound.audio_length and self.sliderMoving == 0:
            stop_start.set_label("gtk-media-play")
            self.PlayButtonMode = 0
            self._song_finished = True
            return False

        slider_val.set_value(round((songPosition / self.sound.audio_length * 100), 2))
        # the slider is a percentage of the song completed

        STElapsed.set_text(self.sound.generateDisplaySongPosition(songPosition) + " / " + self.sound.DisplaySongLength)

        STRemaining.set_text("-" + self.sound.generateDisplayRemaining(songPosition))

        if not self.sound.isPlaying:
            self.s_elapsed = 0
            stop_start.set_label("gtk-media-play")
            self.PlayButtonMode = 0
            return False
        else:
            return True

builder = Gtk.Builder()
builder.add_from_file("mainwindow.glade")
builder.connect_signals(Handler())
window = builder.get_object("window")
stop_start = builder.get_object("song_play_pause")
STElapsed = builder.get_object("song_time_elapsed")
STRemaining = builder.get_object("song_time_remaining")
slider_val = builder.get_object("adjustment1")
window.show_all()
mainloop = Gtk.main()
