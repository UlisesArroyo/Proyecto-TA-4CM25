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
import numpy as np
posicionImagen=0
carpetaAbierta=False
rutasImagenes =[]
listaGenerada = []
categorias = ["Clinico", "Clinico_valvula", "Tela", "Convencional", "Sin_cubrebocas", "Otros"]
lineas = []
# Datos de la lista: Tienen que separarse con una " , "
datosLista = ["Nombre", "UbicacionArchivo", "Categorias", "Dimensiones", "Tipo de archivo", "Numero de personas[Plural Singular]", "Simulacion", "Recortado", "Comentarios"]

estandarRecortado = "NO_Recortado" 
#estandarRecortado = "Recortado"

class Imagen:
	def __init__(self, categoria, nombre, ubicacion, dimensiones, tipoArchivo, numeroPersonas, simulado, recortado, comentarios):
		self.categoria = categoria
		self.nombre = nombre
		self.ubicacion = ubicacion
		self.dimensiones = dimensiones
		self.tipoArchivo = tipoArchivo
		self.numeroPersonas = numeroPersonas
		self.simulado = simulado
		self.recortado = recortado
		self.comentarios = comentarios

	def actualizarAtributos(self, categoria, nombre, ubicacion, dimensiones, tipoArchivo, numeroPersonas, simulado, recortado, comentarios):
		self.categoria = categoria
		self.nombre = nombre
		self.ubicacion = ubicacion
		self.dimensiones = dimensiones
		self.tipoArchivo = tipoArchivo
		self.numeroPersonas = numeroPersonas
		self.simulado = simulado
		self.recortado = recortado
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
		print(f"Simulado: {self.simulado}")
		print(f"Recortado: {self.recortado}")
		print(f"Comentarios:  {self.comentarios}")
		print("-------------------------------")


objImagen = Imagen("Sin asignar", "Nombre", "Ubicacion", "Dimension", "TipoArchivo", "Singular", "NO_Simulado", estandarRecortado , ".")

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
		archivo_abierto += "/"
		rutasImagenes = buscarFicherosEnDirectorios(archivo_abierto)
		rutasImagenes = modificacionrutas(rutasImagenes, rutaRelativa[1])	
		confirmarListas(rutaRelativa[1])

		fichero = open("./Listas/" + rutaRelativa[1] + ".txt","r")
		lines = fichero.readlines()
		fichero.close()
		#posicionImagen = len(lines) - 1

		

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
		
		print("posicionImagen: ", posicionImagen)
		refrescarInformacionLocal()
		carpetaAbierta = True	#Activa el Next, Last y los botones de selección
		pluralSingular(False)
		simulado(False)
		recortado(False)

def refrescarInformacionLocal():
	imagenNueva, posicionImagenLista, categoria, numeroPersonas,simulado, recortado, comentario= comparador(rutasImagenes[posicionImagen])
	nombre, ubicacion, dimensiones, extension = recopilacionInformacion(rutaRelativa[0] + "/" + rutasImagenes[posicionImagen])	
	objImagen.actualizarAtributos(categoria, nombre, ubicacion, dimensiones, extension, numeroPersonas,simulado, recortado, comentario)
	actualizarPantalla()
	objImagen.infObjeto()
	
