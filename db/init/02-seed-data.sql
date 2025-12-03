-- ============================================================================
-- Script de Datos de Prueba Completo (Seed Data)
-- Incluye: usuarios, médicos, pacientes, horarios, citas históricas y futuras
-- Contraseña para todos: Clinica2025!
-- ============================================================================

-- ============================================================================
-- ESPECIALIDADES
-- ============================================================================

INSERT INTO especialidad (nombre, descripcion) VALUES
    ('Medicina General', 'Atención médica general y preventiva'),
    ('Cardiología', 'Especialista en enfermedades del corazón y sistema circulatorio'),
    ('Pediatría', 'Atención médica especializada para niños y adolescentes'),
    ('Dermatología', 'Especialista en enfermedades de la piel'),
    ('Ginecología', 'Especialista en salud femenina y reproductiva'),
    ('Traumatología', 'Especialista en lesiones y enfermedades del sistema músculo-esquelético'),
    ('Oftalmología', 'Especialista en enfermedades de los ojos'),
    ('Otorrinolaringología', 'Especialista en oído, nariz y garganta'),
    ('Psiquiatría', 'Especialista en salud mental'),
    ('Neurología', 'Especialista en enfermedades del sistema nervioso')
ON CONFLICT (nombre) DO NOTHING;

-- ============================================================================
-- USUARIOS (ADMINISTRADORES)
-- ============================================================================

-- Hash bcrypt para "Clinica2025!": $2b$12$Zm8FiLf96pBqGaG/9ak3fejziz9FKphMNxVUn/mEtqH1HJdYezSjq

INSERT INTO usuario (nombre, apellido, email, telefono, contraseña, rol) VALUES
    ('Carlos', 'Rodríguez', 'admin@clinica.com', '+51999000001', '$2b$12$Zm8FiLf96pBqGaG/9ak3fejziz9FKphMNxVUn/mEtqH1HJdYezSjq', 'ADMIN'),
    ('Ana', 'Martínez', 'ana.martinez@clinica.com', '+51999000002', '$2b$12$Zm8FiLf96pBqGaG/9ak3fejziz9FKphMNxVUn/mEtqH1HJdYezSjq', 'ADMIN')
ON CONFLICT (email) DO NOTHING;

-- ============================================================================
-- USUARIOS (MÉDICOS)
-- ============================================================================

INSERT INTO usuario (nombre, apellido, email, telefono, contraseña, rol) VALUES
    ('Juan', 'Fernández', 'juan.fernandez@clinica.com', '+51999100001', '$2b$12$Zm8FiLf96pBqGaG/9ak3fejziz9FKphMNxVUn/mEtqH1HJdYezSjq', 'MEDICO'),
    ('Roberto', 'García', 'roberto.garcia@clinica.com', '+51999100002', '$2b$12$Zm8FiLf96pBqGaG/9ak3fejziz9FKphMNxVUn/mEtqH1HJdYezSjq', 'MEDICO'),
    ('María', 'López', 'maria.lopez@clinica.com', '+51999100003', '$2b$12$Zm8FiLf96pBqGaG/9ak3fejziz9FKphMNxVUn/mEtqH1HJdYezSjq', 'MEDICO'),
    ('Laura', 'Sánchez', 'laura.sanchez@clinica.com', '+51999100004', '$2b$12$Zm8FiLf96pBqGaG/9ak3fejziz9FKphMNxVUn/mEtqH1HJdYezSjq', 'MEDICO'),
    ('Carmen', 'Torres', 'carmen.torres@clinica.com', '+51999100005', '$2b$12$Zm8FiLf96pBqGaG/9ak3fejziz9FKphMNxVUn/mEtqH1HJdYezSjq', 'MEDICO'),
    ('Pedro', 'Ramírez', 'pedro.ramirez@clinica.com', '+51999100006', '$2b$12$Zm8FiLf96pBqGaG/9ak3fejziz9FKphMNxVUn/mEtqH1HJdYezSjq', 'MEDICO')
ON CONFLICT (email) DO NOTHING;

-- ============================================================================
-- USUARIOS (PACIENTES)
-- ============================================================================

