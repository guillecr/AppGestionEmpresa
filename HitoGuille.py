from tkinter import *
import sqlite3
import re
import math

# author Guillermo Casas Reche
# author g.casas.r94@gmail.com

# =========< VARIABLES GLOBALES >=========

# Variables de DDBB
global conn  # Conexión
dbName = "test"
tableName = "Empleados"
COLUMNAS = (
    'COD',
    'NOMBRE',
    'PRIMER APELLIDO',
    'SEGUNDO APELLIDO',
    'FECHA ALTA',
    'FECHA BAJA',
    'CATEGORIA',
    'SALARIO',
    'NUMERO DE PAGAS',
    'SALARIO SEMANAL',
    'PRORRATAS'
)  # No usado

ruta = "Empleados.txt"  # Ruta del archivo
separadorFile = ';'  # Separador en el fichero generado
decimal = 2  # Decimales de los calculos


# =========< FUNCIONES GLOBALES >=========
# Función de conversión de una lista a un objeto Empleado
def parseEmpleado(datos):
    return Empleado(
        datos[0],  # COD
        datos[1],  # Nombre
        datos[2],  # Apellido 1
        datos[3],  # Apellido 2
        datos[4],  # Fecha Alta
        datos[5],  # Fecha baja
        datos[6],  # Categoría
        datos[7],  # Saldo anual
        datos[8],  # Numero Pagas
        datos[9],  # Saldo Mensual
        datos[10])  # Prorrata


def truncate(number, decimals=0):
    factor = 10.0 ** decimals
    return math.trunc(number * factor) / factor


# Función que trasforma una lista de objetos en un String apto para la salida por pantalla
def StringToList(lista, separador, ty=True):
    salida = ""
    for d in lista:
        perlist = [
            str(d.cod),
            str(d.nombre),
            str(d.apellido1),
            str(d.apellido2),
            str(d.fechalta)
        ]
        if ty: perlist.append(str(d.fechbaja))
        perlist.append(str(d.categoria))
        perlist.append(str(d.salanual))
        perlist.append(str(d.numpagas))
        perlist.append(str(d.salmensu))
        perlist.append(str(d.prorrata))

        salida += separador.join(perlist) + "\n"
    return salida


# Función encargada de imprimir en el contenedor una lista de elementos
def printDatos(contenedor, lista):
    # texto = " | ".join(COLUMNAS)+"\n"+StringToList(lista)
    texto = StringToList(lista, '\t|\t', False)
    contenedor.config(state=NORMAL)
    contenedor.delete(1.0, END)
    contenedor.insert(1.0, texto)
    contenedor.config(state=DISABLED)


def saveFile():
    f = open(ruta, 'w')
    f.write(separadorFile.join(COLUMNAS)+"\n")
    f.write(StringToList(getAll(), separadorFile))
    f.close()
    print("Fichero creado")


# =========< FUNCIONES CRUD >=========
def getAll():
    print("Obtener todos")
    cursor = conn.cursor()
    cursor.execute("Select*from {}".format(tableName))
    datos = cursor.fetchall()
    listaEmp = list(map(lambda d: parseEmpleado(d), datos))
    cursor.close()
    return listaEmp


def getActive():
    print("Obtener todos los activos")
    cursor = conn.cursor()
    cursor.execute("Select*from {} where fechbaja IS NULL".format(tableName))
    datos = cursor.fetchall()
    listaEmp = list(map(lambda d: parseEmpleado(d), datos))
    cursor.close()
    return listaEmp


def getID(code=0):
    print("Buscar por codigo",code)
    cursor = conn.cursor()
    cursor.execute("Select*from {} where cod={}".format(tableName, code))
    empleado = Empleado("", "", "", "", "", "", "", "", "", "", "")
    datos = cursor.fetchall()
    if len(datos) > 0:
        print("Encontrado: ",code)
        empleado = parseEmpleado(datos[0])

    cursor.close()
    return empleado


