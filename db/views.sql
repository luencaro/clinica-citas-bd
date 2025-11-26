-- ============================================
-- VISTAS DEL SISTEMA DE CITAS MÉDICAS
-- ============================================

-- 1. VISTA: Citas completas con información JOIN
-- Une todas las tablas para mostrar información completa de citas

CREATE OR REPLACE VIEW vista_citas_completas AS
SELECT 
    c.id_cita,
    c.fecha,
    c.hora,
    c.motivo,
    c.estado,
    c.observaciones,
    -- Información del Paciente
    p.id_paciente,
    up.nombre AS paciente_nombre,
    up.apellido AS paciente_apellido,
    up.email AS paciente_email,
    up.telefono AS paciente_telefono,
    p.fecha_nacimiento,
    EXTRACT(YEAR FROM AGE(p.fecha_nacimiento)) AS paciente_edad,
    -- Información del Médico
    m.id_medico,
    um.nombre AS medico_nombre,
    um.apellido AS medico_apellido,
    um.email AS medico_email,
    m.registro_profesional,
    -- Información de Especialidad
    e.id_especialidad,
    e.nombre AS especialidad,
    e.descripcion AS especialidad_descripcion,
    -- Timestamps
    c.fecha_creacion,
    c.fecha_modificacion
FROM cita c
INNER JOIN paciente p ON c.id_paciente = p.id_paciente
INNER JOIN usuario up ON p.id_usuario = up.id_usuario
INNER JOIN medico m ON c.id_medico = m.id_medico
INNER JOIN usuario um ON m.id_usuario = um.id_usuario
INNER JOIN especialidad e ON m.id_especialidad = e.id_especialidad;

-- Comentario de la vista
COMMENT ON VIEW vista_citas_completas IS 
'Vista completa con información JOIN de citas, pacientes, médicos y especialidades';


-- 2. VISTA: Disponibilidad de médicos
-- Muestra médicos activos con sus horarios

CREATE OR REPLACE VIEW vista_disponibilidad_medicos AS
SELECT 
    m.id_medico,
    u.nombre || ' ' || u.apellido AS medico_nombre,
    e.nombre AS especialidad,
    hm.dia_semana,
    CASE hm.dia_semana
        WHEN 1 THEN 'Lunes'
        WHEN 2 THEN 'Martes'
        WHEN 3 THEN 'Miércoles'
        WHEN 4 THEN 'Jueves'
        WHEN 5 THEN 'Viernes'
        WHEN 6 THEN 'Sábado'
        WHEN 7 THEN 'Domingo'
    END AS dia_nombre,
    hm.hora_inicio,
    hm.hora_fin,
    hm.hora_fin - hm.hora_inicio AS duracion,
    -- Contar citas del día actual si es hoy
    (
        SELECT COUNT(*)
        FROM cita c
        WHERE c.id_medico = m.id_medico
          AND c.fecha = CURRENT_DATE
          AND EXTRACT(ISODOW FROM c.fecha) = hm.dia_semana
          AND c.estado IN ('AGENDADA', 'REPROGRAMADA')
    ) AS citas_hoy
FROM medico m
INNER JOIN usuario u ON m.id_usuario = u.id_usuario
INNER JOIN especialidad e ON m.id_especialidad = e.id_especialidad
LEFT JOIN horario_medico hm ON m.id_medico = hm.id_medico
WHERE m.activo = TRUE
  AND u.activo = TRUE
  AND e.activa = TRUE
ORDER BY e.nombre, medico_nombre, hm.dia_semana, hm.hora_inicio;

COMMENT ON VIEW vista_disponibilidad_medicos IS 
'Vista de médicos activos con sus horarios de atención organizados por especialidad';


-- 3. VISTA: Estadísticas de citas por estado
-- Resumen de citas agrupadas por estado

CREATE OR REPLACE VIEW vista_estadisticas_citas AS
SELECT 
    estado,
    COUNT(*) AS cantidad,
    ROUND(COUNT(*)::NUMERIC * 100.0 / SUM(COUNT(*)) OVER (), 2) AS porcentaje
