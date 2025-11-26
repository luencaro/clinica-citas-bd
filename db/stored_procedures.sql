-- ============================================
-- STORED PROCEDURES DEL SISTEMA DE CITAS
-- ============================================

-- 1. PROCEDURE: Validar disponibilidad de horario
-- Verifica si un médico tiene disponible un horario específico

CREATE OR REPLACE FUNCTION sp_validar_disponibilidad(
    p_id_medico INTEGER,
    p_fecha DATE,
    p_hora TIME
)
RETURNS BOOLEAN AS $$
DECLARE
    v_dia_semana INTEGER;
    v_tiene_horario BOOLEAN;
    v_tiene_cita BOOLEAN;
BEGIN
    -- Obtener día de la semana (1=Lunes, 7=Domingo)
    v_dia_semana := EXTRACT(ISODOW FROM p_fecha);
    
    -- Verificar si el médico tiene horario ese día
    SELECT EXISTS (
        SELECT 1
        FROM horario_medico
        WHERE id_medico = p_id_medico
          AND dia_semana = v_dia_semana
          AND p_hora >= hora_inicio
          AND p_hora < hora_fin
    ) INTO v_tiene_horario;
    
    IF NOT v_tiene_horario THEN
        RETURN FALSE;
    END IF;
    
    -- Verificar si ya hay una cita en ese horario
    SELECT EXISTS (
        SELECT 1
        FROM cita
        WHERE id_medico = p_id_medico
          AND fecha = p_fecha
          AND hora = p_hora
          AND estado NOT IN ('CANCELADA', 'NO_ASISTIO')
    ) INTO v_tiene_cita;
    
    RETURN NOT v_tiene_cita;
END;
$$ LANGUAGE plpgsql;


-- 2. PROCEDURE: Agendar cita completa
-- Agenda una cita con todas las validaciones

CREATE OR REPLACE FUNCTION sp_agendar_cita(
    p_id_paciente INTEGER,
    p_id_medico INTEGER,
    p_fecha DATE,
    p_hora TIME,
    p_motivo TEXT,
    p_observaciones TEXT DEFAULT NULL
)
RETURNS INTEGER AS $$
DECLARE
    v_id_cita INTEGER;
    v_disponible BOOLEAN;
BEGIN
    -- Validar que la fecha sea futura
    IF p_fecha <= CURRENT_DATE THEN
        RAISE EXCEPTION 'La fecha debe ser futura';
    END IF;
    
    -- Validar disponibilidad
    v_disponible := sp_validar_disponibilidad(p_id_medico, p_fecha, p_hora);
    
    IF NOT v_disponible THEN
        RAISE EXCEPTION 'El horario no está disponible';
    END IF;
    
    -- Crear la cita
    INSERT INTO cita (
        id_paciente,
        id_medico,
        fecha,
        hora,
        motivo,
        observaciones,
        estado
    )
    VALUES (
        p_id_paciente,
        p_id_medico,
        p_fecha,
        p_hora,
        p_motivo,
        p_observaciones,
        'AGENDADA'
    )
    RETURNING id_cita INTO v_id_cita;
    
    -- Las notificaciones se crean automáticamente con el trigger
    
    RETURN v_id_cita;
END;
$$ LANGUAGE plpgsql;


-- 3. PROCEDURE: Obtener disponibilidad de médico en un día
-- Retorna todos los horarios disponibles de un médico en una fecha

CREATE OR REPLACE FUNCTION sp_obtener_disponibilidad_dia(
    p_id_medico INTEGER,
    p_fecha DATE
)
RETURNS TABLE(
    hora_disponible TIME
) AS $$
DECLARE
    v_dia_semana INTEGER;
    v_horario RECORD;
    v_hora_actual TIME;
BEGIN
    -- Obtener día de la semana
    v_dia_semana := EXTRACT(ISODOW FROM p_fecha);
    
    -- Iterar sobre los horarios del médico
    FOR v_horario IN
        SELECT hora_inicio, hora_fin
        FROM horario_medico
        WHERE id_medico = p_id_medico
          AND dia_semana = v_dia_semana
        ORDER BY hora_inicio
    LOOP
        -- Generar slots de 30 minutos
        v_hora_actual := v_horario.hora_inicio;
        
        WHILE v_hora_actual < v_horario.hora_fin LOOP
            -- Verificar si está disponible
            IF sp_validar_disponibilidad(p_id_medico, p_fecha, v_hora_actual) THEN
                hora_disponible := v_hora_actual;
                RETURN NEXT;
            END IF;
            
            -- Incrementar 30 minutos
            v_hora_actual := v_hora_actual + INTERVAL '30 minutes';
        END LOOP;
    END LOOP;
    
    RETURN;
END;
$$ LANGUAGE plpgsql;


-- 4. PROCEDURE: Cancelar cita
-- Cancela una cita con validaciones

CREATE OR REPLACE FUNCTION sp_cancelar_cita(
    p_id_cita INTEGER,
    p_motivo TEXT DEFAULT NULL
)
RETURNS VOID AS $$
DECLARE
    v_estado_actual VARCHAR(20);
