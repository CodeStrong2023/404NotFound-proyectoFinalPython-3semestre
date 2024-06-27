import mysql.connector  # Importa el módulo mysql.connector para interactuar con MySQL desde Python
import re  # Importa el módulo re para utilizar expresiones regulares en el manejo de cadenas


class Contacto:  # Esta clase representa un contacto en la agenda.
    def __init__(self, id, nombre, telefono, email):
        self.id = id
        self.nombre = nombre
        self.telefono = telefono
        self.email = email
        self.favorito = False

    def __str__(self):
        return f"ID: {self.id}, Nombre: {self.nombre}, Teléfono: {self.telefono}, Email: {self.email}"


class Agenda:
    def __init__(self):
        self.contactos = []
        self.db_connection = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="ignacio",
            database="agenda_contactos"
        )
        self.cursor = self.db_connection.cursor()  # El cursor se utiliza para ejecutar instrucciones SQL y recuperar datos.

    def validarNumero(self, telefono):
        while not telefono.isdigit():
            print("El número de teléfono debe contener números.")
            telefono = input("Ingrese el número de teléfono del contacto: ")
        return telefono

    def agregar_contacto(self):
        while True:
            nombre = input("\nIngrese el nombre del contacto: ")
            telefono = input("Ingrese el número de teléfono del contacto: ")
            telefono = self.validarNumero(telefono)
            email = input("Ingrese el email del contacto: ")

            if re.match(r"[^@]+@[^@]+\.[^@]+", email):
                # Genera un ID incremental basado en la cantidad de contactos existentes
                id_contacto = len(self.contactos) + 1
                nuevo_contacto = Contacto(id_contacto, nombre, telefono, email)

                exists = any(
                    contacto.nombre == nombre or contacto.email == email or contacto.telefono == telefono for contacto
                    in self.contactos)
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
                    print("\nContacto agregado correctamente!")
                    return True
            else:
                print("\nEl formato del correo electrónico no es válido. Por favor, inténtelo nuevamente.")

    def mostrar_contactos(self):
        if self.contactos:
            for contacto in self.contactos:
                if contacto.favorito:
                    print(f"{contacto} (Favorito)")
                else:
                    print(contacto)
        else:
            print("\nNo hay contactos en la agenda.")

    def buscar_contacto(self):
        self.mostrar_contactos()
        nombre = input("\nIngrese el nombre del contacto que desea buscar: ")
        encontrado = False
        for contacto in self.contactos:
            if contacto.nombre.lower() == nombre.lower():  # Comparamos nombres en minúsculas
                encontrado = True
                if contacto.favorito:
                    print(f"\n{contacto} (Favorito)")
                else:
                    print(contacto)
        if not encontrado:
            print("\n***Contacto no encontrado***")

    def eliminar_contacto(self):
        self.mostrar_contactos()
        nombre = input("\nIngrese el nombre del contacto que desea eliminar: ")
        encontrado = False
        for contacto in self.contactos:
            if contacto.nombre.lower() == nombre.lower():
                encontrado = True
                self.contactos.remove(contacto)
                print(f"\nEl contacto {nombre} ha sido eliminado.")
                self.eliminar_contacto_db(nombre)  # Se elimina el contacto de la base de datos
                break
        if not encontrado:
            print("\n***Contacto no encontrado***")

    def editar_contacto(self):
        self.mostrar_contactos()
        nombre = input("\nIngrese el nombre del contacto que desea editar: ")
        encontrado = False
        for contacto in self.contactos:
            if str(contacto.nombre) == nombre:
                encontrado = True
                print("Editar contacto:")
                nuevo_nombre = input(f"Nuevo nombre ({contacto.nombre}): ") or contacto.nombre
                nuevo_telefono = input(f"Nuevo teléfono ({contacto.telefono}): ") or contacto.telefono
                nuevo_email = input(f"Nuevo email ({contacto.email}): ") or contacto.email
                favorito = input("¿Desea marcar el contacto como favorito? (s/n): ").lower()
                # Se actualizan los atributos del contacto con los nuevos valores
                contacto.nombre = nuevo_nombre
                contacto.telefono = nuevo_telefono
                contacto.email = nuevo_email
                if favorito == "s":
                    contacto.favorito = True
                elif favorito == "n":
                    contacto.favorito = False
                print("¡Contacto actualizado correctamente! ")
                self.editar_contacto_db(contacto)
                break
        if not encontrado:
            print("\n¡Contacto no encontrado!")

    def guardar_agenda_db(self, contacto):
        query = "INSERT INTO contactos (nombre, telefono, email, favorito) VALUES (%s, %s, %s, %s)"  # Insertamos un nuevo registro
        values = (contacto.nombre, contacto.telefono, contacto.email, contacto.favorito)
        self.cursor.execute(query, values)
        self.db_connection.commit()

    def eliminar_contacto_db(self, nombre):
        query = "DELETE FROM contactos WHERE nombre = %s"
        values = (nombre,)
        self.cursor.execute(query, values)
        self.db_connection.commit()

    def editar_contacto_db(self, contacto):
        query = "UPDATE contactos SET nombre = %s, telefono = %s, email = %s, favorito = %s WHERE id = %s"
        values = (contacto.nombre, contacto.telefono, contacto.email, contacto.favorito, contacto.id)
        self.cursor.execute(query, values)  # Ejecutamos la consulta SQL
        self.db_connection.commit()  # Aplicamos los cambios en la base de datos

    def cargar_agenda(self):
        query = "SELECT id, nombre, telefono, email, favorito FROM contactos"
        self.cursor.execute(query)
        for id, nombre, telefono, email, favorito in self.cursor.fetchall():  # Obtiene todas las filas resultantes de la consulta
            contacto = Contacto(id, nombre, telefono, email)
            contacto.favorito = favorito
            self.contactos.append(contacto)  # Con append se agrega el objeto Contacto creado a la lista


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
            break  # Rompe el bucle


if __name__ == "__main__":  # Llama a la función main() cuando el script se ejecuta directamente desde la línea de comandos
    main()