def actualizarPantalla():
	contenidoComentario.set(objImagen.comentarios)
	if objImagen.categoria == "Sin asignar":
		TextoCategoria.configure(text="Categoria: " + objImagen.categoria, bg = "red")
	else:
		TextoCategoria.configure(text="Categoria: " + objImagen.categoria, bg = "green")
	TextoImagen.configure(text="Imagen: " + objImagen.nombre)
	TextoUbicacion.configure(text="Ubicacion " + objImagen.ubicacion)
	TextoDimensiones.configure(text="Dimensiones: " + objImagen.dimensiones)
	TextoTipoArchivo.configure(text="Tipo de archivo: " + objImagen.tipoArchivo)
	TextoNumeroPersonas.configure(text="Numero de Personas: " + objImagen.numeroPersonas)
	TextoSimulado.configure(text="Simulado: " + objImagen.simulado)
	TextoRecortado.configure(text="Recortado: " + objImagen.recortado)
	TextoComentarios.configure(text="Comentario: " + objImagen.comentarios)
	#TextoCategoria.configure(text="Comentarios: " + objImagen.comentarios)
	
	TextoID.configure(text="ID " + str(posicionImagen + 1) + " - " + str(len(rutasImagenes)))

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
	indice = "Categoria" + "," + "Nombre" + "," + "Ubicacion" + "," + "Dimensiones" + "," + "Tipo de archivo" + "," + "Numero de Personas" + "," + "Simulacion" + "," + "Recortado" +  "," + "Comentarios" +"\n"
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
	imagenNueva, posicionImagenLista, categoria, numeroPersonas,simulado, recortado, comentario= comparador(rutasImagenes[posicionImagen])
	nombre, ubicacion, dimensiones, extension = recopilacionInformacion(rutaRelativa[0] + "/" + rutasImagenes[posicionImagen])	
	fichero = open("./Listas/" + rutaRelativa[1] + ".txt","r")
	lines = fichero.readlines()
	fichero.close()
	if posicionImagenLista == 0:
		fichero = open("./Listas/" + rutaRelativa[1] + ".txt","a")
		fichero.write(categoria + "," + nombre + "," + ubicacion + "," + dimensiones + "," + extension + "," + numeroPersonas + "," + simulado + "," + recortado  + "," + comentario + "\n")#Funcion ingreso de datos
	else: 
		fichero = open("./Listas/" + rutaRelativa[1] + ".txt","w")
		for line in range(len(lines)):
			if line != posicionImagenLista:
				fichero.write(lines[line])
			else:
				fichero.write(categoria + "," + nombre + "," + ubicacion + "," + dimensiones + "," + extension + "," + numeroPersonas + "," + simulado + "," + recortado  + "," + comentario + "\n")


	fichero.close()
 	
def Next():
	global posicionImagen, rutaRelativa, objImagen
	if carpetaAbierta and posicionImagen < (len(rutasImagenes) -1) and objImagen.categoria != "Sin asignar":
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

	
		objImagen = Imagen("Sin asignar", "Nombre", "Ubicacion", "Dimension", "TipoArchivo", "Singular", "NO_Simulado", estandarRecortado, ".")
		refrescarInformacionLocal()		
		pluralSingular(False)
		simulado(False)
		recortado(False)
	
def Last():
	global posicionImagen, rutaRelativa, objImagen
	if (carpetaAbierta and posicionImagen > 0 and objImagen.categoria != "Sin asignar") :
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

		objImagen = Imagen("Sin asignar", "Nombre", "Ubicacion", "Dimension", "TipoArchivo", "Singular", "NO_Simulado", estandarRecortado, ".")
		refrescarInformacionLocal()
		pluralSingular(False)
		simulado(False)
		recortado(False)

def pluralSingular(entrada):
	global objImagen
	if carpetaAbierta:
		if entrada:
			if str(objImagen.numeroPersonas) == "Singular":
				objImagen.numeroPersonas = "Plural"
				boton8.config(image=imgBotonPlural)
			else:
				objImagen.numeroPersonas = "Singular"
				boton8.config(image=imgBotonSingular)
		else:
			if objImagen.numeroPersonas == "Singular":
				boton8.config(image=imgBotonSingular)
				
			if objImagen.numeroPersonas == "Plural":
				boton8.config(image=imgBotonPlural)

		#print("numeroPersonas: ", objImagen.numeroPersonas)
		actualizarPantalla()

def simulado(entrada):
	global objImagen
	if carpetaAbierta:
		if entrada:
			if str(objImagen.simulado) == "NO_Simulado":
				objImagen.simulado = "Simulado"
				boton10.config(text="Simulado (X)", bg = "orange")
			else:
				objImagen.simulado = "NO_Simulado"
				boton10.config(text="NO_Simulado (X)", bg = "green")
		else:
			if objImagen.simulado == "NO_Simulado":
				boton10.config(text="NO_Simulado (X)", bg = "green")
				
			if objImagen.simulado == "Simulado":
				boton10.config(text="Simulado (X)", bg =  "orange")

		#print("simulado: ", objImagen.simulado)
		actualizarPantalla()