def addEmplo(empleado):
    print("Añadir", empleado.nombre)
    cursor = conn.cursor()
    cursor.execute("Insert into {} "
                   "(cod,"
                   "nombre,"
                   "apellido1,"
                   "apellido2,"
                   "fechalta,"
                   "fechbaja,"
                   "categoria,"
                   "salanual,"
                   "numpagas)"
                   " values('{}','{}','{}','{}','{}',{},'{}','{}','{}')".format(
        tableName,
        empleado.cod,
        empleado.nombre,
        empleado.apellido1,
        empleado.apellido2,
        empleado.fechalta,
        "'" + empleado.fechbaja + "'" if empleado.fechbaja != "" else 'Null',
        empleado.categoria,
        empleado.salanual,
        empleado.numpagas
    ))
    # cursor.fetchone()
    conn.commit()
    cursor.close()


def updateCalculo(cod, salmensual, prorrata):
    print("Actualizar",cod)
    cursor = conn.cursor()
    cursor.execute("UPDATE {} set salmensu={}, prorrata={} where cod={}".format(tableName, salmensual, prorrata, cod))
    conn.commit()
    cursor.close()


def deleteID(code):
    print("Eliminar",code)
    cursor = conn.cursor()
    cursor.execute("delete from {} where cod={}".format(tableName, code))
    conn.commit()
    cursor.close()


# =========< FUNCIONES TESTs >=========
# Función simple que devuelve el un match
buscaMatch = lambda cad, patr : re.match(patr, cad)


def testFecha(fecha, ty=True):
    test = True
    if ty and not testNoEmpty(fecha):
        test = False
    if testNoEmpty(fecha) and not buscaMatch(fecha, r'\d{2}[-/]\d{2}[-/]\d{4}'):
        test = False
    return test


def testNum(numero):
    if testNoEmpty(numero) and not re.findall(r'\D', numero):
        return float(numero) > 0
    return False


def testNoEmpty(cadena):
    return cadena != ""


def recargar():
    printDatos(MainVentana.cajaTexto, getActive())


# =========< FUNCIONES Nuevas Ventanas >=========
def newVentanaAdd():
    VentanaAdd()


def newVentanaNomina():
    VentanaNomina()


def newVentanaBuscar():
    VentanaBuscar()


def newVentanaEliminar():
    VentanaEliminar()


# =========< CLASES MODELO >=========
class Empleado:
    def __init__(self, cod, nombre, apellido1, apellido2, fechalta, fechbaja, categoria, salanual, numpagas, salmensu = None, prorrata = None):
        self.cod = cod
        self.nombre = nombre
        self.apellido1 = apellido1
        self.apellido2 = apellido2
        self.fechalta = fechalta
        self.fechbaja = fechbaja
        self.categoria = categoria
        self.salanual = salanual
        self.numpagas = numpagas
        self.salmensu = salmensu
        self.prorrata = prorrata

    def __str__(self):
        return "{}\t|\t{}\t|\t{}\t|\t{}\t|\t{}\t|\t{}\t|\t{}\t|\t{}\t|\t{}\t|\t{}\t|\t{}".format(
            self.cod,
            self.nombre,
            self.apellido1,
            self.apellido2,
            self.fechalta,
            self.fechbaja,
            self.categoria,
            self.salanual,
            self.numpagas,
            self.salmensu,
            self.prorrata
        )


# =========< CLASES VENTANAS >=========
# Ventana ERROR
class VentanaError:
    def salir(self):
        self.addV.destroy()

    def __init__(self, mensaje):
        self.addV = Tk()
        self.addV.config(pady=10, padx=10)
        self.addV.resizable(0, 0)

        Label(self.addV, text="ERROR:", justify=CENTER).grid(row=0, column=0)
        Label(self.addV, text=mensaje, justify=CENTER).grid(row=0, column=1)
        Button(self.addV, text="Aceptar", command=self.salir, justify=CENTER).grid(row=1, column=0, columnspan=2)


