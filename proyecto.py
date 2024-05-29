def editar_contacto_db(self, contacto):
    query = "UPDATE contactos SET telefono = %s, email = %s, favorito = %s WHERE nombre = %s"
    values = (contacto.telefono, contacto.email, contacto.favorito, contacto.nombre)
    self.cursor.execute(query, values)
    self.db_connection.commit()