def recortado(entrada):
	global objImagen
	if carpetaAbierta:
		if entrada:
			if str(objImagen.recortado) == "NO_Recortado":
				objImagen.recortado = "Recortado"
				boton11.config(text="Recortado (V)", bg = "orange")
			else:
				objImagen.recortado = "NO_Recortado"
				boton11.config(text="NO_Recortado (V)", bg = "green")
		else:
			if objImagen.recortado == "NO_Recortado":
				boton11.config(text="NO_Recortado (V)", bg = "green")
				
			if objImagen.recortado == "Recortado":
				boton11.config(text="Recortado (V)", bg = "orange")

		#print("recortado: ", objImagen.recortado)
		actualizarPantalla()				

def ingresarComentario(entrada):
	if carpetaAbierta:
		if entrada:
			objImagen.comentarios = contenidoComentario.get()
			#nomCarp =Entry(ventana2, textvariable=contenidoComentario)
		#else:

		"""
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
	"""

def Seleccionar(categoriaSeleccionada):
	if(carpetaAbierta):
		imagenNueva, posicionImagenLista, categoria, numeroPersonas,simulado, recortado, comentario = comparador(rutasImagenes[posicionImagen])
		objImagen.categoria = categorias[categoriaSeleccionada]
		refrescarInformacionLocal()
		"""
		if imagenNueva:
			objImagen.categoria = categorias[categoriaSeleccionada]
			refrescarInformacionLocal()
			
			fichero = open("./Listas/" + rutaRelativa[1] + ".txt","a")
			print("./Listas/" + rutaRelativa[1] + ".txt")
			nombre, ubicacion, dimensiones, extension = recopilacionInformacion(rutaRelativa[0] + "/" + rutasImagenes[posicionImagen])
			fichero.write(categorias[categoriaSeleccionada] + "," + nombre + "," + ubicacion + "," + dimensiones + "," + extension +"\n")#Funcion ingreso de datos
			fichero.close()

		else: 
			if objImagen.categoria == categorias[categoriaSeleccionada]:
				messagebox.showinfo(message="La imagen ya se encuentra en esta Lista (" + categorias[categoriaSeleccionada]+")", title="Error")
			else:
				MsgBox = messagebox.askokcancel(title="Error Imagen repetida", message="Desea cambiar la imagen de " + objImagen.categoria + " a " + categorias[categoriaSeleccionada])
				if (MsgBox == 1):
					objImagen.categoria = categorias[categoriaSeleccionada]
					refrescarInformacionLocal()

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
	#print("UBICACION PROBLEMA: ", ubicacion)
	rutaNombre = os.path.split(ubicacion)
	nombre = rutaNombre[1]
	rutaExtension = os.path.splitext(ubicacion)
	extension = rutaExtension[1]
	#imagen = cv2.imread(ubicacion,0)
	imagen = cv2.imdecode(np.fromfile(ubicacion, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
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
	for linea in range(posicionImagen,len(lineas) - 1):
		izq, der = buscarRangosDatos(2,lineas[linea + 1])#Es un 2 porque buscamos la ubicación
		ubicacion = lineas[linea + 1][izq:der]
		#print("ENTRO")
		print("Ubicacion: ",ubicacion)
		print("Imagen: ",imagen)
		if imagen == ubicacion:
			#print("GANE >:]")
			izq, der = buscarRangosDatos(0,lineas[linea + 1])
			categoria = lineas[linea +1][izq:der]
			izq, der = buscarRangosDatos(5,lineas[linea + 1])
			numeroPersonas =lineas[linea + 1][izq:der]
			izq, der = buscarRangosDatos(6,lineas[linea + 1])
			simulado =lineas[linea + 1][izq:der]
			izq, der = buscarRangosDatos(7,lineas[linea + 1])
			recortado =lineas[linea + 1][izq:der]
			izq, der = buscarRangosDatos(8,lineas[linea + 1])
			comentario =lineas[linea + 1][izq:der]
			if objImagen.categoria == "Sin asignar":
				return False, (linea + 1), categoria, numeroPersonas, simulado, recortado, comentario
			else:
				return False, (linea + 1), objImagen.categoria, objImagen.numeroPersonas, objImagen.simulado, objImagen.recortado, objImagen.comentarios


	#print("Toda la info: ",lineas)


	return (objImagen.categoria == "Sin asignar"), 0, objImagen.categoria, objImagen.numeroPersonas,objImagen.simulado, objImagen.recortado, objImagen.comentarios
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

	#print("listaIndices: ", listaIndices)
	#print(f"izq: {izq}|| der: {der}|| dato: {dato}")
	return izq, der



TextoCategoria = Label(miframe, text = "Categoria: " + objImagen.categoria,fg="black" , font=(32))
TextoCategoria.place(x=800,y=50)

TextoImagen = Label(miframe, text = "Imagen: " + objImagen.nombre,fg="black" , font=(32))
TextoImagen.place(x=800,y=100)

TextoUbicacion = Label(miframe, text = "Ubicacion: " + objImagen.ubicacion,fg="black" , font=(32))
TextoUbicacion.place(x=800,y=150)

TextoDimensiones = Label(miframe, text = "Dimensiones: " + objImagen.dimensiones,fg="black" , font=(32))
TextoDimensiones.place(x=800,y=200)

TextoTipoArchivo = Label(miframe, text = "Tipo de Archivo: " + objImagen.tipoArchivo,fg="black" , font=(32))
TextoTipoArchivo.place(x=800,y=250)

TextoNumeroPersonas = Label(miframe, text = "Numero de Personas: " + objImagen.numeroPersonas,fg="black" , font=(32))
TextoNumeroPersonas.place(x=800,y=300)

TextoSimulado = Label(miframe, text = "Simulado: " + objImagen.simulado,fg="black" , font=(32))
TextoSimulado.place(x=800,y=350)

TextoRecortado = Label(miframe, text = "Recortado: " + objImagen.recortado,fg="black" , font=(32))
TextoRecortado.place(x=800,y=400)

TextoComentarios = Label(miframe, text = "Comentarios: " + objImagen.comentarios,fg="black" , font=(32))
TextoComentarios.place(x=800,y=450)


TextoID = Label(miframe, text = "ID: " + str(posicionImagen + 1) + "-" + str(len(rutasImagenes)),fg="black" , font=(32))
TextoID.place(x=800,y=500)


	




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
Imagen1.place(x=190-(anchoImagenSeleccion/2),y=150+(altoImagenSeleccion/4))
    

#Esta madre debe aparecer mas grande ya que sera la central
Imagen2 = Label(miframe, image=img2)
Imagen2.pack(side="bottom", fill="both", expand="yes")
Imagen2.place(x=220,y=150)

Imagen3 = Label(miframe, image=img3)
Imagen3.pack(side="bottom", fill="both", expand="yes")
Imagen3.place(x=540+(anchoImagenSeleccion/4),y=150+(altoImagenSeleccion/4))





    


boton4 = Button(raiz, image=imgBotonIzquierda, command = Last).place(x=50,y=50)	
Label(miframe, button=boton4,height=50, width = 150)
boton5 = Button(raiz, image=imgBotonAbrir, command=abrir_carpeta).place(x=315,y=50)	
Label(miframe, button=boton5,height=50, width = 150)
boton6 = Button(raiz, image=imgBotonDerecha, command = Next).place(x=600,y=50)	
Label(miframe, button=boton6,height=50, width = 150)
inicio = 75
intervalo = 225



boton7_1 = Button(raiz, image = imgBotonClinico, command = lambda: Seleccionar(0)).place(x=inicio + 0*intervalo,y=425)
Label(miframe, button=boton6,height=50, width = 150)

boton7_2 = Button(raiz, image = imgBotonClinico2, command = lambda: Seleccionar(1)).place(x=inicio + 1*intervalo,y=425)
Label(miframe, button=boton6,height=50, width = 150)

boton7_3 = Button(raiz, image = imgBotonTela, command = lambda: Seleccionar(2)).place(x=inicio + 2*intervalo,y=425)
Label(miframe, button=boton6,height=50, width = 150)



boton7_4 = Button(raiz, image = imgBotonConv , command = lambda: Seleccionar(3)).place(x=inicio + 0*intervalo,y=525)
Label(miframe, button=boton6,height=50, width = 150)

boton7_5 = Button(raiz, image = imgBotonsin, command = lambda: Seleccionar(4)).place(x=inicio + 1*intervalo,y=525)
Label(miframe, button=boton6,height=50, width = 150)

boton7_6 = Button(raiz, image = imgBotonOtros, command = lambda: Seleccionar(5)).place(x=inicio + 2*intervalo,y=525)
Label(miframe, button=boton6,height=50, width = 150)



boton8 = Button(raiz, image = imgBotonSingular, command = lambda: pluralSingular(True))
boton8.place(x=inicio + 0*intervalo,y=625)

Label(miframe, button=boton6,height=50, width = 150)

boton9 = Button(raiz, image = imgBotonComentarios, command = lambda: ingresarComentario(True))
boton9.place(x=inicio + 3*intervalo,y=625)
Label(miframe, button=boton6,height=50, width = 150)

Comentario =Entry(raiz, textvariable=contenidoComentario)
Comentario.place(x = inicio + 4*intervalo -50,y=650, width = 300)

boton10 = Button(raiz, text = "SIMULADO (X)", command =  lambda: simulado(True))
boton10.place(x=inicio + 1*intervalo,y=625)
Label(miframe, button=boton6,height=50, width = 150)

boton11 = Button(raiz, text = "RECORTADO (V)", command = lambda: recortado(True))
boton11.place(x=inicio + 2*intervalo,y=625)
Label(miframe, button=boton6,height=50, width = 150)


def boton_q(event):
	Seleccionar(0)

def boton_w(event):
	Seleccionar(1)	

def boton_e(event):
	Seleccionar(2)

def boton_a(event):
	Seleccionar(3)	

def boton_s(event):
	Seleccionar(4)

def boton_d(event):
	Seleccionar(5)	

def boton_z(event):
	pluralSingular(True)

def boton_x(event):
	simulado(True)

def boton_c(event):
	ingresarComentario(True)	
	actualizarPantalla()
	

def boton_v(event):
	recortado(True)	

def boton_right(event):
	Next()	

def boton_left(event):
	Last()	

"""
def boton(event):
	bp= event.keysym
	if bp =="Right":
		Next()
	elif bp == "Left":
		Last()
