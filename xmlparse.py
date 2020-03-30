import xml.etree.ElementTree as ET
import subprocess
import os
from PIL import Image
from PIL import ImageEnhance
import tkinter
from tkinter import ttk
from tkinter import filedialog
from tkinter import StringVar
from tkinter import messagebox
import threading

tree = ET.parse('style.xml')

root = tree.getroot()

# メインウィンドウ
main_win = tkinter.Tk()
main_win.title(root.attrib['title'])
main_win.geometry(root.attrib['geometry'])

for child1 in root:
    print( child1.tag )
    frame = ttk.Frame(main_win)
    for child2 in child1:
        print( child2.tag )
        if child2.tag == 'label':
            view = ttk.Label(frame,text=child2.text)
            view.place(x=5,y=5,width=int(child2.attrib['width']),height=int(child2.attrib['height']) )
        elif child2.tag == 'entry':
            view = ttk.Entry(frame)
            view.place(x=5,y=5,width=child2.attrib['width'])
        elif child2.tag == 'button':
            view = ttk.Button(frame,text=child2.text)
            view.place(x=5,y=5,width=child2.attrib['width'])

main_win.mainloop()