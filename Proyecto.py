import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox


raiz = Tk()

raiz.title("Ventana de pruebas")
raiz.config(bg = "orange")

miframe = Frame(raiz)
miframe.pack(fill="both",expand ="True")
miframe.config(bg = "orange")
miframe.config(width = "1280",height = "720")


raiz.mainloop()