"""

raiz.bind("<Control-q>", boton_q)
raiz.bind("<Control-Q>", boton_q)

raiz.bind("<Control-w>", boton_w)
raiz.bind("<Control-W>", boton_w)

raiz.bind("<Control-e>", boton_e)
raiz.bind("<Control-E>", boton_e)

raiz.bind("<Control-a>", boton_a)
raiz.bind("<Control-A>", boton_a)

raiz.bind("<Control-s>", boton_s)
raiz.bind("<Control-S>", boton_s)

raiz.bind("<Control-d>", boton_d)
raiz.bind("<Control-D>", boton_d)

raiz.bind("<Control-z>", boton_z)
raiz.bind("<Control-Z>", boton_z)

raiz.bind("<Control-x>", boton_x)
raiz.bind("<Control-X>", boton_x)

raiz.bind("<Control-c>", boton_c)
raiz.bind("<Control-C>", boton_c)

raiz.bind("<Control-v>", boton_v)
raiz.bind("<Control-V>", boton_v)

raiz.bind("<Control-Left>", boton_left)
raiz.bind("<Control-Left>", boton_left)

raiz.bind("<Control-Right>", boton_right)
raiz.bind("<Control-Right>", boton_right)



#raiz.bind("<Key>", boton)
	
	#print("TECLA: ",num)
"""
	
	#elif bp == "Q" or bp == "q":
		#Seleccionar(0)

	elif bp == "W + ctrl" or bp == "w + ctrl":
		Seleccionar(1)
	elif bp == "E" or bp == "e":
		Seleccionar(2)
	elif bp == "A" or bp == "a":
		Seleccionar(3)				
	elif bp == "S" or bp == "s":	
		Seleccionar(4)
	elif bp == "D" or bp == "d":
		Seleccionar(5)
	elif bp == "Z" or bp == "z":
		pluralSingular(True)
	elif bp == "X" or bp == "x":
		simulado(True)		
	elif bp == "C" or bp == "c":	
		recortado(True)
	elif bp == "V" or bp == "v":
		ingresarComentario(True)

"""		

raiz.mainloop()