from numpy.lib.function_base import select
import sys
import json
import re
import hyperlink_manager
import webbrowser
import ttk
from Tkinter import *

top = Tk()
top.wm_title("Active English Vocabulary")

frames = {}

### Frame setup ###

fIntroFrame = Frame(top)
fNounFrame = Frame(top)
fVerbFrame = Frame(top)
fAdverbFrame = Frame(top)
fAdjectiveFrame = Frame(top)
fOthersFrame = Frame(top)
fAboutFrame = Frame(top)
fCodeFrame = Frame(top)

Button(fNounFrame, text='Go to frame 2', command=lambda:openTab("verb")).pack()
Label(fNounFrame, text='FRAME 1').pack()

Button(fVerbFrame, text='Go to frame 1', command=lambda:openTab("noun")).pack()
Label(fVerbFrame, text='FRAME 2').pack()

frames["noun"] = fNounFrame
frames["verb"] = fVerbFrame
frames["adverb"] = fAdverbFrame
frames["adjective"] = fAdjectiveFrame
frames["others"] = fOthersFrame
frames["about"] = fAboutFrame
frames["code"]= fCodeFrame

for f in (fIntroFrame,fNounFrame,fVerbFrame,fAdverbFrame,fAdjectiveFrame,fOthersFrame,fAboutFrame,fCodeFrame):
    f.grid(row=0, column=0, sticky='news')

def openTab(frameName):
    frame = frames[frameName]
    frame.tkraise()

### Menu setup ###

mMenuBar = Menu(top)

# Learn menu: Nouns, Verbs, Adjectives, Adverbs
mLearnMenu = Menu(mMenuBar, tearoff=0)
mLearnMenu.add_command(label="Nouns", command=openTab("noun"))
mLearnMenu.add_command(label="Verbs", command=openTab("verb"))
mLearnMenu.add_command(label="Adjectives", command=openTab("adjective"))
mLearnMenu.add_command(label="Adverbs", command=openTab("adverb"))
mLearnMenu.add_command(label="Others", command=openTab("others"))

# About menu: About, Code
mAboutMenu = Menu(mMenuBar, tearoff=0)
mAboutMenu.add_command(label="About", command=openTab("about"))
mAboutMenu.add_command(label="Code", command=openTab("code"))

# Add options to the menu bar
mMenuBar.add_cascade(label="Learn", menu=mLearnMenu)
mMenuBar.add_cascade(label="About", menu=mAboutMenu)

### Table setup ###
class Table:

    def __init__(self, word_tag):
        words = self.loadWords(word_tag)

    def loadWords(self, word_tag):
        file = open(word_tag+".txt", "r");
        words = {}
        for line in file:
            pair = line.split(',')
            words[pair[0]] = pair[1]


# Create treeview with sample data
tTable = ttk.Treeview(fAboutFrame)
tTable['columns'] = ('word', 'translation')
tTable.column('#0', width=0, minwidth=0)
tTable.heading('word', text='Word')
tTable.column('word', anchor='center')
tTable.heading('translation', text='Translation')
tTable.column('translation', anchor='center')

# Issue: This approach does not support scrolling
tTable.insert('', 'end', values=('A B'))
tTable.insert('', 'end', values=('A D'))
tTable.insert('', 'end', values=('C B'))
tTable.insert('', 'end', values=('A B'))
tTable.insert('', 'end', values=('A D'))
tTable.insert('', 'end', values=('C B'))
tTable.insert('', 'end', values=('A B'))
tTable.insert('', 'end', values=('A D'))
tTable.insert('', 'end', values=('C B'))

top.config(menu=mMenuBar)
tTable.pack(side='top')
#openTab("noun")
top.mainloop()