INSERT INTO usuario (nombre, apellido, email, telefono, contraseña, rol) VALUES
    ('Luis', 'Gómez', 'luis.gomez@email.com', '+51999200001', '$2b$12$Zm8FiLf96pBqGaG/9ak3fejziz9FKphMNxVUn/mEtqH1HJdYezSjq', 'PACIENTE'),
    ('Patricia', 'Díaz', 'patricia.diaz@email.com', '+51999200002', '$2b$12$Zm8FiLf96pBqGaG/9ak3fejziz9FKphMNxVUn/mEtqH1HJdYezSjq', 'PACIENTE'),
    ('Jorge', 'Morales', 'jorge.morales@email.com', '+51999200003', '$2b$12$Zm8FiLf96pBqGaG/9ak3fejziz9FKphMNxVUn/mEtqH1HJdYezSjq', 'PACIENTE'),
    ('Sofía', 'Vargas', 'sofia.vargas@email.com', '+51999200004', '$2b$12$Zm8FiLf96pBqGaG/9ak3fejziz9FKphMNxVUn/mEtqH1HJdYezSjq', 'PACIENTE'),
    ('Miguel', 'Castro', 'miguel.castro@email.com', '+51999200005', '$2b$12$Zm8FiLf96pBqGaG/9ak3fejziz9FKphMNxVUn/mEtqH1HJdYezSjq', 'PACIENTE'),
    ('Elena', 'Ruiz', 'elena.ruiz@email.com', '+51999200006', '$2b$12$Zm8FiLf96pBqGaG/9ak3fejziz9FKphMNxVUn/mEtqH1HJdYezSjq', 'PACIENTE'),
    ('Diego', 'Ortiz', 'diego.ortiz@email.com', '+51999200007', '$2b$12$Zm8FiLf96pBqGaG/9ak3fejziz9FKphMNxVUn/mEtqH1HJdYezSjq', 'PACIENTE'),
    ('Valentina', 'Mendoza', 'valentina.mendoza@email.com', '+51999200008', '$2b$12$Zm8FiLf96pBqGaG/9ak3fejziz9FKphMNxVUn/mEtqH1HJdYezSjq', 'PACIENTE'),
    ('Ricardo', 'Flores', 'ricardo.flores@email.com', '+51999200009', '$2b$12$Zm8FiLf96pBqGaG/9ak3fejziz9FKphMNxVUn/mEtqH1HJdYezSjq', 'PACIENTE'),
    ('Isabella', 'Herrera', 'isabella.herrera@email.com', '+51999200010', '$2b$12$Zm8FiLf96pBqGaG/9ak3fejziz9FKphMNxVUn/mEtqH1HJdYezSjq', 'PACIENTE')
ON CONFLICT (email) DO NOTHING;

-- ============================================================================
-- MÉDICOS
-- ============================================================================

INSERT INTO medico (id_usuario, id_especialidad, registro_profesional) 
SELECT u.id_usuario, e.id_especialidad, reg_prof
FROM (VALUES
    ('juan.fernandez@clinica.com', 'Medicina General', 'CMP-54323'),
    ('roberto.garcia@clinica.com', 'Cardiología', 'CMP-54321'),
    ('maria.lopez@clinica.com', 'Pediatría', 'CMP-54322'),
    ('laura.sanchez@clinica.com', 'Dermatología', 'CMP-54324'),
    ('carmen.torres@clinica.com', 'Ginecología', 'CMP-54326'),
    ('pedro.ramirez@clinica.com', 'Traumatología', 'CMP-54325')
) AS datos(email, especialidad, reg_prof)
JOIN usuario u ON u.email = datos.email
JOIN especialidad e ON e.nombre = datos.especialidad
ON CONFLICT (registro_profesional) DO NOTHING;

-- ============================================================================
-- PACIENTES
-- ============================================================================

INSERT INTO paciente (id_usuario, fecha_nacimiento, direccion)
SELECT u.id_usuario, fecha_nac::date, dir
FROM (VALUES
    ('luis.gomez@email.com', '1985-03-15', 'Av. Arequipa 1234, Lima'),
    ('patricia.diaz@email.com', '1990-07-22', 'Jr. Junín 567, Lima'),
    ('jorge.morales@email.com', '1978-11-08', 'Calle Los Pinos 890, Miraflores'),
    ('sofia.vargas@email.com', '1995-05-30', 'Av. Javier Prado 2345, San Isidro'),
    ('miguel.castro@email.com', '1982-09-18', 'Jr. Lampa 456, Lima'),
    ('elena.ruiz@email.com', '1988-12-25', 'Av. Brasil 3456, Pueblo Libre'),
    ('diego.ortiz@email.com', '1992-04-14', 'Calle Las Flores 123, Surco'),
    ('valentina.mendoza@email.com', '1997-08-07', 'Av. Universitaria 789, Los Olivos'),
    ('ricardo.flores@email.com', '1975-02-28', 'Jr. Carabaya 234, Lima'),
    ('isabella.herrera@email.com', '2000-06-19', 'Av. La Marina 5678, San Miguel')
) AS datos(email, fecha_nac, dir)
JOIN usuario u ON u.email = datos.email
ON CONFLICT (id_usuario) DO NOTHING;

