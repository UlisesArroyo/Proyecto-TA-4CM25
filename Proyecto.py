import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import os, sys, subprocess

raiz = Tk()

raiz.title("Ventana de pruebas")
raiz.config(bg = "orange")

miframe = Frame(raiz)
miframe.pack(fill="both",expand ="True")
miframe.config(bg = "orange")
miframe.config(width = "1280",height = "720")


def abrir_carpeta():
	abrir_e=1
	print(str(abrir_e))
	archivo_abierto = filedialog.askdirectory(initialdir="/", title="Select file")               
	#print ("archivo abierto: " + archivo_abierto)
	print(archivo_abierto)	
	lista1 = os.listdir(archivo_abierto)	
	print(lista1)
	print(len(lista1))

boton5 = Button(raiz, text ="            Abrir (Imagenes)   ", font=(18),fg="black", command=abrir_carpeta).place(x=515,y=600)	
Label(miframe, button=boton5,height=50, width = 150)


raiz.mainloop()