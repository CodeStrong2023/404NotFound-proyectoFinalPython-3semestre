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

    def eliminar_contacto(self):
        self.mostrar_contactos()
        nombre = input("Ingrese el nombre del contacto que desea buscar: ")
        encontrado = False
        for contacto in self.contactos:
            if contacto.nombre.lower() == nombre.lower():
                encontrado = True
                self.contactos.remove(contacto)
                print(f"El contacto {nombre} ha sido eliminado.")
                self.eliminar_contacto_db(nombre)
                break
        if not encontrado:
            print("Contacto no encontrado.")


    def guardar_agenda(self):
        contactos_guardados = set()
        with open("agenda.txt", "w") as file:
            for contacto in self.contactos:
                if contacto.nombre not in contactos_guardados:
                    file.write(f"{contacto.nombre},{contacto.telefono},{contacto.email}\n")
                    contactos_guardados.add(contacto.nombre)
                else:
                    print(f"El contacto {contacto.nombre} ya existe en la agenda y no se ha guardado nuevamente.")


def menu():
    print("\n1. Agregar contacto")
    print("2. Mostrar contactos")
    print("3. Buscar contacto")
    print("4. Eliminar contacto")
    print("5. Editar contacto")
    print("6. Salir")

def main():
    agenda = Agenda()
    agenda.cargar_agenda()

    while True:
        menu()
        opcion = input("Ingrese el número de la opción que desea realizar: ")

        if opcion == '1':
            agenda.agregar_contacto()
        elif opcion == '2':
            agenda.mostrar_contactos()
        elif opcion == '3':
            agenda.buscar_contacto()
        elif opcion == '4':
            agenda.eliminar_contacto()
        elif opcion == '5':
            agenda.editar_contacto()
        elif opcion == '6':
            print("Saliendo del programa...")
            break

if __name__ == "__main__":
    main()