-- ============================================================================
-- HORARIOS DE MÉDICOS
-- ============================================================================

-- Dr. Juan Fernández (Medicina General) - Lunes a Viernes, 8:00 - 17:00
INSERT INTO horario_medico (id_medico, dia_semana, hora_inicio, hora_fin)
SELECT m.id_medico, dia, '08:00:00', '17:00:00'
FROM medico m
JOIN usuario u ON m.id_usuario = u.id_usuario
CROSS JOIN generate_series(1, 5) AS dia
WHERE u.email = 'juan.fernandez@clinica.com'
ON CONFLICT (id_medico, dia_semana, hora_inicio) DO NOTHING;

-- Dr. Roberto García (Cardiología) - Lunes a Viernes, 8:00 - 14:00
INSERT INTO horario_medico (id_medico, dia_semana, hora_inicio, hora_fin)
SELECT m.id_medico, dia, '08:00:00', '14:00:00'
FROM medico m
JOIN usuario u ON m.id_usuario = u.id_usuario
CROSS JOIN generate_series(1, 5) AS dia
WHERE u.email = 'roberto.garcia@clinica.com'
ON CONFLICT (id_medico, dia_semana, hora_inicio) DO NOTHING;

-- Dra. María López (Pediatría) - Lunes a Viernes, 14:00 - 20:00
INSERT INTO horario_medico (id_medico, dia_semana, hora_inicio, hora_fin)
SELECT m.id_medico, dia, '14:00:00', '20:00:00'
FROM medico m
JOIN usuario u ON m.id_usuario = u.id_usuario
CROSS JOIN generate_series(1, 5) AS dia
WHERE u.email = 'maria.lopez@clinica.com'
ON CONFLICT (id_medico, dia_semana, hora_inicio) DO NOTHING;

-- Dra. Laura Sánchez (Dermatología) - Martes, Jueves, Sábado, 9:00 - 15:00
INSERT INTO horario_medico (id_medico, dia_semana, hora_inicio, hora_fin)
SELECT m.id_medico, dia, '09:00:00', '15:00:00'
FROM medico m
JOIN usuario u ON m.id_usuario = u.id_usuario
CROSS JOIN unnest(ARRAY[2, 4, 6]) AS dia
WHERE u.email = 'laura.sanchez@clinica.com'
ON CONFLICT (id_medico, dia_semana, hora_inicio) DO NOTHING;

-- Dra. Carmen Torres (Ginecología) - Lunes, Miércoles, Viernes, 8:00 - 16:00
INSERT INTO horario_medico (id_medico, dia_semana, hora_inicio, hora_fin)
SELECT m.id_medico, dia, '08:00:00', '16:00:00'
FROM medico m
JOIN usuario u ON m.id_usuario = u.id_usuario
CROSS JOIN unnest(ARRAY[1, 3, 5]) AS dia
WHERE u.email = 'carmen.torres@clinica.com'
ON CONFLICT (id_medico, dia_semana, hora_inicio) DO NOTHING;

-- Dr. Pedro Ramírez (Traumatología) - Lunes a Viernes, 10:00 - 18:00
INSERT INTO horario_medico (id_medico, dia_semana, hora_inicio, hora_fin)
SELECT m.id_medico, dia, '10:00:00', '18:00:00'
FROM medico m
JOIN usuario u ON m.id_usuario = u.id_usuario
CROSS JOIN generate_series(1, 5) AS dia
WHERE u.email = 'pedro.ramirez@clinica.com'
ON CONFLICT (id_medico, dia_semana, hora_inicio) DO NOTHING;

-- ============================================================================
-- CITAS HISTÓRICAS - OCTUBRE 2025
-- ============================================================================

