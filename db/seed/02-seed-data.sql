-- ============================================================================
-- Script de Datos de Prueba (Seed Data)
--===========================================================================

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
-- INSERTAR USUARIOS (ADMINISTRADORES)
-- ============================================================================

-- Contraseña para todos los usuarios: "Clinica2025!"
-- Hash bcrypt: $2b$12$Zm8FiLf96pBqGaG/9ak3fejziz9FKphMNxVUn/mEtqH1HJdYezSjq

INSERT INTO usuario (nombre, apellido, email, telefono, contraseña, rol) VALUES
    ('Carlos', 'Rodríguez', 'admin@clinica.com', '+51999000001', '$2b$12$Zm8FiLf96pBqGaG/9ak3fejziz9FKphMNxVUn/mEtqH1HJdYezSjq', 'ADMIN'),
    ('Ana', 'Martínez', 'ana.martinez@clinica.com', '+51999000002', '$2b$12$Zm8FiLf96pBqGaG/9ak3fejziz9FKphMNxVUn/mEtqH1HJdYezSjq', 'ADMIN')
ON CONFLICT (email) DO NOTHING;

-- ============================================================================
-- INSERTAR USUARIOS (MÉDICOS)
-- ============================================================================

INSERT INTO usuario (nombre, apellido, email, telefono, contraseña, rol) VALUES
    ('Roberto', 'García', 'roberto.garcia@clinica.com', '+51999100001', '$2b$12$Zm8FiLf96pBqGaG/9ak3fejziz9FKphMNxVUn/mEtqH1HJdYezSjq', 'MEDICO'),
    ('María', 'López', 'maria.lopez@clinica.com', '+51999100002', '$2b$12$Zm8FiLf96pBqGaG/9ak3fejziz9FKphMNxVUn/mEtqH1HJdYezSjq', 'MEDICO'),
    ('Juan', 'Fernández', 'juan.fernandez@clinica.com', '+51999100003', '$2b$12$Zm8FiLf96pBqGaG/9ak3fejziz9FKphMNxVUn/mEtqH1HJdYezSjq', 'MEDICO'),
    ('Laura', 'Sánchez', 'laura.sanchez@clinica.com', '+51999100004', '$2b$12$Zm8FiLf96pBqGaG/9ak3fejziz9FKphMNxVUn/mEtqH1HJdYezSjq', 'MEDICO'),
    ('Pedro', 'Ramírez', 'pedro.ramirez@clinica.com', '+51999100005', '$2b$12$Zm8FiLf96pBqGaG/9ak3fejziz9FKphMNxVUn/mEtqH1HJdYezSjq', 'MEDICO'),
    ('Carmen', 'Torres', 'carmen.torres@clinica.com', '+51999100006', '$2b$12$Zm8FiLf96pBqGaG/9ak3fejziz9FKphMNxVUn/mEtqH1HJdYezSjq', 'MEDICO')
ON CONFLICT (email) DO NOTHING;

-- ============================================================================
-- INSERTAR USUARIOS (PACIENTES)
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
-- INSERTAR MÉDICOS
-- ============================================================================

INSERT INTO medico (id_usuario, id_especialidad, registro_profesional) 
SELECT u.id_usuario, e.id_especialidad, reg_prof
FROM (VALUES
    ('roberto.garcia@clinica.com', 'Cardiología', 'CMP-54321'),
    ('maria.lopez@clinica.com', 'Pediatría', 'CMP-54322'),
    ('juan.fernandez@clinica.com', 'Medicina General', 'CMP-54323'),
    ('laura.sanchez@clinica.com', 'Dermatología', 'CMP-54324'),
    ('pedro.ramirez@clinica.com', 'Traumatología', 'CMP-54325'),
    ('carmen.torres@clinica.com', 'Ginecología', 'CMP-54326')
) AS datos(email, especialidad, reg_prof)
JOIN usuario u ON u.email = datos.email
JOIN especialidad e ON e.nombre = datos.especialidad
ON CONFLICT (registro_profesional) DO NOTHING;

-- ============================================================================
-- INSERTAR PACIENTES
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
-- INSERTAR HORARIOS DE MÉDICOS
-- ============================================================================

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

-- Dr. Juan Fernández (Medicina General) - Lunes a Sábado, 7:00 - 13:00
INSERT INTO horario_medico (id_medico, dia_semana, hora_inicio, hora_fin)
SELECT m.id_medico, dia, '07:00:00', '13:00:00'
FROM medico m
JOIN usuario u ON m.id_usuario = u.id_usuario
CROSS JOIN generate_series(1, 6) AS dia
WHERE u.email = 'juan.fernandez@clinica.com'
ON CONFLICT (id_medico, dia_semana, hora_inicio) DO NOTHING;

-- Dra. Laura Sánchez (Dermatología) - Martes, Jueves, Sábado, 9:00 - 15:00
INSERT INTO horario_medico (id_medico, dia_semana, hora_inicio, hora_fin)
SELECT m.id_medico, dia, '09:00:00', '15:00:00'
FROM medico m
JOIN usuario u ON m.id_usuario = u.id_usuario
CROSS JOIN unnest(ARRAY[2, 4, 6]) AS dia
WHERE u.email = 'laura.sanchez@clinica.com'
ON CONFLICT (id_medico, dia_semana, hora_inicio) DO NOTHING;

