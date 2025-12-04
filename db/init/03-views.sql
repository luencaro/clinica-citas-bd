-- ============================================
-- VISTAS DEL SISTEMA DE CITAS MÉDICAS
-- Compatible con schema actual (sin campos activo/activa)
-- ============================================

-- 1. VISTA: Estadísticas generales de citas
CREATE OR REPLACE VIEW vista_estadisticas_citas AS
SELECT 
    estado,
    COUNT(*) AS cantidad,
    ROUND(COUNT(*)::NUMERIC * 100.0 / SUM(COUNT(*)) OVER (), 2) AS porcentaje
FROM cita
GROUP BY estado
ORDER BY cantidad DESC;

COMMENT ON VIEW vista_estadisticas_citas IS 'Estadísticas de citas agrupadas por estado';

-- 2. VISTA: Pacientes frecuentes
CREATE OR REPLACE VIEW vista_pacientes_frecuentes AS
SELECT 
    p.id_paciente,
    u.nombre || ' ' || u.apellido AS paciente_nombre,
    u.email,
    u.telefono,
    COUNT(c.id_cita) AS total_citas,
    COUNT(CASE WHEN c.estado = 'ATENDIDA' THEN 1 END) AS citas_atendidas,
    COUNT(CASE WHEN c.estado = 'CANCELADA' THEN 1 END) AS citas_canceladas,
    MAX(c.fecha) AS ultima_cita
FROM paciente p
JOIN usuario u ON p.id_usuario = u.id_usuario
LEFT JOIN cita c ON p.id_paciente = c.id_paciente
GROUP BY p.id_paciente, u.nombre, u.apellido, u.email, u.telefono
HAVING COUNT(c.id_cita) > 0
ORDER BY total_citas DESC;

COMMENT ON VIEW vista_pacientes_frecuentes IS 'Pacientes ordenados por frecuencia de citas';

-- 3. VISTA: Citas por médico
CREATE OR REPLACE VIEW vista_citas_por_medico AS
SELECT 
    m.id_medico,
    u.nombre || ' ' || u.apellido AS medico_nombre,
    e.nombre AS especialidad,
    COUNT(c.id_cita) AS total_citas,
    COUNT(CASE WHEN c.estado = 'ATENDIDA' THEN 1 END) AS citas_atendidas,
    COUNT(CASE WHEN c.estado = 'CANCELADA' THEN 1 END) AS citas_canceladas,
    COUNT(CASE WHEN c.estado = 'AGENDADA' THEN 1 END) AS citas_agendadas
FROM medico m
JOIN usuario u ON m.id_usuario = u.id_usuario
JOIN especialidad e ON m.id_especialidad = e.id_especialidad
LEFT JOIN cita c ON m.id_medico = c.id_medico
GROUP BY m.id_medico, u.nombre, u.apellido, e.nombre
ORDER BY total_citas DESC;

COMMENT ON VIEW vista_citas_por_medico IS 'Estadísticas de citas por médico';

-- 4. VISTA: Citas por especialidad
CREATE OR REPLACE VIEW vista_citas_por_especialidad AS
SELECT 
    e.id_especialidad,
    e.nombre AS especialidad,
    COUNT(c.id_cita) AS total_citas,
    COUNT(CASE WHEN c.estado = 'ATENDIDA' THEN 1 END) AS citas_atendidas,
    COUNT(CASE WHEN c.estado = 'CANCELADA' THEN 1 END) AS citas_canceladas,
    COUNT(DISTINCT m.id_medico) AS num_medicos
FROM especialidad e
JOIN medico m ON e.id_especialidad = m.id_especialidad
LEFT JOIN cita c ON m.id_medico = c.id_medico
GROUP BY e.id_especialidad, e.nombre
ORDER BY total_citas DESC;

COMMENT ON VIEW vista_citas_por_especialidad IS 'Estadísticas de citas por especialidad médica';

-- 5. VISTA: Horarios más demandados
CREATE OR REPLACE VIEW vista_horarios_demandados AS
SELECT 
    EXTRACT(HOUR FROM c.hora) AS hora,
    COUNT(*) AS cantidad_citas,
    COUNT(CASE WHEN c.estado = 'ATENDIDA' THEN 1 END) AS atendidas,
    COUNT(CASE WHEN c.estado = 'CANCELADA' THEN 1 END) AS canceladas
FROM cita c
GROUP BY EXTRACT(HOUR FROM c.hora)
ORDER BY cantidad_citas DESC;

COMMENT ON VIEW vista_horarios_demandados IS 'Horarios del día con mayor demanda de citas';