# Ventana NUEVO EMPLEADO
class VentanaAdd:

    def testDatos(self):
        test = True
        mensaje = ""
        if self.cod.get() == "":
            mensaje = "Debe de indicar un codigo"
            test = False
        elif not testNoEmpty(self.nombre.get()):
            mensaje = "Debe de indicar el nombre"
            test = False
        elif not testNoEmpty(self.apellido1.get()):
            mensaje = "Debe de indicar el primer apellido"
            test = False
        elif not testNoEmpty(self.apellido2.get()):
            mensaje = "Debe de indicar el segundo apellido"
            test = False
        elif not testFecha(self.fechalta.get()):
            mensaje = "Fecha de alta incorrecta (dd-mm-yyyy)"
            test = False
        elif not testFecha(self.fechbaja.get(), False):
            mensaje = "Fecha de baja incorrecta (dd-mm-yyyy)"
            test = False
        elif not testNoEmpty(self.categoria.get()):
            mensaje = "Debe de indicar una categoría"
            test = False
        elif not testNum(self.salanual.get()):
            mensaje = "Saldo anual invalido"
            test = False
        elif not testNum(self.numpagas.get()):
            mensaje = "Numero de pagas invalidas"
            test = False

        if test:
            self.add()
        else:
            VentanaError(mensaje)

    def add(self):
        addEmplo(Empleado(
            self.cod.get(),
            self.nombre.get(),
            self.apellido1.get(),
            self.apellido2.get(),
            self.fechalta.get(),
            self.fechbaja.get(),
            self.categoria.get(),
            self.salanual.get(),
            self.numpagas.get()
        ))
        recargar()
        self.addV.destroy()

    def reset(self):
        self.cod.set('')
        self.nombre.set('')
        self.apellido1.set('')
        self.apellido2.set('')
        self.fechalta.set('')
        self.fechbaja.set('')
        self.categoria.set('')
        self.salanual.set('')
        self.numpagas.set('')

    def __init__(self):
        self.addV = Tk()
        self.cod = StringVar(self.addV)
        self.nombre = StringVar(self.addV)
        self.apellido1 = StringVar(self.addV)
        self.apellido2 = StringVar(self.addV)
        self.fechalta = StringVar(self.addV)
        self.fechbaja = StringVar(self.addV)
        self.categoria = StringVar(self.addV)
        self.salanual = StringVar(self.addV)
        self.numpagas = StringVar(self.addV)

        self.addV.title("Nuevo Empleado")
        self.addV.config(pady=5, padx=5)
        self.addV.resizable(0, 0)

        # Cod
        Label(self.addV, text="Codigo").grid(row=0, column=0)
        Entry(self.addV, textvariable=self.cod).grid(row=0, column=1)

        # Nombre
        Label(self.addV, text="Nombre").grid(row=1, column=0)
        Entry(self.addV, textvariable=self.nombre).grid(row=1, column=1)

        # Apellido1
        Label(self.addV, text="Primer Apellido").grid(row=1, column=2)
        Entry(self.addV, textvariable=self.apellido1).grid(row=1, column=3)

        # Apellido2
        Label(self.addV, text="Segundo Apellido").grid(row=1, column=4)
        Entry(self.addV, textvariable=self.apellido2).grid(row=1, column=5)

        # Fechalta
        Label(self.addV, text="Fecha Alta").grid(row=2, column=0)
        Entry(self.addV, textvariable=self.fechalta).grid(row=2, column=1)

        # Fechbaja
        Label(self.addV, text="Fecha Baja").grid(row=2, column=2)
        Entry(self.addV, textvariable=self.fechbaja).grid(row=2, column=3)

        # Categoria
        Label(self.addV, text="Categoria").grid(row=3, column=0)
        Entry(self.addV, textvariable=self.categoria).grid(row=3, column=1)

        # salanual
        Label(self.addV, text="Salario Anual").grid(row=3, column=2)
        Entry(self.addV, textvariable=self.salanual).grid(row=3, column=3)

        # numpagas
        Label(self.addV, text="Numero de Pagas").grid(row=3, column=4)
        Entry(self.addV, textvariable=self.numpagas).grid(row=3, column=5)

        Button(self.addV, text="Añadir", command=self.testDatos, width=25).grid(row=4, column=1, columnspan=2, pady=10)
        Button(self.addV, text="Restablecer", command=self.reset, width=25).grid(row=4, column=3, columnspan=2, pady=10)
        self.addV.mainloop()


