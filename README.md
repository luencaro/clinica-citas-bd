# 🏥 Sistema de Gestión de Citas Médicas

Sistema completo de gestión de citas médicas con arquitectura en capas, desarrollado en Python con PostgreSQL.

## 📋 Tabla de Contenidos

- [Características](#características)
- [Arquitectura](#arquitectura)
- [Tecnologías](#tecnologías)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Instalación](#instalación)
- [Base de Datos](#base-de-datos)
- [Lógica de Negocio](#lógica-de-negocio)
- [Próximos Pasos](#próximos-pasos)

## ✨ Características

### Funcionalidades Principales
- ✅ **Gestión de Usuarios**: Pacientes, Médicos y Administradores con autenticación bcrypt
- ✅ **Especialidades Médicas**: Catálogo de especialidades con médicos asignados
- ✅ **Agendamiento de Citas**: Sistema completo con validación de disponibilidad
- ✅ **Horarios de Médicos**: Configuración flexible por día de la semana
- ✅ **Notificaciones**: Sistema automático de notificaciones por triggers
- ✅ **Historial de Cambios**: Auditoría completa de cambios de estado de citas
- ✅ **Validaciones Completas**: Reglas de negocio implementadas en todas las capas

### Características Técnicas
- 🔐 **Seguridad**: Contraseñas hasheadas con bcrypt, validaciones exhaustivas
- 🗄️ **Base de Datos**: PostgreSQL 16 con triggers, stored procedures y vistas
- ��️ **Arquitectura en Capas**: Separación clara de responsabilidades
- 🐳 **Docker**: Contenedorización completa del sistema
- 📊 **Vistas SQL**: 9 vistas para reportes y estadísticas
- 🔄 **Triggers**: 5 triggers automáticos para auditoría y notificaciones
- 📦 **Stored Procedures**: 7 procedimientos almacenados para lógica compleja

## 🏛️ Arquitectura

```
┌─────────────────────────────────────┐
│         UI Layer (Django)           │  ← Próxima implementación
├─────────────────────────────────────┤
│       Business Logic Layer          │
│  ┌─────────────────────────────┐   │
│  │        Services             │   │  ← Lógica de negocio
│  └─────────────────────────────┘   │
├─────────────────────────────────────┤
│      Data Access Layer              │
│  ┌─────────────────────────────┐   │
│  │      Repositories           │   │  ← Acceso a datos
│  └─────────────────────────────┘   │
├─────────────────────────────────────┤
│       Domain Layer                  │
│  ┌──────────┬──────────┬────────┐  │
│  │ Models   │Validators│Excep.  │  │  ← Dominio
│  └──────────┴──────────┴────────┘  │
├─────────────────────────────────────┤
│      Database Layer                 │
│  PostgreSQL + Triggers + Views      │
└─────────────────────────────────────┘
```

## 🛠️ Tecnologías

- **Python 3.11**: Lenguaje principal
- **PostgreSQL 16**: Base de datos relacional
- **Docker**: Contenedorización
- **bcrypt**: Hashing de contraseñas
- **Django 4.2**: Framework web (preparado)

## 📁 Estructura del Proyecto

```
app/
├── models/              # 8 modelos del dominio
├── repositories/        # 7 repositorios de datos
├── services/           # 5 servicios de negocio
├── exceptions.py       # 20+ excepciones
├── validators.py       # Validaciones completas
└── database.py         # Conexión PostgreSQL

db/
├── schema.sql          # 8 tablas
├── triggers.sql        # 5 triggers
├── stored_procedures.sql # 7 procedures
└── views.sql          # 9 vistas
```

## 🚀 Instalación

```bash
# Levantar contenedores
sudo docker compose up -d

# Verificar estado
make status
```

**Todo está listo!** Schema, seed data, triggers, procedures y vistas ya aplicados.

## 🗄️ Base de Datos

### Conexión
- Host: `localhost:5433`
- Usuario: `clinica_admin`
- Database: `clinica_citas`
- Admin: `admin@clinica.com` / `Clinica2025!`

### Tablas (8)
usuario | paciente | medico | especialidad | horario_medico | cita | historial_cita | notificacion

### Triggers (5)
- Auditoría automática de cambios
- Notificaciones al agendar/cancelar
- Validación de horarios laborales (06:00-22:00)
- Actualización de timestamps

### Stored Procedures (7)
- sp_validar_disponibilidad
- sp_agendar_cita
- sp_cancelar_cita
- sp_reprogramar_cita
- sp_obtener_disponibilidad_dia
- sp_proximas_citas_paciente
- sp_estadisticas_medico

### Vistas (9)
- vista_citas_completas (JOIN completo)
- vista_disponibilidad_medicos
- vista_estadisticas_citas
- vista_proximas_citas
- vista_historial_citas
- vista_medicos_por_especialidad
- vista_notificaciones_pendientes
- vista_ocupacion_diaria_medicos
- vista_pacientes_frecuentes

## 💼 Lógica de Negocio

### Services Implementados

#### UsuarioService
```python
from app.services import UsuarioService

service = UsuarioService()

# Crear usuario
usuario = service.crear_usuario(
    nombre="Juan", apellido="Pérez",
    email="juan@email.com", telefono="555-1234",
    contraseña="Password123", rol="PACIENTE"
)

# Autenticar
usuario = service.autenticar("juan@email.com", "Password123")
```

#### PacienteService
```python
# Crear paciente completo (usuario + paciente)
usuario, paciente = service.crear_paciente_completo(
    nombre="María", apellido="García",
    email="maria@email.com", telefono="555-5678",
    contraseña="SecurePass123",
    fecha_nacimiento=date(1990, 5, 15)
)
```

#### MedicoService
```python
# Crear médico completo
usuario, medico = service.crear_medico_completo(
    nombre="Dr. Carlos", apellido="Rodríguez",
    email="carlos@clinica.com",
    id_especialidad=1,
    registro_profesional="MED-12345"
)

# Agregar horario
horario = service.agregar_horario(
    id_medico=1, dia_semana=1,
    hora_inicio=time(9,0), hora_fin=time(17,0)
)
```

#### CitaService (El más crítico)
```python
# Agendar cita con todas las validaciones
cita = service.agendar_cita(
    id_paciente=1, id_medico=1,
    fecha=date(2025, 12, 1), hora=time(10, 0),
    motivo="Consulta general"
)

# Obtener disponibilidad
horarios = service.obtener_disponibilidad_medico(1, date(2025, 12, 1))

# Cancelar/Reprogramar
service.cancelar_cita(id_cita=1)
service.reprogramar_cita(id_cita=1, nueva_fecha=..., nueva_hora=...)
```

### Validaciones Automáticas

✅ Email formato válido (regex)  
✅ Teléfono formato válido  
✅ Contraseña: min 8 chars, mayúscula, minúscula, número  
✅ Fechas futuras (máx 6 meses)  
✅ Horarios 06:00-22:00  
✅ Citas en horas exactas/medias (10:00, 10:30)  
✅ Verificación de disponibilidad médico  
✅ Estados válidos de citas

### Excepciones (20+)
EmailDuplicadoError, CitaNoDisponibleError, FechaPasadaError, CredencialesInvalidasError, MedicoInactivoError, HorarioSuperposicionError, y más...

## 📋 Próximos Pasos

### Fase 1: UI con Django ✨
- [ ] Configurar proyecto Django
- [ ] Crear vistas y templates
- [ ] Sistema de autenticación
- [ ] Interfaces para pacientes/médicos
- [ ] Panel de administración

### Fase 2: Mejoras
- [ ] Tests unitarios
- [ ] API REST
- [ ] Notificaciones email
- [ ] Dashboard con gráficos

---

**Estado**: ✅ Lógica de Negocio Completa | ⏳ UI Pendiente  
**Última actualización**: Noviembre 2025
