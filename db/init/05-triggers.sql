-- ============================================
-- TRIGGERS DEL SISTEMA DE CITAS MÉDICAS
-- ============================================

-- 1. TRIGGER: Auditar cambios en citas (historial_cita)
-- Registra automáticamente cualquier cambio de estado en una cita

CREATE OR REPLACE FUNCTION registrar_historial_cita()
RETURNS TRIGGER AS $$
BEGIN
    -- Solo registrar si cambió el estado
    IF (TG_OP = 'UPDATE' AND OLD.estado != NEW.estado) THEN
        INSERT INTO historial_cita (
            id_cita,
            fecha_cambio,
            estado_anterior,
            estado_nuevo,
            descripcion
        )
        VALUES (
            NEW.id_cita,
            CURRENT_TIMESTAMP,
            OLD.estado,
            NEW.estado,
            NEW.observaciones
        );
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_historial_cita
AFTER UPDATE ON cita
FOR EACH ROW
EXECUTE FUNCTION registrar_historial_cita();


-- 2. TRIGGER: Crear notificaciones automáticas al agendar cita
-- Notifica al paciente y al médico cuando se agenda una cita nueva

CREATE OR REPLACE FUNCTION notificar_nueva_cita()
RETURNS TRIGGER AS $$
DECLARE
    v_id_usuario_paciente INTEGER;
    v_id_usuario_medico INTEGER;
BEGIN
    -- Obtener ID de usuario del paciente
    SELECT id_usuario INTO v_id_usuario_paciente
    FROM paciente
    WHERE id_paciente = NEW.id_paciente;
    
    -- Obtener ID de usuario del médico
    SELECT id_usuario INTO v_id_usuario_medico
    FROM medico
    WHERE id_medico = NEW.id_medico;
    
    -- Notificar al paciente
    INSERT INTO notificacion (id_usuario, tipo, mensaje)
    VALUES (
        v_id_usuario_paciente,
        'CONFIRMACION',
        'Cita agendada para el ' || NEW.fecha || ' a las ' || NEW.hora
    );
    
    -- Notificar al médico
    INSERT INTO notificacion (id_usuario, tipo, mensaje)
    VALUES (
        v_id_usuario_medico,
        'INFO',
        'Nueva cita agendada para el ' || NEW.fecha || ' a las ' || NEW.hora
    );
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_notificar_nueva_cita
AFTER INSERT ON cita
FOR EACH ROW
EXECUTE FUNCTION notificar_nueva_cita();


-- 3. TRIGGER: Notificar cancelación de cita
-- Envía notificación cuando se cancela una cita

CREATE OR REPLACE FUNCTION notificar_cancelacion_cita()
RETURNS TRIGGER AS $$
DECLARE
    v_id_usuario_paciente INTEGER;
BEGIN
    -- Solo actuar si cambió a CANCELADA
    IF (OLD.estado != 'CANCELADA' AND NEW.estado = 'CANCELADA') THEN
        -- Obtener ID de usuario del paciente
        SELECT id_usuario INTO v_id_usuario_paciente
        FROM paciente
        WHERE id_paciente = NEW.id_paciente;
        
        -- Notificar cancelación
        INSERT INTO notificacion (id_usuario, tipo, mensaje)
        VALUES (
            v_id_usuario_paciente,
            'ALERTA',
            'Su cita del ' || NEW.fecha || ' a las ' || NEW.hora || ' ha sido cancelada'
        );
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_notificar_cancelacion
AFTER UPDATE ON cita
FOR EACH ROW
EXECUTE FUNCTION notificar_cancelacion_cita();


-- 4. TRIGGER: Validar horario laboral al insertar/actualizar horarios
-- Asegura que los horarios estén dentro del rango permitido (6:00 - 22:00)

CREATE OR REPLACE FUNCTION validar_horario_laboral()
RETURNS TRIGGER AS $$
BEGIN
    -- Validar que hora_inicio y hora_fin estén en rango
    IF (NEW.hora_inicio < '06:00:00' OR NEW.hora_inicio > '22:00:00') THEN
        RAISE EXCEPTION 'Hora de inicio debe estar entre 06:00 y 22:00';
    END IF;
    
    IF (NEW.hora_fin < '06:00:00' OR NEW.hora_fin > '22:00:00') THEN
        RAISE EXCEPTION 'Hora de fin debe estar entre 06:00 y 22:00';
    END IF;
    
    IF (NEW.hora_fin <= NEW.hora_inicio) THEN
        RAISE EXCEPTION 'Hora de fin debe ser mayor que hora de inicio';
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_validar_horario_laboral
BEFORE INSERT OR UPDATE ON horario_medico
FOR EACH ROW
EXECUTE FUNCTION validar_horario_laboral();


-- NOTA: Los triggers de fecha_modificacion fueron removidos porque
-- las tablas no tienen la columna fecha_modificacion en el esquema actual.
-- El registro de cambios se hace a través de historial_cita para la tabla cita.