# Ventana NOMINA
class VentanaNomina:
    buscado = Empleado(None, None, None, None, None, None, None, None, None, None, None)

    def buscar(self):
        if not testNoEmpty(self.cod.get()):
            self.cod.set(0)

        self.buscado = getID(self.cod.get())
        self.butCal.config(state=DISABLED)
        self.burActu.config(state=DISABLED)
        if testNoEmpty(self.buscado.cod): self.butCal.config(state=NORMAL)
        self.nomAll.set("{} {} {}".format(self.buscado.nombre, self.buscado.apellido1, self.buscado.apellido2))
        self.salanual.set(self.buscado.salanual)
        self.salmensual.set(self.buscado.salmensu)
        self.prorrata.set(self.buscado.prorrata)

    def calcular(self):
        self.burActu.config(state=NORMAL)
        self.salmensual.set("ERROR")
        self.prorrata.set("ERROR")

        if type(self.buscado.salanual) == float and (type(self.buscado.numpagas) == int):
            self.salmensual.set(truncate(self.buscado.salanual/12, decimal))
            self.prorrata.set(truncate(eval("({}*{})/{}".format(self.buscado.numpagas, self.buscado.salanual/12, 12)), decimal))

    def actualizar(self):
        updateCalculo(self.buscado.cod, self.salmensual.get(), self.prorrata.get())
        recargar()
        self.addV.destroy()

    def __init__(self):
        self.addV = Tk()
        self.addV.title("Nomina")
        self.addV.config(pady=5, padx=5)
        self.addV.resizable(0, 0)

        self.cod = StringVar(self.addV)
        self.nomAll = StringVar(self.addV)
        self.salanual = StringVar(self.addV)
        self.salmensual = StringVar(self.addV)
        self.prorrata = StringVar(self.addV)

        # Cod
        Label(self.addV, text="Codigo").grid(row=0, column=0)
        Entry(self.addV, textvariable=self.cod).grid(row=0, column=1)
        Button(self.addV, text="Buscar", command=self.buscar, width=10).grid(row=0, column=2, pady=10)

        # Nombre  y apellidos
        Label(self.addV, text="Nombre").grid(row=1, column=0)
        Entry(self.addV, textvariable=self.nomAll, state=DISABLED, disabledforeground="#000000", width=56).grid(row=1, column=1, columnspan=3)

        # salanual
        Label(self.addV, text="Salario Anual").grid(row=2, column=0)
        Entry(self.addV, textvariable=self.salanual, state=DISABLED, disabledforeground="#000000").grid(row=2, column=1)

        # salmensual
        Label(self.addV, text="Salario Mensual").grid(row=2, column=2)
        Entry(self.addV, textvariable=self.salmensual, state=DISABLED, disabledforeground="#000000").grid(row=2, column= 3)

        # prorrata
        Label(self.addV, text="Prorrata").grid(row=3, column=2)
        Entry(self.addV, textvariable=self.prorrata, state=DISABLED, disabledforeground="#000000").grid(row=3, column=3)

        self.butCal = Button(self.addV, text="Calcular", command=self.calcular, state=DISABLED, width=20)
        self. butCal.grid(row=4, column=0, columnspan=2, pady=10)
        self.burActu = Button(self.addV, text="Actualizar", command=self.actualizar, state=DISABLED, width=20)
        self.burActu.grid(row=4, column=2, columnspan=2, pady=10)

        self.addV.mainloop()


