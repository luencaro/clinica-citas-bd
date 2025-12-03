"""
Servicio de Reportes - Usa VISTAS SQL para generar reportes
"""

from typing import List, Dict, Any
from datetime import date, datetime, timedelta
from database import db


class ReporteService:
    """
    Servicio para generar reportes usando las VISTAS SQL creadas
    """
    
    def obtener_estadisticas_generales(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas generales del sistema
        Usa: vista_estadisticas_citas
        """
        query = """
            SELECT estado, cantidad, porcentaje
            FROM vista_estadisticas_citas
            ORDER BY cantidad DESC
        """
        results = db.execute_query(query, fetch='all')
        
        estadisticas = []
        for row in results:
            estadisticas.append({
                'estado': row[0],
                'cantidad': row[1],
                'porcentaje': float(row[2]) if row[2] else 0
            })
        
        return {
            'estadisticas_por_estado': estadisticas,
            'fecha_generacion': datetime.now().isoformat()
        }
    
    def obtener_citas_por_medico(
        self,
        fecha_desde: date = None,
        fecha_hasta: date = None
    ) -> List[Dict[str, Any]]:
        """
        Reporte de citas agrupadas por médico con estadísticas
        """
        if not fecha_desde:
            fecha_desde = date.today() - timedelta(days=30)
        if not fecha_hasta:
            fecha_hasta = date.today()
        
        query = """
            SELECT 
                m.id_medico,
                u.nombre || ' ' || u.apellido AS medico,
                e.nombre AS especialidad,
                COUNT(*) AS total_citas,
                COUNT(*) FILTER (WHERE c.estado = 'AGENDADA') AS agendadas,
                COUNT(*) FILTER (WHERE c.estado = 'ATENDIDA') AS atendidas,
                COUNT(*) FILTER (WHERE c.estado = 'CANCELADA') AS canceladas,
                COUNT(*) FILTER (WHERE c.estado = 'NO_ASISTIO') AS no_asistio,
                ROUND(
                    COUNT(*) FILTER (WHERE c.estado = 'ATENDIDA')::NUMERIC * 100.0 / 
                    NULLIF(COUNT(*), 0), 2
                ) AS tasa_atencion
            FROM cita c
            INNER JOIN medico m ON c.id_medico = m.id_medico
            INNER JOIN usuario u ON m.id_usuario = u.id_usuario
            INNER JOIN especialidad e ON m.id_especialidad = e.id_especialidad
            WHERE c.fecha BETWEEN %s AND %s
            GROUP BY m.id_medico, medico, e.nombre
            ORDER BY total_citas DESC, medico
        """
        
        results = db.execute_query(query, (fecha_desde, fecha_hasta), fetch='all')
        
        reportes = []
        for row in results:
            reportes.append({
                'id_medico': row[0],
                'medico': row[1],
                'especialidad': row[2],
                'total_citas': row[3],
                'agendadas': row[4],
                'atendidas': row[5],
                'canceladas': row[6],
                'no_asistio': row[7],
                'tasa_atencion': float(row[8]) if row[8] else 0
            })
        
        return reportes
    
    def obtener_citas_por_especialidad(
        self,
        fecha_desde: date = None,
        fecha_hasta: date = None
    ) -> List[Dict[str, Any]]:
        """
        Reporte de citas agrupadas por especialidad
        Usa: vista_medicos_por_especialidad + datos de citas
        """
        if not fecha_desde:
            fecha_desde = date.today() - timedelta(days=30)
        if not fecha_hasta:
            fecha_hasta = date.today()
        
        query = """
            SELECT 
                e.id_especialidad,
                e.nombre AS especialidad,
                COUNT(*) AS total_citas,
                COUNT(DISTINCT c.id_medico) AS medicos_activos,
                COUNT(*) FILTER (WHERE c.estado = 'ATENDIDA') AS atendidas,
                COUNT(*) FILTER (WHERE c.estado = 'CANCELADA') AS canceladas,
                ROUND(
                    COUNT(*) FILTER (WHERE c.estado = 'ATENDIDA')::NUMERIC * 100.0 / 
                    NULLIF(COUNT(*), 0), 2
                ) AS tasa_atencion
            FROM cita c
            INNER JOIN medico m ON c.id_medico = m.id_medico
            INNER JOIN especialidad e ON m.id_especialidad = e.id_especialidad
            WHERE c.fecha BETWEEN %s AND %s
            GROUP BY e.id_especialidad, e.nombre
            ORDER BY total_citas DESC
        """
        
        results = db.execute_query(query, (fecha_desde, fecha_hasta), fetch='all')
        
        reportes = []
        for row in results:
            reportes.append({
                'id_especialidad': row[0],
                'especialidad': row[1],
                'total_citas': row[2],
                'medicos_activos': row[3],
                'atendidas': row[4],
                'canceladas': row[5],
                'tasa_atencion': float(row[6]) if row[6] else 0
            })
        
        return reportes
    
    def obtener_pacientes_frecuentes(self, limite: int = 20) -> List[Dict[str, Any]]:
        """
        Obtiene los pacientes más frecuentes
        Usa: vista_pacientes_frecuentes
        """
        query = f"""
            SELECT 
                id_paciente,
                paciente_nombre,
                email,
                telefono,
                total_citas,
                citas_atendidas,
                citas_canceladas,
                ultima_cita
            FROM vista_pacientes_frecuentes
            LIMIT {limite}
        """
        
        results = db.execute_query(query, fetch='all')
        
        pacientes = []
        for row in results:
            pacientes.append({
                'id_paciente': row[0],
                'paciente': row[1],
                'email': row[2],
                'telefono': row[3],
                'total_citas': row[4],
                'citas_atendidas': row[5],
                'citas_canceladas': row[6],
                'ultima_cita': row[7].isoformat() if row[7] else None
            })
        
        return pacientes
    
    def obtener_horarios_demandados(
        self,
        fecha_desde: date = None,
        fecha_hasta: date = None
    ) -> List[Dict[str, Any]]:
        """
        Obtiene los horarios con más demanda
        """
        if not fecha_desde:
            fecha_desde = date.today() - timedelta(days=30)
        if not fecha_hasta:
            fecha_hasta = date.today()
        
        query = """
            SELECT 
                c.hora,
                COUNT(*) AS total_citas,
                COUNT(*) FILTER (WHERE c.estado = 'ATENDIDA') AS atendidas,
                COUNT(*) FILTER (WHERE c.estado = 'CANCELADA') AS canceladas,
                ROUND(AVG(EXTRACT(EPOCH FROM (c.fecha_creacion - (c.fecha + c.hora)::TIMESTAMP))/3600), 2) AS horas_anticipacion_promedio
            FROM cita c
            WHERE c.fecha BETWEEN %s AND %s
            GROUP BY c.hora
            ORDER BY total_citas DESC
        """
        
        results = db.execute_query(query, (fecha_desde, fecha_hasta), fetch='all')
        
        horarios = []
        for row in results:
            horarios.append({
                'hora': str(row[0]),
                'total_citas': row[1],
                'atendidas': row[2],
                'canceladas': row[3],
                'horas_anticipacion_promedio': float(row[4]) if row[4] else 0
            })
        
        return horarios
    
    def obtener_tasa_cancelacion(
        self,
        fecha_desde: date = None,
        fecha_hasta: date = None
    ) -> Dict[str, Any]:
        """
        Calcula la tasa de cancelación del sistema
        """
        if not fecha_desde:
            fecha_desde = date.today() - timedelta(days=30)
        if not fecha_hasta:
            fecha_hasta = date.today()
        
        query = """
            SELECT 
                COUNT(*) AS total_citas,
                COUNT(*) FILTER (WHERE estado = 'CANCELADA') AS canceladas,
                COUNT(*) FILTER (WHERE estado = 'ATENDIDA') AS atendidas,
                COUNT(*) FILTER (WHERE estado = 'NO_ASISTIO') AS no_asistio,
                ROUND(
                    COUNT(*) FILTER (WHERE estado = 'CANCELADA')::NUMERIC * 100.0 / 
                    NULLIF(COUNT(*), 0), 2
                ) AS tasa_cancelacion,
                ROUND(
                    COUNT(*) FILTER (WHERE estado = 'ATENDIDA')::NUMERIC * 100.0 / 
                    NULLIF(COUNT(*), 0), 2
                ) AS tasa_asistencia
            FROM cita
            WHERE fecha BETWEEN %s AND %s
        """
        
        result = db.execute_query(query, (fecha_desde, fecha_hasta), fetch='one')
        
        return {
            'periodo': {
                'desde': fecha_desde.isoformat(),
                'hasta': fecha_hasta.isoformat()
            },
            'total_citas': result[0],
            'canceladas': result[1],
            'atendidas': result[2],
            'no_asistio': result[3],
            'tasa_cancelacion': float(result[4]) if result[4] else 0,
            'tasa_asistencia': float(result[5]) if result[5] else 0
        }
    
    def obtener_ocupacion_medicos(
        self,
        fecha_desde: date = None,
        fecha_hasta: date = None
    ) -> List[Dict[str, Any]]:
        """
        Obtiene la ocupación diaria de médicos
        Usa: vista_ocupacion_diaria_medicos
        """
        if not fecha_desde:
            fecha_desde = date.today()
        if not fecha_hasta:
            fecha_hasta = date.today() + timedelta(days=7)
        
        query = """
            SELECT 
                id_medico,
                medico_nombre,
                especialidad,
                fecha,
                citas_del_dia,
                atendidas,
                canceladas
            FROM vista_ocupacion_diaria_medicos
            WHERE fecha BETWEEN %s AND %s
            ORDER BY fecha, medico_nombre
        """
        
        results = db.execute_query(query, (fecha_desde, fecha_hasta), fetch='all')
        
        ocupacion = []
        for row in results:
            ocupacion.append({
                'id_medico': row[0],
                'medico': row[1],
                'especialidad': row[2],
                'fecha': row[3].isoformat() if row[3] else None,
                'total_citas': row[4],
                'atendidas': row[5],
                'canceladas': row[6]
            })
        
        return ocupacion
