-- Aseguramos el uso de la base de datos
CREATE DATABASE IF NOT EXISTS presupuesto;
USE presupuesto;

-- ==========================================================
-- 1. ESTRUCTURA ORIGINAL (Mantenida según tu requerimiento)
-- ==========================================================

CREATE TABLE IF NOT EXISTS clientes (
    id_cliente INT AUTO_INCREMENT PRIMARY KEY,
    razon_social VARCHAR(150) NOT NULL,
    cuit_cuil VARCHAR(20) NOT NULL UNIQUE,
    rubro VARCHAR(100),
    direccion VARCHAR(255),
    localidad VARCHAR(100),
    provincia VARCHAR(100),
    fecha_alta TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS tipos_servicio (
    id_tipo_servicio INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    activo BOOLEAN DEFAULT TRUE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS presupuestos (
    id_presupuesto INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT NOT NULL,
    fecha_emision TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total DECIMAL(10, 2) NOT NULL,
    estado ENUM('Pendiente', 'Aprobado', 'Rechazado') DEFAULT 'Pendiente',
    observaciones TEXT,
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS presupuesto_detalle (
    id_detalle INT AUTO_INCREMENT PRIMARY KEY,
    id_presupuesto INT NOT NULL,
    id_tipo_servicio INT NOT NULL,
    cantidad INT DEFAULT 1,
    FOREIGN KEY (id_presupuesto) REFERENCES presupuestos(id_presupuesto) ON DELETE CASCADE,
    FOREIGN KEY (id_tipo_servicio) REFERENCES tipos_servicio(id_tipo_servicio)
) ENGINE=InnoDB;

-- ==========================================================
-- 2. NUEVAS TABLAS DE ESPECIALIZACIÓN (Extensiones Técnicas)
-- ==========================================================

-- Tabla para Medición de Ruido y Medición de Iluminación
CREATE TABLE IF NOT EXISTS detalle_mediciones (
    id_detalle_medicion INT AUTO_INCREMENT PRIMARY KEY,
    id_detalle INT NOT NULL,
    kilometros DECIMAL(8, 2) DEFAULT 0.00,
    precio_km DECIMAL(10, 2) DEFAULT 600.00,
    cantidad_puestos INT DEFAULT 0,
    precio_por_puesto DECIMAL(10, 2) DEFAULT 0.00,
    requiere_croquis BOOLEAN DEFAULT FALSE,
    precio_croquis DECIMAL(10, 2) DEFAULT 0.00,
    FOREIGN KEY (id_detalle) REFERENCES presupuesto_detalle(id_detalle) ON DELETE CASCADE
) ENGINE=InnoDB;

-- Tabla para RGRL
CREATE TABLE IF NOT EXISTS detalle_rgrl (
    id_detalle_rgrl INT AUTO_INCREMENT PRIMARY KEY,
    id_detalle INT NOT NULL,
    kilometros DECIMAL(8, 2) DEFAULT 0.00,
    precio_km DECIMAL(10, 2) DEFAULT 600.00,
    cantidad_horas INT DEFAULT 0,
    precio_por_hora DECIMAL(10, 2) DEFAULT 0.00,
    FOREIGN KEY (id_detalle) REFERENCES presupuesto_detalle(id_detalle) ON DELETE CASCADE
) ENGINE=InnoDB;

-- Tabla para Capacitación
CREATE TABLE IF NOT EXISTS detalle_capacitacion (
    id_detalle_cap INT AUTO_INCREMENT PRIMARY KEY,
    id_detalle INT NOT NULL,
    kilometros DECIMAL(8, 2) DEFAULT 0.00,
    precio_km DECIMAL(10, 2) DEFAULT 600.00,
    valor_capacitacion DECIMAL(10, 2) DEFAULT 0.00,
    FOREIGN KEY (id_detalle) REFERENCES presupuesto_detalle(id_detalle) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ==========================================================
-- 3. CARGA DE CATÁLOGO DE SERVICIOS (Ajustado)
-- ==========================================================
-- Se eliminó la tarifa_base ya que ahora el precio se calcula dinámicamente

INSERT INTO tipos_servicio (nombre, descripcion) VALUES
('Medición de Iluminación', 'Protocolo SRT 84/12. Evaluación de niveles de iluminancia.'),
('Medición de Ruido', 'Protocolo SRT 85/12. Evaluación de nivel sonoro continuo equivalente.'),
('Asesoramiento Presencial', 'Visita técnica a planta y relevamiento de riesgos.'),
('Asesoramiento Virtual', 'Consultoría remota sobre normativa de Higiene y Seguridad.'),
('Carga de Matafuegos', 'Servicio de mantenimiento y recarga de extintores.'),
('RGRL', 'Relevamiento General de Riesgos Laborales obligatorio para ART.'),
('Capacitación', 'Dictado de cursos sobre prevención y uso de EPP.');

-- ==========================================================
-- 4. CARGA MASIVA DE 100 CLIENTES FICTICIOS
-- ==========================================================

DELIMITER //
CREATE PROCEDURE PoblarClientes()
BEGIN
    DECLARE i INT DEFAULT 1;
    WHILE i <= 100 DO
        INSERT INTO clientes (razon_social, cuit_cuil, rubro, direccion, localidad, provincia)
        VALUES (
            CONCAT('Empresa ', i, CASE MOD(i,3) WHEN 0 THEN ' S.A.' WHEN 1 THEN ' SRL' ELSE ' S.H.' END),
            CONCAT('30-', LPAD(i + 20000000, 8, '0'), '-', MOD(i, 9)),
            CASE MOD(i, 4) 
                WHEN 0 THEN 'Vitivinícola' 
                WHEN 1 THEN 'Metalúrgica' 
                WHEN 2 THEN 'Logística' 
                ELSE 'Servicios Industriales' 
            END,
            CONCAT('Av. Libertador ', i * 10),
            CASE MOD(i, 3) 
                WHEN 0 THEN 'San Miguel de Tucumán' 
                WHEN 1 THEN 'Yerba Buena' 
                ELSE 'Concepción' 
            END,
            'Tucumán'
        );
        SET i = i + 1;
    END WHILE;
END //
DELIMITER ;

-- Ejecutamos la carga y eliminamos el procedimiento
CALL PoblarClientes();
DROP PROCEDURE PoblarClientes;

-- Verificación de resultados
SELECT 'Servicios' as Tabla, COUNT(*) as Registros FROM tipos_servicio
UNION
SELECT 'Clientes' as Tabla, COUNT(*) as Registros FROM clientes;