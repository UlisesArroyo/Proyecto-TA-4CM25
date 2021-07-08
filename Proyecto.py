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
lineas = []
# Datos de la lista: Tienen que separarse con una " , "
datosLista = ["Nombre", "UbicacionArchivo", "Categorias", "Dimensiones", "Tipo de archivo", "Numero de personas[Plural Singular]", "Comentarios"]

class Imagen:
	def __init__(self, categoria, nombre, ubicacion, dimensiones, tipoArchivo, numeroPersonas, comentarios):
		self.categoria = categoria
		self.nombre = nombre
		self.ubicacion = ubicacion
		self.dimensiones = dimensiones
		self.tipoArchivo = tipoArchivo
		self.numeroPersonas = numeroPersonas
		self.comentarios = comentarios

	def actualizarAtributos(self, categoria, nombre, ubicacion, dimensiones, tipoArchivo, numeroPersonas, comentarios):
		self.categoria = categoria
		self.nombre = nombre
		self.ubicacion = ubicacion
		self.dimensiones = dimensiones
		self.tipoArchivo = tipoArchivo
		self.numeroPersonas = numeroPersonas
		self.comentarios = comentarios

	def infObjeto(self):
		print("-------------------------------")
		print("Objeto: ")
		print(f"Categoria: {self.categoria}")
		print(f"Nombre: {self.nombre}")
		print(f"Ubicacion: {self.ubicacion}")
		print(f"Dimensiones: {self.dimensiones}")
		print(f"Tipo de archivo: {self.tipoArchivo}")
		print(f"Numero de Personas: {self.numeroPersonas}")
		print(f"Comentarios:  {self.comentarios}")
		print("-------------------------------")


objImagen = Imagen("Sin asignar", "Nombre", "Ubicacion", "Dimension", "TipoArchivo", "True", ".")

anchoImagenSeleccion = 320;
altoImagenSeleccion = 240;
anchoImagenAdyacente = 120;
altoImagenAdyacente = 90;

raiz = Tk()  #ventana
contenidoComentario = tk.StringVar()
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
imgBotonClinico = PhotoImage(file = "back/clinico.png")
imgBotonClinico2 = PhotoImage(file = "back/clinico2.png")
imgBotonTela = PhotoImage(file = "back/tela.png")
imgBotonConv = PhotoImage(file = "back/conv.png")
imgBotonsin = PhotoImage(file = "back/sin.png")
imgBotonOtros = PhotoImage(file = "back/otros.png")
imgBotonPlural = PhotoImage(file = "back/plu.png")
imgBotonSingular = PhotoImage(file = "back/sing.png")
imgBotonComentarios = PhotoImage(file = "back/comentarios.png")
imgRandom = str(random.randint(1,5))
imgFondo = PhotoImage(file = "back/f"+imgRandom+".png")
lblFondo = Label(miframe,image=imgFondo).place(x=0,y=0)

def abrir_carpeta():
	global rutasImagenes,carpetaAbierta, posicionImagen, rutaRelativa
	posicionImagen = 0
	archivo_abierto = filedialog.askdirectory(initialdir="./", title="Select file")               	
	if(len(archivo_abierto) != 0):
		rutaRelativa = os.path.split(archivo_abierto)
		#print("Cola: ", rutaRelativa[0])
		#print("Cabeza: ", rutaRelativa[1])
		archivo_abierto += "/"
		rutasImagenes = buscarFicherosEnDirectorios(archivo_abierto)
		rutasImagenes = modificacionrutas(rutasImagenes, rutaRelativa[1])	
		confirmarListas(rutaRelativa[1])

		img = Image.open(rutaRelativa[0] + "/" + rutasImagenes[posicionImagen-1]) 
		img = img.resize((anchoImagenAdyacente, altoImagenAdyacente), Image.ANTIALIAS) 
		img = ImageTk.PhotoImage(image=img)
		Imagen1.configure(image=img)
		Imagen1.image = img

		img = Image.open(rutaRelativa[0] + "/" + rutasImagenes[posicionImagen])  
		img = img.resize((anchoImagenSeleccion, altoImagenSeleccion), Image.ANTIALIAS) 
		img = ImageTk.PhotoImage(image=img) 
		Imagen2.configure(image=img)
		Imagen2.image = img	

		img = Image.open(rutaRelativa[0] + "/" + rutasImagenes[posicionImagen + 1])  
		img = img.resize((anchoImagenAdyacente, altoImagenAdyacente), Image.ANTIALIAS) 
		img = ImageTk.PhotoImage(image=img)
		Imagen3.configure(image=img)
		Imagen3.image = img

		refrescarInformacionLocal()
		carpetaAbierta = True	#Activa el Next, Last y los botones de selección
		pluralSingular(False)

