import gi
# import math
import cairo
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk
from utils import getGenDescriptions
from utils import generateMap
from utils import saveFile
from utils import readFileWithProb
# from utils import MouseButtons

class mapaWin:


    def __init__(self):
        builder = Gtk.Builder()
        builder.add_from_file("MapaUI.glade")
        builder.connect_signals(self)
        window = builder.get_object("winMapa")
        self.boxLabelGen = builder.get_object("boxLabelGen")
        self.boxTxtGen = builder.get_object("boxTxtGen")
        self.layoutTable = builder.get_object("fixedMatrix")
        self.spinBtn = builder.get_object("spGens")
        self.fileChooser = builder.get_object("fcGen")
        self.fileChooserDialog = builder.get_object("filechooserdialogD")
        self.fileChooserDialog.add_button("Cancel", 1)
        self.fileChooserDialog.add_button("Ok", 2)
        self.labelGenList = []
        self.txtGenList = []
        self.arrayProb = []
        self.gens = 0
        self.maps = {}
        self.space = 0
        self.displayMap = False
        self.genLenght = []
        self.countFile = 0
        window.set_default_size(1000, 1000)
        window.show_all()
        self.arrayGen = getGenDescriptions("genDescriptions.txt")
        self.boxDrawMap = builder.get_object("boxMap")
        self.initDrawingArea()

    def initDrawingArea(self):
        self.drawingMap = Gtk.DrawingArea()
        self.drawingMap.set_size_request(400, 200)
        self.drawingMap.connect('draw', self.draw)
        # self.drawingMap.set_events(Gdk.EventMask.BUTTON_PRESS_MASK)
        # self.drawingMap.connect('button-press-event', self.on_button_press)
        self.drawingMap.show()
        self.boxDrawMap.pack_start(self.drawingMap, True, True, 1)

    # Signal triggered to update drawing area
    def draw(self, widget, cr):
        if self.displayMap:
            cr.set_source_rgba(0, 0, 0, 1)
            cr.set_line_width(20)

            cr.set_source_rgba(0, 0.35, 1, 1)
            cr.set_line_cap(cairo.LINE_CAP_ROUND)
            cr.move_to(60, 130)
            cr.line_to(330, 130)
            cr.stroke()

            cr.set_line_width(1.5)
            cr.set_source_rgba(0, 0.7, 1, 1)
            for x in self.genLenght:
                offset = int(float(x) *100.0)+100
                cr.move_to(60 + offset, 90)
                cr.line_to(60 + offset, 150)
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

    # Signal triggered by spiner when user changes the value
    def onSpinChange(self, button):
        newQty = self.spinBtn.get_value_as_int()
        self.createTextBoxes(self.gens, newQty)
        self.gens = self.spinBtn.get_value_as_int()
        # self.space = 300 / self.gens

    # Validation for entry values
    def validateEmptyTextBox(self):
        for i in range(0, self.gens):
            if self.txtGenList[i].get_text() == '':
                return False
        return True

    # Signal to generate the default table values
    def onBtnGenerate(self, button):
        self.displayMap = False
        self.cleanTable()
        self.arrayProb = []
        self.generateTable(self.gens)

    # Signal triggered when the entry is changed.
    def onEntryChanged(self, entry, x, y):
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
        self.arrayProb[x][y] = entry
        self.displayRelation()

    # INFERENCE
    def displayRelation(self):
        i = 0
        j = 0
        tempFlag = True
        self.genLenght = []
        for row in self.arrayProb:
            for col in row:
                if i < j and col.get_text() == "0.0":
                    tempFlag = False
                elif i == 0:
                    name = "GE" + str(j)
                    self.maps[name] = col.get_text()
                    self.genLenght.append(col.get_text())
                j += 1
            i+=1
            j = 0
        if not self.displayMap:
            self.displayMap = tempFlag
        self.drawingMap.queue_draw()

    # Clean up UI on gen list side.
    def cleanGrid(self):
        # self.labelGenList = []
        # self.txtGenList = []
        self.spinBtn.set_value(0)

    # Clean up UI on probability side.
    def cleanTable(self):
        self.genLenght = []
        self.drawingMap.queue_draw()
        for l in self.layoutTable:
            self.layoutTable.remove(l)

    #
    def calculateProb(self, widget):
        self.displayMap = generateMap(self.arrayProb)
        self.drawingMap.queue_draw()


    #Signal triggered when file is selected to save the filename.
    def onFileSelected(self, widget):
        if widget.get_filename():
            self.fileName = widget.get_filename()

    # Signal for the response dialog.
    def onResponseDialog(self, widget, response):
        if response == 2:
            self.cleanTable()
            self.cleanGrid()
            result = readFileWithProb(self.fileName)
            self.loadFileGen(result[0])
            self.loadMatrix(result[1], len(result[0]))

    # Reads the list of elements thar were loaded from the
    # file and display it on the application.
    def loadFileGen(self, list):
        length = len(list)
        self.arrayGen = list
        self.spinBtn.set_value(length)

    # Reads the list of elements thar were loaded from the
    # file and display it on the application.
    def loadMatrix(self, matrix, qty):
        self.arrayProb = []
        self.generateTable(qty)
        i = 0
        j = 0
        for row in matrix:
            for col in row:
                self.arrayProb[i][j].set_text(col)
                j+=1
            j = 0
            i += 1

    # Generical methd to generate the UI for the gen list
    def createTextBoxes(self, gens, newQty):
        if gens < newQty:
            for i in range(gens,newQty):
                label = Gtk.Label("GE"+str(i+1))
                self.labelGenList.append(label)
                self.boxLabelGen.pack_start(label, True, True, 1)
                label.show()
                entry = Gtk.Entry()
                strDescription = "GE"+str(i+1)
                if len(self.arrayGen)>=newQty:
                    strDescription = self.arrayGen[i-1]
                else:
                    self.arrayGen.append(strDescription)
                entry.set_text(strDescription)
                self.txtGenList.append(entry)
                self.boxTxtGen.pack_start(entry, True, True, 1)
                entry.show()
        else:
            for i in range(newQty, self.gens):
                self.boxTxtGen.remove(self.txtGenList.pop())
                self.boxLabelGen.remove(self.labelGenList.pop())

    def generateTable(self, qty):
        x = 75
        y = 0
        if self.validateEmptyTextBox():
            for i in range(qty + 1):
                lineProb = []
                for j in range(qty + 1):
                    if i == 0:
                        if not j == qty:
                            label = Gtk.Label("GE" + str(j + 1))
                            self.layoutTable.put(label, x, y)
                            label.show()
                    elif j == 0:
                        label = Gtk.Label("GE" + str(i))
                        self.layoutTable.put(label, x, y)
                        label.show()
                    else:
                        entry = Gtk.Entry()
                        entry.set_text("0.0")
                        if i == j:
                            entry.set_editable(False)
                            entry.modify_fg(Gtk.StateFlags.NORMAL, Gdk.RGBA(0.0, 0.0, 1.0).to_color())
                        elif i < j:
                            entry.modify_fg(Gtk.StateFlags.NORMAL, Gdk.RGBA(1.0, 0.0, 0.0).to_color())
                            entry.connect("changed", self.onEntryChanged, i - 1, j - 1)
                        else:
                            entry.modify_fg(Gtk.StateFlags.NORMAL, Gdk.RGBA(0.0, 0.0, 1.0).to_color())
                            entry.set_text("---")
                            entry.set_editable(False)
                        entry.set_width_chars(5)
                        self.layoutTable.put(entry, x, y)
                        entry.show()
                        lineProb.append(entry)
                    x += 75
                y += 50
                x = 0
                if len(lineProb) > 0:
                    self.arrayProb.append(lineProb)
        else:
            print("Make sure you fill all the gen descriptions")

    # Exports values inserted on the UI to save it as a file.
    def onSaveFile(self,btn):
        saveFile(self.txtGenList, self.arrayProb, self.countFile)
        self.countFile+=1

if __name__=="__main__":
    window = mapaWin()
    Gtk.main()