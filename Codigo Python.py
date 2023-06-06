from tkinter import *
from tkinter import messagebox
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime
import time
#----Creacion Raiz-----
dt=datetime.now()
fechahoy="{}/0{}/{}".format(dt.day, dt.month, dt.year)
raiz=Tk()
raiz.title("Intefaz Usuario " + str(fechahoy))
raiz.geometry("320x300")


#------Variables-------

Nombre=StringVar()
Apellido=StringVar()
ID=StringVar()
ID2=StringVar()
Edad=float()
Peso=float()
Altura=float()
Ciudad=StringVar()
Pais=StringVar()
Email=StringVar()
Genero=StringVar()
Generos=StringVar()
MuestraNombre=StringVar()
MuestraApellido=StringVar()
MuestraID=StringVar()
MuestraEdad=StringVar()
MuestraPeso=StringVar()
MuestraAltura=StringVar()
MuestraCiudad=StringVar()
MuestraPais=StringVar()
MuestraEmail=StringVar()
UltimoUsuario=[]
InsertarUsuario=[]
Usuarioss=[]
arroba=0
valor=False
Validacion=False



#------Funciones BBDD-------


def ExportarCSV():
	conexion=sqlite3.connect("BBDD-Usuarios")
	Vcursor=conexion.cursor()
	Datos=pd.read_sql('''SELECT * FROM "Usuarios"''',conexion)
	Datos.to_csv('TablaUsuarios.csv',sep=",",index=0)
	messagebox.showinfo("Archvivo","Se ha exportado/actualizado el archivo TablaUsuarios.csv")

def ExportarExcel():
	conexion=sqlite3.connect("BBDD-Usuarios")
	Vcursor=conexion.cursor()
	Datos=pd.read_sql('''SELECT * FROM "Usuarios"''',conexion)
	Datos.to_excel('TablaUsuarios.xlsx',sheet_name='Usuarios',index=0)
	messagebox.showinfo("Archvivo Excel","Se ha exportado/actualizado el archivo TablaUsuarios.xlsx")
 
def Salir():
	valor=messagebox.askokcancel("Salir", "Desea Salir?")	
	ExportarCSV()
	if valor==True:
		raiz.destroy()
  

def BorrarTodos():
    MuestraNombre.set("")
    MuestraApellido.set("")
    MuestraID.set("")
    MuestraEdad.set("")
    MuestraPeso.set("")
    MuestraAltura.set("")
    MuestraCiudad.set("")
    MuestraPais.set("")
    MuestraEmail.set("")
   
       	
def Chequeo(Ingreso,Tipo):
	conexion=sqlite3.connect("BBDD-Usuarios")
	Vcursor=conexion.cursor()
	if Tipo=="Edad":
		try:
			Edad=int(Ingreso)
			if Edad<1 or Edad>100:
				messagebox.showwarning("Carga Incorrecta","Edad debe ser un numero correcto")
				MuestraEmail.set("")
				MuestraEdad.set("")
			else:
				return True
		except:
			messagebox.showwarning("Carga Incorrecta","Edad debe ser un numero")
			MuestraEmail.set("")
			MuestraEdad.set("")
	elif Tipo=="Peso":
		try:
			Peso=float(Ingreso)
			if Peso<1 or Peso>200:
				messagebox.showwarning("Carga Incorrecta","Peso debe ser un numero correcto")
				MuestraEmail.set("")
				MuestraPeso.set("")
			else:
				return True
		except ValueError:
			messagebox.showwarning("Carga Incorrecta","Peso debe ser un numero")
			MuestraEmail.set("")
			MuestraPeso.set("")
 
	elif Tipo=="Altura":
		try:
			Altura=float(Ingreso)
			if Altura<1 or Altura>2.5:
				messagebox.showwarning("Carga Incorrecta","Altura debe ser un numero")
				MuestraEmail.set("")
				MuestraAltura.set("")
			else:
				return True
		except:
			messagebox.showwarning("Carga Incorrecta","Altura debe ser un numero")
			MuestraEmail.set("")
			MuestraAltura.set("")
	elif Tipo=="Email":
		global arroba
		arroba=0
		Mail=str(Ingreso)+".com"
		Letrapost=False
		try: 
			Vcursor.execute("""SELECT * FROM Usuarios WHERE Email=?""",[Mail])
			CargaAutomatica=Vcursor.fetchall()
			UltimoUsuariod=CargaAutomatica.pop()
			if Mail==UltimoUsuariod[7]:
				messagebox.showinfo("Usuario existente","Ese usuario ya existe, por favor introduzca otro mail")
				MuestraEmail.set("")
		except:
			for char in Ingreso:
				if char=='@':
					arroba+=1
				elif char.isalpha()==False and arroba==1:
					messagebox.showinfo("Carga incorrecta","Por favor introduzca un mail correcto")
					MuestraEmail.set("")
					break
				elif char.isalpha()==True and arroba==1:
					Letrapost=True
			if arroba!=1 or Letrapost==False:
				MuestraEmail.set("")
				messagebox.showinfo("Carga incorrecta","Por favor introduzca un mail correcto")

               

