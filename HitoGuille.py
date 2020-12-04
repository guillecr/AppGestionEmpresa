from tkinter import *
import sqlite3

# =========< VARIABLES GLOBALES >=========

# Variables de DDBB
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
    'NUMERO DE PAGAS'
)

ruta = ""  # Ruta del archivo
global conn  # Conexión


# =========< FUNCIONES GLOBALES >=========
# Operaciones CRUD
def getAll():
    cursor = conn.cursor()
    cursor.execute("Select*from {}".format(tableName))
    datos = cursor.fetchall()
    listaEmp = list(map(lambda d: parseEmpleado(d), datos))
    cursor.close()
    return listaEmp


def getID(code):
    cursor = conn.cursor()
    cursor.execute("Select*from {} where cod={}".format(tableName, code))
    empleado = parseEmpleado(cursor.fetchone())
    cursor.close()
    return empleado


def addEmplo(empleado):
    cursor = conn.cursor()
    cursor.execute("Insert into {} values('{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(
        tableName,
        empleado.cod,
        empleado.nombre,
        empleado.apellido1,
        empleado.apellido2,
        empleado.fechalta,
        empleado.fechbaja,
        empleado.categoria,
        empleado.salanual,
        empleado.numpagas
    ))
    cursor.fetchone()
    conn.commit()
    cursor.close()


def deleteID(code):
    cursor = conn.cursor()
    cursor.execute("delete from {} where cod={}".format(tableName, code))
    datos = cursor.fetchall()
    cursor.close()
    return datos


def parseEmpleado(datos):
    return Empleado(datos[0], datos[1], datos[2], datos[3], datos[4], datos[5], datos[6], datos[7], datos[8])


def StringToList(lista):
    salida = ""
    for f in lista:
        salida += str(f)+"\n"
    print("Salida:", salida)
    return salida


def printDatos(contenedor, lista):
    # texto = " | ".join(COLUMNAS)+"\n"+StringToList(lista)
    texto = StringToList(lista)
    contenedor.config(state=NORMAL)
    contenedor.delete(1.0, END)
    contenedor.insert(1.0, texto)
    contenedor.config(state=DISABLED)


def recargar():
    printDatos(MainVentana.cajaTexto, getAll())


def newVentanaAdd():
    VentanaAdd()


def newVentanaNomina():
    VentanaNomina()


def newVentanaBuscar():
    VentanaBuscar()


def newVentanaEliminar():
    VentanaEliminar()

# =========< CLASES MODELO >=========

class Empleado():
    def __init__(self, cod, nombre, apellido1, apellido2, fechalta, fechbaja, categoria, salanual, numpagas):
        self.cod = cod
        self.nombre = nombre
        self.apellido1 = apellido1
        self.apellido2 = apellido2
        self.fechalta = fechalta
        self.fechbaja = fechbaja
        self.categoria = categoria
        self.salanual = salanual
        self.numpagas = numpagas

    def __str__(self):
        return "{}\t|\t{}\t|\t{}\t|\t{}\t|\t{}\t|\t{}\t|\t{}\t|\t{}\t|\t{}".format(
            self.cod,
            self.nombre,
            self.apellido1,
            self.apellido2,
            self.fechalta,
            self.fechbaja,
            self.categoria,
            self.salanual,
            self.numpagas
        )


# =========< CLASES VENTANAS >=========

class VentanaAdd:

    def add(self):
        nuevoEmp = Empleado(
            self.cod.get(),
            self.nombre.get(),
            self.apellido1.get(),
            self.apellido2.get(),
            self.fechalta.get(),
            self.fechbaja.get(),
            self.categoria.get(),
            self.salanual.get(),
            self.numpagas.get()
        )
        addEmplo(nuevoEmp)
        recargar()
        self.addV.destroy()

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

        # Cod
        Label(self.addV, text="Codigo").grid(row=0, column=0)
        Entry(self.addV, textvariable=self.cod).grid(row=0, column=1)

        # Nombre
        Label(self.addV, text="Nombre").grid(row=1, column=0)
        Entry(self.addV, textvariable=self.nombre).grid(row=1, column=1)

        # Apellido1
        Label(self.addV, text="Primer apellido").grid(row=1, column=2)
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

        Button(self.addV, text="Añadir", command=self.add, width=40).grid(row=4, column=1, columnspan=4,pady=10)
        self.addV.mainloop()