def refrescarInformacionLocal():
	imagenNueva, posicionImagenLista, categoria, numeroPersonas, comentario= comparador(rutasImagenes[posicionImagen])
	nombre, ubicacion, dimensiones, extension = recopilacionInformacion(rutaRelativa[0] + "/" + rutasImagenes[posicionImagen])	
	objImagen.actualizarAtributos(categoria, nombre, ubicacion, dimensiones, extension, numeroPersonas, comentario)
	objImagen.infObjeto()

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

def modificacionrutas(imagenes, nombreCarpeta):
	for imagen in range(len(imagenes)):
		#print("Ruta Original: ", imagenes[imagen])
		izq = imagenes[imagen].find(nombreCarpeta)
		nombreRelativo = imagenes[imagen][izq:]
		#print("Ruta Relativa: ", nombreRelativo)
		imagenes[imagen] = nombreRelativo
	return imagenes

def confirmarListas(carpetaRaiz):
	global lineas
	indice = "Categoria" + "," + "Nombre" + "," + "Ubicacion" + "," + "Dimensiones" + "," + "Tipo de archivo" + "," + "Numero de Personas" + "," + "Comentarios" +"\n"
	try:
		os.stat("./Listas")
	except OSError as e:
		os.mkdir("./Listas")	
	x = 0
	lista = "./Listas/" + carpetaRaiz + ".txt"
	if os.path.exists(lista):
		fichero = open(lista,"r")
		lineas = fichero.readlines()
		fichero.close()
		if len(lineas) != 0:
			print(lineas[0])
			print(indice)
			if lineas[0] != indice:
				print("ENTRO")
				lineas.insert(0, indice)
				fichero = open(lista,"w")
				print("AAA", lineas)
				for c in lineas:
					print("==>",c)
					fichero.write(c)
				fichero.close()
		else:
			fichero = open(lista, "a+")
			fichero.write(indice)
			fichero.close()
	else:
		fichero = open(lista,"a+")
		fichero.write(indice)
		fichero.close()
	"""		
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
		
		x += 1	
	"""	


def escribirLista():
	imagenNueva, posicionImagenLista, categoria, numeroPersonas, comentario= comparador(rutasImagenes[posicionImagen])
	nombre, ubicacion, dimensiones, extension = recopilacionInformacion(rutaRelativa[0] + "/" + rutasImagenes[posicionImagen])	
	fichero = open("./Listas/" + rutaRelativa[1] + ".txt","r")
	lines = fichero.readlines()
	fichero.close()
	if posicionImagenLista == 0:
		fichero = open("./Listas/" + rutaRelativa[1] + ".txt","a")
		fichero.write(categoria + "," + nombre + "," + ubicacion + "," + dimensiones + "," + extension + "," + str(numeroPersonas) + "," + comentario + "\n")#Funcion ingreso de datos
	else: 
		fichero = open("./Listas/" + rutaRelativa[1] + ".txt","w")
		for line in range(len(lines)):
			if line != posicionImagenLista:
				fichero.write(lines[line])
			else:
				fichero.write(categoria + "," + nombre + "," + ubicacion + "," + dimensiones + "," + extension + "," + str(numeroPersonas) + "," + comentario + "\n")


	fichero.close()
 	
 