def Crear():		
	conexion=sqlite3.connect("BBDD-Usuarios")
	Vcursor=conexion.cursor()
	if MuestraID.get()!="":
		messagebox.showwarning("Carga Incorrecta","La informacion cargada en ID no sera valida")
	MuestraID.set("")	
  
	Nombre=MuestraNombre.get()
	Apellido=MuestraApellido.get()
	if Chequeo(MuestraEdad.get(),"Edad")==True:
		Edad=int(MuestraEdad.get())
	if Chequeo(MuestraPeso.get(),"Peso")==True:
		Peso=float(MuestraPeso.get())
	if Chequeo(MuestraAltura.get(),"Altura")==True:
		Altura=float(MuestraAltura.get())
	Ciudad=MuestraCiudad.get()
	Pais=MuestraPais.get()
	Chequeo(MuestraEmail.get(),"Email")
	Email=MuestraEmail.get()
	Email2=str(Email)+".com"
	Generos=Genero.get()
 
	if Nombre!="" and Apellido!="" and Email!="":
		InsertarUsuario=[Nombre,Apellido,Generos,Edad,Peso,Altura,Email2,Ciudad,Pais,fechahoy]
		Vcursor.execute("INSERT INTO Usuarios VALUES (NULL,?,?,?,?,?,?,?,?,?,?)",InsertarUsuario)
		conexion.commit()
		messagebox.showinfo("Insertar Usuario","Usuario insertado con exito")
		Vcursor.execute("SELECT * FROM Usuarios WHERE APELLIDO=?",[Apellido])
		CargaAutomatica=Vcursor.fetchall()
		UltimoUsuariod=CargaAutomatica.pop()
		Mostrar(UltimoUsuariod)
	else:
		messagebox.showinfo("Crear Usuario","Para crear un usuario por favor llene los casilleros: Nombre, Apellido, Email y Password")
			

def Buscar():
	conexion=sqlite3.connect("BBDD-Usuarios")
	Vcursor=conexion.cursor()
	Email=MuestraEmail.get()
	Email2=str(Email)+".com"
	try:
		Vcursor.execute("SELECT * FROM USUARIOS WHERE Email='"+Email2+"'")
		CargaAutomatica=Vcursor.fetchall()
		UltimoUsuariod=CargaAutomatica.pop()
		Mostrar(UltimoUsuariod)
		conexion.commit()
		return True
	except:
		try:
			Vcursor.execute("SELECT * FROM USUARIOS WHERE ID="+MuestraID.get())
			CargaAutomatica=Vcursor.fetchall()
			UltimoUsuariod=CargaAutomatica.pop()
			Mostrar(UltimoUsuariod)
			conexion.commit()
			return True
		except:
			BorrarTodos()
			messagebox.showinfo("Read Usuario","Usuario inexistente, por favor indique un ID o Email existente")


def Modificar():
	conexion=sqlite3.connect("BBDD-Usuarios")
	Vcursor=conexion.cursor()
	global Validacion
	global ID2
	valor2=messagebox.askokcancel("Modificar Registro", "Desea modificar el registro?")
	if Validacion==False and valor2==True:
		Buscar()
		ID2=MuestraID.get()
		Validacion=True
		messagebox.showinfo("Actualizar Usuario","Por favor realice las modificaciones correspondientes")
	elif Validacion==True and valor2==True:
		Cambio()
		Validacion=False