BEGIN
    -- Obtener estado actual
    SELECT estado INTO v_estado_actual
    FROM cita
    WHERE id_cita = p_id_cita;
    
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Cita no encontrada';
    END IF;
    
    -- Solo se pueden cancelar citas AGENDADAS
    IF v_estado_actual != 'AGENDADA' THEN
        RAISE EXCEPTION 'Solo se pueden cancelar citas agendadas';
    END IF;
    
    -- Actualizar estado
    UPDATE cita
    SET estado = 'CANCELADA',
        observaciones = COALESCE(p_motivo, observaciones)
    WHERE id_cita = p_id_cita;
    
    -- Los triggers se encargan del resto (historial + notificaciones)
END;
$$ LANGUAGE plpgsql;


-- 5. PROCEDURE: Reprogramar cita
-- Cambia fecha/hora de una cita existente

CREATE OR REPLACE FUNCTION sp_reprogramar_cita(
    p_id_cita INTEGER,
    p_nueva_fecha DATE,
    p_nueva_hora TIME
)
RETURNS VOID AS $$
DECLARE
    v_id_medico INTEGER;
    v_estado_actual VARCHAR(20);
    v_disponible BOOLEAN;
BEGIN
    -- Obtener datos de la cita
    SELECT id_medico, estado
    INTO v_id_medico, v_estado_actual
    FROM cita
    WHERE id_cita = p_id_cita;
    
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Cita no encontrada';
    END IF;
    
    -- Solo se pueden reprogramar citas AGENDADAS o REPROGRAMADAS
    IF v_estado_actual NOT IN ('AGENDADA', 'REPROGRAMADA') THEN
        RAISE EXCEPTION 'Esta cita no puede ser reprogramada';
    END IF;
    
    -- Validar nueva disponibilidad
    v_disponible := sp_validar_disponibilidad(
        v_id_medico,
        p_nueva_fecha,
        p_nueva_hora
    );
    
    IF NOT v_disponible THEN
        RAISE EXCEPTION 'El nuevo horario no está disponible';
    END IF;
    
    -- Actualizar cita
    UPDATE cita
    SET fecha = p_nueva_fecha,
        hora = p_nueva_hora,
        estado = 'REPROGRAMADA'
    WHERE id_cita = p_id_cita;
END;
$$ LANGUAGE plpgsql;


-- 6. PROCEDURE: Obtener próximas citas de un paciente
-- Retorna las próximas N citas de un paciente

CREATE OR REPLACE FUNCTION sp_proximas_citas_paciente(
    p_id_paciente INTEGER,
    p_limite INTEGER DEFAULT 10
)
RETURNS TABLE(
    id_cita INTEGER,
    fecha DATE,
    hora TIME,
    estado VARCHAR(20),
    nombre_medico TEXT,
    especialidad TEXT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        c.id_cita,
        c.fecha,
        c.hora,
        c.estado,
        (u.nombre || ' ' || u.apellido) AS nombre_medico,
        e.nombre AS especialidad
    FROM cita c
    INNER JOIN medico m ON c.id_medico = m.id_medico
    INNER JOIN usuario u ON m.id_usuario = u.id_usuario
    INNER JOIN especialidad e ON m.id_especialidad = e.id_especialidad
    WHERE c.id_paciente = p_id_paciente
      AND c.fecha >= CURRENT_DATE
      AND c.estado IN ('AGENDADA', 'REPROGRAMADA')
    ORDER BY c.fecha, c.hora
    LIMIT p_limite;
END;
$$ LANGUAGE plpgsql;


-- 7. PROCEDURE: Estadísticas de citas por médico
-- Retorna estadísticas de citas de un médico

CREATE OR REPLACE FUNCTION sp_estadisticas_medico(
    p_id_medico INTEGER,
    p_fecha_desde DATE DEFAULT NULL,
    p_fecha_hasta DATE DEFAULT NULL
)
RETURNS TABLE(
    total_citas BIGINT,
    citas_atendidas BIGINT,
    citas_canceladas BIGINT,
    citas_no_asistio BIGINT,
    tasa_asistencia NUMERIC
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        COUNT(*) AS total_citas,
        COUNT(*) FILTER (WHERE estado = 'ATENDIDA') AS citas_atendidas,
        COUNT(*) FILTER (WHERE estado = 'CANCELADA') AS citas_canceladas,
        COUNT(*) FILTER (WHERE estado = 'NO_ASISTIO') AS citas_no_asistio,
        ROUND(
            COUNT(*) FILTER (WHERE estado = 'ATENDIDA')::NUMERIC * 100.0 / 
            NULLIF(COUNT(*), 0),
            2
        ) AS tasa_asistencia
    FROM cita
    WHERE id_medico = p_id_medico
      AND (p_fecha_desde IS NULL OR fecha >= p_fecha_desde)
      AND (p_fecha_hasta IS NULL OR fecha <= p_fecha_hasta);
END;
$$ LANGUAGE plpgsql;
