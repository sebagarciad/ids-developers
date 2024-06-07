USE tpintro_dev;

CREATE TABLE IF NOT EXISTS aeropuertos (
    codigo_aeropuerto VARCHAR(3) PRIMARY KEY,
    nombre_aeropuerto VARCHAR(30),
    ciudad VARCHAR(30),
    pais VARCHAR(30)
);

CREATE TABLE IF NOT EXISTS vuelos (
    id_vuelo INT AUTO_INCREMENT PRIMARY KEY,
    codigo_aeropuerto_origen VARCHAR(3),
    codigo_aeropuerto_destino VARCHAR(3),
    hora_salida DATETIME,
    hora_llegada DATETIME,
    duracion INT,
    precio DECIMAL(10, 2),
    pasajes_disponibles INT,
    FOREIGN KEY (codigo_aeropuerto_origen) REFERENCES aeropuertos(codigo_aeropuerto),
    FOREIGN KEY (codigo_aeropuerto_destino) REFERENCES aeropuertos(codigo_aeropuerto)
);


CREATE TABLE IF NOT EXISTS usuarios (
    cuil INT PRIMARY KEY,
    nombre VARCHAR(30),
    apellido VARCHAR(30),
    mail VARCHAR(40) 
);

CREATE TABLE IF NOT EXISTS transacciones (
    num_transaccion INT AUTO_INCREMENT PRIMARY KEY,
    id_vuelo INT,
    total_transaccion DECIMAL(10, 2),
    cuil INT,
    FOREIGN KEY (id_vuelo) REFERENCES vuelos(id_vuelo),
    FOREIGN KEY (cuil) REFERENCES usuarios(cuil)
);



