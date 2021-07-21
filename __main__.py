import audioplayer
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class Handler:
    def __init__(self):
        self.PlayButtonMode = 0  # 0 is paused, 1 is playing
        self.Audio = None  # tracks filename of audio file
        self.sound = None  # audioplayer object
        self.sliderPos = 0

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
            stop_start.set_label("gtk-media-play")
            self.sound.ms_elapsed = 0

        print("Song path: " + str(self.Audio))
        print("Song Length in ms: " + str(self.sound.audio_length))  # pydub uses ms
        slider_val.set_value(0)
        STElapsed.set_text("0:00 / " + str(self.sound.DisplaySongLength))

    def playClicked(self, widget):
        if self.PlayButtonMode == 0:
            print("Starting Sound.")
            self.sound.play(0)
            widget.set_label("gtk-media-pause")
            self.PlayButtonMode = 1
        else:
            self.sound.stop()
            print("Stopped Sound.")
            self.PlayButtonMode = 0
            widget.set_label("gtk-media-play")

    def sliderMoved(self, gtkRange, scroll, value):
        self.sliderPos = (max(min(int(value), 100), 0))

    def sliderReleased(self, widget, event):
        if self.PlayButtonMode == 0 and self.sound:
            self.sound.play(int((self.sliderPos / 100) * self.sound.audio_length))
            stop_start.set_label("gtk-media-pause")


    def sliderPressed(self, widget, event):
        if self.PlayButtonMode == 1:
            self.sound.stop()
            stop_start.set_label("gtk-media-play")


builder = Gtk.Builder()
builder.add_from_file("mainwindow.glade")
builder.connect_signals(Handler())
window = builder.get_object("window")
stop_start = builder.get_object("song_play_pause")
STElapsed = builder.get_object("song_time_elapsed")
STRemaining = builder.get_object("song_time_remaining")
slider_val = builder.get_object("adjustment1")
window.show_all()
Gtk.main()