INSERT INTO cita (id_paciente, id_medico, fecha, hora, motivo, estado, observaciones)
SELECT 
    pac.id_paciente,
    med.id_medico,
    fecha_cita::date,
    hora_cita::time,
    motivo_cita,
    estado_cita,
    obs_cita
FROM (VALUES
    ('luis.gomez@email.com', 'juan.fernandez@clinica.com', '2025-10-07', '09:00:00', 'Consulta general', 'ATENDIDA', 'Paciente en buen estado de salud'),
    ('jorge.morales@email.com', 'roberto.garcia@clinica.com', '2025-10-08', '10:00:00', 'Control cardiológico', 'ATENDIDA', 'Presión arterial controlada'),
    ('sofia.vargas@email.com', 'maria.lopez@clinica.com', '2025-10-09', '15:00:00', 'Revisión pediátrica', 'ATENDIDA', 'Desarrollo normal'),
    ('miguel.castro@email.com', 'laura.sanchez@clinica.com', '2025-10-10', '10:30:00', 'Consulta dermatológica', 'ATENDIDA', 'Tratamiento tópico recetado'),
    ('elena.ruiz@email.com', 'carmen.torres@clinica.com', '2025-10-14', '09:30:00', 'Control ginecológico', 'ATENDIDA', 'Exámenes de rutina solicitados'),
    ('luis.gomez@email.com', 'pedro.ramirez@clinica.com', '2025-10-15', '15:00:00', 'Lesión deportiva', 'CANCELADA', 'Paciente canceló por motivos personales'),
    ('jorge.morales@email.com', 'juan.fernandez@clinica.com', '2025-10-16', '10:00:00', 'Chequeo general', 'ATENDIDA', 'Todo en orden'),
    ('sofia.vargas@email.com', 'roberto.garcia@clinica.com', '2025-10-17', '11:30:00', 'Electrocardiograma', 'ATENDIDA', 'Resultado normal'),
    ('miguel.castro@email.com', 'maria.lopez@clinica.com', '2025-10-21', '16:30:00', 'Vacunación', 'ATENDIDA', 'Vacuna anual aplicada'),
    ('elena.ruiz@email.com', 'laura.sanchez@clinica.com', '2025-10-22', '11:00:00', 'Tratamiento dermatológico', 'ATENDIDA', 'Continuar con crema'),
    ('luis.gomez@email.com', 'carmen.torres@clinica.com', '2025-10-23', '09:00:00', 'Consulta ginecológica', 'ATENDIDA', 'Sin novedad'),
    ('jorge.morales@email.com', 'pedro.ramirez@clinica.com', '2025-10-24', '16:00:00', 'Rehabilitación', 'ATENDIDA', 'Progreso satisfactorio'),
    ('sofia.vargas@email.com', 'juan.fernandez@clinica.com', '2025-10-28', '10:30:00', 'Consulta general', 'ATENDIDA', 'Paciente saludable'),
    ('miguel.castro@email.com', 'roberto.garcia@clinica.com', '2025-10-29', '13:00:00', 'Control presión arterial', 'ATENDIDA', 'Mantener medicación'),
    ('elena.ruiz@email.com', 'maria.lopez@clinica.com', '2025-10-30', '17:00:00', 'Revisión pediátrica', 'ATENDIDA', 'Crecimiento adecuado')
) AS datos(email_pac, email_med, fecha_cita, hora_cita, motivo_cita, estado_cita, obs_cita)
JOIN paciente pac ON pac.id_usuario = (SELECT id_usuario FROM usuario WHERE email = datos.email_pac)
JOIN medico med ON med.id_usuario = (SELECT id_usuario FROM usuario WHERE email = datos.email_med)
ON CONFLICT (id_medico, fecha, hora) DO NOTHING;

-- ============================================================================
-- CITAS HISTÓRICAS - NOVIEMBRE 2025 (Semana 1)
-- ============================================================================

INSERT INTO cita (id_paciente, id_medico, fecha, hora, motivo, estado, observaciones)
SELECT 
    pac.id_paciente,
    med.id_medico,
    fecha_cita::date,
    hora_cita::time,
    motivo_cita,
    estado_cita,
    obs_cita
