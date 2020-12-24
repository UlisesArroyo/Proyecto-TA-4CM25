import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import os, sys, subprocess
from PIL import Image, ImageTk


raiz = Tk()  #ventana

raiz.title("Ventana de pruebas")
raiz.config(bg = "orange")

miframe = Frame(raiz)
miframe.pack(fill="both",expand ="True")
miframe.config(bg = "black")
miframe.config(width = "1280",height = "720")

#Ejemplo
img3 = Image.open("C:/Users/HP/Desktop/Pruebas/img/1CV12_12_R_#89_003809.jpg") 
img3 = img3.resize((320, 240), Image.ANTIALIAS)
img3 = ImageTk.PhotoImage(image=img3)
Imagen3 = Label(miframe, image=img3)
Imagen3.pack(side="bottom", fill="both", expand="yes")
Imagen3.place(x=740,y=200)



def abrir_carpeta():
	
	abrir_e=1
	print(str(abrir_e))
	archivo_abierto = filedialog.askdirectory(initialdir="/", title="Select file")               
	#print ("archivo abierto: " + archivo_abierto)
	print(archivo_abierto)	
	lista1 = os.listdir(archivo_abierto)	
	print(lista1)
	print(len(lista1))
	

	rutas=[]

	for n in range(len(lista1)):
		rutas.append(archivo_abierto+"/"+lista1[n])

	

	print("Las rutas de las imagenes " ,rutas)

	openimg(rutas)

	
	
	
	





def openimg(ruta):
	
	imagen = Image.open(ruta[3])
	imagen = imagen.resize((320, 240), Image.ANTIALIAS)   #con esta madre hacemos mas chicas las imagenes de los costados para que se vea mamalon
	imagen = ImageTk.PhotoImage(image=imagen)          
	Imagen1 = Label(miframe, image=imagen)
	Imagen1.pack(side="bottom", fill="both", expand="yes")
	Imagen1.place(x=100,y=200)
    
	'''
	img2 = Image.open(ruta[1]) 
	img2 = img2.resize((320, 240), Image.ANTIALIAS)
	img2 = ImageTk.PhotoImage(image=img2)         #Esta madre debe aparecer mas grande ya que sera la central
	Imagen2 = Label(miframe, image=img2)
	Imagen2.pack(side="bottom", fill="both", expand="yes")
	Imagen2.place(x=420,y=200)

	img3 = Image.open(ruta[2]) 
	img3 = img3.resize((320, 240), Image.ANTIALIAS)
	img3 = ImageTk.PhotoImage(image=img3)
	Imagen3 = Label(miframe, image=img3)
	Imagen3.pack(side="bottom", fill="both", expand="yes")
	Imagen3.place(x=740,y=200)
	'''



	print("es la ruta 1",ruta[0])
	print("es la ruta 2",ruta[1])

    





boton5 = Button(raiz, text ="        Abrir (Imagenes)   ", font=(18),fg="black", command=abrir_carpeta).place(x=515,y=600)	
Label(miframe, button=boton5,height=50, width = 150)



	
		

raiz.mainloop()