def Next():
	global posicionImagen, rutaRelativa
	if carpetaAbierta and posicionImagen < len(rutasImagenes) and objImagen.categoria != "Sin asignar":
		escribirLista()
		posicionImagen += 1
		posicionImagen %= len(rutasImagenes)
		rutaImagenCompleta = rutaRelativa[0] + "/" + rutasImagenes[posicionImagen-1]

		img = Image.open(rutaRelativa[0] + "/" + rutasImagenes[posicionImagen-1]) 
		img = img.resize((anchoImagenAdyacente, altoImagenAdyacente), Image.ANTIALIAS) 
		img = ImageTk.PhotoImage(image=img)
		Imagen1.configure(image=img)
		Imagen1.image = img

		img = Image.open(rutaRelativa[0] + "/" + rutasImagenes[posicionImagen])  
		img = img.resize((anchoImagenSeleccion, altoImagenSeleccion), Image.ANTIALIAS) 
		img = ImageTk.PhotoImage(image=img)
		Imagen2.configure(image=img)
		Imagen2.image = img	

		if(posicionImagen == len(rutasImagenes)-1):
			img = Image.open(rutaRelativa[0] + "/" + rutasImagenes[0])  
			img = img.resize((anchoImagenAdyacente, altoImagenAdyacente), Image.ANTIALIAS) 
			img = ImageTk.PhotoImage(image=img)
			Imagen3.configure(image=img)
			Imagen3.image = img	
		else:
			img = Image.open(rutaRelativa[0] + "/" + rutasImagenes[posicionImagen+1])  
			img = img.resize((anchoImagenAdyacente, altoImagenAdyacente), Image.ANTIALIAS) 
			img = ImageTk.PhotoImage(image=img)
			Imagen3.configure(image=img)
			Imagen3.image = img	

	
	objImagen.actualizarAtributos("Sin asignar", "Nombre", "Ubicacion", "Dimension", "TipoArchivo", "True", ".")
	refrescarInformacionLocal()		
	pluralSingular(False)
	


def Last():
	global posicionImagen, rutaRelativa
	if (carpetaAbierta and posicionImagen >= 0 and objImagen.categoria != "Sin asignar") :
		escribirLista()
		posicionImagen -= 1
		if(posicionImagen<0):
			posicionImagen += len(rutasImagenes)

		img = Image.open(rutaRelativa[0] + "/" + rutasImagenes[posicionImagen-1]) 
		img = img.resize((anchoImagenAdyacente, altoImagenAdyacente), Image.ANTIALIAS) 
		img = ImageTk.PhotoImage(image=img)
		Imagen1.configure(image=img)
		Imagen1.image = img

		img = Image.open(rutaRelativa[0] + "/" + rutasImagenes[posicionImagen])  
		img = img.resize((anchoImagenSeleccion, altoImagenSeleccion), Image.ANTIALIAS) 
		img = ImageTk.PhotoImage(image=img)
		Imagen2.configure(image=img)
		Imagen2.image = img	

		if(posicionImagen==len(rutasImagenes)-1):
			img = Image.open(rutaRelativa[0] + "/" + rutasImagenes[0])  
			img = img.resize((anchoImagenAdyacente, altoImagenAdyacente), Image.ANTIALIAS) 
			img = ImageTk.PhotoImage(image=img)
			Imagen3.configure(image=img)
			Imagen3.image = img		
		else:
			img = Image.open(rutaRelativa[0] + "/" + rutasImagenes[posicionImagen+1])  
			img = img.resize((anchoImagenAdyacente, altoImagenAdyacente), Image.ANTIALIAS) 
			img = ImageTk.PhotoImage(image=img)
			Imagen3.configure(image=img)
			Imagen3.image = img	

	objImagen.actualizarAtributos("Sin asignar", "Nombre", "Ubicacion", "Dimension", "TipoArchivo", "True", ".")		
	refrescarInformacionLocal()
	pluralSingular(False)