FROM (VALUES
    ('luis.gomez@email.com', 'juan.fernandez@clinica.com', '2025-11-03', '09:00:00', 'Consulta de control general', 'ATENDIDA', 'Todo normal'),
    ('jorge.morales@email.com', 'roberto.garcia@clinica.com', '2025-11-03', '10:30:00', 'Control cardiológico mensual', 'ATENDIDA', 'Sin cambios'),
    ('sofia.vargas@email.com', 'maria.lopez@clinica.com', '2025-11-04', '15:00:00', 'Revisión pediátrica', 'ATENDIDA', 'Desarrollo normal'),
    ('miguel.castro@email.com', 'laura.sanchez@clinica.com', '2025-11-04', '10:00:00', 'Consulta dermatológica', 'CANCELADA', 'Reagendó para otra fecha'),
    ('elena.ruiz@email.com', 'carmen.torres@clinica.com', '2025-11-05', '09:30:00', 'Control ginecológico', 'ATENDIDA', 'Exámenes solicitados'),
    ('luis.gomez@email.com', 'pedro.ramirez@clinica.com', '2025-11-05', '15:00:00', 'Dolor en rodilla', 'ATENDIDA', 'Tratamiento fisioterapéutico'),
    ('jorge.morales@email.com', 'juan.fernandez@clinica.com', '2025-11-06', '10:00:00', 'Seguimiento tratamiento', 'ATENDIDA', 'Evolución favorable'),
    ('sofia.vargas@email.com', 'roberto.garcia@clinica.com', '2025-11-06', '11:30:00', 'Chequeo cardiaco', 'ATENDIDA', 'Resultados normales'),
    ('miguel.castro@email.com', 'maria.lopez@clinica.com', '2025-11-07', '16:30:00', 'Consulta pediátrica urgente', 'ATENDIDA', 'Medicamento recetado')
) AS datos(email_pac, email_med, fecha_cita, hora_cita, motivo_cita, estado_cita, obs_cita)
JOIN paciente pac ON pac.id_usuario = (SELECT id_usuario FROM usuario WHERE email = datos.email_pac)
JOIN medico med ON med.id_usuario = (SELECT id_usuario FROM usuario WHERE email = datos.email_med)
ON CONFLICT (id_medico, fecha, hora) DO NOTHING;

-- ============================================================================
-- CITAS HISTÓRICAS - NOVIEMBRE 2025 (Semana 2)
-- ============================================================================

INSERT INTO cita (id_paciente, id_medico, fecha, hora, motivo, estado, observaciones)
SELECT 
    pac.id_paciente,
    med.id_medico,
    fecha_cita::date,
    hora_cita::time,
    motivo_cita,
    estado_cita,
    obs_cita
FROM (VALUES
    ('elena.ruiz@email.com', 'laura.sanchez@clinica.com', '2025-11-10', '09:00:00', 'Tratamiento dermatológico', 'ATENDIDA', 'Mejora notable'),
    ('luis.gomez@email.com', 'carmen.torres@clinica.com', '2025-11-10', '14:30:00', 'Control ginecológico', 'CANCELADA', 'Conflicto de horario'),
    ('jorge.morales@email.com', 'pedro.ramirez@clinica.com', '2025-11-11', '10:00:00', 'Rehabilitación rodilla', 'ATENDIDA', 'Ejercicios indicados'),
    ('sofia.vargas@email.com', 'juan.fernandez@clinica.com', '2025-11-11', '15:30:00', 'Consulta medicina general', 'ATENDIDA', 'Receta entregada'),
    ('miguel.castro@email.com', 'roberto.garcia@clinica.com', '2025-11-12', '09:00:00', 'Control presión arterial', 'ATENDIDA', 'Valores estables'),
    ('elena.ruiz@email.com', 'maria.lopez@clinica.com', '2025-11-12', '18:00:00', 'Vacunación infantil', 'ATENDIDA', 'Vacuna aplicada sin reacción'),
    ('luis.gomez@email.com', 'laura.sanchez@clinica.com', '2025-11-13', '10:30:00', 'Revisión dermatológica', 'ATENDIDA', 'Tratamiento efectivo'),
    ('jorge.morales@email.com', 'carmen.torres@clinica.com', '2025-11-13', '13:00:00', 'Consulta ginecológica', 'ATENDIDA', 'Control de rutina OK'),
    ('sofia.vargas@email.com', 'pedro.ramirez@clinica.com', '2025-11-14', '14:00:00', 'Fisioterapia', 'ATENDIDA', 'Sesión completada')
) AS datos(email_pac, email_med, fecha_cita, hora_cita, motivo_cita, estado_cita, obs_cita)
JOIN paciente pac ON pac.id_usuario = (SELECT id_usuario FROM usuario WHERE email = datos.email_pac)
JOIN medico med ON med.id_usuario = (SELECT id_usuario FROM usuario WHERE email = datos.email_med)
ON CONFLICT (id_medico, fecha, hora) DO NOTHING;

