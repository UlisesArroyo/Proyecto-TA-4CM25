import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import os, sys, subprocess
from PIL import Image, ImageTk
import shutil

#

posicionImagen=0
carpetaAbierta=False
rutas =[]
listaGenerada = []

anchoImagenSeleccion = 320;
altoImagenSeleccion = 240;


anchoImagenAdyacente = 120;
altoImagenAdyacente = 90;


raiz = Tk()  #ventana

nombreCarpeta = tk.StringVar()

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
	global rutas,carpetaAbierta
	abrir_e=1
	print(str(abrir_e))
	archivo_abierto = filedialog.askdirectory(initialdir="./", title="Select file")               	
	if(len(archivo_abierto) != 0):
		print(archivo_abierto)
		lista1 = os.listdir(archivo_abierto)	
		print(lista1)
		print(len(lista1))
		rutas=[]

		for n in range(len(lista1)):
			rutas.append(archivo_abierto+"/"+lista1[n])

		
		img = Image.open(rutas[posicionImagen-1]) 
		img = img.resize((anchoImagenAdyacente, altoImagenAdyacente), Image.ANTIALIAS) 
		img = ImageTk.PhotoImage(image=img)
		Imagen1.configure(image=img)
		Imagen1.image = img

		img = Image.open(rutas[posicionImagen])  
		img = img.resize((anchoImagenSeleccion, altoImagenSeleccion), Image.ANTIALIAS) 
		img = ImageTk.PhotoImage(image=img)
		Imagen2.configure(image=img)
		Imagen2.image = img	

		img = Image.open(rutas[posicionImagen+1])  
		img = img.resize((anchoImagenAdyacente, altoImagenAdyacente), Image.ANTIALIAS) 
		img = ImageTk.PhotoImage(image=img)
		Imagen3.configure(image=img)
		Imagen3.image = img
		
		carpetaAbierta = True	#Activa el next y last


	

def Next():
	global posicionImagen
	if carpetaAbierta and posicionImagen < len(rutas) :
		posicionImagen += 1
		posicionImagen %= len(rutas)
		


		img = Image.open(rutas[posicionImagen-1]) 
		img = img.resize((anchoImagenAdyacente, altoImagenAdyacente), Image.ANTIALIAS) 
		img = ImageTk.PhotoImage(image=img)
		Imagen1.configure(image=img)
		Imagen1.image = img

		img = Image.open(rutas[posicionImagen])  
		img = img.resize((anchoImagenSeleccion, altoImagenSeleccion), Image.ANTIALIAS) 
		img = ImageTk.PhotoImage(image=img)
		Imagen2.configure(image=img)
		Imagen2.image = img	

		if(posicionImagen == len(rutas)-1):
			img = Image.open(rutas[0])  
			img = img.resize((anchoImagenAdyacente, altoImagenAdyacente), Image.ANTIALIAS) 
			img = ImageTk.PhotoImage(image=img)
			Imagen3.configure(image=img)
			Imagen3.image = img	
		else:
			img = Image.open(rutas[posicionImagen+1])  
			img = img.resize((anchoImagenAdyacente, altoImagenAdyacente), Image.ANTIALIAS) 
			img = ImageTk.PhotoImage(image=img)
			Imagen3.configure(image=img)
			Imagen3.image = img		

	


def Last():
	global posicionImagen
	if (carpetaAbierta and posicionImagen >= 0):
		posicionImagen -= 1
		if(posicionImagen<0):
			posicionImagen += len(rutas)
		img = Image.open(rutas[posicionImagen-1]) 
		img = img.resize((anchoImagenAdyacente, altoImagenAdyacente), Image.ANTIALIAS) 
		img = ImageTk.PhotoImage(image=img)
		Imagen1.configure(image=img)
		Imagen1.image = img

		img = Image.open(rutas[posicionImagen])  
		img = img.resize((anchoImagenSeleccion, altoImagenSeleccion), Image.ANTIALIAS) 
		img = ImageTk.PhotoImage(image=img)
		Imagen2.configure(image=img)
		Imagen2.image = img	

		if(posicionImagen==len(rutas)-1):
			img = Image.open(rutas[0])  
			img = img.resize((anchoImagenAdyacente, altoImagenAdyacente), Image.ANTIALIAS) 
			img = ImageTk.PhotoImage(image=img)
			Imagen3.configure(image=img)
			Imagen3.image = img		
		else:
			img = Image.open(rutas[posicionImagen+1])  
			img = img.resize((anchoImagenAdyacente, altoImagenAdyacente), Image.ANTIALIAS) 
			img = ImageTk.PhotoImage(image=img)
			Imagen3.configure(image=img)
			Imagen3.image = img	


