# 🏥 Sistema de Gestión de Citas Médicas

Sistema completo de gestión de citas médicas desarrollado con Python, PostgreSQL y Django, utilizando arquitectura en capas con stored procedures y triggers.

## 🚀 Inicio Rápido

```bash
# Levantar el sistema
sudo docker compose up -d

# Acceder a la aplicación
http://localhost:5000

# Credenciales de prueba
Admin:    admin@clinica.com / Clinica2025!
Médico:   juan.fernandez@email.com / Clinica2025!
Paciente: luis.gomez@email.com / Clinica2025!
```

## ✨ Características Principales

- ✅ **Gestión de Citas**: Agendamiento con validación de disponibilidad en tiempo real
- ✅ **3 Roles**: Admin, Médico y Paciente con permisos diferenciados
- ✅ **Stored Procedures**: Lógica crítica de negocio en PostgreSQL
- ✅ **Triggers Automáticos**: Auditoría y notificaciones
- ✅ **Reportes SQL**: 9 vistas para dashboard administrativo
- ✅ **Autenticación Segura**: bcrypt para contraseñas
- ✅ **Interfaz Web**: Django con plantillas Bootstrap

## 🏛️ Arquitectura

```
┌─────────────────────────────────────┐
│      Django Web Interface           │  ← Templates + Views
├─────────────────────────────────────┤
│         Service Layer               │  ← Lógica de negocio
├─────────────────────────────────────┤
│       Repository Pattern            │  ← Acceso a datos
├─────────────────────────────────────┤
│  PostgreSQL (Triggers + Procedures) │  ← Base de datos
└─────────────────────────────────────┘
```

## 🗄️ Base de Datos

### Tablas (8)
- `usuario` - Usuarios del sistema
- `paciente` - Información de pacientes
- `medico` - Médicos con especialidades
- `especialidad` - Catálogo de especialidades
- `horario_medico` - Horarios por día de semana
- `cita` - Citas médicas
- `historial_cita` - Auditoría de cambios
- `notificacion` - Sistema de notificaciones

### Stored Procedures (7)
- `sp_validar_disponibilidad()` - Verifica horarios libres
- `sp_agendar_cita()` - Crea citas con validaciones
- `sp_cancelar_cita()` - Cancela citas con auditoría
- `sp_reprogramar_cita()` - Cambia fecha/hora de citas
- `sp_obtener_disponibilidad_dia()` - Slots disponibles
- `sp_proximas_citas_paciente()` - Próximas citas
- `sp_estadisticas_medico()` - Reportes por médico

### Triggers (5)
- `trigger_historial_cita` - Registra cambios de estado
- `trigger_notificar_nueva_cita` - Notifica al agendar
- `trigger_notificar_cancelacion` - Notifica al cancelar
- `trigger_validar_horario_laboral` - Valida rango 06:00-22:00

### Vistas SQL (9)
- `vista_estadisticas_citas` - Estadísticas generales
- `vista_pacientes_frecuentes` - Top pacientes
- `vista_citas_por_medico` - Citas por médico
- `vista_citas_por_especialidad` - Por especialidad
- `vista_horarios_demandados` - Horarios populares
- `vista_citas_por_fecha` - Estadísticas diarias
- `vista_ocupacion_diaria_medicos` - Ocupación
- `vista_resumen_medicos` - Resumen general
- `vista_tasa_cancelacion_medicos` - Tasa de cancelación

## 📁 Estructura del Proyecto

```
clinica-citas-bd/
├── app/
│   ├── database/           # Conexión y pooling PostgreSQL
│   ├── models/             # 8 modelos del dominio
│   ├── repositories/       # 8 repositorios (patrón Repository)
│   ├── services/           # 4 servicios de negocio
│   ├── validators.py       # Validaciones de datos
│   ├── exceptions.py       # Excepciones personalizadas
│   └── webapp/
│       ├── views.py        # Controladores Django
│       ├── urls.py         # Rutas
│       └── templates/      # Plantillas HTML
├── db/
│   └── init/               # Scripts de inicialización
│       ├── 01-schema.sql
│       ├── 02-seed-data.sql
│       ├── 03-views.sql
│       ├── 04-stored-procedures.sql
│       └── 05-triggers.sql
└── docker-compose.yml
```

## 🛠️ Tecnologías

- **Backend:** Python 3.11, Django 4.2
- **Base de Datos:** PostgreSQL 16
- **Frontend:** Bootstrap 5, HTML5
- **Containerización:** Docker Compose
- **Seguridad:** bcrypt para contraseñas
- **Patrón:** Repository + Service Layer

## 📊 Datos de Prueba

El sistema incluye:
- 18 usuarios (2 admin, 6 médicos, 10 pacientes)
- 10 especialidades médicas
- 26 horarios configurados para médicos
- 63 citas (histórico Octubre-Diciembre 2025)
- 21 notificaciones generadas automáticamente

## 🎯 Funcionalidades por Rol

### 👨‍⚕️ Médico
- Ver citas del día
- Marcar citas como atendidas
- Ver horarios configurados
- Gestionar perfil

### 👤 Paciente
- Agendar nuevas citas
- Ver próximas citas
- Cancelar citas propias
- Ver historial de citas
- Recibir notificaciones

### 👔 Administrador
- Gestionar todos los usuarios
- Agendar citas para cualquier paciente
- Ver todas las citas del sistema
- Acceder a reportes y estadísticas
- Dashboard con 9 vistas SQL

## 🔧 Comandos Útiles

```bash
# Ver logs
sudo docker compose logs app -f

# Acceder a PostgreSQL
sudo docker compose exec db psql -U clinica_admin -d clinica_citas

# Reiniciar base de datos
sudo docker compose down -v
sudo docker compose up -d
```

## 📝 Notas Técnicas

### Validaciones Implementadas
- Fecha de cita debe ser futura 
- Horario debe estar en rango del médico (06:00-22:00)
- No permite citas duplicadas (mismo médico, fecha, hora)
- Paciente no puede tener dos citas a la misma hora
- Solo se cancelan citas AGENDADAS

### Reglas de Negocio
- Médicos trabajan L-V con horarios configurables
- Citas tienen estados: AGENDADA, ATENDIDA, CANCELADA, REPROGRAMADA
- Notificaciones automáticas al agendar/cancelar
- Historial completo de cambios de estado
- Triggers automáticos para auditoría

### Puertos
- Aplicación: http://localhost:5000
- PostgreSQL: localhost:5432 (interno), 5433 (externo)