FROM cita
GROUP BY estado
ORDER BY cantidad DESC;

COMMENT ON VIEW vista_estadisticas_citas IS 
'Estadísticas generales de citas agrupadas por estado con porcentajes';


-- 4. VISTA: Próximas citas (agenda general)
-- Muestra todas las citas futuras ordenadas

CREATE OR REPLACE VIEW vista_proximas_citas AS
SELECT 
    c.id_cita,
    c.fecha,
    c.hora,
    c.estado,
    up.nombre || ' ' || up.apellido AS paciente,
    up.telefono AS telefono_paciente,
    um.nombre || ' ' || um.apellido AS medico,
    e.nombre AS especialidad,
    c.motivo
FROM cita c
INNER JOIN paciente p ON c.id_paciente = p.id_paciente
INNER JOIN usuario up ON p.id_usuario = up.id_usuario
INNER JOIN medico m ON c.id_medico = m.id_medico
INNER JOIN usuario um ON m.id_usuario = um.id_usuario
INNER JOIN especialidad e ON m.id_especialidad = e.id_especialidad
WHERE c.fecha >= CURRENT_DATE
  AND c.estado IN ('AGENDADA', 'REPROGRAMADA')
ORDER BY c.fecha, c.hora;

COMMENT ON VIEW vista_proximas_citas IS 
'Todas las citas futuras activas ordenadas por fecha y hora';


-- 5. VISTA: Historial de cambios de citas
-- Auditoría completa de cambios de estado

CREATE OR REPLACE VIEW vista_historial_citas AS
SELECT 
    hc.id_historial,
    hc.id_cita,
    hc.fecha_cambio,
    hc.estado_anterior,
    hc.estado_nuevo,
    hc.observaciones,
    c.fecha AS fecha_cita,
    c.hora AS hora_cita,
    up.nombre || ' ' || up.apellido AS paciente,
    um.nombre || ' ' || um.apellido AS medico
FROM historial_cita hc
INNER JOIN cita c ON hc.id_cita = c.id_cita
INNER JOIN paciente p ON c.id_paciente = p.id_paciente
INNER JOIN usuario up ON p.id_usuario = up.id_usuario
INNER JOIN medico m ON c.id_medico = m.id_medico
INNER JOIN usuario um ON m.id_usuario = um.id_usuario
ORDER BY hc.fecha_cambio DESC;

COMMENT ON VIEW vista_historial_citas IS 
'Historial completo de cambios de estado de citas para auditoría';


-- 6. VISTA: Médicos por especialidad con estadísticas
-- Información de médicos agrupados por especialidad con métricas

CREATE OR REPLACE VIEW vista_medicos_por_especialidad AS
SELECT 
    e.id_especialidad,
    e.nombre AS especialidad,
    e.descripcion AS especialidad_descripcion,
    COUNT(m.id_medico) AS total_medicos,
    COUNT(m.id_medico) FILTER (WHERE m.activo = TRUE) AS medicos_activos,
    COUNT(DISTINCT hm.id_horario) AS total_horarios_configurados,
    COALESCE(
        SUM(
            (SELECT COUNT(*) 
             FROM cita c 
             WHERE c.id_medico = m.id_medico 
               AND c.fecha >= CURRENT_DATE - INTERVAL '30 days'
               AND c.estado = 'ATENDIDA'
            )
        ), 0
    ) AS citas_atendidas_ultimo_mes
FROM especialidad e
LEFT JOIN medico m ON e.id_especialidad = m.id_especialidad
LEFT JOIN horario_medico hm ON m.id_medico = hm.id_medico
WHERE e.activa = TRUE
GROUP BY e.id_especialidad, e.nombre, e.descripcion
ORDER BY total_medicos DESC, especialidad;

COMMENT ON VIEW vista_medicos_por_especialidad IS 
'Resumen de médicos por especialidad con estadísticas de actividad';


-- 7. VISTA: Notificaciones pendientes por usuario
-- Notificaciones no leídas organizadas por usuario

