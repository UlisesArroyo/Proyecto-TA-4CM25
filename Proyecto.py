import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import os, sys, subprocess
from PIL import Image, ImageTk

i=0
x=0
rutas =[]


raiz = Tk()  #ventana

raiz.title("Ventana de pruebas")
raiz.config(bg = "orange")
ruta_1= "img/mi_amor_1.jpg"
ruta_2= "img/mi_amor_2.jpg"
ruta_3= "img/mi_amor_3.jpg"
miframe = Frame(raiz)
miframe.pack(fill="both",expand ="True")
miframe.config(bg = "black")
miframe.config(width = "1280",height = "720")





def abrir_carpeta():
	global rutas,x

	
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

	
	img = Image.open(rutas[i-1]) 
	img = img.resize((320, 240), Image.ANTIALIAS) 
	img = ImageTk.PhotoImage(image=img)
	Imagen1.configure(image=img)
	Imagen1.image = img

	img = Image.open(rutas[i])  
	img = img.resize((320, 240), Image.ANTIALIAS) 
	img = ImageTk.PhotoImage(image=img)
	Imagen2.configure(image=img)
	Imagen2.image = img	

	img = Image.open(rutas[i+1])  
	img = img.resize((320, 240), Image.ANTIALIAS) 
	img = ImageTk.PhotoImage(image=img)
	Imagen3.configure(image=img)
	Imagen3.image = img
	
	x=1	#Activa el next y last

	

	#print("Las rutas de las imagenes " ,rutas)

	

def Next():
	global x,i,rutas
	if x > 0 and i < len(rutas) :
		i = i+1
		i = i%len(rutas)
		


		img = Image.open(rutas[i-1]) 
		img = img.resize((320, 240), Image.ANTIALIAS) 
		img = ImageTk.PhotoImage(image=img)
		Imagen1.configure(image=img)
		Imagen1.image = img

		img = Image.open(rutas[i])  
		img = img.resize((320, 240), Image.ANTIALIAS) 
		img = ImageTk.PhotoImage(image=img)
		Imagen2.configure(image=img)
		Imagen2.image = img	

		if(i == len(rutas)-1):
			img = Image.open(rutas[0])  
			img = img.resize((320, 240), Image.ANTIALIAS) 
			img = ImageTk.PhotoImage(image=img)
			Imagen3.configure(image=img)
			Imagen3.image = img	
		else:
			img = Image.open(rutas[i+1])  
			img = img.resize((320, 240), Image.ANTIALIAS) 
			img = ImageTk.PhotoImage(image=img)
			Imagen3.configure(image=img)
			Imagen3.image = img		

	


def Last():
	global x,i,rutas
	if x > 0 and i >= 0:
		i = i-1
		if(i<0):
			i=i+len(rutas)
		img = Image.open(rutas[i-1]) 
		img = img.resize((320, 240), Image.ANTIALIAS) 
		img = ImageTk.PhotoImage(image=img)
		Imagen1.configure(image=img)
		Imagen1.image = img

		img = Image.open(rutas[i])  
		img = img.resize((320, 240), Image.ANTIALIAS) 
		img = ImageTk.PhotoImage(image=img)
		Imagen2.configure(image=img)
		Imagen2.image = img	

		if(i==len(rutas)-1):
			img = Image.open(rutas[0])  
			img = img.resize((320, 240), Image.ANTIALIAS) 
			img = ImageTk.PhotoImage(image=img)
			Imagen3.configure(image=img)
			Imagen3.image = img		
		else:
			img = Image.open(rutas[i+1])  
			img = img.resize((320, 240), Image.ANTIALIAS) 
			img = ImageTk.PhotoImage(image=img)
			Imagen3.configure(image=img)
			Imagen3.image = img	


def Seleccionar():
	print("ala chaval")

Next()
Last()
	
	





	
imagen = Image.open(ruta_1)
imagen = imagen.resize((320, 240), Image.ANTIALIAS)   #con esta madre hacemos mas chicas las imagenes de los costados para que se vea mamalon
imagen = ImageTk.PhotoImage(image=imagen) 
img2 = Image.open(ruta_2) 
img2 = img2.resize((320, 240), Image.ANTIALIAS)
img2 = ImageTk.PhotoImage(image=img2) 
img3 = Image.open(ruta_3) 
img3 = img3.resize((320, 240), Image.ANTIALIAS)
img3 = ImageTk.PhotoImage(image=img3)
	

Imagen1 = Label(miframe, image=imagen)
Imagen1.pack(side="bottom", fill="both", expand="yes")
Imagen1.place(x=100,y=200)
    

#Esta madre debe aparecer mas grande ya que sera la central
Imagen2 = Label(miframe, image=img2)
Imagen2.pack(side="bottom", fill="both", expand="yes")
Imagen2.place(x=420,y=200)

Imagen3 = Label(miframe, image=img3)
Imagen3.pack(side="bottom", fill="both", expand="yes")
Imagen3.place(x=740,y=200)





    




boton4 = Button(raiz, text ="            Anterior           ", font=(18),fg="blue", command = Last).place(x=250,y=600)	
Label(miframe, button=boton4,height=50, width = 150)
boton5 = Button(raiz, text ="        Abrir (Imagenes)   ", font=(18),fg="black", command=abrir_carpeta).place(x=515,y=600)	
Label(miframe, button=boton5,height=50, width = 150)
boton6 = Button(raiz, text ="            Siguiente            ", font=(18),fg="blue", command = Next).place(x=800,y=600)	
Label(miframe, button=boton6,height=50, width = 150)

boton7 = Button(raiz, text ="    Seleccionar    ", font=(18),fg="GREEN", command = Seleccionar).place(x=540,y=650)
Label(miframe, button=boton6,height=50, width = 150)






def boton_p(event):
	
	bp= event.keysym
	if bp =="Right":
		Next()
	elif bp == "Left":
		Last()
	elif bp == "Q" or bp == "q":
		Seleccionar()
	'''
	elif bp == "W" or bp == "w":
		chos()
	elif bp == "E" or bp == "e":
		manos()
	elif bp == "R" or bp == "r":
		MANO()				
	elif bp == "B" or bp == "b":	
		BORRAR()
	'''	




raiz.bind("<Key>", boton_p)
	
		

raiz.mainloop()