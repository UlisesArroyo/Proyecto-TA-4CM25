import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import os, sys, subprocess
from PIL import Image, ImageTk
import shutil
import random
from os import path
import cv2

posicionImagen=0
carpetaAbierta=False
rutasImagenes =[]
listaGenerada = []
categorias = ["Clinico", "Clinico_(valvula)", "Tela", "Convencional", "Sin_cubrebocas", "Otros"]
lineas = [*categorias]
# Datos de la lista: Tienen que separarse con una " , "
datosLista = ["Nombre", "UbicacionArchivo", "Categorias", "Dimensiones", "Tipo de archivo", "Numero de personas[Plural Singular]", "Comentarios"]

anchoImagenSeleccion = 320;
altoImagenSeleccion = 240;
anchoImagenAdyacente = 120;
altoImagenAdyacente = 90;

raiz = Tk()  #ventana
nombreCarpeta = tk.StringVar()
miframe = Frame(raiz)
miframe.pack(fill="both",expand ="True")
miframe.config(bg = "black")
miframe.config(width = "1280",height = "720")

ruta_1= "img/1.png"
ruta_2= "img/1.png"
ruta_3= "img/1.png"
imgBotonIzquierda= PhotoImage(file = "back/izq.png")
imgBotonDerecha= PhotoImage(file = "back/der.png")
imgBotonAbrir= PhotoImage(file = "back/abr.png")
imgBotonSeleccion= PhotoImage(file = "back/sel.png")
imgBotonCarpeta= PhotoImage(file = "back/car.png")
imgRandom = str(random.randint(1,5))
imgFondo = PhotoImage(file = "back/f"+imgRandom+".png")
lblFondo = Label(miframe,image=imgFondo).place(x=0,y=0)



def buscarFicherosEnDirectorios(direccion):
	imagenes = []
	lista = os.listdir(direccion)
	#print(direccion,"\n")
	#print(lista,"\n")
	for fichero in lista:
		#print(fichero)
		if os.path.isdir(direccion + "/" + fichero):
			nuevaDireccion = direccion + fichero + "/"
			#print(nuevaDireccion)
			imagenes += (buscarFicherosEnDirectorios(nuevaDireccion))
		if os.path.isfile(direccion + "/" + fichero):
			imagenes.append(direccion + fichero)
	return imagenes		

def confirmarListas():
	global lineas
	try:
		os.stat("./Listas")
	except OSError as e:
		os.mkdir("./Listas")	
	x = 0
	for categoria in categorias:
		lista = "./Listas/" + categoria + ".txt"
		if os.path.exists(lista):
			
			fichero = open(lista,"r")
			lineas[x] = [fichero.readlines()]
			fichero.close()
			if len(lineas[x]) != 0:
				print(lineas[x][0][0])
				print(categoria)
				if str(categoria + "\n")  != lineas[x][0][0]:
					print("ENTRO")
					lineas[x].insert(0,categoria +"\n")
					fichero = open(lista,"w")
					print("AAA",lineas[x])
					for c in lineas[x]:
						print("==>",c)
						print(type(c))
						fichero.write(c)
					fichero.close()
			else:
				fichero = open(lista,"a+")
				fichero.write(categoria +"\n")
				fichero.close			
		else:
			fichero = open(lista,"a+")
			fichero.write(categoria +"\n")
			fichero.close
		x += 1	

def abrir_carpeta():
	global rutasImagenes,carpetaAbierta, posicionImagen
	posicionImagen = 0
	archivo_abierto = filedialog.askdirectory(initialdir="./", title="Select file")               	
	if(len(archivo_abierto) != 0):
		archivo_abierto += "/"
		rutasImagenes = buscarFicherosEnDirectorios(archivo_abierto)	
		confirmarListas()

		img = Image.open(rutasImagenes[posicionImagen-1]) 
		img = img.resize((anchoImagenAdyacente, altoImagenAdyacente), Image.ANTIALIAS) 
		img = ImageTk.PhotoImage(image=img)
		Imagen1.configure(image=img)
		Imagen1.image = img

		img = Image.open(rutasImagenes[posicionImagen])  
		img = img.resize((anchoImagenSeleccion, altoImagenSeleccion), Image.ANTIALIAS) 
		img = ImageTk.PhotoImage(image=img)
		Imagen2.configure(image=img)
		Imagen2.image = img	

		img = Image.open(rutasImagenes[posicionImagen+1])  
		img = img.resize((anchoImagenAdyacente, altoImagenAdyacente), Image.ANTIALIAS) 
		img = ImageTk.PhotoImage(image=img)
		Imagen3.configure(image=img)
		Imagen3.image = img
		
		carpetaAbierta = True	#Activa el Next, Last y los botones de selección


	