def Cambio():
	conexion=sqlite3.connect("BBDD-Usuarios")
	Vcursor=conexion.cursor()
	global ID2
	Nombre=MuestraNombre.get()
	Apellido=MuestraApellido.get()
	if Chequeo(MuestraEdad.get(),"Edad")==True:
		Edad=int(MuestraEdad.get())
	if Chequeo(MuestraPeso.get(),"Peso")==True:
		Peso=float(MuestraPeso.get())
	if Chequeo(MuestraAltura.get(),"Altura")==True:
		Altura=float(MuestraAltura.get())
	Ciudad=MuestraCiudad.get()
	Pais=MuestraPais.get()
	Generos=Genero.get()
	Usuarioss=[Nombre,Apellido,Generos,Edad,Peso,Altura,Ciudad,Pais,ID2]
	
	if MuestraID.get()!=ID2:
		messagebox.showinfo("Actualizar Usuario","Por favor realice las modificaciones en el usurio ?",[ID2])
		BorrarTodos()
	else:
		Vcursor.execute("UPDATE Usuarios SET Nombre = ?, Apellido = ?, Genero = ?, Edad = ?, Peso = ?, Altura = ?, Ciudad = ?, Pais = ? WHERE ID=?", Usuarioss)
		conexion.commit()
		messagebox.showinfo("Actualizar Usuario", "Usuario actualizado con exito")
		Vcursor.execute("SELECT * FROM Usuarios WHERE ID=" + MuestraID.get())
		CargaAutomatica = Vcursor.fetchall()
		UltimoUsuario = CargaAutomatica.pop()
		Mostrar(UltimoUsuario)

def Delete():
	conexion=sqlite3.connect("BBDD-Usuarios")
	Vcursor=conexion.cursor()
	global valor
	if Buscar()==True:
		valor=messagebox.askokcancel("Eliminar Registro", "Desea eliminar el registro?")	
		if valor==True:
				Vcursor.execute("DELETE FROM USUARIOS WHERE ID=" + MuestraID.get())
				conexion.commit()
				messagebox.showinfo("Eliminar registro","Registro Eliminado")
				BorrarTodos()
		else:
				Vcursor.execute("SELECT * FROM USUARIOS WHERE ID=" + MuestraID.get())
				CargaAutomatica=Vcursor.fetchall()
				UltimoUsuario=CargaAutomatica.pop()
				Mostrar(UltimoUsuario)
	valor=False
  	

def Mostrar(Parametro):
    MuestraID.set(Parametro[0])
    MuestraNombre.set(Parametro[1])
    MuestraApellido.set(Parametro[2])
    Genero.set(Parametro[3])
    MuestraEdad.set(Parametro[4])
    MuestraAltura.set(Parametro[6])
    MuestraPeso.set(Parametro[5])
    MuestraEmail.set(Parametro[7][:-4])
    MuestraPais.set(Parametro[9])
    MuestraCiudad.set(Parametro[8])

	

##-------------Barra Menu-------------
Menus=Menu(raiz)
raiz.config(menu=Menus, width=300,height=300)

BBDDmenu=Menu(Menus, tearoff=0)
Menus.add_cascade(label="BBDD", menu=BBDDmenu)
BBDDmenu.add_command(label="Exportar Tabla - .csv",command=ExportarCSV)
BBDDmenu.add_command(label="Exportar Tabla - .xlsx",command=ExportarExcel)
BBDDmenu.add_command(label="Salir",command=Salir)


CRUDMenu=Menu(Menus,tearoff=0)
Menus.add_cascade(label="CRUD", menu=CRUDMenu)
CRUDMenu.add_command(label="Crear", command=Crear)
CRUDMenu.add_command(label="Buscar", command=Buscar)
CRUDMenu.add_command(label="Modificar", command=Modificar)
CRUDMenu.add_command(label="Borrar", command=BorrarTodos)

AyudaMenu=Menu(Menus,tearoff=0)
Menus.add_cascade(label="Ayuda", menu=AyudaMenu)
AyudaMenu.add_command(label="Licencia",command=ExportarCSV)
AyudaMenu.add_command(label="Acerca de...")

##--------------Labels y Entry----------

miframe=Frame(raiz)
miframe.pack()

LabelID=Label(miframe,text="ID:")
LabelID.grid(row=1,column=1,sticky="se",pady=5)

VariableID=Entry(miframe,textvariable=MuestraID,width=5)
VariableID.grid(row=1,column=2,sticky="sw", padx=2,pady=5)

LabelNombre=Label(miframe,text="Nombre:")
LabelNombre.grid(row=2,column=1,sticky="se",pady=8)

VariableNombre=Entry(miframe,textvariable=MuestraNombre,width=11)
VariableNombre.grid(row=2,column=2,sticky="sw", padx=2, pady=8,columnspan=2)


