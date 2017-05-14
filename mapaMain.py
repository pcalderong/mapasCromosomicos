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
        self.boxLabelGen = builder.get_object("boxLabelGen")
        self.boxTxtGen = builder.get_object("boxTxtGen")
        self.layoutTable = builder.get_object("fixedMatrix")
        self.labelGenList = []
        self.txtGenList = []
        self.arrayProb = []
        self.gens = 0
        window.set_default_size(1000, 1000)
        window.show_all()
        self.arrayGen = getGenDescriptions("genDescriptions.txt")

    def onSpinChange(self, button):
        newQty = button.get_value_as_int()
        if self.gens < newQty:
            for i in range(self.gens,newQty):
                label = Gtk.Label("GE"+str(i+1))
                self.labelGenList.append(label)
                self.boxLabelGen.pack_start(label, True, True, 1)
                label.show()
                entry = Gtk.Entry()
                strDescription = "GE"+str(i+1)
                if len(self.arrayGen)>newQty:
                    strDescription = self.arrayGen[i-1]
                else:
                    self.arrayGen.append(strDescription)
                entry.set_text(strDescription)
                self.txtGenList.append(entry)
                self.boxTxtGen.pack_start(entry, True, True, 1)
                entry.show()
        self.gens = button.get_value_as_int()

    def onBtnGenerate(self, button):
        self.cleanTable()
        self.arrayProb = []
        x = 75
        y = 0
        for i in range(self.gens+1):
            lineProb = []
            for j in range(self.gens+1):
                if i == 0:
                    if not j == self.gens:
                        label = Gtk.Label("GE"+str(j+1))
                        self.layoutTable.put(label, x, y)
                        label.show()
                elif j == 0:
                    label = Gtk.Label("GE" + str(i))
                    self.layoutTable.put(label, x, y)
                    label.show()
                else:
                    entry = Gtk.Entry()
                    entry.connect("changed", self.onEntryChanged, i-1, j-1)
                    entry.set_width_chars(3)
                    self.layoutTable.put(entry, x, y)
                    entry.show()
                    lineProb.append(entry)
                x += 75
            y += 50
            x = 0
            if len(lineProb) > 0:
                self.arrayProb.append(lineProb)

    def onEntryChanged(self, entry, x, y):
        print("Hello"+str(x)+"-"+str(y))
        self.arrayProb[x][y] = entry.get_text()


    def cleanGrid(self):
        self.labelGenList = []
        self.txtGenList = []
        for g in self.boxLabelGen:
            self.boxLabelGen.remove(g)
        for g in self.boxTxtGen:
            self.boxTxtGen.remove(g)

    def cleanTable(self):
        for l in self.layoutTable:
            self.layoutTable.remove(l)

if __name__=="__main__":
    window = mapaWin()
    Gtk.main()