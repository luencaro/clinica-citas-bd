# 🏥 Sistema de Gestión de Citas Médicas

Sistema completo de gestión de citas médicas con interfaz web, desarrollado con Django y PostgreSQL.

## 📋 Tabla de Contenidos

- [Características](#características)
- [Arquitectura](#arquitectura)
- [Tecnologías](#tecnologías)
- [Instalación y Uso](#instalación-y-uso)
- [Interfaz Web](#interfaz-web)
- [Base de Datos](#base-de-datos)
- [Estructura del Proyecto](#estructura-del-proyecto)

## ✨ Características

### Funcionalidades Principales
- ✅ **Interfaz Web Completa**: Sistema web responsive con Bootstrap 5
- ✅ **Gestión de Usuarios**: Pacientes, Médicos y Administradores con autenticación
- ✅ **Agendamiento de Citas**: Sistema completo con validación de disponibilidad
- ✅ **Dashboard Personalizado**: Vista específica según el rol del usuario
- ✅ **Gestión de Horarios**: Configuración flexible por médico y día
- ✅ **Notificaciones**: Sistema automático de alertas
- ✅ **Historial de Cambios**: Auditoría completa de citas
- ✅ **Validaciones Completas**: Reglas de negocio en todas las capas

### Características Técnicas
- 🔐 **Seguridad**: Contraseñas hasheadas con bcrypt, sesiones seguras
- 🗄️ **Base de Datos**: PostgreSQL 16 con triggers, stored procedures y vistas
- 🏛️ **Arquitectura en Capas**: Separación clara de responsabilidades
- 🐳 **Docker**: Contenedorización completa del sistema
- 🎨 **UI Moderna**: Bootstrap 5 con diseño responsive
- 📱 **Responsive**: Funciona en desktop, tablet y móvil

## 🏛️ Arquitectura

```
┌─────────────────────────────────────┐
│      UI Layer (Django + Bootstrap)  │  ← Interfaz web
├─────────────────────────────────────┤
│       Presentation Layer            │
│  ┌─────────────────────────────┐   │
│  │      Views + Templates      │   │  ← Vistas y plantillas
│  └─────────────────────────────┘   │
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

- **Backend**: Python 3.11, Django 4.2
- **Base de Datos**: PostgreSQL 16
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Seguridad**: bcrypt, Django sessions
- **Containerización**: Docker, Docker Compose

## 🚀 Instalación y Uso

### Requisitos Previos
- Docker Desktop instalado y corriendo
- Git (opcional)

### Inicio Rápido

**Windows (PowerShell):**
```powershell
# Iniciar la aplicación
.\start.ps1

# O manualmente:
docker compose up -d

# Ver logs
docker compose logs -f app
```

**Linux/Mac:**
```bash
# Iniciar la aplicación
docker compose up -d

# Ver logs
docker compose logs -f app
```

La aplicación estará disponible en: **http://localhost:5000**

### Credenciales de Prueba

**Administrador:**
- Email: `admin@clinica.com`
- Password: `Clinica2025!`

**Paciente de Prueba:**
- Email: `luis.gomez@email.com`
- Password: `Clinica2025!`

**Médico de Prueba:**
- Email: `maria.lopez@clinica.com`
- Password: `Clinica2025!`

## 🌐 Interfaz Web

### Páginas Disponibles

#### Para Todos los Usuarios
- **Inicio**: `/` - Página de bienvenida
- **Login**: `/login/` - Iniciar sesión
- **Registro**: `/register/` - Crear cuenta (Paciente o Médico)

#### Para Usuarios Autenticados
- **Dashboard**: `/dashboard/` - Panel principal personalizado
- **Mis Citas**: `/citas/` - Lista de citas
- **Nueva Cita**: `/citas/nueva/` - Agendar cita (Paciente/Admin)
- **Detalle de Cita**: `/citas/{id}/` - Ver detalles
- **Médicos**: `/medicos/` - Directorio de médicos
- **Perfil**: `/perfil/` - Mi perfil
- **Notificaciones**: `/notificaciones/` - Mis notificaciones

#### Solo Administradores
- **Pacientes**: `/pacientes/` - Gestión de pacientes

### Funcionalidades por Rol

#### Paciente
- ✅ Agendar citas con médicos
- ✅ Ver mis citas programadas
- ✅ Cancelar/reprogramar citas
- ✅ Consultar médicos y especialidades
- ✅ Ver notificaciones
- ✅ Gestionar perfil

#### Médico
- ✅ Ver agenda diaria
- ✅ Consultar citas programadas
- ✅ Marcar citas como atendidas
- ✅ Ver historial de pacientes
- ✅ Gestionar perfil

#### Administrador
- ✅ Todas las funciones de Paciente
- ✅ Todas las funciones de Médico
- ✅ Gestionar todos los usuarios
- ✅ Ver todas las citas del sistema
- ✅ Agendar citas para pacientes

## 🗄️ Base de Datos

### Conexión
- Host: `localhost:5432`
- Usuario: `clinica_admin`
- Database: `clinica_citas`
- Password: `clinica_2025_secure`

### Tablas (8)
- `usuario` - Usuarios del sistema
- `paciente` - Datos de pacientes
- `medico` - Datos de médicos
- `especialidad` - Especialidades médicas
- `horario_medico` - Horarios de atención
- `cita` - Citas médicas
- `historial_cita` - Auditoría de cambios
- `notificacion` - Notificaciones del sistema

### Triggers (5)
- Auditoría automática de cambios en citas
- Notificaciones al agendar/cancelar citas
- Validación de horarios laborales
- Actualización de timestamps

### Stored Procedures (7)
- `sp_validar_disponibilidad`
- `sp_agendar_cita`
- `sp_cancelar_cita`
- `sp_reprogramar_cita`
- `sp_obtener_disponibilidad_dia`
- `sp_proximas_citas_paciente`
- `sp_estadisticas_medico`

### Vistas (9)
- `vista_citas_completas` - Información completa de citas
- `vista_disponibilidad_medicos` - Disponibilidad por médico
- `vista_estadisticas_citas` - Estadísticas generales
- Y más...

## 📁 Estructura del Proyecto

```
clinica-citas-bd/
├── app/                    # Aplicación Python
│   ├── webapp/            # Django Web Application
│   │   ├── templates/     # Plantillas HTML
│   │   ├── static/        # CSS, JS, imágenes
│   │   ├── views.py       # Vistas de Django
│   │   ├── urls.py        # URLs
│   │   └── settings.py    # Configuración Django
│   ├── models/            # Modelos del dominio
│   ├── services/          # Lógica de negocio
│   ├── repositories/      # Acceso a datos
│   ├── run_webapp.py      # Iniciar aplicación web
│   └── requirements.txt   # Dependencias Python
│
├── db/                    # Base de datos
│   ├── init/             # Scripts de inicialización
│   ├── seed/             # Datos de prueba
│   ├── triggers.sql      # Triggers
│   ├── stored_procedures.sql  # Procedimientos
│   └── views.sql         # Vistas
│
├── docker-compose.yml    # Configuración Docker
├── start.ps1            # Script de inicio (Windows)
└── README.md            # Este archivo
```

## 🔧 Comandos Útiles

```bash
# Ver estado de contenedores
docker compose ps

# Ver logs en tiempo real
docker compose logs -f app

# Detener aplicación
docker compose down

# Reiniciar aplicación
docker compose restart app

# Acceder a la base de datos
docker compose exec db psql -U clinica_admin -d clinica_citas

# Reconstruir contenedores
docker compose up -d --build
```

## 📝 Próximos Pasos

- [ ] Implementar recordatorios automáticos por email
- [ ] Agregar calendario visual para médicos
- [ ] Reportes y estadísticas avanzadas
- [ ] Integración con sistemas de pago
- [ ] App móvil nativa
- [ ] Sistema de videoconsultas

## 👥 Autores

Desarrollado como proyecto académico del curso Base de Datos 2025-30-2497

## 📄 Licencia

Este proyecto es de código abierto y está disponible para fines educativos.

---

**¿Problemas?** Verifica que Docker esté corriendo y que los puertos 5000 y 5432 estén disponibles.
