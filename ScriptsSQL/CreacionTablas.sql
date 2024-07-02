-- Tabla Cliente
CREATE TABLE Cliente (
    cliente_id SERIAL PRIMARY KEY,
    nombre VARCHAR(20),
    apellido VARCHAR(20),
    direccion VARCHAR(100),
    telefono CHAR(10),
    email VARCHAR(30) UNIQUE,
    pais VARCHAR(100)
);
SELECT * FROM Cliente;

-- Tabla Empleado
CREATE TABLE Empleado (
    empleado_id SERIAL PRIMARY KEY,
    nombre VARCHAR(20),
    apellido VARCHAR(20),
    cargo CHAR(20),
    fecha_contratacion DATE
);
SELECT * FROM Empleado;

-- Tabla Entrega
CREATE TABLE Entrega (
    entrega_id SERIAL PRIMARY KEY,
    metodo_entrega CHAR(50),
    descripcion VARCHAR(200)
);
SELECT * FROM Entrega;

-- Tabla Pedido
CREATE TABLE Pedido (
    pedido_id SERIAL PRIMARY KEY,
    cliente_id INT REFERENCES Cliente(cliente_id),
    empleado_id INT REFERENCES Empleado(empleado_id),
    entrega_id INT REFERENCES Entrega(entrega_id),
    fecha_pedido DATE,
    fecha_envio DATE,
    estado VARCHAR(30)
);
SELECT * FROM Pedido;

-- Tabla Proveedor
CREATE TABLE Proveedor (
    proveedor_id SERIAL PRIMARY KEY,
    nombre VARCHAR(20),
    direccion VARCHAR(100),
    telefono CHAR(10),
    email VARCHAR(80) UNIQUE
);
SELECT * FROM Proveedor;

-- Tabla Flor
CREATE TABLE Flor (
    flor_id SERIAL PRIMARY KEY,
    proveedor_id INT REFERENCES Proveedor(proveedor_id),
    nombre VARCHAR(20),
    especie VARCHAR(20),
    color VARCHAR(20),
    precio_unitario DECIMAL(10, 2),
    descripcion VARCHAR(200)
);
SELECT * FROM Flor;

-- Tabla Cultivo
CREATE TABLE Cultivo (
    cultivo_id SERIAL PRIMARY KEY,
    fecha_siembra DATE,
    fecha_cosecha DATE,
    cantidad_cosechada INT,
    UNIQUE (fecha_siembra, fecha_cosecha)
);
SELECT * FROM Cultivo;

-- Tabla Lote
CREATE TABLE Lote (
    lote_id SERIAL PRIMARY KEY,
    nombre VARCHAR(30),
    numero_lote INT,
    tamano DECIMAL(10, 2),
    tipo CHAR(30),
    UNIQUE (nombre, numero_lote)
);
SELECT * FROM Lote;

-- Tabla CultivoLote
CREATE TABLE CultivoLote (
    cultivo_id INT,
    lote_id INT,
    PRIMARY KEY (cultivo_id, lote_id),
    FOREIGN KEY (cultivo_id) REFERENCES Cultivo(cultivo_id),
    FOREIGN KEY (lote_id) REFERENCES Lote(lote_id)
);
SELECT * FROM CultivoLote;

-- Tabla LoteFlor
CREATE TABLE LoteFlor (
    lote_id INT,
    flor_id INT,
    PRIMARY KEY (lote_id, flor_id),
    FOREIGN KEY (lote_id) REFERENCES Lote(lote_id),
    FOREIGN KEY (flor_id) REFERENCES Flor(flor_id)
);
SELECT * FROM LoteFlor;

-- Tabla FlorPedido
CREATE TABLE FlorPedido (
    pedido_id INT,
    flor_id INT,
    cantidad INT,
    PRIMARY KEY (pedido_id, flor_id),
    FOREIGN KEY (pedido_id) REFERENCES Pedido(pedido_id),
    FOREIGN KEY (flor_id) REFERENCES Flor(flor_id)
);
SELECT * FROM FlorPedido;