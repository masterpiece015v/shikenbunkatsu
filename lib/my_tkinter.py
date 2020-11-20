import tkinter
from tkinter import ttk
from tkinter import filedialog
from tkinter import StringVar
from tkinter import messagebox
import threading

class MyWin(tkinter.Tk):
    def __init__(self,title,geometry):
        self.title(title)
        self.geometry(geometry)

class MyFrame(ttk.Frame):
    def __init__(self,win):
        super(win)