# Ventana BUSCAR
class VentanaBuscar:

    def buscar(self):
        if not testNoEmpty(self.cod.get()):
            self.cod.set(0)

        buscado = getID(self.cod.get() )
        self.nombre.set(buscado.nombre)
        self.apellido1.set(buscado.apellido1)
        self.apellido2.set(buscado.apellido2)
        self.fechalta.set(buscado.fechalta)
        self.fechbaja.set(buscado.fechbaja)
        self.categoria.set(buscado.categoria)
        self.salanual.set(buscado.salanual)
        self.numpagas.set(buscado.numpagas)
        self.salmensual.set(buscado.salmensu)
        self.prorrata.set(buscado.prorrata)

    def __init__(self):
        self.addV = Tk()
        self.addV.title("Buscar")
        self.addV.config(pady=5, padx=5)
        self.addV.resizable(0, 0)

        self.cod = StringVar(self.addV)
        self.nombre = StringVar(self.addV)
        self.apellido1 = StringVar(self.addV)
        self.apellido2 = StringVar(self.addV)
        self.fechalta = StringVar(self.addV)
        self.fechbaja = StringVar(self.addV)
        self.categoria = StringVar(self.addV)
        self.salanual = StringVar(self.addV)
        self.numpagas = StringVar(self.addV)
        self.salmensual = StringVar(self.addV)
        self.prorrata = StringVar(self.addV)

        # Cod
        Label(self.addV, text="Codigo").grid(row=0, column=0)
        Entry(self.addV, textvariable=self.cod).grid(row=0, column=1)

        # Nombre
        Label(self.addV, text="Nombre").grid(row=1, column=0)
        Entry(self.addV, textvariable=self.nombre, state=DISABLED, disabledforeground="#000000").grid(row=1, column=1)

        # Apellido1
        Label(self.addV, text="Primer apellido").grid(row=1, column=2)
        Entry(self.addV, textvariable=self.apellido1, state=DISABLED, disabledforeground="#000000").grid(row=1, column=3)

        # Apellido2
        Label(self.addV, text="Segundo Apellido").grid(row=1, column=4)
        Entry(self.addV, textvariable=self.apellido2, state=DISABLED, disabledforeground="#000000").grid(row=1, column=5)

        # Fechalta
        Label(self.addV, text="Fecha Alta").grid(row=2, column=0)
        Entry(self.addV, textvariable=self.fechalta, state=DISABLED, disabledforeground="#000000").grid(row=2, column=1)

        # Fechbaja
        Label(self.addV, text="Fecha Baja").grid(row=2, column=2)
        Entry(self.addV, textvariable=self.fechbaja, state=DISABLED, disabledforeground="#000000").grid(row=2, column=3)

        # Categoria
        Label(self.addV, text="Categoria").grid(row=3, column=0)
        Entry(self.addV, textvariable=self.categoria, state=DISABLED, disabledforeground="#000000").grid(row=3, column=1)

        # salanual
        Label(self.addV, text="Salario Anual").grid(row=3, column=2)
        Entry(self.addV, textvariable=self.salanual, state=DISABLED, disabledforeground="#000000").grid(row=3, column=3)

        # numpagas
        Label(self.addV, text="Numero de Pagas").grid(row=3, column=4)
        Entry(self.addV, textvariable=self.numpagas, state=DISABLED, disabledforeground="#000000").grid(row=3, column=5)

        # salmensual
        Label(self.addV, text="Salario Mensual").grid(row=4, column=0)
        Entry(self.addV, textvariable=self.salmensual, state=DISABLED, disabledforeground="#000000").grid(row=4, column=1)

        # prorrata
        Label(self.addV, text="Prorrata").grid(row=4, column=2)
        Entry(self.addV, textvariable=self.prorrata, state=DISABLED, disabledforeground="#000000").grid(row=4, column=3)

        Button(self.addV, text="Buscar", command=self.buscar, width=40).grid(row=5, column=2, columnspan=2, pady=10)
        self.addV.mainloop()


