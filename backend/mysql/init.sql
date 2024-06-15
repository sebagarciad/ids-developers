USE tpintro_dev;

CREATE TABLE IF NOT EXISTS aeropuertos (
    codigo_aeropuerto VARCHAR(3) PRIMARY KEY,
    nombre_aeropuerto VARCHAR(50),
    ciudad VARCHAR(40),
    pais VARCHAR(40)
);

CREATE TABLE IF NOT EXISTS vuelos (
id_vuelo INT AUTO_INCREMENT PRIMARY KEY,
codigo_aeropuerto_origen VARCHAR(3),
codigo_aeropuerto_destino VARCHAR(3),
fecha_salida DATE,
fecha_llegada DATE,
hora_salida TIME,
hora_llegada TIME,
duracion TIME,
precio DECIMAL(10, 2),
pasajes_disponibles INT,
FOREIGN KEY (codigo_aeropuerto_origen) REFERENCES aeropuertos (codigo_aeropuerto),
FOREIGN KEY (codigo_aeropuerto_destino) REFERENCES aeropuertos (codigo_aeropuerto)
);


CREATE TABLE IF NOT EXISTS usuarios (
    dni INT PRIMARY KEY,
    nombre VARCHAR(30),
    apellido VARCHAR(30),
    mail VARCHAR(40)
);

CREATE TABLE IF NOT EXISTS transacciones (
    num_transaccion INT AUTO_INCREMENT PRIMARY KEY,
    id_vuelo INT,
    total_transaccion DECIMAL(10, 2),
    dni INT,
    FOREIGN KEY (id_vuelo) REFERENCES vuelos(id_vuelo),
    FOREIGN KEY (dni) REFERENCES usuarios(dni)
);


INSERT INTO usuarios VALUES (40123456, 'Juan', 'Perez', 'juanperez@gmail.com');

INSERT INTO aeropuertos (codigo_aeropuerto, nombre_aeropuerto, ciudad, pais) VALUES 
('BUE', 'Aeropuerto de Buenos Aires', 'Buenos Aires', 'Argentina'),
('BCR', 'Aeropuerto de Bariloche', 'Bariloche', 'Argentina'),
('COR', 'Aeropuerto de Cordoba', 'Cordoba', 'Argentina'),
('MDZ', 'Aeropuerto de Mendoza', 'Mendoza', 'Argentina'),
('NQN', 'Aeropuerto de Neuquen', 'Neuquen', 'Argentina'),
('USH', 'Aeropuerto de Ushuaia', 'Ushuaia', 'Argentina'),
('SLA', 'Aeropuerto de Salta', 'Salta', 'Argentina');

INSERT INTO vuelos (codigo_aeropuerto_origen, codigo_aeropuerto_destino, fecha_salida, fecha_llegada, hora_salida, hora_llegada, duracion, precio, pasajes_disponibles)
VALUES 
('BUE', 'BCR', '2024-07-20', '2024-07-20', '14:30:00', '16:30:00', '02:00:00', 300000.00, 150),
('BUE', 'COR', '2024-07-20', '2024-07-20', '14:30:00', '16:30:00', '02:00:00', 250000.00, 150),
('BUE', 'MDZ', '2024-07-20', '2024-07-20', '14:00:00', '16:30:00', '02:30:00', 350000.00, 150),
('BUE', 'USH', '2024-07-20', '2024-07-20', '13:30:00', '16:30:00', '03:00:00', 400000.00, 150),
('COR', 'BUE', '2024-07-20', '2024-07-20', '14:30:00', '16:30:00', '02:00:00', 300000.00, 150),
('BUE', 'SLA', '2024-07-20', '2024-07-20', '14:30:00', '16:30:00', '02:00:00', 150000.00, 150),
('MDZ', 'BUE', '2024-07-20', '2024-07-20', '14:30:00', '16:30:00', '02:00:00', 300000.00, 150),
('USH', 'BUE', '2024-07-20', '2024-07-20', '14:30:00', '16:30:00', '02:00:00', 300000.00, 150),
('BUE', 'NQN', '2024-07-20', '2024-07-20', '14:30:00', '16:30:00', '02:00:00', 300000.00, 150),
('BCR', 'BUE', '2024-07-21', '2024-07-21', '14:30:00', '16:30:00', '02:00:00', 300000.00, 150),
('COR', 'MDZ', '2024-07-21', '2024-07-21', '14:30:00', '16:30:00', '02:00:00', 250000.00, 150),
('MDZ', 'COR', '2024-07-21', '2024-07-21', '14:30:00', '16:30:00', '02:00:00', 350000.00, 150),
('USH', 'COR', '2024-07-21', '2024-07-21', '14:30:00', '16:30:00', '02:00:00', 400000.00, 150),
('COR', 'SLA', '2024-07-21', '2024-07-21', '14:30:00', '16:30:00', '02:00:00', 300000.00, 150),
('SLA', 'BUE', '2024-07-21', '2024-07-21', '14:30:00', '16:30:00', '02:00:00', 150000.00, 150),
('NQN', 'BUE', '2024-07-21', '2024-07-21', '14:30:00', '16:30:00', '02:00:00', 300000.00, 150),
('USH', 'MDZ', '2024-07-21', '2024-07-21', '14:30:00', '16:30:00', '02:00:00', 300000.00, 150),
('SLA', 'MDZ', '2024-07-21', '2024-07-21', '14:30:00', '16:30:00', '02:00:00', 300000.00, 150);