-- ============================================================================
-- CITAS HISTÓRICAS - NOVIEMBRE 2025 (Semana 3)
-- ============================================================================

INSERT INTO cita (id_paciente, id_medico, fecha, hora, motivo, estado, observaciones)
SELECT 
    pac.id_paciente,
    med.id_medico,
    fecha_cita::date,
    hora_cita::time,
    motivo_cita,
    estado_cita,
    obs_cita
FROM (VALUES
    ('miguel.castro@email.com', 'juan.fernandez@clinica.com', '2025-11-17', '09:30:00', 'Chequeo anual', 'ATENDIDA', 'Estado de salud excelente'),
    ('elena.ruiz@email.com', 'roberto.garcia@clinica.com', '2025-11-17', '11:00:00', 'Electrocardiograma', 'ATENDIDA', 'Sin anomalías'),
    ('luis.gomez@email.com', 'maria.lopez@clinica.com', '2025-11-18', '17:00:00', 'Control pediátrico hijo', 'CANCELADA', 'Emergencia familiar'),
    ('jorge.morales@email.com', 'laura.sanchez@clinica.com', '2025-11-18', '13:00:00', 'Tratamiento acné', 'ATENDIDA', 'Nueva medicación'),
    ('sofia.vargas@email.com', 'carmen.torres@clinica.com', '2025-11-19', '09:00:00', 'Control prenatal', 'ATENDIDA', 'Embarazo evoluciona bien'),
    ('miguel.castro@email.com', 'pedro.ramirez@clinica.com', '2025-11-19', '14:30:00', 'Lesión deportiva', 'ATENDIDA', 'Reposo indicado'),
    ('elena.ruiz@email.com', 'juan.fernandez@clinica.com', '2025-11-20', '08:00:00', 'Consulta general', 'ATENDIDA', 'Gripe leve'),
    ('luis.gomez@email.com', 'roberto.garcia@clinica.com', '2025-11-20', '13:00:00', 'Seguimiento cardiológico', 'ATENDIDA', 'Control mensual OK'),
    ('jorge.morales@email.com', 'maria.lopez@clinica.com', '2025-11-21', '19:00:00', 'Revisión pediátrica', 'ATENDIDA', 'Vacunas al día')
) AS datos(email_pac, email_med, fecha_cita, hora_cita, motivo_cita, estado_cita, obs_cita)
JOIN paciente pac ON pac.id_usuario = (SELECT id_usuario FROM usuario WHERE email = datos.email_pac)
JOIN medico med ON med.id_usuario = (SELECT id_usuario FROM usuario WHERE email = datos.email_med)
ON CONFLICT (id_medico, fecha, hora) DO NOTHING;

-- ============================================================================
-- CITAS HISTÓRICAS - NOVIEMBRE 2025 (Semana 4)
-- ============================================================================

INSERT INTO cita (id_paciente, id_medico, fecha, hora, motivo, estado, observaciones)
SELECT 
    pac.id_paciente,
    med.id_medico,
    fecha_cita::date,
    hora_cita::time,
    motivo_cita,
    estado_cita,
    obs_cita