class VentanaNomina:

    def calcular(self):
        buscado = getID(self.cod.get())
        self.nomAll.set("{} {} {}".format(buscado.nombre, buscado.apellido1, buscado.apellido2))
        self.salanual.set(buscado.salanual)
        self.salmensual.set(buscado.salanual/12)
        self.prorrata.set(eval("({}*{})/{}".format(buscado.numpagas,buscado.salanual/12,12)))

    def __init__(self):
        self.addV = Tk()
        self.addV.title("Nomina")
        self.addV.config(pady=5, padx=5)

        self.cod = StringVar(self.addV)
        self.nomAll = StringVar(self.addV)
        self.salanual = StringVar(self.addV)
        self.salmensual = StringVar(self.addV)
        self.prorrata = StringVar(self.addV)

        # Cod
        Label(self.addV, text="Codigo").grid(row=0, column=0)
        Entry(self.addV, textvariable=self.cod).grid(row=0, column=1)

        # Nombre  y apellidos
        Label(self.addV, text="Nombre").grid(row=0, column=2)
        Entry(self.addV, textvariable=self.nomAll, state=DISABLED, disabledforeground="#000000").grid(row=0, column=3)

        # salanual
        Label(self.addV, text="Salario Anual").grid(row=1, column=0)
        Entry(self.addV, textvariable=self.salanual, state=DISABLED, disabledforeground="#000000").grid(row=1, column=1)

        # salmensual
        Label(self.addV, text="Salario Mensual").grid(row=1, column=2)
        Entry(self.addV, textvariable=self.salmensual, state=DISABLED, disabledforeground="#000000").grid(row=1, column=3)

        # prorrata
        Label(self.addV, text="Prorrata").grid(row=2, column=2)
        Entry(self.addV, textvariable=self.prorrata, state=DISABLED, disabledforeground="#000000").grid(row=2, column=3)

        Button(self.addV, text="Buscar", command=self.calcular, width=40).grid(row=3, column=1, columnspan=2, pady=10)

        self.addV.mainloop()


class VentanaBuscar:

    def buscar(self):
        print("A buscar: "+self.cod.get())
        buscado = getID(self.cod.get())
        self.nombre.set(buscado.nombre)
        self.apellido1.set(buscado.apellido1)
        self.apellido2.set(buscado.apellido2)
        self.fechalta.set(buscado.fechalta)
        self.fechbaja.set(buscado.fechbaja)
        self.categoria.set(buscado.categoria)
        self.salanual.set(buscado.salanual)
        self.numpagas.set(buscado.numpagas)

    def __init__(self):
        self.addV = Tk()
        self.addV.title("Buscar")

        self.cod = StringVar(self.addV)
        self.nombre = StringVar(self.addV)
        self.apellido1 = StringVar(self.addV)
        self.apellido2 = StringVar(self.addV)
        self.fechalta = StringVar(self.addV)
        self.fechbaja = StringVar(self.addV)
        self.categoria = StringVar(self.addV)
        self.salanual = StringVar(self.addV)
        self.numpagas = StringVar(self.addV)

        self.cuadros = (
            self.cod,
            self.nombre,
            self.apellido1,
            self.apellido2,
            self.fechalta,
            self.fechbaja,
            self.categoria,
            self.salanual,
            self.numpagas,
        )

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

        Button(self.addV, text="Buscar", command=self.buscar, width=40).grid(row=4, column=2, columnspan=2, pady=10)
        self.addV.mainloop()


class VentanaEliminar:
    def __init__(self):
        self.addV = Tk()
        self.usuario = StringVar(self.addV)
        self.puesto = StringVar(self.addV)
        self.addV.title("Eliminar")

        Label(self.addV, text="Usuario").grid(row=0, column=0)
        Entry(self.addV, textvariable=self.usuario).grid(row=0, column=1)
        Label(self.addV, text="Puesto").grid(row=1, column=0)
        Entry(self.addV, textvariable=self.puesto).grid(row=1, column=1)
        # Button(self.addV, text="Añadir", command=self.add, width=30).grid(row=2, column=0, columnspan=2)
        self.addV.mainloop()


class MainVentana:
    root = Tk()
    root.title("Principal")
    root.geometry('1100x400')

    # Generación de menús
    menuBarra = Menu(root)  # Menu principal que se añadirá a la ventana principal
    menuCascada = Menu(menuBarra, tearoff=0)  # Menú interno de la barra de menu. Contiene las funciones de menuBarra

    # Opciones menú
    menuCascada.add_command(label='Añadir', command=newVentanaAdd)
    menuCascada.add_command(label='Nómina', command=newVentanaNomina)
    menuCascada.add_command(label='Buscar', command=newVentanaBuscar)
    menuCascada.add_command(label='Eliminar', command=newVentanaEliminar)
    menuCascada.add_command(label='Listado', command=recargar)

    menuBarra.add_cascade(menu=menuCascada, label="Archivo")  # MenuCascada lo añadimos al menuBarra en forma de cascada
    root.config(menu=menuBarra)  # Incicamos que la ventana principal tendrá como menu la barraMenu

    # Caja de texto central
    cajaTexto = Text(root)
    cajaTexto.pack(fill="both")
    cajaTexto.config(bd=0, padx=6, pady=4, state=DISABLED, font=("Consolas", 10))

    def __init__(self):
        recargar()
        self.root.mainloop()


# =========< INICIALIZADOR >=========
def start():
    global conn
    conn = sqlite3.connect(dbName + ".db")
    MainVentana()  # Ejecución del programa


start()  # Iniciamos la ejecución