def Seleccionar():
	if(carpetaAbierta):
		if(comparador(listaGenerada,rutas[posicionImagen]) == True):
			print("listaGenerada (old): " , listaGenerada)
			listaGenerada.append(rutas[posicionImagen])
			ordenar_quicksort(listaGenerada,0,len(listaGenerada)-1)
			print("Elemento agregado: " + rutas[posicionImagen])
			print("listaGenerada (new): " , listaGenerada)
		else: 
			messagebox.showinfo(message="La imagen ya se encuentra en esta Lista", title="Error")
	

def comparador(lista,elemento):
	for m in range(len(lista)):
		if(elemento == lista[m]):
			return False
	return True 


def generarCarpeta():
	global nombreCarpeta
	if(len(listaGenerada) > 0):
		print("ala chaval")
		ventana2 = tk.Toplevel()
		ventana2.geometry("380x300+200+100")
		ventana2.configure(background = "dark turquoise")
		mensaje1 =Label(ventana2,text="Ingrese nombre de la carpeta").place(x=50,y=30)
		nomCarp =Entry(ventana2, textvariable=nombreCarpeta).place(x=100, y=60)
		boton4 = Button(ventana2, text ="OK", font=(18),fg="blue", command = lambda: desVen(ventana2)).place(x=50,y=60)		
		Label(ventana2, button=boton4,height=50, width = 150)
		

def desVen(ventana2):
	global listaGenerada	
	ventana2.destroy()
	print("nombreCarpeta: " +    nombreCarpeta.get())
	os.mkdir(nombreCarpeta.get())
	for imagen in listaGenerada:
		direccion,nombre = os.path.split(imagen)
		shutil.copy(imagen, nombreCarpeta.get() + "/"+nombre)
	listaGenerada = []	



	



def ordenar_quicksort(lista,izq,der):
	
	pivote = lista[izq]		
	i = izq					
	j = der					
	aux = 0					

	while i < j:								

		while lista[i] <= pivote and i < j:	
			i += 1								

		while lista[j] > pivote:			
			j -= 1								

		if i < j:								
			aux = lista[i]					
			lista[i] = lista[j]				
			lista[j] = aux					

	lista[izq] = lista[j]					
	lista[j] = pivote							

	if izq < j-1:								
		ordenar_quicksort(lista,izq,j-1)				

	if j+1 < der:								 
		ordenar_quicksort(lista,j+1,der)



	
	





	
imagen = Image.open(ruta_1)
imagen = imagen.resize((anchoImagenAdyacente, altoImagenAdyacente), Image.ANTIALIAS)   #con esta madre hacemos mas chicas las imagenes de los costados para que se vea mamalon
imagen = ImageTk.PhotoImage(image=imagen) 
img2 = Image.open(ruta_2) 
img2 = img2.resize((anchoImagenSeleccion, altoImagenSeleccion), Image.ANTIALIAS)
img2 = ImageTk.PhotoImage(image=img2) 
img3 = Image.open(ruta_3) 
img3 = img3.resize((anchoImagenAdyacente, altoImagenAdyacente), Image.ANTIALIAS)
img3 = ImageTk.PhotoImage(image=img3)
	

Imagen1 = Label(miframe, image=imagen)
Imagen1.pack(side="bottom", fill="both", expand="yes")
Imagen1.place(x=390-(anchoImagenSeleccion/2),y=200+(altoImagenSeleccion/4))
    

#Esta madre debe aparecer mas grande ya que sera la central
Imagen2 = Label(miframe, image=img2)
Imagen2.pack(side="bottom", fill="both", expand="yes")
Imagen2.place(x=420,y=200)

Imagen3 = Label(miframe, image=img3)
Imagen3.pack(side="bottom", fill="both", expand="yes")
Imagen3.place(x=740+(anchoImagenSeleccion/4),y=200+(altoImagenSeleccion/4))





    


boton4 = Button(raiz, text ="            Anterior           ", font=(18),fg="blue", command = Last).place(x=250,y=600)	
Label(miframe, button=boton4,height=50, width = 150)
boton5 = Button(raiz, text ="        Abrir (Imagenes)   ", font=(18),fg="black", command=abrir_carpeta).place(x=515,y=600)	
Label(miframe, button=boton5,height=50, width = 150)
boton6 = Button(raiz, text ="            Siguiente            ", font=(18),fg="blue", command = Next).place(x=800,y=600)	
Label(miframe, button=boton6,height=50, width = 150)

boton7 = Button(raiz, text ="    Seleccionar    ", font=(18),fg="GREEN", command = Seleccionar).place(x=540,y=650)
Label(miframe, button=boton6,height=50, width = 150)

boton8 = Button(raiz, text ="     Crear Carpeta     ", font=(18),fg="orange", command = generarCarpeta).place(x=1050,y=650)
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