FROM (VALUES
    ('sofia.vargas@email.com', 'laura.sanchez@clinica.com', '2025-11-24', '10:00:00', 'Consulta dermatológica', 'ATENDIDA', 'Piel mejoró notablemente'),
    ('miguel.castro@email.com', 'carmen.torres@clinica.com', '2025-11-24', '14:00:00', 'Control ginecológico', 'ATENDIDA', 'Resultados normales'),
    ('elena.ruiz@email.com', 'pedro.ramirez@clinica.com', '2025-11-25', '10:00:00', 'Dolor lumbar', 'CANCELADA', 'Paciente enfermo, reprogramó'),
    ('luis.gomez@email.com', 'juan.fernandez@clinica.com', '2025-11-25', '15:30:00', 'Resfriado común', 'ATENDIDA', 'Antigripal recetado'),
    ('jorge.morales@email.com', 'roberto.garcia@clinica.com', '2025-11-26', '10:30:00', 'Control hipertensión', 'ATENDIDA', 'Presión estable'),
    ('sofia.vargas@email.com', 'maria.lopez@clinica.com', '2025-11-26', '18:30:00', 'Vacunas niño', 'ATENDIDA', 'Esquema completo'),
    ('miguel.castro@email.com', 'laura.sanchez@clinica.com', '2025-11-27', '09:30:00', 'Revisión piel', 'ATENDIDA', 'Protector solar recomendado'),
    ('elena.ruiz@email.com', 'carmen.torres@clinica.com', '2025-11-27', '11:00:00', 'Consulta ginecológica', 'ATENDIDA', 'Chequeo anual completado'),
    ('luis.gomez@email.com', 'pedro.ramirez@clinica.com', '2025-11-28', '16:00:00', 'Terapia física', 'ATENDIDA', 'Recuperación en progreso')
) AS datos(email_pac, email_med, fecha_cita, hora_cita, motivo_cita, estado_cita, obs_cita)
JOIN paciente pac ON pac.id_usuario = (SELECT id_usuario FROM usuario WHERE email = datos.email_pac)
JOIN medico med ON med.id_usuario = (SELECT id_usuario FROM usuario WHERE email = datos.email_med)
ON CONFLICT (id_medico, fecha, hora) DO NOTHING;

-- ============================================================================
-- CITAS FUTURAS - DICIEMBRE 2025
-- ============================================================================

INSERT INTO cita (id_paciente, id_medico, fecha, hora, motivo, estado)
SELECT 
    pac.id_paciente,
    med.id_medico,
    fecha_cita::date,
    hora_cita::time,
    motivo_cita,
    estado_cita
FROM (VALUES
    ('luis.gomez@email.com', 'roberto.garcia@clinica.com', CURRENT_DATE + 1, '08:30:00', 'Control de presión arterial', 'AGENDADA'),
    ('patricia.diaz@email.com', 'maria.lopez@clinica.com', CURRENT_DATE + 1, '15:00:00', 'Consulta pediátrica - vacunas', 'AGENDADA'),
    ('jorge.morales@email.com', 'juan.fernandez@clinica.com', CURRENT_DATE + 2, '09:00:00', 'Chequeo médico general', 'AGENDADA'),
    ('sofia.vargas@email.com', 'laura.sanchez@clinica.com', CURRENT_DATE + 3, '10:30:00', 'Consulta dermatológica - acné', 'AGENDADA'),
    ('miguel.castro@email.com', 'pedro.ramirez@clinica.com', CURRENT_DATE + 3, '11:00:00', 'Dolor en rodilla izquierda', 'AGENDADA'),
    ('elena.ruiz@email.com', 'carmen.torres@clinica.com', CURRENT_DATE + 4, '09:30:00', 'Consulta ginecológica de rutina', 'AGENDADA'),
    ('diego.ortiz@email.com', 'roberto.garcia@clinica.com', CURRENT_DATE + 5, '10:00:00', 'Dolor en el pecho', 'AGENDADA'),
    ('valentina.mendoza@email.com', 'maria.lopez@clinica.com', CURRENT_DATE + 5, '16:00:00', 'Control de crecimiento', 'AGENDADA'),
    ('ricardo.flores@email.com', 'juan.fernandez@clinica.com', CURRENT_DATE + 7, '08:00:00', 'Resultados de análisis', 'AGENDADA'),
    ('isabella.herrera@email.com', 'laura.sanchez@clinica.com', CURRENT_DATE + 10, '11:00:00', 'Consulta por manchas en la piel', 'AGENDADA')
) AS datos(email_pac, email_med, fecha_cita, hora_cita, motivo_cita, estado_cita)
JOIN paciente pac ON pac.id_usuario = (SELECT id_usuario FROM usuario WHERE email = datos.email_pac)
JOIN medico med ON med.id_usuario = (SELECT id_usuario FROM usuario WHERE email = datos.email_med)
ON CONFLICT (id_medico, fecha, hora) DO NOTHING;

-- ============================================================================
-- NOTIFICACIONES DE BIENVENIDA
-- ============================================================================

