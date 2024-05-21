CREATE DATABASE agenda_contactos;
USE agenda_contactos;
CREATE TABLE contactos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    telefono VARCHAR(20),
    email VARCHAR(255) NOT NULL,
    favorito BOOLEAN
);