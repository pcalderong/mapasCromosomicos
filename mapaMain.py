import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from utils import getGenDescriptions

class mapaWin:


    def __init__(self):
        builder = Gtk.Builder()
        builder.add_from_file("MapaUI.glade")
        builder.connect_signals(self)
        window = builder.get_object("winMapa")
        self.grid = builder.get_object("gridGenDescription")
        self.gens = 0
        window.set_default_size(800, 800)
        window.show_all()
        self.hashGens = getGenDescriptions("genDescriptions.txt")

    def onSpinChange(self, button):
        self.gens = button.get_value_as_int()
        self.cleanGrid()
        print("TEST----"+str(self.gens))
        i=0
        for h in self.hashGens:
            if i < self.gens:
                print(h+"=>"+self.hashGens[h])
            i+=1




    def cleanGrid(self):
        for g in self.grid:
            self.grid.remove(g)

if __name__=="__main__":
    window = mapaWin()
    Gtk.main()