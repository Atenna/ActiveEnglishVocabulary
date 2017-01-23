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

def openMenu(wordClass):
    if(wordClass == "noun"):
        print ""


mMenuBar = Menu(top)

# Learn menu: Nouns, Verbs, Adjectives, Adverbs
mLearnMenu = Menu(mMenuBar, tearoff=0)
mLearnMenu.add_command(label="Nouns", command=openMenu("noun"))
mLearnMenu.add_command(label="Verbs", command=openMenu("verb"))
mLearnMenu.add_command(label="Adjectives", command=openMenu("adjective"))
mLearnMenu.add_command(label="Adverbs", command=openMenu("adverb"))
mLearnMenu.add_command(label="Others", command=openMenu("others"))

# About menu: About, Code
mAboutMenu = Menu(mMenuBar, tearoff=0)
mAboutMenu.add_command(label="About", command=openMenu("about"))
mAboutMenu.add_command(label="Code", command=openMenu("code"))

# Add options to the menu bar
mMenuBar.add_cascade(label="Learn", menu=mLearnMenu)
mMenuBar.add_cascade(label="About", menu=mAboutMenu)

# Create treeview with sample data
tTable = ttk.Treeview(top)
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
top.mainloop()