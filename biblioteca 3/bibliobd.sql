-- Seleccionar o crear la base de datos bibliodb
USE bibliodb;

-- Crear la tabla libros
CREATE TABLE IF NOT EXISTS libros (
    libro_id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    ISBN VARCHAR(40) NOT NULL,
    Título VARCHAR(40) NOT NULL,
    Categoría VARCHAR(40) NOT NULL,
    Subcategoría VARCHAR(40) NOT NULL,
    Autor VARCHAR(40) NOT NULL,
    Editorial VARCHAR(40) NOT NULL,
    Descripción VARCHAR(100) NOT NULL
);

-- Insertar datos en la tabla libros
INSERT INTO libros (ISBN, Título, Categoría, Subcategoría, Autor, Editorial, Descripción)
VALUES 
('978-987-3863-45-5', 'La Sombra de su secreto', 'Novela', 'Romántica', 'Cardoza Claudia', 'Vestalles', 'El amor surge entre dos personas con secretos'),
('978-84-16363-87-2', 'Sin límites', 'Novela', 'Novela Negra', 'Adler-Olsen Jussi', 'MAEVA', 'Oscuro asesinato no resuelto'),
('978-987-8474-16-8', 'Robada', 'Novela', 'Thriller Psicológico', 'Stimson Tess', 'MOTUS', 'Atrapante libro ¿Quien se llevó a Lottie?');

-- Crear la tabla socios
CREATE TABLE IF NOT EXISTS socios (
    id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    apellido VARCHAR(40) NOT NULL,
    nombre VARCHAR(40) NOT NULL,
    dni VARCHAR(20) NOT NULL,  -- Identificación única del socio
    domicilio VARCHAR(100) NOT NULL,
    fechadepago DATE NOT NULL,  -- Cambiado a tipo DATE
    telefono VARCHAR(20) NOT NULL,
    sexo ENUM('Masculino', 'Femenino') NOT NULL  -- Uso de ENUM para valores controlados
);

-- Insertar datos en la tabla socios
INSERT INTO socios (apellido, nombre, dni, domicilio, fechadepago, telefono, sexo)
VALUES
('Carrasco', 'Pedro', '12345678', 'Aconcagua 200', '2024-11-13', '0000000', 'Masculino'),
('Pedraza', 'Juan', '87654321', 'Mitre 500', '2024-11-10', '1111111', 'Masculino'),
('Lopez', 'Ana', '22334455', 'Belgrano 750', '2024-11-15', '2222222', 'Femenino');

-- Crear la tabla prestamos con claves foráneas
CREATE TABLE IF NOT EXISTS prestamos (
    id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    socio_id INT NOT NULL,
    libro_id INT NOT NULL,
    Fecha_de_devolucion DATE NOT NULL,
    Estado ENUM('Pendiente', 'Devuelto') NOT NULL,
    
    -- Clave foránea que se refiere a la tabla socios
    FOREIGN KEY (socio_id) REFERENCES socios(id) ON DELETE CASCADE,
    
    -- Clave foránea que se refiere a la tabla libros
    FOREIGN KEY (libro_id) REFERENCES libros(libro_id) ON DELETE CASCADE
);

-- Insertar datos en la tabla prestamos
INSERT INTO prestamos (socio_id, libro_id, Fecha_de_devolucion, Estado)
VALUES
(1, 2, '2024-12-15', 'Pendiente'),  -- Pedro con el libro 'Sin límites'
(2, 3, '2024-12-20', 'Pendiente'),  -- Juan con el libro 'Robada'
(1, 3, '2024-12-25', 'Pendiente'),  -- Pedro con el libro 'Robada'
(3, 1, '2024-12-18', 'Pendiente'),  -- Ana con el libro 'La Sombra de su secreto'
(2, 1, '2024-12-10', 'Pendiente'),  -- Juan con el libro 'La Sombra de su secreto'
(3, 2, '2024-12-22', 'Pendiente'),  -- Ana con el libro 'Sin límites'
(1, 1, '2024-12-01', 'Pendiente'),  -- Pedro con el libro 'La Sombra de su secreto'
(2, 2, '2024-12-05', 'Pendiente'),  -- Juan con el libro 'Sin límites'
(3, 3, '2024-12-12', 'Pendiente'),  -- Ana con el libro 'Robada'
(1, 3, '2024-12-07', 'Pendiente'),  -- Pedro con el libro 'Robada'
(2, 1, '2024-12-15', 'Pendiente'),  -- Juan con el libro 'La Sombra de su secreto'
(3, 2, '2024-12-20', 'Pendiente');  -- Ana con el libro 'Sin límites'

-- Consultar las tablas para verificar los datos
SELECT * FROM libros;
SELECT * FROM socios;
SELECT * FROM prestamos;

-- Consulta para obtener los detalles completos de los préstamos
SELECT 
    p.id AS Prestamo_ID, 
    s.nombre AS Socio_Nombre, 
    s.apellido AS Socio_Apellido, 
    s.dni AS Socio_DNI, 
    l.Título AS Libro_Título, 
    l.ISBN AS Libro_ISBN, 
    p.Fecha_de_devolucion, 
    p.Estado
FROM prestamos p
JOIN socios s ON p.socio_id = s.id
JOIN libros l ON p.libro_id = l.libro_id;

SELECT DISTINCT 
    p.id AS Prestamo_ID, 
    s.nombre AS Socio_Nombre, 
    s.apellido AS Socio_Apellido, 
    s.dni AS Socio_DNI, 
    l.Título AS Libro_Título, 
    l.ISBN AS Libro_ISBN, 
    p.Fecha_de_devolucion, 
    p.Estado
FROM prestamos p
JOIN socios s ON p.socio_id = s.id
JOIN libros l ON p.libro_id = l.libro_id;