CREATE OR REPLACE VIEW vista_notificaciones_pendientes AS
SELECT 
    n.id_notificacion,
    n.id_usuario,
    u.nombre || ' ' || u.apellido AS usuario,
    u.email,
    u.rol,
    n.tipo,
    n.mensaje,
    n.fecha_envio,
    EXTRACT(EPOCH FROM (CURRENT_TIMESTAMP - n.fecha_envio))/3600 AS horas_desde_envio
FROM notificacion n
INNER JOIN usuario u ON n.id_usuario = u.id_usuario
WHERE n.leido = FALSE
ORDER BY n.fecha_envio DESC;

COMMENT ON VIEW vista_notificaciones_pendientes IS 
'Notificaciones no leídas con tiempo transcurrido desde el envío';


-- 8. VISTA: Ocupación diaria de médicos
-- Muestra cuántas citas tiene cada médico por día

CREATE OR REPLACE VIEW vista_ocupacion_diaria_medicos AS
SELECT 
    m.id_medico,
    um.nombre || ' ' || um.apellido AS medico,
    e.nombre AS especialidad,
    c.fecha,
    COUNT(*) AS total_citas,
    COUNT(*) FILTER (WHERE c.estado = 'AGENDADA') AS agendadas,
    COUNT(*) FILTER (WHERE c.estado = 'ATENDIDA') AS atendidas,
    COUNT(*) FILTER (WHERE c.estado = 'CANCELADA') AS canceladas,
    -- Calcular tasa de ocupación (asumiendo slots de 30 min)
    ROUND(
        COUNT(*)::NUMERIC * 100.0 / 
        NULLIF(
            (SELECT SUM(EXTRACT(EPOCH FROM (hora_fin - hora_inicio))/1800)
             FROM horario_medico hm
             WHERE hm.id_medico = m.id_medico
               AND hm.dia_semana = EXTRACT(ISODOW FROM c.fecha)
            ), 0
        ), 2
    ) AS porcentaje_ocupacion
FROM cita c
INNER JOIN medico m ON c.id_medico = m.id_medico
INNER JOIN usuario um ON m.id_usuario = um.id_usuario
INNER JOIN especialidad e ON m.id_especialidad = e.id_especialidad
WHERE c.fecha >= CURRENT_DATE - INTERVAL '7 days'
  AND c.fecha <= CURRENT_DATE + INTERVAL '30 days'
GROUP BY m.id_medico, medico, e.nombre, c.fecha
ORDER BY c.fecha, medico;

COMMENT ON VIEW vista_ocupacion_diaria_medicos IS 
'Ocupación diaria de médicos con métricas de citas y porcentaje de ocupación';


-- 9. VISTA: Pacientes frecuentes
-- Pacientes con más citas en el sistema

CREATE OR REPLACE VIEW vista_pacientes_frecuentes AS
SELECT 
    p.id_paciente,
    u.nombre || ' ' || u.apellido AS paciente,
    u.email,
    u.telefono,
    EXTRACT(YEAR FROM AGE(p.fecha_nacimiento)) AS edad,
    COUNT(*) AS total_citas,
    COUNT(*) FILTER (WHERE c.estado = 'ATENDIDA') AS citas_atendidas,
    COUNT(*) FILTER (WHERE c.estado = 'CANCELADA') AS citas_canceladas,
    COUNT(*) FILTER (WHERE c.estado = 'NO_ASISTIO') AS inasistencias,
    MAX(c.fecha) AS ultima_cita,
    ROUND(
        COUNT(*) FILTER (WHERE c.estado = 'ATENDIDA')::NUMERIC * 100.0 / 
        NULLIF(COUNT(*), 0), 2
    ) AS tasa_asistencia
FROM paciente p
INNER JOIN usuario u ON p.id_usuario = u.id_usuario
LEFT JOIN cita c ON p.id_paciente = c.id_paciente
GROUP BY p.id_paciente, paciente, u.email, u.telefono, p.fecha_nacimiento
HAVING COUNT(c.id_cita) > 0
ORDER BY total_citas DESC, tasa_asistencia DESC;

COMMENT ON VIEW vista_pacientes_frecuentes IS 
'Pacientes ordenados por frecuencia de citas con métricas de asistencia';