# Ventana ELIMINAR
class VentanaEliminar:

    def buscar(self):
        if not testNoEmpty(self.cod.get()):
            self.cod.set(0)

        buscado = getID(self.cod.get())

        self.butEliminar.config(state=DISABLED)
        if testNoEmpty(buscado.cod):
            self.butEliminar.config(state=NORMAL)

        self.nombre.set(buscado.nombre)
        self.apellido1.set(buscado.apellido1)
        self.apellido2.set(buscado.apellido2)
        self.fechalta.set(buscado.fechalta)
        self.fechbaja.set(buscado.fechbaja)
        self.categoria.set(buscado.categoria)
        self.salanual.set(buscado.salanual)
        self.numpagas.set(buscado.numpagas)
        self.salmensual.set(buscado.salmensu)
        self.prorrata.set(buscado.prorrata)

    def eliminar(self):
        print("A eliminar: "+self.cod.get())
        deleteID(self.cod.get())
        recargar()
        self.addV.destroy()

    def __init__(self):
        self.addV = Tk()
        self.addV.title("Buscar")
        self.addV.config(pady=5, padx=5)
        self.addV.resizable(0, 0)

        self.cod = StringVar(self.addV)
        self.nombre = StringVar(self.addV)
        self.apellido1 = StringVar(self.addV)
        self.apellido2 = StringVar(self.addV)
        self.fechalta = StringVar(self.addV)
        self.fechbaja = StringVar(self.addV)
        self.categoria = StringVar(self.addV)
        self.salanual = StringVar(self.addV)
        self.numpagas = StringVar(self.addV)
        self.salmensual = StringVar(self.addV)
        self.prorrata = StringVar(self.addV)

        # Cod
        Label(self.addV, text="Codigo").grid(row=0, column=0)
        Entry(self.addV, textvariable=self.cod).grid(row=0, column=1)

        # Nombre
        Label(self.addV, text="Nombre").grid(row=1, column=0)
        Entry(self.addV, textvariable=self.nombre, state=DISABLED, disabledforeground="#000000").grid(row=1, column=1)

        # Apellido1
        Label(self.addV, text="Primer apellido").grid(row=1, column=2)
        Entry(self.addV, textvariable=self.apellido1, state=DISABLED, disabledforeground="#000000").grid(row=1, column=3)

        # Apellido2
        Label(self.addV, text="Segundo Apellido").grid(row=1, column=4)
        Entry(self.addV, textvariable=self.apellido2, state=DISABLED, disabledforeground="#000000").grid(row=1, column=5)

        # Fechalta
        Label(self.addV, text="Fecha Alta").grid(row=2, column=0)
        Entry(self.addV, textvariable=self.fechalta, state=DISABLED, disabledforeground="#000000").grid(row=2, column=1)

        # Fechbaja
        Label(self.addV, text="Fecha Baja").grid(row=2, column=2)
        Entry(self.addV, textvariable=self.fechbaja, state=DISABLED, disabledforeground="#000000").grid(row=2, column=3)

        # Categoria
        Label(self.addV, text="Categoria").grid(row=3, column=0)
        Entry(self.addV, textvariable=self.categoria, state=DISABLED, disabledforeground="#000000").grid(row=3, column=1)

        # salanual
        Label(self.addV, text="Salario Anual").grid(row=3, column=2)
        Entry(self.addV, textvariable=self.salanual, state=DISABLED, disabledforeground="#000000").grid(row=3, column=3)

        # numpagas
        Label(self.addV, text="Numero de Pagas").grid(row=3, column=4)
        Entry(self.addV, textvariable=self.numpagas, state=DISABLED, disabledforeground="#000000").grid(row=3, column=5)

        # salmensual
        Label(self.addV, text="Salario Mensual").grid(row=4, column=0)
        Entry(self.addV, textvariable=self.salmensual, state=DISABLED, disabledforeground="#000000").grid(row=4, column=1)

        # prorrata
        Label(self.addV, text="Prorrata").grid(row=4, column=2)
        Entry(self.addV, textvariable=self.prorrata, state=DISABLED, disabledforeground="#000000").grid(row=4, column=3)

        Button(self.addV, text="Buscar", command=self.buscar, width=20).grid(row=5, column=1, columnspan=2, pady=10)
        self.butEliminar = Button(self.addV, text="Eliminar", command=self.eliminar, width=20, state=DISABLED)
        self.butEliminar.grid(row=5, column=3, columnspan=2, pady=10)
        self.addV.mainloop()


# =========< VENTANA PRINCIPAL >=========
class MainVentana:
    root = Tk()
    root.title("Principal")
    root.geometry('1100x350')
    root.resizable(0, 0)
    # root.config(pady=5, padx=5)

    # Generación de menús
    menuBarra = Menu(root)  # Menu principal que se añadirá a la ventana principal
    menuCascada = Menu(menuBarra, tearoff=0)  # Menú interno de la barra de menu. Contiene las funciones de menuBarra

    # Opciones menú
    menuCascada.add_command(label='Añadir', command=newVentanaAdd)
    menuCascada.add_command(label='Nómina', command=newVentanaNomina)
    menuCascada.add_command(label='Buscar', command=newVentanaBuscar)
    menuCascada.add_command(label='Eliminar', command=newVentanaEliminar)
    menuCascada.add_separator()
    menuCascada.add_command(label='Listado', command=saveFile)
    menuCascada.add_command(label='Alta', command=recargar)

    menuBarra.add_cascade(menu=menuCascada, label="Empleado")  # MenuCascada lo añadimos al menuBarra en forma de cascada
    root.config(menu=menuBarra)  # Incicamos que la ventana principal tendrá como menu la barraMenu

    # Caja de texto central
    cajaTexto = Text(root)
    cajaTexto.pack(fill="both")
    cajaTexto.config(bd=0, padx=6, pady=4, state=DISABLED, font=("Consolas", 10))

    def __init__(self):
        self.root.mainloop()


# =========< INICIALIZADOR >=========
def start():
    global conn
    conn = sqlite3.connect(dbName + ".db")
    MainVentana()  # Ejecución del programa


start()  # Iniciamos la ejecución