def Next():
	global posicionImagen
	if carpetaAbierta and posicionImagen < len(rutasImagenes) :
		posicionImagen += 1
		posicionImagen %= len(rutasImagenes)
		
		img = Image.open(rutasImagenes[posicionImagen-1]) 
		img = img.resize((anchoImagenAdyacente, altoImagenAdyacente), Image.ANTIALIAS) 
		img = ImageTk.PhotoImage(image=img)
		Imagen1.configure(image=img)
		Imagen1.image = img

		img = Image.open(rutasImagenes[posicionImagen])  
		img = img.resize((anchoImagenSeleccion, altoImagenSeleccion), Image.ANTIALIAS) 
		img = ImageTk.PhotoImage(image=img)
		Imagen2.configure(image=img)
		Imagen2.image = img	

		if(posicionImagen == len(rutasImagenes)-1):
			img = Image.open(rutasImagenes[0])  
			img = img.resize((anchoImagenAdyacente, altoImagenAdyacente), Image.ANTIALIAS) 
			img = ImageTk.PhotoImage(image=img)
			Imagen3.configure(image=img)
			Imagen3.image = img	
		else:
			img = Image.open(rutasImagenes[posicionImagen+1])  
			img = img.resize((anchoImagenAdyacente, altoImagenAdyacente), Image.ANTIALIAS) 
			img = ImageTk.PhotoImage(image=img)
			Imagen3.configure(image=img)
			Imagen3.image = img		

	


def Last():
	global posicionImagen
	if (carpetaAbierta and posicionImagen >= 0):
		posicionImagen -= 1
		if(posicionImagen<0):
			posicionImagen += len(rutasImagenes)
		img = Image.open(rutasImagenes[posicionImagen-1]) 
		img = img.resize((anchoImagenAdyacente, altoImagenAdyacente), Image.ANTIALIAS) 
		img = ImageTk.PhotoImage(image=img)
		Imagen1.configure(image=img)
		Imagen1.image = img

		img = Image.open(rutasImagenes[posicionImagen])  
		img = img.resize((anchoImagenSeleccion, altoImagenSeleccion), Image.ANTIALIAS) 
		img = ImageTk.PhotoImage(image=img)
		Imagen2.configure(image=img)
		Imagen2.image = img	

		if(posicionImagen==len(rutasImagenes)-1):
			img = Image.open(rutasImagenes[0])  
			img = img.resize((anchoImagenAdyacente, altoImagenAdyacente), Image.ANTIALIAS) 
			img = ImageTk.PhotoImage(image=img)
			Imagen3.configure(image=img)
			Imagen3.image = img		
		else:
			img = Image.open(rutasImagenes[posicionImagen+1])  
			img = img.resize((anchoImagenAdyacente, altoImagenAdyacente), Image.ANTIALIAS) 
			img = ImageTk.PhotoImage(image=img)
			Imagen3.configure(image=img)
			Imagen3.image = img	


def Seleccionar(categoriaSeleccionada):
	if(carpetaAbierta):
		ImagenNueva, listaRepetida,ubicacionImagenRepetida = comparador(rutasImagenes[posicionImagen])
		if ImagenNueva:
			fichero = open("./Listas/" + categorias[categoriaSeleccionada] + ".txt","a")
			print("./Listas/" + categorias[categoriaSeleccionada] + ".txt")
			nombre, ubicacion, dimensiones, extension = recopilacionInformacion(rutasImagenes[posicionImagen])
			fichero.write(nombre + "," + ubicacion + "," + dimensiones + "," + extension +"\n")#Funcion ingreso de datos
			fichero.close()

		else: 
			if listaRepetida == categoriaSeleccionada:
				messagebox.showinfo(message="La imagen ya se encuentra en esta Lista (" + categorias[categoriaSeleccionada]+")", title="Error")
			else:
				MsgBox = messagebox.askokcancel(title="Error Imagen repetida", message="Desea cambiar la imagen de " + categorias[listaRepetida] + " a " + categorias[categoriaSeleccionada])
				if (MsgBox == 1):
					fichero = open("./Listas/" + categorias[listaRepetida] + ".txt","r")
					lines = fichero.readlines()
					fichero.close()
					fichero = open("./Listas/" + categorias[listaRepetida] + ".txt","w")
					line=0
					for line in range (len(lines)):
						if(line != ubicacionImagenRepetida):
							izq = lines[line].find(",") + 1
							der = lines[line][izq:].find(",") + izq
							ubicacion = lines[line][izq:der]
							print("PRUEBA DE FUEGO->",ubicacion)
							nombre, ubicacion, dimensiones, extension = recopilacionInformacion(ubicacion)
							fichero.write(lines[line])
					fichero.close()				
					fichero = open("./Listas/" + categorias[categoriaSeleccionada] + ".txt","a")
					nombre, ubicacion, dimensiones, extension = recopilacionInformacion(rutasImagenes[posicionImagen])
					fichero.write(nombre + "," + ubicacion + "," + dimensiones + "," + extension +"\n")#Funcion ingreso de datos
					fichero.close()	

