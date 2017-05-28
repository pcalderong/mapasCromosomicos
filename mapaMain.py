import gi
import math
import cairo
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk
from utils import getGenDescriptions
from utils import MouseButtons

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
        self.coords = []
        self.size = 0
        window.set_default_size(1000, 1000)
        window.show_all()
        self.arrayGen = getGenDescriptions("genDescriptions.txt")
        self.boxDrawMap = builder.get_object("boxMap")
        self.initDrawingArea()

    def initDrawingArea(self):
        self.drawingMap = Gtk.DrawingArea()
        self.drawingMap.set_size_request(600, 200)
        self.drawingMap.connect('draw', self.draw)
        # self.drawingMap.set_events(Gdk.EventMask.BUTTON_PRESS_MASK)
        # self.drawingMap.connect('button-press-event', self.on_button_press)
        self.drawingMap.show()
        self.boxDrawMap.pack_start(self.drawingMap, True, True, 1)

    def draw(self, widget, cr):
        cr.set_source_rgba(0, 0, 0, 1)
        cr.set_line_width(20)

        cr.set_source_rgba(0, 0.45, 1, 1)
        cr.set_line_cap(cairo.LINE_CAP_ROUND)
        cr.move_to(30, 90)
        cr.line_to(560, 90)
        cr.stroke()

        cr.set_line_width(1.5)

        cr.move_to(30, 65)
        cr.line_to(30, 100)
        cr.stroke()

        cr.move_to(150, 65)
        cr.line_to(150, 115)
        cr.stroke()

        cr.move_to(155, 65)
        cr.line_to(155, 115)
        cr.stroke()

    # def onBtnPress(self, w, e):
    #     if e.type == Gdk.EventType.BUTTON_PRESS \
    #         and e.button == MouseButtons.LEFT_BUTTON:
    #         # self.drawingMap.queue_draw()
    #         self.cr.arc(0, 0, 50, 0, 2*math.pi)
    #         self.cr.stroke_preserve()
    #         self.cr.set_source_rgb(0.3, 0.4, 0.6)
    #         self.cr.fill()
    #         print("LEFT")
    #     if e.type == Gdk.EventType.BUTTON_PRESS \
    #             and e.button == MouseButtons.RIGHT_BUTTON:
    #         self.drawingMap.queue_draw()
    #         print("RIGHT")

    def onSpinChange(self, button):
        newQty = button.get_value_as_int()
        if self.gens < newQty:
            print("--Add--")
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
        else:
            print("--Substract--")
            for i in range(newQty, self.gens):
                self.boxTxtGen.remove(self.txtGenList.pop())
                self.boxLabelGen.remove(self.labelGenList.pop())
        self.gens = button.get_value_as_int()

    def validateEmptyTextBox(self):
        for i in range(0, self.gens):
            if self.txtGenList[i].get_text() == '':
                return False
        return True

    def onBtnGenerate(self, button):
        self.cleanTable()
        self.arrayProb = []
        x = 75
        y = 0
        if self.validateEmptyTextBox():
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
                        entry.set_text("0.0")
                        entry.modify_fg(Gtk.StateFlags.NORMAL, Gdk.RGBA(1.0, 0.0, 0.0).to_color())
                        entry.connect("changed", self.onEntryChanged, i-1, j-1)
                        entry.set_width_chars(5)
                        self.layoutTable.put(entry, x, y)
                        entry.show()
                        lineProb.append(entry.get_text())
                    x += 75
                y += 50
                x = 0
                if len(lineProb) > 0:
                    self.arrayProb.append(lineProb)
        else:
            print("Make sure you fill all the gen descriptions")

    def onEntryChanged(self, entry, x, y):
        # self.draw()
        print("Hello"+str(x)+"-"+str(y))
        flagRed = False
        try:
            value = float(entry.get_text())
            if value <= 0.0 or value > 1.0:
                flagRed = True
        except:
            entry.set_text("0.0")
            flagRed = True
        if flagRed:
            entry.modify_fg(Gtk.StateFlags.NORMAL, Gdk.RGBA(1.0, 0.0, 0.0).to_color())
        else:
            entry.modify_fg(Gtk.StateFlags.NORMAL, Gdk.RGBA(0.0, 0.7, 0.4).to_color())
        self.arrayProb[x][y] = entry.get_text()
        self.displayRelation()

    def displayRelation(self):
        i = 0
        j = 0
        for row in self.arrayProb:
            for col in row:
                # if i != j:
                    # value = col.get_text()
                print("GE"+str(i)+" and GE"+str(j)+" have "+col+"%")
                j += 1
            i+=1
            j = 0


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