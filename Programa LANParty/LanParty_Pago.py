from tkinter import Tk,StringVar,Frame,LabelFrame,Label,Entry,Button
from tkinter.filedialog import askopenfile,asksaveasfile
from tkinter.messagebox import showinfo,showerror

import urllib.request
import pyrebase
import json

config = {
    "apiKey": "API firebase",
    "authDomain": "lanparty-b7120.firebaseapp.com",
    "databaseURL": "https://lanparty-b7120.firebaseio.com",
    "storageBucket": "lanparty-b7120.appspot.com"
}

firebase = pyrebase.initialize_app(config)

db = firebase.database()
data = db.child("ParticipantesIV").get().val()

class Formulario(Frame):

    def __init__(self,parent=None):
        Frame.__init__(self,parent)
        self.pack(expand=False)
        self.crear_componentes()

    def crear_componentes(self):

        # Título de la ventana
        self.winfo_toplevel().title('LanParty_Pago')

        # INFORMACIÓN CLIENTE
        lframe = LabelFrame(self,text='Participante')
        lframe.grid(row=0,column=0,columnspan=3,padx=(10,10),pady=(10,10),ipadx=10)

        # DNI
        lab = Label(lframe,width=15,text='DNI')
        lab.grid(row=0,column=0)
        self.nifV = StringVar()
        self.nifE = Entry(lframe,textvariable=self.nifV)
        self.nifE.grid(row=0,column=1)

        # Nombre
        lab = Label(lframe,width=15,text='Nombre')
        lab.grid(row=1,column=0)
        self.nombreV = StringVar()
        self.nombreE = Entry(lframe,textvariable=self.nombreV)
        self.nombreE.grid(row=1,column=1)

        # Fecha
        lab = Label(lframe,width=15,text='Fecha')
        lab.grid(row=2,column=0)
        self.fechaV = StringVar()
        self.fechaE = Entry(lframe,textvariable=self.fechaV)
        self.fechaE.grid(row=2,column=1)

        # Teléfono
        lab = Label(lframe,width=15,text='Teléfono')
        lab.grid(row=3,column=0)
        self.teléfonoV = StringVar()
        self.teléfonoE = Entry(lframe,textvariable=self.teléfonoV)
        self.teléfonoE.grid(row=3,column=1)

        # Email
        lab = Label(lframe,width=15,text='Email')
        lab.grid(row=4,column=0)
        self.emailV = StringVar()
        self.emailE = Entry(lframe,textvariable=self.emailV)
        self.emailE.grid(row=4,column=1)

        # Dirección
        lab = Label(lframe,width=15,text='Dirección')
        lab.grid(row=5,column=0)
        self.dirV = StringVar()
        self.dirE = Entry(lframe,textvariable=self.dirV)
        self.dirE.grid(row=5,column=1)

        # Localidad
        lab = Label(lframe,width=15,text='Localidad')
        lab.grid(row=6,column=0)
        self.localV = StringVar()
        self.localE = Entry(lframe,textvariable=self.localV)
        self.localE.grid(row=6,column=1)


        # Nick
        lab = Label(lframe,width=15,text='Nick')
        lab.grid(row=7,column=0)
        self.nickV = StringVar()
        self.nickE = Entry(lframe,textvariable=self.nickV)
        self.nickE.grid(row=7,column=1)

        # Clan
        lab = Label(lframe,width=15,text='Clan')
        lab.grid(row=8,column=0)
        self.clanV = StringVar()
        self.clanE = Entry(lframe,textvariable=self.clanV)
        self.clanE.grid(row=8,column=1)

        # Nombre en camiseta
        lab = Label(lframe,width=15,text='Nombre en camiseta')
        lab.grid(row=9,column=0)
        self.precioV = StringVar()
        self.precioE = Entry(lframe,textvariable=self.precioV)
        self.precioE.grid(row=9,column=1)

        # Talla
        lab = Label(lframe,width=15,text='Talla')
        lab.grid(row=10,column=0)
        self.tallaV = StringVar()
        self.tallaE = Entry(lframe,textvariable=self.tallaV)
        self.tallaE.grid(row=10,column=1)

        # Torneos
        lab = Label(lframe,width=15,text='Torneos')
        lab.grid(row=11,column=0)
        self.torneosV = StringVar()
        self.torneosE = Entry(lframe,textvariable=self.torneosV)
        self.torneosE.grid(row=11,column=1)

        # Pagado
        lab = Label(lframe,width=15,text='Pagado')
        lab.grid(row=12,column=0)
        self.pagadoV = StringVar()
        self.pagadoE = Entry(lframe,textvariable=self.pagadoV)
        self.pagadoE.grid(row=12,column=1)

        # Sugerencias
        lab = Label(lframe,width=15,text='Sugerencias')
        lab.grid(row=13,column=0)
        self.sugerenciasV = StringVar()
        self.sugerenciasE = Entry(lframe,textvariable=self.sugerenciasV)
        self.sugerenciasE.grid(row=13,column=1)

        # Posicion
        lab = Label(lframe,width=15,text='Posición al inscribirse')
        lab.grid(row=14,column=0)
        self.posV = StringVar()
        self.posE = Entry(lframe,textvariable=self.posV)
        self.posE.grid(row=14,column=1)

        # Botón Buscar
        bot = Button(self,text='Buscar',command=self.buscar,width=40)
        bot.grid(row=1,column=0)

        # Botón Modificar
        bot = Button(self,text='Modificar',command=self.modificar,width=40)
        bot.grid(row=2,column=0)

        # Botón Camisetas
        bot = Button(self,text='Lista de Camisetas',command=self.camisetas,width=40)
        bot.grid(row=3,column=0)

        # Botón Pagado
        bot = Button(self,text='Lista de pagados',command=self.pagado,width=40)
        bot.grid(row=4,column=0)

        # Registrados
        bot = Button(self,text='Registrados',command=self.registrados,width=40)
        bot.grid(row=5,column=0)

        # Botón Limpiar
        bot = Button(self,text='Limpiar',command=self.limpiar,width=40)
        bot.grid(row=6,column=0)

        # Botón Exportar a CSV
        bot = Button(self,text='Exportar a CSV',command=self.exportar,width=40)
        bot.grid(row=7,column=0)

    def registrados(self):
        texto = "Registrados\n" + "--------------------\n"
        for key in data:
            if key != "Inscritos" :
                usuario = data[key]
                texto += usuario["nombre"] + "\n"

        f = open("registrados.txt", "w")
        f.write(texto)
        f.close()

    def exportar(self):
        fichero = asksaveasfile(initialdir = '.',title = 'Guardar',filetypes = [('CSV','*.csv')])
        if fichero:
            fichero.write('"NIF", "Nombre", "Fecha de nacimiento", "Telefono", "Email", "Direccion", "Localidad", "Nick", "Clan", "Posicion", "Talla de camiseta", "Nombre en camiseta", "Torneos", "Sugerencias", "Pagado"\n')
            for key in data:
                if key != "Inscritos" :
                    usuario= data[key];
                    fichero.write('"' + key + '",')
                    fichero.write('"' + usuario["nombre"] + '",')
                    fichero.write('"' + usuario["fecha_nacimiento"] + '",')
                    fichero.write('"' + str(usuario["telefono"]) + '",')
                    fichero.write('"' + usuario["email"] + '",')
                    fichero.write('"' + usuario["dir"] + '",')
                    fichero.write('"' + usuario["localidad"] + '",')
                    fichero.write('"' + str(usuario["nick"]) + '",')
                    fichero.write('"' + usuario["clan"] + '",')
                    fichero.write('"' + str(usuario["numero_de_inscripcion"]) + '",')
                    fichero.write('"' + usuario["talla_camiseta"] + '",')
                    fichero.write('"' + usuario["nombre_camiseta"] + '",')
                    fichero.write('"' + usuario["torneos"] + '",')
                    fichero.write('"' + usuario["sugerencias"] + '",')
                    fichero.write('"' + usuario["pagado"] + '"\n')
            fichero.close()




    def pagado(self):
        texto = "PAGOS\n" + "--------------------\n"
        for key in data:
            if key != "Inscritos" :
                usuario = data[key]
                texto += key + " " + usuario["nombre"] + "\t\t\t" + "Inscrito el " + str(usuario["numero_de_inscripcion"]) + "º\t" + usuario["pagado"] + "\n"

        f = open("pagos.txt", "w")
        f.write(texto)
        f.close()

    def camisetas(self):
        texto = "CAMISETAS\n" + "--------------------\n"
        doce = 0
        nombre_12 = 0
        dieciseis = 0
        nombre_16 = 0
        xs = 0
        nombre_xs = 0
        s = 0
        nombre_s = 0
        m = 0
        nombre_m = 0
        l = 0
        nombre_l = 0
        xl = 0
        nombre_xl = 0
        xxl = 0
        nombre_xxl = 0
        xxxl = 0
        nombre_xxxl = 0
        for key in data:

            if key != "Inscritos" :
                usuario = data[key]
                texto += key + " " + usuario["nombre"] + "\t\t\t" + str(usuario["talla_camiseta"]) + "\tNombre: " + usuario["nombre_camiseta"] + "\n"

                if usuario["talla_camiseta"] == "12" :
                    xs += 1
                    if usuario["nombre_camiseta"] == "si":
                        nombre_12 += 1
                if usuario["talla_camiseta"] == "16" :
                    xs += 1
                    if usuario["nombre_camiseta"] == "si":
                        nombre_16 += 1
                if usuario["talla_camiseta"] == "XS" :
                    xs += 1
                    if usuario["nombre_camiseta"] == "si":
                        nombre_xs += 1
                if usuario["talla_camiseta"] == "S" :
                    s += 1
                    if usuario["nombre_camiseta"] == "si":
                        nombre_s += 1
                if usuario["talla_camiseta"] == "M" :
                    m += 1
                    if usuario["nombre_camiseta"] == "si":
                        nombre_m += 1
                if usuario["talla_camiseta"] == "L" :
                    l += 1
                    if usuario["nombre_camiseta"] == "si":
                        nombre_l += 1
                if usuario["talla_camiseta"] == "XL" :
                    xl += 1
                    if usuario["nombre_camiseta"] == "si":
                        nombre_xl += 1
                if usuario["talla_camiseta"] == "XXL" :
                    xxl += 1
                    if usuario["nombre_camiseta"] == "si":
                        nombre_xxl += 1
                if usuario["talla_camiseta"] == "XXXL" :
                    xxxl += 1
                    if usuario["nombre_camiseta"] == "si":
                        nombre_xxxl += 1

        texto += "--------------------\n"
        texto += "Nº camisetas 12: " + str(doce) + "\t con nombre: " + str(nombre_12) + "\n"
        texto += "Nº camisetas 16: " + str(dieciseis) + "\t con nombre: " + str(nombre_16) + "\n"
        texto += "Nº camisetas XS: " + str(xs) + "\t con nombre: " + str(nombre_xs) + "\n"
        texto += "Nº camisetas S: " + str(s) + "\t con nombre: " + str(nombre_s) + "\n"
        texto += "Nº camisetas M: " + str(m) + "\t con nombre: " + str(nombre_m) + "\n"
        texto += "Nº camisetas L: " + str(l) + "\t con nombre: " + str(nombre_l) + "\n"
        texto += "Nº camisetas XL: " + str(xl) + "\t con nombre: " + str(nombre_xl) + "\n"
        texto += "Nº camisetas XXL: " + str(xxl) + "\t con nombre: " + str(nombre_xxl) + "\n"
        texto += "Nº camisetas XXXL: " + str(xxxl) + "\t con nombre: " + str(nombre_xxxl) + "\n"

        f = open("camisetas.txt", "w")
        f.write(texto)
        f.close()



    def modificar(self):

        dni = self.nifV.get()
        if dni in data:
            usuario = data[dni]
            usuario["nombre"] = self.nombreV.get()
            usuario["fecha_nacimiento"] = self.fechaV.get()
            usuario["telefono"] = self.teléfonoV.get()
            usuario["email"] = self.emailV.get()
            usuario["dir"] = self.dirV.get()
            usuario["localidad"] = self.localV.get()
            usuario["nick"] = self.nickV.get()
            usuario["clan"] = self.clanV.get()
            usuario["nombre_camiseta"] = self.precioV.get()
            usuario["talla_camiseta"] = self.tallaV.get()
            usuario["torneos"] = self.torneosV.get()
            usuario["pagado"] = self.pagadoV.get()
            usuario["sugerencias"] = self.sugerenciasV.get()

            db.child("ParticipantesIV").child(dni).update(usuario)

            return True
        else:
            return False

    def buscar(self):

        dni = self.nifV.get()
        if dni in data:
            usuario = data[dni]
            self.nombreV.set(usuario["nombre"])
            self.fechaV.set(usuario["fecha_nacimiento"])
            self.teléfonoV.set(usuario["telefono"])
            self.emailV.set(usuario["email"])
            self.dirV.set(usuario["dir"])
            self.localV.set(usuario["localidad"])
            self.nickV.set(usuario["nick"])
            self.clanV.set(usuario["clan"])
            self.precioV.set(usuario["nombre_camiseta"])
            self.tallaV.set(usuario["talla_camiseta"])
            self.torneosV.set(usuario["torneos"])
            self.pagadoV.set(usuario["pagado"])
            self.sugerenciasV.set(usuario["sugerencias"])
            self.posV.set(usuario["numero_de_inscripcion"])
            return True
        else:
            showerror('Error', 'No hay ninguna inscripción con ese DNI.')
            return False

    def limpiar(self):

        self.nifE.config(background='white')
        self.nombreE.config(background='white')
        self.fechaE.config(background='white')
        self.teléfonoE.config(background='white')
        self.emailE.config(background='white')
        self.dirE.config(background='white')
        self.localE.config(background='white')
        self.nickE.config(background='white')
        self.clanE.config(background='white')
        self.precioE.config(background='white')
        self.tallaE.config(background='white')
        self.torneosE.config(background='white')
        self.pagadoE.config(background='white')
        self.sugerenciasE.config(background='white')
        self.posE.config(background="white")

        self.nifV.set('')
        self.nombreV.set('')
        self.fechaV.set('')
        self.teléfonoV.set('')
        self.emailV.set('')
        self.dirV.set('')
        self.localV.set('')
        self.nickV.set('')
        self.clanV.set('')
        self.precioV.set('')
        self.tallaV.set('')
        self.torneosV.set('')
        self.pagadoV.set('')
        self.sugerenciasV.set('')
        self.posV.set('')


if __name__ == '__main__':
    master = Tk()
    f = Formulario(master)
    master.mainloop()
