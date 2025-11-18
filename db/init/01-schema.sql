-- ============================================================================
-- Script de Inicialización de Base de Datos
-- Sistema de Gestión de Citas Médicas
-- ============================================================================
-- Curso: Base de Datos 2025-30-2497
-- Fecha: Noviembre 2025
-- ============================================================================

\c clinica_citas;

-- ============================================================================
-- TABLAS PRINCIPALES
-- ============================================================================

-- Tabla: USUARIO
CREATE TABLE IF NOT EXISTS usuario (
    id_usuario SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    telefono VARCHAR(20) NOT NULL UNIQUE,
    contraseña VARCHAR(255) NOT NULL,
    rol VARCHAR(20) NOT NULL CHECK (rol IN ('ADMIN', 'MEDICO', 'PACIENTE')),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    activo BOOLEAN DEFAULT TRUE
);

-- Tabla: ESPECIALIDAD
CREATE TABLE IF NOT EXISTS especialidad (
    id_especialidad SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    descripcion TEXT,
    activo BOOLEAN DEFAULT TRUE
);

-- Tabla: PACIENTE
CREATE TABLE IF NOT EXISTS paciente (
    id_paciente SERIAL PRIMARY KEY,
    id_usuario INTEGER NOT NULL UNIQUE,
    fecha_nacimiento DATE NOT NULL,
    direccion TEXT,
    
    CONSTRAINT fk_paciente_usuario 
        FOREIGN KEY (id_usuario) 
        REFERENCES usuario(id_usuario)
        ON DELETE CASCADE
);

-- Tabla: MEDICO
CREATE TABLE IF NOT EXISTS medico (
    id_medico SERIAL PRIMARY KEY,
    id_usuario INTEGER NOT NULL UNIQUE,
    id_especialidad INTEGER NOT NULL,
    registro_profesional VARCHAR(50) NOT NULL UNIQUE,
    activo BOOLEAN DEFAULT TRUE,
    
    CONSTRAINT fk_medico_usuario 
        FOREIGN KEY (id_usuario) 
        REFERENCES usuario(id_usuario)
        ON DELETE CASCADE,
    
    CONSTRAINT fk_medico_especialidad 
        FOREIGN KEY (id_especialidad) 
        REFERENCES especialidad(id_especialidad)
);

-- Tabla: HORARIO_MEDICO
CREATE TABLE IF NOT EXISTS horario_medico (
    id_horario SERIAL PRIMARY KEY,
    id_medico INTEGER NOT NULL,
    dia_semana INTEGER NOT NULL CHECK (dia_semana BETWEEN 1 AND 7),
    hora_inicio TIME NOT NULL,
    hora_fin TIME NOT NULL,
    activo BOOLEAN DEFAULT TRUE,
    
    CONSTRAINT fk_horario_medico 
        FOREIGN KEY (id_medico) 
        REFERENCES medico(id_medico)
        ON DELETE CASCADE,
    
    CONSTRAINT chk_hora_valida 
        CHECK (hora_inicio < hora_fin)
);

-- Tabla: CITA
CREATE TABLE IF NOT EXISTS cita (
    id_cita SERIAL PRIMARY KEY,
    id_paciente INTEGER NOT NULL,
    id_medico INTEGER NOT NULL,
    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    motivo TEXT NOT NULL,
    estado VARCHAR(20) NOT NULL DEFAULT 'AGENDADA'
        CHECK (estado IN ('AGENDADA', 'CANCELADA', 'REPROGRAMADA', 'ATENDIDA')),
    observaciones TEXT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_cita_paciente 
        FOREIGN KEY (id_paciente) 
        REFERENCES paciente(id_paciente),
    
    CONSTRAINT fk_cita_medico 
        FOREIGN KEY (id_medico) 
        REFERENCES medico(id_medico),
    
    CONSTRAINT uq_medico_fecha_hora 
        UNIQUE (id_medico, fecha, hora)
);

-- Tabla: HISTORIAL_CITA
CREATE TABLE IF NOT EXISTS historial_cita (
    id_historial SERIAL PRIMARY KEY,
    id_cita INTEGER NOT NULL,
    estado_anterior VARCHAR(20),
    estado_nuevo VARCHAR(20) NOT NULL,
    fecha_cambio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    descripcion TEXT,
    
    CONSTRAINT fk_historial_cita 
        FOREIGN KEY (id_cita) 
        REFERENCES cita(id_cita)
        ON DELETE CASCADE
);

-- Tabla: NOTIFICACION
CREATE TABLE IF NOT EXISTS notificacion (
    id_notificacion SERIAL PRIMARY KEY,
    id_usuario INTEGER NOT NULL,
    tipo VARCHAR(50) NOT NULL DEFAULT 'INFO'
        CHECK (tipo IN ('INFO', 'RECORDATORIO', 'ALERTA', 'CONFIRMACION')),
    mensaje TEXT NOT NULL,
    fecha_envio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    leida BOOLEAN DEFAULT FALSE,
    
    CONSTRAINT fk_notificacion_usuario 
        FOREIGN KEY (id_usuario) 
        REFERENCES usuario(id_usuario)
        ON DELETE CASCADE
);

-- ============================================================================
-- ÍNDICES BÁSICOS
-- ============================================================================

CREATE INDEX idx_usuario_email ON usuario(email);
CREATE INDEX idx_usuario_rol ON usuario(rol);
CREATE INDEX idx_cita_fecha ON cita(fecha);
CREATE INDEX idx_cita_estado ON cita(estado);

-- ============================================================================
-- PERMISOS
-- ============================================================================

GRANT CONNECT ON DATABASE clinica_citas TO clinica_admin;
GRANT USAGE ON SCHEMA public TO clinica_admin;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO clinica_admin;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO clinica_admin;

-- ============================================================================
-- FIN DE INICIALIZACIÓN
-- ============================================================================

DO $$
BEGIN
    RAISE NOTICE 'Base de datos inicializada correctamente';
    RAISE NOTICE 'Sistema: Gestión de Citas Médicas';
END $$;