-- Notificaciones para administradores
INSERT INTO notificacion (id_usuario, tipo, mensaje)
SELECT u.id_usuario, 'INFO', 'Bienvenido al Sistema de Gestión de Citas Médicas. Su cuenta de administrador ha sido creada exitosamente.'
FROM usuario u
WHERE u.rol = 'ADMIN'
ON CONFLICT DO NOTHING;

-- Notificaciones para médicos
INSERT INTO notificacion (id_usuario, tipo, mensaje)
SELECT u.id_usuario, 'INFO', 'Bienvenido al Sistema de Gestión de Citas Médicas. Su perfil de médico ha sido activado.'
FROM usuario u
WHERE u.rol = 'MEDICO'
ON CONFLICT DO NOTHING;

-- Notificaciones para pacientes
INSERT INTO notificacion (id_usuario, tipo, mensaje)
SELECT u.id_usuario, 'INFO', 'Bienvenido al Sistema de Gestión de Citas Médicas. Ya puede agendar sus citas médicas.'
FROM usuario u
WHERE u.rol = 'PACIENTE'
ON CONFLICT DO NOTHING;

-- ============================================================================
-- RESUMEN Y VERIFICACIÓN
-- ============================================================================

DO $$
DECLARE
    v_count_usuarios INTEGER;
    v_count_pacientes INTEGER;
    v_count_medicos INTEGER;
    v_count_especialidades INTEGER;
    v_count_horarios INTEGER;
    v_count_citas INTEGER;
    v_count_citas_oct INTEGER;
    v_count_citas_nov INTEGER;
    v_count_citas_dic INTEGER;
    v_count_notificaciones INTEGER;
BEGIN
    SELECT COUNT(*) INTO v_count_usuarios FROM usuario;
    SELECT COUNT(*) INTO v_count_pacientes FROM paciente;
    SELECT COUNT(*) INTO v_count_medicos FROM medico;
    SELECT COUNT(*) INTO v_count_especialidades FROM especialidad;
    SELECT COUNT(*) INTO v_count_horarios FROM horario_medico;
    SELECT COUNT(*) INTO v_count_citas FROM cita;
    SELECT COUNT(*) INTO v_count_citas_oct FROM cita WHERE fecha >= '2025-10-01' AND fecha < '2025-11-01';
    SELECT COUNT(*) INTO v_count_citas_nov FROM cita WHERE fecha >= '2025-11-01' AND fecha < '2025-12-01';
    SELECT COUNT(*) INTO v_count_citas_dic FROM cita WHERE fecha >= '2025-12-01';
    SELECT COUNT(*) INTO v_count_notificaciones FROM notificacion;
    
    RAISE NOTICE '========================================================';
    RAISE NOTICE 'DATOS DE PRUEBA CARGADOS EXITOSAMENTE';
    RAISE NOTICE '========================================================';
    RAISE NOTICE 'Estadísticas del Sistema:';
    RAISE NOTICE '  Total Usuarios: % (% Admin, % Médicos, % Pacientes)', 
        v_count_usuarios, 
        (SELECT COUNT(*) FROM usuario WHERE rol = 'ADMIN'),
        v_count_medicos,
        v_count_pacientes;
    RAISE NOTICE '  Especialidades: %', v_count_especialidades;
    RAISE NOTICE '  Horarios Médicos: %', v_count_horarios;
    RAISE NOTICE '  Total Citas: %', v_count_citas;
    RAISE NOTICE '    - Octubre 2025: % citas', v_count_citas_oct;
    RAISE NOTICE '    - Noviembre 2025: % citas', v_count_citas_nov;
    RAISE NOTICE '    - Diciembre 2025: % citas', v_count_citas_dic;
    RAISE NOTICE '  Notificaciones: %', v_count_notificaciones;
    RAISE NOTICE '========================================================';
    RAISE NOTICE 'Credenciales de Acceso:';
    RAISE NOTICE '  ADMIN:    admin@clinica.com';
    RAISE NOTICE '  MÉDICO:   juan.fernandez@clinica.com';
    RAISE NOTICE '  PACIENTE: luis.gomez@email.com';
    RAISE NOTICE '  PASSWORD: Clinica2025!';
    RAISE NOTICE '========================================================';
    RAISE NOTICE 'La base de datos está lista para pruebas completas';
    RAISE NOTICE '========================================================';
END $$;