def pluralSingular(entrada):
	global objImagen
	if carpetaAbierta:
		if entrada:
			if str(objImagen.numeroPersonas) == "True":
				objImagen.numeroPersonas = "False"
				boton8.config(image=imgBotonPlural)
			else:
				objImagen.numeroPersonas = "True"
				boton8.config(image=imgBotonSingular)
		else:
			if objImagen.numeroPersonas == "True":
				boton8.config(image=imgBotonSingular)
				
			if objImagen.numeroPersonas == "False":
				boton8.config(image=imgBotonPlural)

		print("numeroPersonas: ", objImagen.numeroPersonas)

			

def ingresarComentario():
	if carpetaAbierta:
		contenidoComentario.set(objImagen.comentarios)
		ventana2 = tk.Toplevel()
		ventana2.geometry("380x300+200+100")
		ventana2.configure(background = "dark turquoise")
		Label(ventana2,image=imgFondo).place(x=0,y=0)
		mensaje1 =Label(ventana2,text="Ingrese Comentario").place(x=50,y=30)
		nomCarp =Entry(ventana2, textvariable=contenidoComentario)
		nomCarp.place(x=100, y=60, width = 250)
		boton4 = Button(ventana2, text ="OK", font=(18),fg="blue", command = lambda: cerrarVentana(ventana2)).place(x=50,y=60)		
		Label(ventana2, button=boton4,height=50, width = 150)

def cerrarVentana(ventana2):
	ventana2.destroy()
	print("comentario: " +    contenidoComentario.get())
	objImagen.comentarios = contenidoComentario.get()
	refrescarInformacionLocal();
	

		

def Seleccionar(categoriaSeleccionada):
	if(carpetaAbierta):
		imagenNueva, posicionImagenLista, categoria, numeroPersonas, comentario = comparador(rutasImagenes[posicionImagen])
		if imagenNueva:
			objImagen.categoria = categorias[categoriaSeleccionada]
			refrescarInformacionLocal()
			"""
			fichero = open("./Listas/" + rutaRelativa[1] + ".txt","a")
			print("./Listas/" + rutaRelativa[1] + ".txt")
			nombre, ubicacion, dimensiones, extension = recopilacionInformacion(rutaRelativa[0] + "/" + rutasImagenes[posicionImagen])
			fichero.write(categorias[categoriaSeleccionada] + "," + nombre + "," + ubicacion + "," + dimensiones + "," + extension +"\n")#Funcion ingreso de datos
			fichero.close()
			"""
		else: 
			if objImagen.categoria == categorias[categoriaSeleccionada]:
				messagebox.showinfo(message="La imagen ya se encuentra en esta Lista (" + categorias[categoriaSeleccionada]+")", title="Error")
			else:
				MsgBox = messagebox.askokcancel(title="Error Imagen repetida", message="Desea cambiar la imagen de " + objImagen.categoria + " a " + categorias[categoriaSeleccionada])
				if (MsgBox == 1):
					objImagen.categoria = categorias[categoriaSeleccionada]
					refrescarInformacionLocal()
					"""
					fichero = open("./Listas/" + rutaRelativa[1] + ".txt","r")
					lines = fichero.readlines()
					fichero.close()
					fichero = open("./Listas/" + rutaRelativa[1] + ".txt","w")
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
					fichero = open("./Listas/" + rutaRelativa[1] + ".txt","a")
					nombre, ubicacion, dimensiones, extension = recopilacionInformacion(rutasImagenes[posicionImagen])
					fichero.write(nombre + "," + ubicacion + "," + dimensiones + "," + extension +"\n")#Funcion ingreso de datos
					fichero.close()	
					"""


def recopilacionInformacion(ubicacion):
	rutaNombre = os.path.split(ubicacion)
	nombre = rutaNombre[1]
	rutaExtension = os.path.splitext(ubicacion)
	extension = rutaExtension[1]
	imagen = cv2.imread(ubicacion,0)
	alto, ancho = imagen.shape[:2]
	dimensiones = str(alto) + "x" + str(ancho)
	ubicacion = rutasImagenes[posicionImagen]
	#numeroPersonas = True
	#comentarios = ""
	return nombre, ubicacion, dimensiones, extension #Falta numeroPersonas y comentarios





