import audioplayer
import gi
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
        print("Song path: " + str(self.Audio))

    def playClicked(self, widget):
        if self.PlayButtonMode == 0:
            self.sound = audioplayer.PlaySound(self.Audio)
            print("Song Length in ms: " + str(self.sound.audio_length))  # pydub uses ms
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
window.show_all()
Gtk.main()
