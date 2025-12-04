"""
Django Views for Medical Appointments System
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse, HttpResponseForbidden
from datetime import datetime, date, time, timedelta
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.usuario_service import UsuarioService
from services.paciente_service import PacienteService
from services.medico_service import MedicoService
from services.especialidad_service import EspecialidadService
from services.cita_service import CitaService
from repositories.notificacion_repository import NotificacionRepository
from exceptions import *


# Initialize services
usuario_service = UsuarioService()
paciente_service = PacienteService()
medico_service = MedicoService()
especialidad_service = EspecialidadService()
cita_service = CitaService()
notif_repo = NotificacionRepository()


# Helper functions
def get_current_user(request):
    """Get current user from session"""
    user_id = request.session.get('user_id')
    if not user_id:
        return None
    try:
        return usuario_service.obtener_por_id(user_id)
    except:
        return None


def login_required(view_func):
    """Decorator to require login"""
    def wrapper(request, *args, **kwargs):
        if not get_current_user(request):
            messages.warning(request, 'Debes iniciar sesión para acceder')
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper


def role_required(*roles):
    """Decorator to require specific role"""
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            user = get_current_user(request)
            if not user or user.rol not in roles:
                return HttpResponseForbidden('No tienes permisos para acceder a esta página')
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


# Authentication Views
def home(request):
    """Home page"""
    user = get_current_user(request)
    if user:
        return redirect('dashboard')
    return render(request, 'home.html')


def login_view(request):
    """Login page"""
    if get_current_user(request):
        return redirect('dashboard')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            user = usuario_service.autenticar(email, password)
            request.session['user_id'] = user.id_usuario
            request.session['user_name'] = f"{user.nombre} {user.apellido}"
            request.session['user_role'] = user.rol
            
            messages.success(request, f'¡Bienvenido {user.nombre}!')
            return redirect('dashboard')
        except CredencialesInvalidasError as e:
            messages.error(request, str(e))
        except Exception as e:
            messages.error(request, 'Error al iniciar sesión')
    
    return render(request, 'auth/login.html')


def logout_view(request):
    """Logout"""
    request.session.flush()
    messages.success(request, 'Sesión cerrada correctamente')
    return redirect('home')


def register_view(request):
    """Register new user"""
    if get_current_user(request):
        return redirect('dashboard')
    
    if request.method == 'POST':
        try:
            # Get form data
            tipo_usuario = request.POST.get('tipo_usuario')
            nombre = request.POST.get('nombre')
            apellido = request.POST.get('apellido')
            email = request.POST.get('email')
            telefono = request.POST.get('telefono')
            password = request.POST.get('password')
            password_confirm = request.POST.get('password_confirm')
            
            # Validate passwords match
            if password != password_confirm:
                messages.error(request, 'Las contraseñas no coinciden')
                return render(request, 'auth/register.html')
            
            # Create user based on type
            if tipo_usuario == 'PACIENTE':
                fecha_nacimiento = request.POST.get('fecha_nacimiento')
                direccion = request.POST.get('direccion', '')
                genero = request.POST.get('genero', '')
                
                paciente_service.crear_paciente_completo(
                    nombre=nombre,
                    apellido=apellido,
                    email=email,
                    telefono=telefono,
                    contraseña=password,
                    fecha_nacimiento=datetime.strptime(fecha_nacimiento, '%Y-%m-%d').date(),
                    direccion=direccion if direccion else None,
                    genero=genero if genero else None
                )
                
                messages.success(request, 'Cuenta de paciente creada exitosamente. Por favor inicia sesión.')
                
            elif tipo_usuario == 'MEDICO':
                id_especialidad = int(request.POST.get('id_especialidad'))
                registro_profesional = request.POST.get('registro_profesional')
                
                usuario, medico = medico_service.crear_medico_completo(
                    nombre=nombre,
                    apellido=apellido,
                    email=email,
                    telefono=telefono,
                    contraseña=password,
                    id_especialidad=id_especialidad,
                    registro_profesional=registro_profesional
                )
                
                messages.success(
                    request, 
                    'Cuenta de médico creada exitosamente. Se han configurado horarios por defecto '
                    '(Lunes a Viernes 08:00-17:00). Puedes personalizarlos desde tu perfil.'
                )
            
            return redirect('login')
            
        except EmailDuplicadoError as e:
            messages.error(request, str(e))
        except TelefonoDuplicadoError as e:
            messages.error(request, str(e))
        except Exception as e:
            messages.error(request, f'Error al crear cuenta: {str(e)}')
    
    # Get especialidades for form
    especialidades = especialidad_service.listar_activas()
    
    return render(request, 'auth/register.html', {
        'especialidades': especialidades
    })


# Dashboard
@login_required
def dashboard(request):
    """Main dashboard"""
    user = get_current_user(request)
    
    context = {
        'user': user,
    }
    
    try:
        if user.rol == 'PACIENTE':
            # Get patient data
            from repositories.paciente_repository import PacienteRepository
            from repositories.medico_repository import MedicoRepository
            from repositories.usuario_repository import UsuarioRepository
            
            paciente_repo = PacienteRepository()
            medico_repo = MedicoRepository()
            usuario_repo = UsuarioRepository()
            
            paciente = paciente_repo.find_by_usuario(user.id_usuario)
            
            if paciente:
                # Get upcoming appointments
                proximas_citas = cita_service.obtener_proximas_citas(id_paciente=paciente.id_paciente, limit=5)
                
                # Enrich with medico names
                for cita in proximas_citas:
                    medico = medico_repo.find_by_id(cita.id_medico, 'id_medico')
                    if medico:
                        usuario_med = usuario_repo.find_by_id(medico.id_usuario, 'id_usuario')
                        cita.medico_nombre = f"{usuario_med.nombre} {usuario_med.apellido}" if usuario_med else "N/A"
                        # Asignar color según estado
                        if cita.estado == 'AGENDADA':
                            cita.estado_color = 'primary'
                        elif cita.estado == 'ATENDIDA':
                            cita.estado_color = 'success'
                        elif cita.estado == 'CANCELADA':
                            cita.estado_color = 'danger'
                        elif cita.estado == 'REPROGRAMADA':
                            cita.estado_color = 'info'
                        else:
                            cita.estado_color = 'warning'
                    else:
                        cita.medico_nombre = "N/A"
                
                context['paciente'] = paciente
                context['proximas_citas'] = proximas_citas
        
        elif user.rol == 'MEDICO':
            # Get doctor data
            from repositories.medico_repository import MedicoRepository
            from repositories.paciente_repository import PacienteRepository
            from repositories.usuario_repository import UsuarioRepository
            from repositories.especialidad_repository import EspecialidadRepository
            
            medico_repo = MedicoRepository()
            paciente_repo = PacienteRepository()
            usuario_repo = UsuarioRepository()
            especialidad_repo = EspecialidadRepository()
            
            medico = medico_repo.find_by_usuario(user.id_usuario)
            
            if medico:
                # Enrich medico with user and specialty data
                usuario_med = usuario_repo.find_by_id(medico.id_usuario, 'id_usuario')
                if usuario_med:
                    medico.nombre = usuario_med.nombre
                    medico.apellido = usuario_med.apellido
                    medico.email = usuario_med.email
                    medico.telefono = usuario_med.telefono
                
                especialidad = especialidad_repo.find_by_id(medico.id_especialidad, 'id_especialidad')
                if especialidad:
                    medico.especialidad_nombre = especialidad.nombre
                
                # Check if medico has horarios configured
                from repositories.horario_repository import HorarioRepository
                horario_repo = HorarioRepository()
                horarios = horario_repo.find_by_medico(medico.id_medico)
                context['sin_horarios'] = len(horarios) == 0
                
                # Get today's appointments
                hoy = date.today()
                citas_hoy = cita_service.obtener_citas_fecha(hoy, id_medico=medico.id_medico)
                
                # Enrich with paciente names
                for cita in citas_hoy:
                    paciente = paciente_repo.find_by_id(cita.id_paciente, 'id_paciente')
                    if paciente:
                        usuario_pac = usuario_repo.find_by_id(paciente.id_usuario, 'id_usuario')
                        cita.paciente_nombre = f"{usuario_pac.nombre} {usuario_pac.apellido}" if usuario_pac else "N/A"
                        # Asignar color según estado
                        if cita.estado == 'AGENDADA':
                            cita.estado_color = 'primary'
                        elif cita.estado == 'ATENDIDA':
                            cita.estado_color = 'success'
                        elif cita.estado == 'CANCELADA':
                            cita.estado_color = 'danger'
                        elif cita.estado == 'REPROGRAMADA':
                            cita.estado_color = 'info'
                        else:
                            cita.estado_color = 'warning'
                    else:
                        cita.paciente_nombre = "N/A"
                
                context['medico'] = medico
                context['citas_hoy'] = citas_hoy
        
        # Get unread notifications
        notificaciones = notif_repo.find_by_usuario(user.id_usuario, solo_no_leidas=True, limit=5)
        context['notificaciones'] = notificaciones
        
    except Exception as e:
        messages.error(request, f'Error al cargar dashboard: {str(e)}')
    
    return render(request, 'dashboard/dashboard.html', context)


# Citas Views
@login_required
def citas_list(request):
    """List appointments"""
    user = get_current_user(request)
    
    try:
        if user.rol == 'PACIENTE':
            from repositories.paciente_repository import PacienteRepository
            paciente_repo = PacienteRepository()
            paciente = paciente_repo.find_by_usuario(user.id_usuario)
            citas = cita_service.obtener_citas_paciente(paciente.id_paciente)
        
        elif user.rol == 'MEDICO':
            from repositories.medico_repository import MedicoRepository
            medico_repo = MedicoRepository()
            medico = medico_repo.find_by_usuario(user.id_usuario)
            citas = cita_service.obtener_citas_medico(medico.id_medico)
        
        else:  # ADMIN
            # Get all recent appointments
            from repositories.cita_repository import CitaRepository
            cita_repo = CitaRepository()
            citas = cita_repo.find_all(order_by="fecha DESC, hora DESC")
        
        # Enrich citas with paciente and medico names
        from repositories.paciente_repository import PacienteRepository
        from repositories.medico_repository import MedicoRepository
        from repositories.usuario_repository import UsuarioRepository
        
        paciente_repo = PacienteRepository()
        medico_repo = MedicoRepository()
        usuario_repo = UsuarioRepository()
        
        for cita in citas:
            # Get paciente name
            paciente = paciente_repo.find_by_id(cita.id_paciente, 'id_paciente')
            if paciente:
                usuario_pac = usuario_repo.find_by_id(paciente.id_usuario, 'id_usuario')
                cita.paciente_nombre = f"{usuario_pac.nombre} {usuario_pac.apellido}" if usuario_pac else "N/A"
            else:
                cita.paciente_nombre = "N/A"
            
            # Get medico name
            medico = medico_repo.find_by_id(cita.id_medico, 'id_medico')
            if medico:
                usuario_med = usuario_repo.find_by_id(medico.id_usuario, 'id_usuario')
                cita.medico_nombre = f"{usuario_med.nombre} {usuario_med.apellido}" if usuario_med else "N/A"
            else:
                cita.medico_nombre = "N/A"
        
        return render(request, 'citas/list.html', {
            'citas': citas,
            'user': user
        })
    
    except Exception as e:
        messages.error(request, f'Error al cargar citas: {str(e)}')
        return redirect('dashboard')


@login_required
@role_required('PACIENTE', 'ADMIN')
def cita_nueva(request):
    """Create new appointment"""
    user = get_current_user(request)
    
    if request.method == 'POST':
        try:
            # Get patient
            if user.rol == 'PACIENTE':
                from repositories.paciente_repository import PacienteRepository
                paciente_repo = PacienteRepository()
                paciente = paciente_repo.find_by_usuario(user.id_usuario)
                id_paciente = paciente.id_paciente
            else:
                id_paciente = int(request.POST.get('id_paciente'))
            
            id_medico = int(request.POST.get('id_medico'))
            fecha_str = request.POST.get('fecha')
            hora_str = request.POST.get('hora')
            motivo = request.POST.get('motivo')
            observaciones = request.POST.get('observaciones', '')
            
            # Parse date and time
            fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
            hora = datetime.strptime(hora_str, '%H:%M').time()
            
            # Create appointment
            cita = cita_service.agendar_cita(
                id_paciente=id_paciente,
                id_medico=id_medico,
                fecha=fecha,
                hora=hora,
                motivo=motivo,
                observaciones=observaciones if observaciones else None
            )
            
            messages.success(request, f'Cita agendada exitosamente para el {fecha} a las {hora}')
            return redirect('citas_list')
            
        except CitaDuplicadaError as e:
            messages.error(request, str(e))
        except CitaNoDisponibleError as e:
            messages.error(request, str(e))
        except FueraDeHorarioError as e:
            messages.error(request, str(e))
        except Exception as e:
            messages.error(request, f'Error al agendar cita: {str(e)}')
    
    # Get data for form
    import json
    from repositories.usuario_repository import UsuarioRepository
    
    especialidades = especialidad_service.listar_activas()
    medicos = medico_service.listar_activos()
    usuario_repo = UsuarioRepository()
    
    # Enrich medicos with user data
    medicos_data = []
    for m in medicos:
        usuario = usuario_repo.find_by_id(m.id_usuario, 'id_usuario')
        if usuario:
            medicos_data.append({
                'id_medico': m.id_medico,
                'nombre': usuario.nombre,
                'apellido': usuario.apellido,
                'id_especialidad': m.id_especialidad
            })
    
    # Serialize medicos to JSON
    medicos_json = json.dumps(medicos_data)
    
    # Get patients if admin
    pacientes = []
    if user.rol == 'ADMIN':
        from repositories.paciente_repository import PacienteRepository
        paciente_repo = PacienteRepository()
        pacientes_raw = paciente_repo.find_all()
        
        # Enrich pacientes with user data
        for p in pacientes_raw:
            usuario = usuario_repo.find_by_id(p.id_usuario, 'id_usuario')
            if usuario:
                p.nombre = usuario.nombre
                p.apellido = usuario.apellido
                pacientes.append(p)
    
    return render(request, 'citas/nueva.html', {
        'especialidades': especialidades,
        'medicos': medicos_json,
        'pacientes': pacientes,
        'user': user,
        'today': date.today()
    })


@login_required
def cita_detalle(request, id_cita):
    """Appointment detail"""
    try:
        cita = cita_service.obtener_por_id(id_cita)
        
        # Check permissions
        user = get_current_user(request)
        if user.rol == 'PACIENTE':
            from repositories.paciente_repository import PacienteRepository
            paciente_repo = PacienteRepository()
            paciente = paciente_repo.find_by_usuario(user.id_usuario)
            if cita.id_paciente != paciente.id_paciente:
                return HttpResponseForbidden('No tienes permiso para ver esta cita')
        
        elif user.rol == 'MEDICO':
            from repositories.medico_repository import MedicoRepository
            medico_repo = MedicoRepository()
            medico = medico_repo.find_by_usuario(user.id_usuario)
            if cita.id_medico != medico.id_medico:
                return HttpResponseForbidden('No tienes permiso para ver esta cita')
        
        # Get full details
        from repositories.paciente_repository import PacienteRepository
        from repositories.medico_repository import MedicoRepository
        from repositories.usuario_repository import UsuarioRepository
        from repositories.especialidad_repository import EspecialidadRepository
        from repositories.historial_cita_repository import HistorialCitaRepository
        
        paciente_repo = PacienteRepository()
        medico_repo = MedicoRepository()
        usuario_repo = UsuarioRepository()
        especialidad_repo = EspecialidadRepository()
        historial_repo = HistorialCitaRepository()
        
        paciente = paciente_repo.find_by_id(cita.id_paciente, 'id_paciente')
        medico = medico_repo.find_by_id(cita.id_medico, 'id_medico')
        
        # Enrich paciente with user data
        if paciente:
            usuario_pac = usuario_repo.find_by_id(paciente.id_usuario, 'id_usuario')
            if usuario_pac:
                paciente.nombre = usuario_pac.nombre
                paciente.apellido = usuario_pac.apellido
                paciente.email = usuario_pac.email
                paciente.telefono = usuario_pac.telefono
        
        # Enrich medico with user and specialty data
        if medico:
            usuario_med = usuario_repo.find_by_id(medico.id_usuario, 'id_usuario')
            if usuario_med:
                medico.nombre = usuario_med.nombre
                medico.apellido = usuario_med.apellido
                medico.email = usuario_med.email
                medico.telefono = usuario_med.telefono
            
            especialidad = especialidad_repo.find_by_id(medico.id_especialidad, 'id_especialidad')
            if especialidad:
                medico.especialidad_nombre = especialidad.nombre
        
        # Get history
        historial = historial_repo.find_by_cita(id_cita)
        
        from datetime import date
        return render(request, 'citas/detalle.html', {
            'cita': cita,
            'paciente': paciente,
            'medico': medico,
            'user': user,
            'historial': historial,
            'today': date.today().isoformat()
        })
    
    except CitaNoEncontradaError:
        messages.error(request, 'Cita no encontrada')
        return redirect('citas_list')
    except Exception as e:
        messages.error(request, f'Error al cargar cita: {str(e)}')
        return redirect('citas_list')


@login_required
def cita_cancelar(request, id_cita):
    """Cancel appointment"""
    if request.method == 'POST':
        try:
            motivo = request.POST.get('motivo', '')
            cita = cita_service.cancelar_cita(id_cita, motivo)
            messages.success(request, 'Cita cancelada exitosamente')
            return redirect('cita_detalle', id_cita=id_cita)
        except Exception as e:
            messages.error(request, f'Error al cancelar cita: {str(e)}')
    
    return redirect('cita_detalle', id_cita=id_cita)


@login_required
def cita_reprogramar(request, id_cita):
    """Reschedule appointment"""
    if request.method == 'POST':
        try:
            fecha_str = request.POST.get('fecha')
            hora_str = request.POST.get('hora')
            motivo = request.POST.get('motivo', '')
            
            fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
            hora = datetime.strptime(hora_str, '%H:%M').time()
            
            cita = cita_service.reprogramar_cita(id_cita, fecha, hora, motivo)
            messages.success(request, f'Cita reprogramada exitosamente para el {fecha.strftime("%d/%m/%Y")} a las {hora.strftime("%H:%M")}')
            return redirect('cita_detalle', id_cita=id_cita)
        except Exception as e:
            messages.error(request, f'Error al reprogramar cita: {str(e)}')
    
    return redirect('cita_detalle', id_cita=id_cita)


@login_required
@role_required('MEDICO', 'ADMIN')
def cita_atender(request, id_cita):
    """Mark appointment as attended"""
    if request.method == 'POST':
        try:
            observaciones = request.POST.get('observaciones', '')
            cita = cita_service.marcar_como_atendida(id_cita, observaciones)
            messages.success(request, 'Cita marcada como atendida exitosamente')
            return redirect('cita_detalle', id_cita=id_cita)
        except Exception as e:
            messages.error(request, f'Error al marcar cita: {str(e)}')
    
    return redirect('cita_detalle', id_cita=id_cita)


# Medicos Views
@login_required
def medicos_list(request):
    """List doctors"""
    try:
        from repositories.usuario_repository import UsuarioRepository
        from repositories.especialidad_repository import EspecialidadRepository
        
        usuario_repo = UsuarioRepository()
        especialidad_repo = EspecialidadRepository()
        
        especialidad_id = request.GET.get('especialidad')
        
        if especialidad_id:
            medicos = medico_service.obtener_por_especialidad(int(especialidad_id))
        else:
            medicos = medico_service.listar_activos()
        
        # Enrich medicos with user and specialty data
        for m in medicos:
            usuario = usuario_repo.find_by_id(m.id_usuario, 'id_usuario')
            if usuario:
                m.nombre = usuario.nombre
                m.apellido = usuario.apellido
                m.email = usuario.email
                m.telefono = usuario.telefono
            
            especialidad = especialidad_repo.find_by_id(m.id_especialidad, 'id_especialidad')
            if especialidad:
                m.especialidad_nombre = especialidad.nombre
        
        especialidades = especialidad_service.listar_activas()
        
        return render(request, 'medicos/list.html', {
            'medicos': medicos,
            'especialidades': especialidades
        })
    except Exception as e:
        messages.error(request, f'Error al cargar médicos: {str(e)}')
        return redirect('dashboard')


@login_required
def medico_detalle(request, id_medico):
    """Doctor detail"""
    user = get_current_user(request)
    
    try:
        from repositories.usuario_repository import UsuarioRepository
        from repositories.especialidad_repository import EspecialidadRepository
        
        medico = medico_service.obtener_por_id(id_medico)
        horarios = medico_service.obtener_horarios(id_medico)
        
        # Enrich medico with user and specialty data
        usuario_repo = UsuarioRepository()
        especialidad_repo = EspecialidadRepository()
        
        usuario = usuario_repo.find_by_id(medico.id_usuario, 'id_usuario')
        if usuario:
            medico.nombre = usuario.nombre
            medico.apellido = usuario.apellido
            medico.email = usuario.email
            medico.telefono = usuario.telefono
        
        especialidad = especialidad_repo.find_by_id(medico.id_especialidad, 'id_especialidad')
        if especialidad:
            medico.especialidad_nombre = especialidad.nombre
        
        return render(request, 'medicos/detalle.html', {
            'user': user,
            'medico': medico,
            'horarios': horarios
        })
    except Exception as e:
        messages.error(request, f'Error al cargar médico: {str(e)}')
        return redirect('medicos_list')


@login_required
def medico_disponibilidad(request, id_medico):
    """Check doctor availability"""
    fecha_str = request.GET.get('fecha')
    
    if not fecha_str:
        fecha = date.today()
    else:
        fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
    
    try:
        from repositories.usuario_repository import UsuarioRepository
        from repositories.especialidad_repository import EspecialidadRepository
        
        disponibilidad = cita_service.obtener_disponibilidad_medico(id_medico, fecha)
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'disponibilidad': [h.strftime('%H:%M') for h in disponibilidad]
            })
        
        medico = medico_service.obtener_por_id(id_medico)
        
        # Enrich medico with user data
        usuario_repo = UsuarioRepository()
        especialidad_repo = EspecialidadRepository()
        
        usuario = usuario_repo.find_by_id(medico.id_usuario, 'id_usuario')
        if usuario:
            medico.nombre = usuario.nombre
            medico.apellido = usuario.apellido
        
        especialidad = especialidad_repo.find_by_id(medico.id_especialidad, 'id_especialidad')
        if especialidad:
            medico.especialidad_nombre = especialidad.nombre
        
        return render(request, 'medicos/disponibilidad.html', {
            'medico': medico,
            'fecha': fecha,
            'disponibilidad': disponibilidad
        })
    except Exception as e:
        messages.error(request, f'Error al cargar disponibilidad: {str(e)}')
        return redirect('medico_detalle', id_medico=id_medico)


# Especialidades Views
@login_required
def especialidades_list(request):
    """List specialties"""
    try:
        especialidades = especialidad_service.listar_activas()
        
        return render(request, 'especialidades/list.html', {
            'especialidades': especialidades
        })
    except Exception as e:
        messages.error(request, f'Error al cargar especialidades: {str(e)}')
        return redirect('dashboard')


# Pacientes Views (Admin only)
@login_required
@role_required('ADMIN')
def pacientes_list(request):
    """List patients (admin only)"""
    try:
        from repositories.paciente_repository import PacienteRepository
        from repositories.usuario_repository import UsuarioRepository
        
        paciente_repo = PacienteRepository()
        usuario_repo = UsuarioRepository()
        
        pacientes = paciente_repo.find_all()
        
        # Enrich pacientes with user data
        for p in pacientes:
            usuario = usuario_repo.find_by_id(p.id_usuario, 'id_usuario')
            if usuario:
                p.nombre = usuario.nombre
                p.apellido = usuario.apellido
                p.email = usuario.email
                p.telefono = usuario.telefono
        
        return render(request, 'pacientes/list.html', {
            'pacientes': pacientes
        })
    except Exception as e:
        messages.error(request, f'Error al cargar pacientes: {str(e)}')
        return redirect('dashboard')


@login_required
def paciente_detalle(request, id_paciente):
    """Patient detail"""
    try:
        from repositories.paciente_repository import PacienteRepository
        from repositories.usuario_repository import UsuarioRepository
        from repositories.medico_repository import MedicoRepository
        from repositories.especialidad_repository import EspecialidadRepository
        
        paciente_repo = PacienteRepository()
        usuario_repo = UsuarioRepository()
        medico_repo = MedicoRepository()
        especialidad_repo = EspecialidadRepository()
        
        paciente = paciente_repo.find_by_id(id_paciente, 'id_paciente')
        
        # Enrich paciente with usuario data
        if paciente:
            usuario = usuario_repo.find_by_id(paciente.id_usuario, 'id_usuario')
            if usuario:
                paciente.nombre = usuario.nombre
                paciente.apellido = usuario.apellido
                paciente.email = usuario.email
                paciente.telefono = usuario.telefono
        
        # Check permissions
        user = get_current_user(request)
        if user.rol == 'PACIENTE':
            paciente_user = paciente_repo.find_by_usuario(user.id_usuario)
            if paciente.id_paciente != paciente_user.id_paciente:
                return HttpResponseForbidden('No tienes permiso para ver este paciente')
        
        citas = cita_service.obtener_citas_paciente(id_paciente)
        
        # Enrich citas with medico and especialidad data
        for cita in citas:
            if cita.id_medico:
                medico = medico_repo.find_by_id(cita.id_medico, 'id_medico')
                if medico:
                    usuario_med = usuario_repo.find_by_id(medico.id_usuario, 'id_usuario')
                    if usuario_med:
                        medico.nombre = usuario_med.nombre
                        medico.apellido = usuario_med.apellido
                    especialidad = especialidad_repo.find_by_id(medico.id_especialidad, 'id_especialidad')
                    if especialidad:
                        medico.especialidad_nombre = especialidad.nombre
                    cita.medico = medico
        
        return render(request, 'pacientes/detalle.html', {
            'paciente': paciente,
            'citas': citas
        })
    except Exception as e:
        messages.error(request, f'Error al cargar paciente: {str(e)}')
        return redirect('dashboard')


# Profile Views
@login_required
def perfil(request):
    """User profile"""
    user = get_current_user(request)
    
    context = {'user': user}
    
    try:
        if user.rol == 'PACIENTE':
            from repositories.paciente_repository import PacienteRepository
            from repositories.usuario_repository import UsuarioRepository
            paciente_repo = PacienteRepository()
            usuario_repo = UsuarioRepository()
            paciente = paciente_repo.find_by_usuario(user.id_usuario)
            if paciente:
                usuario = usuario_repo.find_by_id(paciente.id_usuario, 'id_usuario')
                if usuario:
                    paciente.nombre = usuario.nombre
                    paciente.apellido = usuario.apellido
                    paciente.email = usuario.email
                    paciente.telefono = usuario.telefono
            context['paciente'] = paciente
        
        elif user.rol == 'MEDICO':
            from repositories.medico_repository import MedicoRepository
            from repositories.especialidad_repository import EspecialidadRepository
            from repositories.usuario_repository import UsuarioRepository
            medico_repo = MedicoRepository()
            especialidad_repo = EspecialidadRepository()
            usuario_repo = UsuarioRepository()
            medico = medico_repo.find_by_usuario(user.id_usuario)
            if medico:
                usuario = usuario_repo.find_by_id(medico.id_usuario, 'id_usuario')
                if usuario:
                    medico.nombre = usuario.nombre
                    medico.apellido = usuario.apellido
                    medico.email = usuario.email
                    medico.telefono = usuario.telefono
                especialidad = especialidad_repo.find_by_id(medico.id_especialidad, 'id_especialidad')
                if especialidad:
                    medico.especialidad_nombre = especialidad.nombre
            context['medico'] = medico
    
    except Exception as e:
        messages.error(request, f'Error al cargar perfil: {str(e)}')
    
    return render(request, 'perfil/perfil.html', context)


@login_required
def perfil_editar(request):
    """Edit user profile"""
    user = get_current_user(request)
    context = {'user': user}
    
    # Load user data
    try:
        if user.rol == 'PACIENTE':
            from repositories.paciente_repository import PacienteRepository
            paciente_repo = PacienteRepository()
            paciente = paciente_repo.find_by_usuario(user.id_usuario)
            context['paciente'] = paciente
        
        elif user.rol == 'MEDICO':
            from repositories.medico_repository import MedicoRepository
            from repositories.especialidad_repository import EspecialidadRepository
            medico_repo = MedicoRepository()
            especialidad_repo = EspecialidadRepository()
            medico = medico_repo.find_by_usuario(user.id_usuario)
            especialidades = especialidad_repo.get_all()
            context['medico'] = medico
            context['especialidades'] = especialidades
    
    except Exception as e:
        messages.error(request, f'Error al cargar datos: {str(e)}')
    
    if request.method == 'POST':
        try:
            nombre = request.POST.get('nombre')
            apellido = request.POST.get('apellido')
            email = request.POST.get('email')
            telefono = request.POST.get('telefono')
            password = request.POST.get('password')
            password_confirm = request.POST.get('password_confirm')
            
            # Validate password if provided
            if password:
                if password != password_confirm:
                    messages.error(request, 'Las contraseñas no coinciden')
                    return render(request, 'perfil/editar.html', context)
                if len(password) < 6:
                    messages.error(request, 'La contraseña debe tener al menos 6 caracteres')
                    return render(request, 'perfil/editar.html', context)
            
            # Update usuario
            update_data = {
                'nombre': nombre,
                'apellido': apellido,
                'email': email,
                'telefono': telefono
            }
            if password:
                update_data['contraseña'] = password
            
            usuario_service.actualizar_usuario(user.id_usuario, **update_data)
            
            # Update role-specific data
            if user.rol == 'PACIENTE':
                fecha_nacimiento = request.POST.get('fecha_nacimiento')
                direccion = request.POST.get('direccion')
                paciente_service.actualizar_datos_paciente(
                    context['paciente'].id_paciente,
                    fecha_nacimiento=fecha_nacimiento,
                    direccion=direccion
                )
            
            elif user.rol == 'MEDICO':
                id_especialidad = request.POST.get('id_especialidad')
                medico_service.actualizar_medico(
                    context['medico'].id_medico,
                    id_especialidad=int(id_especialidad)
                )
            
            request.session['user_name'] = f"{nombre} {apellido}"
            messages.success(request, 'Perfil actualizado exitosamente')
            return redirect('perfil')
        
        except Exception as e:
            messages.error(request, f'Error al actualizar perfil: {str(e)}')
    
    return render(request, 'perfil/editar.html', context)


# Horarios Management
@login_required
def medico_horarios(request, id_medico):
    """Manage medico schedule"""
    user = get_current_user(request)
    
    # Check permissions: only admin or the medico themselves
    if user.rol == 'MEDICO':
        from repositories.medico_repository import MedicoRepository
        medico_repo = MedicoRepository()
        medico_user = medico_repo.find_by_usuario(user.id_usuario)
        if not medico_user or medico_user.id_medico != id_medico:
            messages.error(request, 'No tienes permiso para editar estos horarios')
            return redirect('dashboard')
    elif user.rol != 'ADMIN':
        messages.error(request, 'No tienes permiso para editar horarios')
        return redirect('dashboard')
    
    try:
        from repositories.medico_repository import MedicoRepository
        from repositories.horario_repository import HorarioRepository
        from repositories.especialidad_repository import EspecialidadRepository
        from repositories.usuario_repository import UsuarioRepository
        
        medico_repo = MedicoRepository()
        horario_repo = HorarioRepository()
        especialidad_repo = EspecialidadRepository()
        usuario_repo = UsuarioRepository()
        
        medico = medico_repo.find_by_id(id_medico, 'id_medico')
        if not medico:
            messages.error(request, 'Médico no encontrado')
            return redirect('medicos_list')
        
        # Enrich medico data
        usuario = usuario_repo.find_by_id(medico.id_usuario, 'id_usuario')
        if usuario:
            medico.nombre = usuario.nombre
            medico.apellido = usuario.apellido
        especialidad = especialidad_repo.find_by_id(medico.id_especialidad, 'id_especialidad')
        if especialidad:
            medico.especialidad_nombre = especialidad.nombre
        
        # Handle POST - add new horario
        if request.method == 'POST':
            dia_semana_str = request.POST.get('dia_semana')
            hora_inicio = request.POST.get('hora_inicio')
            hora_fin = request.POST.get('hora_fin')
            
            # Map day names to integers
            dias_map = {
                'LUNES': 1,
                'MARTES': 2,
                'MIERCOLES': 3,
                'JUEVES': 4,
                'VIERNES': 5,
                'SABADO': 6,
                'DOMINGO': 7
            }
            
            # Validate
            if not all([dia_semana_str, hora_inicio, hora_fin]):
                messages.error(request, 'Todos los campos son obligatorios')
            elif dia_semana_str not in dias_map:
                messages.error(request, 'Día de la semana inválido')
            else:
                dia_semana = dias_map[dia_semana_str]
                
                # Validate 30-minute intervals
                from datetime import datetime
                try:
                    hi = datetime.strptime(hora_inicio, '%H:%M')
                    hf = datetime.strptime(hora_fin, '%H:%M')
                    if hi.minute not in [0, 30] or hf.minute not in [0, 30]:
                        messages.error(request, 'Las horas deben estar en intervalos de 30 minutos (00 o 30)')
                        return redirect('medico_horarios', id_medico=id_medico)
                except ValueError:
                    messages.error(request, 'Formato de hora inválido')
                    return redirect('medico_horarios', id_medico=id_medico)
                
                # Check for overlaps
                horarios_existentes = horario_repo.find_by_medico(id_medico)
                overlap = False
                for h in horarios_existentes:
                    if h.dia_semana == dia_semana:
                        if not (hora_fin <= str(h.hora_inicio) or hora_inicio >= str(h.hora_fin)):
                            overlap = True
                            break
                
                if overlap:
                    messages.error(request, 'Este horario se solapa con uno existente')
                else:
                    horario_repo.create(
                        id_medico=id_medico,
                        dia_semana=dia_semana,
                        hora_inicio=hora_inicio,
                        hora_fin=hora_fin
                    )
                    messages.success(request, 'Horario agregado exitosamente')
            
            return redirect('medico_horarios', id_medico=id_medico)
        
        # GET - show horarios
        horarios = horario_repo.find_by_medico(id_medico)
        
        # Add day names to horarios
        dias_nombres = {
            1: 'Lunes',
            2: 'Martes',
            3: 'Miércoles',
            4: 'Jueves',
            5: 'Viernes',
            6: 'Sábado',
            7: 'Domingo'
        }
        
        for horario in horarios:
            horario.dia_nombre = dias_nombres.get(horario.dia_semana, 'Desconocido')
        
        # Sort horarios by day (integer) and time
        horarios_sorted = sorted(horarios, key=lambda h: (h.dia_semana, h.hora_inicio))
        
        return render(request, 'medicos/horarios.html', {
            'medico': medico,
            'horarios': horarios_sorted
        })
    
    except Exception as e:
        messages.error(request, f'Error al cargar horarios: {str(e)}')
        return redirect('medicos_list')


@login_required
def horario_eliminar(request, id_horario):
    """Delete a horario"""
    user = get_current_user(request)
    
    if request.method == 'POST':
        try:
            from repositories.horario_repository import HorarioRepository
            horario_repo = HorarioRepository()
            
            horario = horario_repo.find_by_id(id_horario, 'id_horario')
            if not horario:
                messages.error(request, 'Horario no encontrado')
                return redirect('dashboard')
            
            # Check permissions
            if user.rol == 'MEDICO':
                from repositories.medico_repository import MedicoRepository
                medico_repo = MedicoRepository()
                medico_user = medico_repo.find_by_usuario(user.id_usuario)
                if not medico_user or medico_user.id_medico != horario.id_medico:
                    messages.error(request, 'No tienes permiso para eliminar este horario')
                    return redirect('dashboard')
            elif user.rol != 'ADMIN':
                messages.error(request, 'No tienes permiso para eliminar horarios')
                return redirect('dashboard')
            
            id_medico = horario.id_medico
            horario_repo.update(id_horario, activo=False)
            messages.success(request, 'Horario eliminado exitosamente')
            return redirect('medico_horarios', id_medico=id_medico)
        
        except Exception as e:
            messages.error(request, f'Error al eliminar horario: {str(e)}')
            return redirect('dashboard')
    
    return redirect('dashboard')


# Reports (Admin only)
@login_required
def reportes(request):
    """Generate reports using SQL VIEWS and STORED PROCEDURES"""
    user = get_current_user(request)
    
    # Only admin can access reports
    if user.rol != 'ADMIN':
        messages.error(request, 'No tienes permiso para acceder a reportes')
        return redirect('dashboard')
    
    try:
        from services.reporte_service import ReporteService
        from datetime import date, timedelta
        
        reporte_service = ReporteService()
        
        # Get date filters from request
        fecha_desde_str = request.GET.get('fecha_desde')
        fecha_hasta_str = request.GET.get('fecha_hasta')
        
        if fecha_desde_str and fecha_hasta_str:
            from datetime import datetime
            fecha_desde = datetime.strptime(fecha_desde_str, '%Y-%m-%d').date()
            fecha_hasta = datetime.strptime(fecha_hasta_str, '%Y-%m-%d').date()
        else:
            fecha_hasta = date.today()
            fecha_desde = fecha_hasta - timedelta(days=30)
        
        # Generate all reports
        estadisticas = reporte_service.obtener_estadisticas_generales()
        citas_por_medico = reporte_service.obtener_citas_por_medico(fecha_desde, fecha_hasta)
        citas_por_especialidad = reporte_service.obtener_citas_por_especialidad(fecha_desde, fecha_hasta)
        pacientes_frecuentes = reporte_service.obtener_pacientes_frecuentes(10)
        horarios_demandados = reporte_service.obtener_horarios_demandados(fecha_desde, fecha_hasta)
        tasa_cancelacion = reporte_service.obtener_tasa_cancelacion(fecha_desde, fecha_hasta)
        ocupacion_medicos = reporte_service.obtener_ocupacion_medicos(date.today(), date.today() + timedelta(days=7))
        
        return render(request, 'reportes/dashboard.html', {
            'estadisticas': estadisticas,
            'citas_por_medico': citas_por_medico,
            'citas_por_especialidad': citas_por_especialidad,
            'pacientes_frecuentes': pacientes_frecuentes,
            'horarios_demandados': horarios_demandados,
            'tasa_cancelacion': tasa_cancelacion,
            'ocupacion_medicos': ocupacion_medicos,
            'fecha_desde': fecha_desde,
            'fecha_hasta': fecha_hasta
        })
    
    except Exception as e:
        messages.error(request, f'Error al generar reportes: {str(e)}')
        return redirect('dashboard')


# Notifications
@login_required
def notificaciones(request):
    """User notifications"""
    user = get_current_user(request)
    
    try:
        notifs = notif_repo.find_by_usuario(user.id_usuario)
        
        # Mark as read
        for notif in notifs:
            if not notif.leida:
                notif_repo.marcar_como_leida(notif.id_notificacion)
        
        return render(request, 'notificaciones/list.html', {
            'notificaciones': notifs
        })
    except Exception as e:
        messages.error(request, f'Error al cargar notificaciones: {str(e)}')
        return redirect('dashboard')
