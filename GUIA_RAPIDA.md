# 🚀 Guía Rápida de Inicio - Interfaz Web

## ✅ Tu Aplicación Web Está Lista!

La aplicación está corriendo en: **http://localhost:5000**

---

## 🔐 Credenciales de Acceso

### Administrador
```
Email: admin@clinica.com
Password: Clinica2025!
```

### Paciente de Prueba
```
Email: luis.gomez@email.com
Password: Clinica2025!
```

### Médico de Prueba
```
Email: maria.lopez@clinica.com
Password: Clinica2025!
```

---

## 📱 Funcionalidades Principales

### Como Paciente Puedes:
1. ✅ **Agendar Citas**
   - Ir a "Nueva Cita"
   - Seleccionar especialidad
   - Elegir médico
   - Seleccionar fecha y hora
   
2. ✅ **Ver Mis Citas**
   - Dashboard muestra próximas citas
   - "Mis Citas" muestra historial completo
   
3. ✅ **Gestionar Citas**
   - Cancelar citas agendadas
   - Reprogramar citas
   - Ver detalles completos

4. ✅ **Consultar Médicos**
   - Ver todos los médicos
   - Filtrar por especialidad
   - Ver horarios de atención

### Como Médico Puedes:
1. ✅ **Ver Agenda**
   - Dashboard muestra citas de hoy
   - Ver todas las citas programadas
   
2. ✅ **Gestionar Citas**
   - Marcar citas como atendidas
   - Ver información de pacientes
   - Consultar historial

### Como Administrador Puedes:
1. ✅ **Gestión Completa**
   - Ver todas las citas del sistema
   - Agendar citas para pacientes
   - Ver lista de pacientes
   - Ver lista de médicos

---

## 🎨 Navegación de la Interfaz

### Menú Principal (Barra Superior)
- **Dashboard** - Panel principal
- **Citas** - Gestión de citas
- **Nueva Cita** - Agendar (Paciente/Admin)
- **Médicos** - Directorio
- **Perfil** - Tu información
- **Notificaciones** - Alertas

### Dashboard Personalizado
Cada rol ve un dashboard diferente:
- **Paciente**: Próximas citas y accesos rápidos
- **Médico**: Agenda del día
- **Admin**: Panel de control completo

---

## 🔧 Comandos Útiles

### Iniciar Aplicación
```powershell
# Windows
.\start.ps1

# O manualmente
docker compose up -d
```

### Ver Logs
```powershell
docker compose logs -f app
```

### Detener Aplicación
```powershell
docker compose down
```

### Reiniciar
```powershell
docker compose restart app
```

---

## 📝 Flujo de Uso Típico

### 1️⃣ Registro (Si eres nuevo)
1. Ir a "Registrarse"
2. Elegir tipo de usuario (Paciente o Médico)
3. Llenar formulario
4. Confirmar registro

### 2️⃣ Iniciar Sesión
1. Ir a "Iniciar Sesión"
2. Ingresar email y contraseña
3. Acceder al dashboard

### 3️⃣ Agendar Cita (Paciente)
1. Clic en "Nueva Cita"
2. Seleccionar especialidad
3. Elegir médico
4. Seleccionar fecha disponible
5. Elegir hora disponible
6. Escribir motivo de consulta
7. Confirmar cita

### 4️⃣ Ver y Gestionar Citas
1. Ir a "Mis Citas"
2. Clic en "Ver" para ver detalles
3. Opciones disponibles:
   - Cancelar cita
   - Reprogramar cita
   - Ver información completa

### 5️⃣ Atender Cita (Médico)
1. Ver citas del día en Dashboard
2. Clic en "Ver" en la cita
3. Clic en "Marcar Atendida"
4. Agregar observaciones (opcional)
5. Confirmar

---

## 🎯 Características Destacadas

### ✨ Validaciones en Tiempo Real
- La interfaz valida disponibilidad automáticamente
- No permite agendar citas duplicadas
- Verifica horarios de médicos

### 🔔 Sistema de Notificaciones
- Notificaciones al agendar citas
- Alertas de cancelación
- Recordatorios de reprogramación

### 📱 Diseño Responsive
- Funciona en desktop, tablet y móvil
- Interfaz moderna con Bootstrap 5
- Navegación intuitiva

### 🔒 Seguridad
- Contraseñas encriptadas con bcrypt
- Sesiones seguras con Django
- Control de acceso por roles

---

## ❓ Solución de Problemas

### No puedo acceder a http://localhost:5000
```powershell
# Verificar que los contenedores están corriendo
docker compose ps

# Si no están corriendo, iniciarlos
docker compose up -d

# Ver logs para diagnosticar
docker compose logs app
```

### Olvidé mi contraseña
Por el momento usa las credenciales de prueba proporcionadas arriba.
Implementación de "recuperar contraseña" pendiente.

### La página no carga correctamente
```powershell
# Limpiar caché del navegador
# O usar modo incógnito
# O probar en otro navegador
```

### Error de base de datos
```powershell
# Reiniciar contenedor de base de datos
docker compose restart db

# Si persiste, reiniciar todo
docker compose down
docker compose up -d
```

---

## 📚 Recursos Adicionales

- **README.md** - Documentación completa del proyecto
- **README_WEB.md** - Guía detallada de la interfaz web
- **RESUMEN.md** - Resumen técnico del proyecto

---

## 💡 Tips y Consejos

1. **Usa el Dashboard** - Es tu punto de partida, tiene accesos rápidos
2. **Explora los Médicos** - Antes de agendar, revisa los médicos disponibles
3. **Verifica Horarios** - Cada médico tiene horarios específicos
4. **Lee las Notificaciones** - Mantente informado de cambios en tus citas
5. **Actualiza tu Perfil** - Mantén tu información actualizada

---

## 🎉 ¡Disfruta de la Aplicación!

Si tienes preguntas o encuentras problemas, revisa los logs:
```powershell
docker compose logs -f app
```

**URL de la Aplicación**: http://localhost:5000