def comparador(imagen):
	global lineas, rutaRelativa

	fichero = open("./Listas/" + rutaRelativa[1] + ".txt","r")
	lineas = fichero.readlines()
	#print("XXX",lineas)
	fichero.close()
	for linea in range(len(lineas) - 1):
		izq, der = buscarRangosDatos(2,lineas[linea + 1])#Es un 2 porque buscamos la ubicación
		ubicacion = lineas[linea + 1][izq:der]
		print("ENTRO")
		print("Ubicacion: ",ubicacion)
		print("Imagen: ",imagen)
		if imagen == ubicacion:
			print("GANE >:]")
			izq, der = buscarRangosDatos(0,lineas[linea + 1])
			categoria = lineas[linea +1][izq:der]
			izq, der = buscarRangosDatos(6,lineas[linea + 1])
			comentario =lineas[linea + 1][izq:der]
			izq, der = buscarRangosDatos(5,lineas[linea + 1])
			numeroPersonas =lineas[linea + 1][izq:der]
			if objImagen.categoria == "Sin asignar":
				return False, (linea + 1), categoria, numeroPersonas, comentario
			else:
				return False, (linea + 1), objImagen.categoria, objImagen.numeroPersonas, objImagen.comentarios


	#print("Toda la info: ",lineas)


	return (objImagen.categoria == "Sin asignar"), 0, objImagen.categoria, objImagen.numeroPersonas, objImagen.comentarios
"""
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
"""

def buscarRangosDatos(dato, linea):
	listaIndices = [0]
	for i in range(len(linea)):
		if linea[i] == ",":
			listaIndices.append(i)
	listaIndices.append(len(linea))
	if dato * 2 == 0:
		izq = listaIndices[(dato)]
	else:
		izq = listaIndices[(dato)] + 1

	if 	listaIndices[(dato) + 1] == len(linea):
		der = listaIndices[(dato) + 1] - 1
	else: 
		der = listaIndices[(dato) + 1]

	print("listaIndices: ", listaIndices)
	print(f"izq: {izq}|| der: {der}|| dato: {dato}")
	return izq, der






	




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


boton7_1 = Button(raiz, image = imgBotonClinico, command = lambda: Seleccionar(0)).place(x=inicio + 0*intervalo,y=500)
Label(miframe, button=boton6,height=50, width = 150)

boton7_2 = Button(raiz, image = imgBotonClinico2, command = lambda: Seleccionar(1)).place(x=inicio + 1*intervalo,y=500)
Label(miframe, button=boton6,height=50, width = 150)

boton7_3 = Button(raiz, image = imgBotonTela, command = lambda: Seleccionar(2)).place(x=inicio + 2*intervalo,y=500)
Label(miframe, button=boton6,height=50, width = 150)

boton7_4 = Button(raiz, image = imgBotonConv , command = lambda: Seleccionar(3)).place(x=inicio + 3*intervalo,y=500)
Label(miframe, button=boton6,height=50, width = 150)

boton7_5 = Button(raiz, image = imgBotonsin, command = lambda: Seleccionar(4)).place(x=inicio + 4*intervalo,y=500)
Label(miframe, button=boton6,height=50, width = 150)

boton7_6 = Button(raiz, image = imgBotonOtros, command = lambda: Seleccionar(5)).place(x=inicio + 5*intervalo,y=500)
Label(miframe, button=boton6,height=50, width = 150)

boton8 = Button(raiz, image = imgBotonSingular, command = lambda: pluralSingular(True))
boton8.place(x=inicio + 2*intervalo,y=600)

Label(miframe, button=boton6,height=50, width = 150)

boton9 = Button(raiz, image = imgBotonComentarios, command = ingresarComentario)
boton9.place(x=inicio + 4*intervalo,y=600)
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