LabelApellido=Label(miframe,text="Apellido:")
LabelApellido.grid(row=2,column=4,sticky="se",padx=2,pady=8)

VariableApellido=Entry(miframe,textvariable=MuestraApellido,width=11)
VariableApellido.grid(row=2,column=5,sticky="sw", padx=2, pady=8,columnspan=2)

LabelGenero=Label(miframe,text="Genero:")
LabelGenero.grid(row=3,column=1,sticky="se",padx=2,pady=8)

Masculino=Radiobutton(miframe,text="M", variable=Genero, value="M")
Masculino.grid(row=3,column=2,sticky="sw",pady=6)
Femenino=Radiobutton(miframe,text="F", variable=Genero, value="F")
Femenino.grid(row=3,column=3,sticky="sw",pady=6)
Genero.set("M")

LabelEdad=Label(miframe,text="Edad:")
LabelEdad.grid(row=3,column=4,sticky="se",padx=2,pady=8)


VariableEdad=Entry(miframe,textvariable=MuestraEdad,width=5)
VariableEdad.grid(row=3,column=5,sticky="sw", padx=2, pady=8)



LabelPeso=Label(miframe,text="Peso:")
LabelPeso.grid(row=4,column=1,sticky="se",padx=2,pady=8)

VariablePeso=Entry(miframe,textvariable=MuestraPeso,width=5)
VariablePeso.grid(row=4,column=2,sticky="sw", padx=2, pady=8)

LabelKg=Label(miframe,text="Kg.")
LabelKg.grid(row=4,column=3,sticky="sw",pady=8)



LabelAltura=Label(miframe,text="Altura:")
LabelAltura.grid(row=4,column=4,sticky="se",padx=2,pady=8)

VariableAltura=Entry(miframe,textvariable=MuestraAltura,width=5)
VariableAltura.grid(row=4,column=5,sticky="sw", padx=2, pady=8)

LabelMts=Label(miframe,text="mts.")
LabelMts.grid(row=4,column=6,sticky="sw",padx=1,pady=8)

LabelEmail=Label(miframe,text="Email:")
LabelEmail.grid(row=5,column=1,sticky="se",padx=1,pady=8)

VariableEmail=Entry(miframe,textvariable=MuestraEmail,width=25)
VariableEmail.grid(row=5,column=2,sticky="sw", padx=1, pady=8,columnspan=4)

LabelCom=Label(miframe,text=".com")
LabelCom.grid(row=5,column=5,sticky="sw",padx=1,pady=8)

LabelCiudad=Label(miframe,text="Ciudad:")
LabelCiudad.grid(row=6,column=1,sticky="se",pady=8)

VariableCiudad=Entry(miframe,textvariable=MuestraCiudad,width=11)
VariableCiudad.grid(row=6,column=2,sticky="sw", padx=2, pady=8,columnspan=2)


LabelPais=Label(miframe,text="Pais:")
LabelPais.grid(row=6,column=4,sticky="se",padx=2,pady=8)

VariablePais=Entry(miframe,textvariable=MuestraPais,width=11)
VariablePais.grid(row=6,column=5,sticky="sw", padx=2, pady=8,columnspan=2)

##-----------------Botones------------

miframe2=Frame(raiz)
miframe2.pack()

CreateButton=Button(miframe2,text="Crear", command=Crear)
CreateButton.grid(row=2,column=1,sticky="se",padx=6,pady=5)
CreateButton.config(width=5)

ReadButton=Button(miframe2,text="Buscar", command=Buscar)
ReadButton.grid(row=1,column=2,padx=6,pady=5)
ReadButton.config(width=11)

BorrarButton=Button(miframe2,text="Borrar Campos",command=BorrarTodos)
BorrarButton.grid(row=1,column=3,sticky="se",padx=6,pady=5)
BorrarButton.config(width=11)

ModificarButton=Button(miframe2,text="Modificar",command=Modificar)
ModificarButton.grid(row=2,column=2,sticky="se",padx=6,pady=5)
ModificarButton.config(width=11)

DeleteButton=Button(miframe2,text="Delete Usuario",command=Delete)
DeleteButton.grid(row=2,column=3,sticky="se",padx=6,pady=5)
DeleteButton.config(width=11)

SalirButton=Button(miframe2,text="Salir",command=Salir)
SalirButton.grid(row=2,column=4,sticky="se",padx=6,pady=5)
SalirButton.config(width=5)

raiz.mainloop()




