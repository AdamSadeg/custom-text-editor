from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from filetab import FileTab
import json
import os
import sys

class App(Tk):
    tabs_open = []
    current_tab = None
    filetypes = {
        '.py' : "./color/python.json",
        '.pyw' : "./color/python.json"
    }

    def __init__(self, w, h):
        super().__init__()
        
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.geometry(f"{w}x{h}")

        self.createTabSystem()
        self.createMenuBar()

    def createMenuBar(self):
        self.menubar = Menu(self)

        self.filemenu = Menu(self.menubar)
        self.filemenu.add_command(label="New",  command="")
        self.filemenu.add_command(label="Open", command=self.on_openFile)
        self.filemenu.add_command(label="Exit", command="")

        self.debugmenu = Menu(self.menubar)
        self.debugmenu.add_command(label="Print Tabs", command=self.printTabs)

        self.menubar.add_cascade(label="Debug", menu=self.debugmenu)
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        self.config(menu=self.menubar)
    
    def createTabSystem(self):
        self.tabcontrol = ttk.Notebook(self)
        self.tabcontrol.pack()

    def printTabs(self):
        print(self.tabs_open)

    def getCurrentTabClass(self):
        current_tab = self.tabcontrol.index('current')
        
        for i in range(len(self.tabs_open)):
            if self.tabs_open[i][1] == current_tab:
                return self.tabs_open[i]

    def newTab(self):
        tab = FileTab(self.tabcontrol)
        entrywidget = Text(tab)
        tab.textwidget = entrywidget
        self.tabs_open.append((tab, len(self.tabs_open)))
        return tab, entrywidget

    def on_openFile(self):
        f = filedialog.askopenfilename(initialdir="/Desktop", title="select file")
        if f == None: return
        
        filename, file_extension = os.path.splitext(f)
        jsonpath = None

        for filetype in self.filetypes:
            print((filetype, file_extension))
            if file_extension == filetype:
                print("Fount a file match")
                jsonpath = self.filetypes[file_extension]

        # read the data from the file
        data = open(f, 'r').read()

        # create a new tab and entry widget
        tab, textwidget = self.newTab()
        scroll = Scrollbar(tab, orient='vertical', command=textwidget.yview)

        # put the data inside the text widget,
        # for editing
        textwidget.configure(yscrollcommand=scroll.set)
        textwidget.insert(INSERT, data)
        textwidget.insert(END, "\n")

        if jsonpath != None:
            print("Color json is not equal to none!")
            colorjson = open(jsonpath, 'r')
            colordata = json.load(colorjson)
            for i in colordata:
                textwidget.tag_config(i, background="white", foreground=colordata[i])

        textwidget.pack(expand=1, fill=BOTH)
        scroll.pack()
        
        # finally, add the tab to the screen
        self.tabcontrol.add(tab, text=filename)

def getSavedScreenSize():
    settings_file = open('settings.json')
    screen_data = json.load(settings_file)['screen'][0]
    x = screen_data['w']
    y = screen_data['h']
    return x, y


if __name__ == '__main__':
    x, y = getSavedScreenSize()
    app = App(x, y)
    app.mainloop()
