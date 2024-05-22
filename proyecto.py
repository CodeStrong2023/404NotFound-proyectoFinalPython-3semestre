import mysql.connector
import re


class Contacto:
    def __init__(self, nombre, telefono, email):
        self.nombre = nombre
        self.telefono = telefono
        self.email = email
        self.favorito = False


class Agenda:
    def __init__(self):
        self.contactos = []
        self.db_connection = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="ignacio",
            database="agenda_contactos"
        )
        self.cursor = self.db_connection.cursor()

    def validarNumero(self, telefono):
        while not telefono.isdigit():
            print("El número de teléfono debe contener números")
            telefono = input("Ingrese el número de teléfono del contacto: ")
        return telefono
        
    def agregar_contacto(self):
        while True:
            nombre = input("Ingrese el nombre del contacto: ")
            telefono = input("Ingrese el número de teléfono del contacto: ")
            telefono = self.validarNumero(telefono)
            email = input("Ingrese el email del contacto: ")
            
            if re.match(r"[^@]+@[^@]+\.[^@]+", email):
                nuevo_contacto = Contacto(nombre, telefono, email)
                
                exists = any(contacto.nombre == nombre or contacto.email == email or contacto.telefono == telefono for contacto in self.contactos)
                if exists:
                    print("El contacto ya existe.")
                    return False
                else:
                    favorito = input("¿Desea marcar el contacto como favorito? (s/n): ").lower()
                    if favorito == "s":
                        nuevo_contacto.favorito = True
                    elif favorito == "n":
                        nuevo_contacto.favorito = False
                    self.contactos.append(nuevo_contacto)
                    self.guardar_agenda_db(nuevo_contacto)
                    print("Contacto agregado correctamente.")
                    return True
            else:
                print("El formato del correo electrónico no es válido. Por favor, inténtelo nuevamente.")