def recopilacionInformacion(ubicacion):

	rutaNombre = os.path.split(ubicacion)
	nombre = rutaNombre[1]
	rutaExtension = os.path.splitext(ubicacion)
	extension = rutaExtension[1]
	imagen = cv2.imread(ubicacion,0)
	alto, ancho = imagen.shape[:2]
	dimensiones = str(alto) + "x" + str(ancho)
	#numeroPersonas = True
	#comentarios = ""
	return nombre, ubicacion, dimensiones, extension #Falta numeroPersonas y comentarios



class Imagen:
	def __init__(self, nombre, ubicacion, dimensiones, tipoArchivo, numeroPersonas, comentarios):
		self.nombre
		self.ubicacion
		self.dimensiones
		self.tipoArchivo
		self.numeroPersonas
		self.comentarios


def comparador(imagen):
	global lineas
	x = 0
	for categoria in categorias:	
		fichero = open("./Listas/" + categoria + ".txt","r")
		lineas[x] = [fichero.readlines()]
		print("XXX",lineas[x])
		fichero.close()
		x += 1

	for categoria in range(len(categorias)):
		print("--->",lineas[categoria])
		print("777:", len(lineas[categoria]) - 1)
		for linea in range(len(lineas[categoria][0]) - 1):
			mensaje = imagen
			mensaje = mensaje[0 : len(mensaje)]
			izq = lineas[categoria][0][linea + 1].find(",") + 1
			der = lineas[categoria][0][linea + 1][izq:].find(",") + izq
			ubicacion = lineas[categoria][0][linea + 1][izq:der]
			print("ENTRO")
			print(ubicacion)
			print(mensaje)
			if (mensaje) == ubicacion:
				return False, categoria, (linea + 1)


	print("Toda la info: ",lineas)
	return True, 0, 0





def desVen(ventana2):
	global listaGenerada	
	ventana2.destroy()
	print("nombreCarpeta: " +    nombreCarpeta.get())
	os.mkdir(nombreCarpeta.get())
	for imagen in listaGenerada:
		direccion,nombre = os.path.split(imagen)
		shutil.copy(imagen, nombreCarpeta.get() + "/"+nombre)
	listaGenerada = []	



	




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





    


boton4 = Button(raiz, image=imgBotonIzquierda, command = Last).place(x=250,y=50)	
Label(miframe, button=boton4,height=50, width = 150)
boton5 = Button(raiz, image=imgBotonAbrir, command=abrir_carpeta).place(x=515,y=50)	
Label(miframe, button=boton5,height=50, width = 150)
boton6 = Button(raiz, image=imgBotonDerecha, command = Next).place(x=800,y=50)	
Label(miframe, button=boton6,height=50, width = 150)
inicio = 50
intervalo = 175


boton7_1 = Button(raiz, text ="            Clinico            ", command = lambda: Seleccionar(0)).place(x=inicio + 0*intervalo,y=500)
Label(miframe, button=boton6,height=50, width = 150)

boton7_2 = Button(raiz, text ="            Clinico (valvula)            ", command = lambda: Seleccionar(1)).place(x=inicio + 1*intervalo,y=500)
Label(miframe, button=boton6,height=50, width = 150)

boton7_3 = Button(raiz, text ="            Tela         ", command = lambda: Seleccionar(2)).place(x=inicio + 2*intervalo,y=500)
Label(miframe, button=boton6,height=50, width = 150)

boton7_4 = Button(raiz, text ="            Convencional            ", command = lambda: Seleccionar(3)).place(x=inicio + 3*intervalo,y=500)
Label(miframe, button=boton6,height=50, width = 150)

boton7_5 = Button(raiz, text ="            Sin cubrebocas            ", command = lambda: Seleccionar(4)).place(x=inicio + 4*intervalo,y=500)
Label(miframe, button=boton6,height=50, width = 150)

boton8 = Button(raiz, text ="            Otros            ", command = lambda: Seleccionar(5)).place(x=inicio + 5*intervalo,y=500)
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