-- Dr. Pedro Ramírez (Traumatología) - Lunes a Viernes, 10:00 - 18:00
INSERT INTO horario_medico (id_medico, dia_semana, hora_inicio, hora_fin)
SELECT m.id_medico, dia, '10:00:00', '18:00:00'
FROM medico m
JOIN usuario u ON m.id_usuario = u.id_usuario
CROSS JOIN generate_series(1, 5) AS dia
WHERE u.email = 'pedro.ramirez@clinica.com'
ON CONFLICT (id_medico, dia_semana, hora_inicio) DO NOTHING;

-- Dra. Carmen Torres (Ginecología) - Lunes, Miércoles, Viernes, 8:00 - 16:00
INSERT INTO horario_medico (id_medico, dia_semana, hora_inicio, hora_fin)
SELECT m.id_medico, dia, '08:00:00', '16:00:00'
FROM medico m
JOIN usuario u ON m.id_usuario = u.id_usuario
CROSS JOIN unnest(ARRAY[1, 3, 5]) AS dia
WHERE u.email = 'carmen.torres@clinica.com'
ON CONFLICT (id_medico, dia_semana, hora_inicio) DO NOTHING;

-- ============================================================================
-- INSERTAR CITAS DE EJEMPLO
-- ============================================================================

-- Citas futuras (próximos días)
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

-- Citas pasadas (para historial)
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
    ('luis.gomez@email.com', 'roberto.garcia@clinica.com', CURRENT_DATE - 7, '08:30:00', 'Control cardiológico', 'ATENDIDA', 'Paciente estable, continuar con tratamiento'),
    ('patricia.diaz@email.com', 'juan.fernandez@clinica.com', CURRENT_DATE - 5, '09:00:00', 'Consulta por gripe', 'ATENDIDA', 'Recetado antigripal, reposo 3 días'),
    ('jorge.morales@email.com', 'pedro.ramirez@clinica.com', CURRENT_DATE - 3, '11:00:00', 'Dolor de espalda', 'ATENDIDA', 'Recomendado fisioterapia'),
    ('sofia.vargas@email.com', 'maria.lopez@clinica.com', CURRENT_DATE - 10, '15:30:00', 'Control pediátrico', 'CANCELADA', 'Paciente canceló por motivos personales'),
    ('miguel.castro@email.com', 'juan.fernandez@clinica.com', CURRENT_DATE - 2, '10:00:00', 'Chequeo de rutina', 'ATENDIDA', 'Todo en orden, próximo control en 6 meses')
) AS datos(email_pac, email_med, fecha_cita, hora_cita, motivo_cita, estado_cita, obs_cita)
JOIN paciente pac ON pac.id_usuario = (SELECT id_usuario FROM usuario WHERE email = datos.email_pac)
JOIN medico med ON med.id_usuario = (SELECT id_usuario FROM usuario WHERE email = datos.email_med)
ON CONFLICT (id_medico, fecha, hora) DO NOTHING;

-- ============================================================================
-- INSERTAR NOTIFICACIONES DE BIENVENIDA
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
-- ESTADÍSTICAS Y VERIFICACIÓN
-- ============================================================================

DO $$
DECLARE
    v_count_usuarios INTEGER;
    v_count_pacientes INTEGER;
    v_count_medicos INTEGER;
    v_count_especialidades INTEGER;
    v_count_horarios INTEGER;
    v_count_citas INTEGER;
    v_count_notificaciones INTEGER;
BEGIN
    SELECT COUNT(*) INTO v_count_usuarios FROM usuario;
    SELECT COUNT(*) INTO v_count_pacientes FROM paciente;
    SELECT COUNT(*) INTO v_count_medicos FROM medico;
    SELECT COUNT(*) INTO v_count_especialidades FROM especialidad;
    SELECT COUNT(*) INTO v_count_horarios FROM horario_medico;
    SELECT COUNT(*) INTO v_count_citas FROM cita;
    SELECT COUNT(*) INTO v_count_notificaciones FROM notificacion;
    
    RAISE NOTICE '================================================';
    RAISE NOTICE 'Datos de prueba cargados correctamente';
    RAISE NOTICE '================================================';
    RAISE NOTICE 'Estadísticas:';
    RAISE NOTICE '  - Usuarios: %', v_count_usuarios;
    RAISE NOTICE '  - Pacientes: %', v_count_pacientes;
    RAISE NOTICE '  - Médicos: %', v_count_medicos;
    RAISE NOTICE '  - Especialidades: %', v_count_especialidades;
    RAISE NOTICE '  - Horarios: %', v_count_horarios;
    RAISE NOTICE '  - Citas: %', v_count_citas;
    RAISE NOTICE '  - Notificaciones: %', v_count_notificaciones;
    RAISE NOTICE '================================================';
    RAISE NOTICE 'Credenciales de acceso:';
    RAISE NOTICE '  Usuario: admin@clinica.com';
    RAISE NOTICE '  Contraseña: Clinica2025!';
    RAISE NOTICE '================================================';
END $$;