-- 6. VISTA: Citas por fecha (últimos 30 días)
CREATE OR REPLACE VIEW vista_citas_por_fecha AS
SELECT 
    c.fecha,
    COUNT(*) AS total_citas,
    COUNT(CASE WHEN c.estado = 'ATENDIDA' THEN 1 END) AS atendidas,
    COUNT(CASE WHEN c.estado = 'CANCELADA' THEN 1 END) AS canceladas,
    COUNT(CASE WHEN c.estado = 'AGENDADA' THEN 1 END) AS agendadas
FROM cita c
WHERE c.fecha >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY c.fecha
ORDER BY c.fecha DESC;

COMMENT ON VIEW vista_citas_por_fecha IS 'Estadísticas diarias de citas de los últimos 30 días';

-- 7. VISTA: Ocupación diaria por médico
CREATE OR REPLACE VIEW vista_ocupacion_diaria_medicos AS
SELECT 
    m.id_medico,
    u.nombre || ' ' || u.apellido AS medico_nombre,
    e.nombre AS especialidad,
    c.fecha,
    COUNT(*) AS citas_del_dia,
    COUNT(CASE WHEN c.estado = 'ATENDIDA' THEN 1 END) AS atendidas,
    COUNT(CASE WHEN c.estado = 'CANCELADA' THEN 1 END) AS canceladas
FROM medico m
JOIN usuario u ON m.id_usuario = u.id_usuario
JOIN especialidad e ON m.id_especialidad = e.id_especialidad
JOIN cita c ON m.id_medico = c.id_medico
WHERE c.fecha >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY m.id_medico, u.nombre, u.apellido, e.nombre, c.fecha
ORDER BY c.fecha DESC, citas_del_dia DESC;

COMMENT ON VIEW vista_ocupacion_diaria_medicos IS 'Ocupación diaria de cada médico en los últimos 30 días';

-- 8. VISTA: Resumen de médicos
CREATE OR REPLACE VIEW vista_resumen_medicos AS
SELECT 
    m.id_medico,
    u.nombre || ' ' || u.apellido AS medico_nombre,
    u.email,
    e.nombre AS especialidad,
    m.registro_profesional,
    COUNT(DISTINCT hm.id_horario) AS total_horarios,
    COUNT(c.id_cita) AS total_citas,
    COUNT(CASE WHEN c.fecha >= CURRENT_DATE THEN 1 END) AS citas_futuras
FROM medico m
JOIN usuario u ON m.id_usuario = u.id_usuario
JOIN especialidad e ON m.id_especialidad = e.id_especialidad
LEFT JOIN horario_medico hm ON m.id_medico = hm.id_medico
LEFT JOIN cita c ON m.id_medico = c.id_medico
GROUP BY m.id_medico, u.nombre, u.apellido, u.email, e.nombre, m.registro_profesional
ORDER BY total_citas DESC;

COMMENT ON VIEW vista_resumen_medicos IS 'Resumen completo de médicos con estadísticas';

-- 9. VISTA: Tasa de cancelación por médico
CREATE OR REPLACE VIEW vista_tasa_cancelacion_medicos AS
SELECT 
    m.id_medico,
    u.nombre || ' ' || u.apellido AS medico_nombre,
    e.nombre AS especialidad,
    COUNT(c.id_cita) AS total_citas,
    COUNT(CASE WHEN c.estado = 'CANCELADA' THEN 1 END) AS canceladas,
    CASE 
        WHEN COUNT(c.id_cita) > 0 THEN
            ROUND(COUNT(CASE WHEN c.estado = 'CANCELADA' THEN 1 END)::NUMERIC * 100.0 / COUNT(c.id_cita), 2)
        ELSE 0
    END AS tasa_cancelacion
FROM medico m
JOIN usuario u ON m.id_usuario = u.id_usuario
JOIN especialidad e ON m.id_especialidad = e.id_especialidad
LEFT JOIN cita c ON m.id_medico = c.id_medico
GROUP BY m.id_medico, u.nombre, u.apellido, e.nombre
HAVING COUNT(c.id_cita) > 0
ORDER BY tasa_cancelacion DESC;

COMMENT ON VIEW vista_tasa_cancelacion_medicos IS 'Tasa de cancelación de citas por médico';

-- Resumen de vistas creadas
DO $$
DECLARE
    v_count_views INTEGER;
BEGIN
    SELECT COUNT(*) INTO v_count_views
    FROM information_schema.views 
    WHERE table_schema = 'public';
    
    RAISE NOTICE '========================================================';
    RAISE NOTICE 'VISTAS CREADAS EXITOSAMENTE';
    RAISE NOTICE '========================================================';
    RAISE NOTICE 'Total de vistas: %', v_count_views;
    RAISE NOTICE '========================================================';
END $$;
