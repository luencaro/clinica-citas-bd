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
                
                medico_service.crear_medico_completo(
                    nombre=nombre,
                    apellido=apellido,
                    email=email,
                    telefono=telefono,
                    contraseña=password,
                    id_especialidad=id_especialidad,
                    registro_profesional=registro_profesional
                )
                
                messages.success(request, 'Cuenta de médico creada exitosamente. Por favor inicia sesión.')
            
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
            paciente_repo = PacienteRepository()
            paciente = paciente_repo.find_by_usuario(user.id_usuario)
            
            if paciente:
                # Get upcoming appointments
                proximas_citas = cita_service.obtener_proximas_citas(id_paciente=paciente.id_paciente, limit=5)
                context['paciente'] = paciente
                context['proximas_citas'] = proximas_citas
        
        elif user.rol == 'MEDICO':
            # Get doctor data
            from repositories.medico_repository import MedicoRepository
            medico_repo = MedicoRepository()
            medico = medico_repo.find_by_usuario(user.id_usuario)
            
            if medico:
                # Get today's appointments
                hoy = date.today()
                citas_hoy = cita_service.obtener_citas_fecha(hoy, id_medico=medico.id_medico)
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
            citas = cita_repo.find_all()
        
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
            return redirect('cita_detalle', id_cita=cita.id_cita)
            
        except CitaDuplicadaError as e:
            messages.error(request, str(e))
        except CitaNoDisponibleError as e:
            messages.error(request, str(e))
        except FueraDeHorarioError as e:
            messages.error(request, str(e))
        except Exception as e:
            messages.error(request, f'Error al agendar cita: {str(e)}')
    
    # Get data for form
    especialidades = especialidad_service.listar_activas()
    medicos = medico_service.listar_activos()
    
    # Get patients if admin
    pacientes = []
    if user.rol == 'ADMIN':
        from repositories.paciente_repository import PacienteRepository
        paciente_repo = PacienteRepository()
        pacientes = paciente_repo.find_all()
    
    return render(request, 'citas/nueva.html', {
        'especialidades': especialidades,
        'medicos': medicos,
        'pacientes': pacientes,
        'user': user
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
        
        paciente_repo = PacienteRepository()
        medico_repo = MedicoRepository()
        
        paciente = paciente_repo.find_by_id(cita.id_paciente, 'id_paciente')
        medico = medico_repo.find_by_id(cita.id_medico, 'id_medico')
        
        return render(request, 'citas/detalle.html', {
            'cita': cita,
            'paciente': paciente,
            'medico': medico,
            'user': user
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
            messages.success(request, f'Cita reprogramada para el {fecha} a las {hora}')
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
            messages.success(request, 'Cita marcada como atendida')
            return redirect('cita_detalle', id_cita=id_cita)
        except Exception as e:
            messages.error(request, f'Error al marcar cita: {str(e)}')
    
    return redirect('cita_detalle', id_cita=id_cita)


# Medicos Views
@login_required
def medicos_list(request):
    """List doctors"""
    try:
        especialidad_id = request.GET.get('especialidad')
        
        if especialidad_id:
            medicos = medico_service.obtener_por_especialidad(int(especialidad_id))
        else:
            medicos = medico_service.listar_activos()
        
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
    try:
        medico = medico_service.obtener_por_id(id_medico)
        horarios = medico_service.obtener_horarios(id_medico)
        
        return render(request, 'medicos/detalle.html', {
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
        disponibilidad = cita_service.obtener_disponibilidad_medico(id_medico, fecha)
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'disponibilidad': [h.strftime('%H:%M') for h in disponibilidad]
            })
        
        medico = medico_service.obtener_por_id(id_medico)
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
        paciente_repo = PacienteRepository()
        pacientes = paciente_repo.find_all()
        
        return render(request, 'dashboard/dashboard.html', {
            'pacientes': pacientes,
            'seccion': 'pacientes'
        })
    except Exception as e:
        messages.error(request, f'Error al cargar pacientes: {str(e)}')
        return redirect('dashboard')


@login_required
def paciente_detalle(request, id_paciente):
    """Patient detail"""
    try:
        from repositories.paciente_repository import PacienteRepository
        paciente_repo = PacienteRepository()
        paciente = paciente_repo.find_by_id(id_paciente, 'id_paciente')
        
        # Check permissions
        user = get_current_user(request)
        if user.rol == 'PACIENTE':
            paciente_user = paciente_repo.find_by_usuario(user.id_usuario)
            if paciente.id_paciente != paciente_user.id_paciente:
                return HttpResponseForbidden('No tienes permiso para ver este paciente')
        
        citas = cita_service.obtener_citas_paciente(id_paciente)
        
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
            paciente_repo = PacienteRepository()
            paciente = paciente_repo.find_by_usuario(user.id_usuario)
            context['paciente'] = paciente
        
        elif user.rol == 'MEDICO':
            from repositories.medico_repository import MedicoRepository
            medico_repo = MedicoRepository()
            medico = medico_repo.find_by_usuario(user.id_usuario)
            context['medico'] = medico
    
    except Exception as e:
        messages.error(request, f'Error al cargar perfil: {str(e)}')
    
    return render(request, 'perfil/perfil.html', context)


@login_required
def perfil_editar(request):
    """Edit user profile"""
    user = get_current_user(request)
    
    if request.method == 'POST':
        try:
            nombre = request.POST.get('nombre')
            apellido = request.POST.get('apellido')
            telefono = request.POST.get('telefono')
            
            usuario_service.actualizar_usuario(
                user.id_usuario,
                nombre=nombre,
                apellido=apellido,
                telefono=telefono
            )
            
            request.session['user_name'] = f"{nombre} {apellido}"
            messages.success(request, 'Perfil actualizado exitosamente')
            return redirect('perfil')
        
        except Exception as e:
            messages.error(request, f'Error al actualizar perfil: {str(e)}')
    
    return render(request, 'perfil/editar.html', {'user': user})


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
