import audioplayer
import gi
import math
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class Handler:
    def __init__(self):
        self.PlayButtonMode = 0 # 0 is paused, 1 is playing
        self.Audio = None  # tracks filename of audio file
        self.sound = None  # audioplayer object

    def onDestroy(self, *args):  # used for closing window
        Gtk.main_quit()

    def fileChosen(self, widget):  # when file chooser selects a file
        self.Audio = widget.get_filename()

        if self.sound == None:
            self.sound = audioplayer.PlaySound(self.Audio)
        else:
            self.sound.stop()
            self.sound = None  # not sure if this is needed or if python can handle this GC
            self.sound = audioplayer.PlaySound(self.Audio)
            self.PlayButtonMode = 0
            stop_start.set_label("gtk-media-play")

        print("Song path: " + str(self.Audio))
        print("Song Length in ms: " + str(self.sound.audio_length))  # pydub uses ms
        STElapsed.set_text("0:00 / " + str(self.sound.DisplaySongLength))

    def playClicked(self, widget):
            if self.PlayButtonMode == 0:
                self.sound.play()
                widget.set_label("gtk-media-pause")
                self.PlayButtonMode = 1
            else:
                self.sound.stop()
                print("Stopped Sound.")
                self.PlayButtonMode = 0
                widget.set_label("gtk-media-play")


builder = Gtk.Builder()
builder.add_from_file("mainwindow.glade")
builder.connect_signals(Handler())
window = builder.get_object("window")
stop_start = builder.get_object("song_play_pause")
STElapsed = builder.get_object("song_time_elapsed")
STRemaining = builder.get_object("song_time_remaining")
window.show_all()
Gtk.main()
