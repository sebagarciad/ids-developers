USE tpintro_dev;

CREATE TABLE IF NOT EXISTS aeropuertos (
    codigo_aeropuerto VARCHAR(3) PRIMARY KEY,
<<<<<<< HEAD
    nombre_aeropuerto VARCHAR(30),
    ciudad VARCHAR(30),
    pais VARCHAR(30)
=======
    nombre_aeropuerto VARCHAR(50),
    ciudad VARCHAR(40),
    pais VARCHAR(40)
>>>>>>> c8862a5df85513e8a2e4d93dbeb25a6f192b8959
);

CREATE TABLE IF NOT EXISTS vuelos (
    id_vuelo INT AUTO_INCREMENT PRIMARY KEY,
    codigo_aeropuerto_origen VARCHAR(3),
    codigo_aeropuerto_destino VARCHAR(3),
    hora_salida DATETIME,
    hora_llegada DATETIME,
<<<<<<< HEAD
    duracion INT,
=======
    duracion TIME,
>>>>>>> c8862a5df85513e8a2e4d93dbeb25a6f192b8959
    precio DECIMAL(10, 2),
    pasajes_disponibles INT,
    FOREIGN KEY (codigo_aeropuerto_origen) REFERENCES aeropuertos(codigo_aeropuerto),
    FOREIGN KEY (codigo_aeropuerto_destino) REFERENCES aeropuertos(codigo_aeropuerto)
);


CREATE TABLE IF NOT EXISTS usuarios (
<<<<<<< HEAD
    cuil INT PRIMARY KEY,
    nombre VARCHAR(30),
    apellido VARCHAR(30),
    mail VARCHAR(40) 
=======
    dni INT PRIMARY KEY,
    nombre VARCHAR(30),
    apellido VARCHAR(30),
    mail VARCHAR(40)
>>>>>>> c8862a5df85513e8a2e4d93dbeb25a6f192b8959
);

CREATE TABLE IF NOT EXISTS transacciones (
    num_transaccion INT AUTO_INCREMENT PRIMARY KEY,
    id_vuelo INT,
    total_transaccion DECIMAL(10, 2),
<<<<<<< HEAD
    cuil INT,
    FOREIGN KEY (id_vuelo) REFERENCES vuelos(id_vuelo),
    FOREIGN KEY (cuil) REFERENCES usuarios(cuil)
);



=======
    dni INT,
    FOREIGN KEY (id_vuelo) REFERENCES vuelos(id_vuelo),
    FOREIGN KEY (dni) REFERENCES usuarios(dni)
);


INSERT INTO usuarios VALUES (40123456, 'Juan', 'Perez', 'juanperez@gmail.com');

INSERT INTO aeropuertos VALUES ('BUE', 'Aeropuerto de Buenos Aires ', 'Buenos Aires', 'Argentina');
INSERT INTO aeropuertos VALUES ('BCR', 'Aeropuerto de Bariloche', 'Bariloche', 'Argentina');
INSERT INTO aeropuertos VALUES ('COR', 'Aeropuerto de Cordoba', 'Cordoba', 'Argentina');
INSERT INTO aeropuertos VALUES ('MDZ', 'Aeropuerto de Mendoza', 'Mendoza', 'Argentina');
INSERT INTO aeropuertos VALUES ('NQN', 'Aeropuerto de Neuquen', 'Neuquen', 'Argentina');
INSERT INTO aeropuertos VALUES ('USH', 'Aeropuerto de Ushuaia', 'Ushuaia', 'Argentina');
INSERT INTO aeropuertos VALUES ('SLA', 'Aeropuerto de Salta', 'Salta', 'Argentina');

INSERT INTO vuelos (codigo_aeropuerto_origen, codigo_aeropuerto_destino, hora_salida, hora_llegada, duracion, precio, pasajes_disponibles)
VALUES ('BUE','BCR','2024-06-20 14:30:00','2024-06-20 16:30:00','02:00:00',300000.00,150)
;

INSERT INTO vuelos (codigo_aeropuerto_origen, codigo_aeropuerto_destino, hora_salida, hora_llegada, duracion, precio, pasajes_disponibles)
VALUES ('BUE','COR','2024-06-20 14:30:00','2024-06-20 16:30:00','02:00:00',250000.00,150)
;

INSERT INTO vuelos (codigo_aeropuerto_origen, codigo_aeropuerto_destino, hora_salida, hora_llegada, duracion, precio, pasajes_disponibles)
VALUES ('BUE','MDZ','2024-06-20 14:00:00','2024-06-20 16:30:00','02:30:00',350000.00,150)
;

INSERT INTO vuelos (codigo_aeropuerto_origen, codigo_aeropuerto_destino, hora_salida, hora_llegada, duracion, precio, pasajes_disponibles)
VALUES ('BUE','USH','2024-06-20 13:30:00','2024-06-20 16:30:00','03:00:00',400000.00,150)
;

INSERT INTO vuelos (codigo_aeropuerto_origen, codigo_aeropuerto_destino, hora_salida, hora_llegada, duracion, precio, pasajes_disponibles)
VALUES ('COR','BUE','2024-06-20 14:30:00','2024-06-20 16:30:00','02:00:00',300000.00,150)
;

INSERT INTO vuelos (codigo_aeropuerto_origen, codigo_aeropuerto_destino, hora_salida, hora_llegada, duracion, precio, pasajes_disponibles)
VALUES ('BUE','SLA','2024-06-20 14:30:00','2024-06-20 16:30:00','02:00:00',150000.00,150)
;

INSERT INTO vuelos (codigo_aeropuerto_origen, codigo_aeropuerto_destino, hora_salida, hora_llegada, duracion, precio, pasajes_disponibles)
VALUES ('MDZ','BUE','2024-06-20 14:30:00','2024-06-20 16:30:00','02:00:00',300000.00,150)
;

INSERT INTO vuelos (codigo_aeropuerto_origen, codigo_aeropuerto_destino, hora_salida, hora_llegada, duracion, precio, pasajes_disponibles)
VALUES ('USH','BUE','2024-06-20 14:30:00','2024-06-20 16:30:00','02:00:00',300000.00,150)
;

INSERT INTO vuelos (codigo_aeropuerto_origen, codigo_aeropuerto_destino, hora_salida, hora_llegada, duracion, precio, pasajes_disponibles)
VALUES ('BUE','NQN','2024-06-20 14:30:00','2024-06-20 16:30:00','02:00:00',300000.00,150)
;
>>>>>>> c8862a5df85513e8a2e4d93dbeb25a6f192b8959
