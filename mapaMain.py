import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class mapaWin:


    def __init__(self):
        builder = Gtk.Builder()
        builder.add_from_file("MapaUI.glade")
        builder.connect_signals(self)
        window = builder.get_object("winMapa")
        window.set_default_size(800, 800)
        window.show_all()

if __name__=="__main__":
    window = mapaWin()
    Gtk.main()