"""
URL Configuration for Medical Appointments System
"""

from django.contrib import admin
from django.urls import path
from webapp import views

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # Authentication
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Citas
    path('citas/', views.citas_list, name='citas_list'),
    path('citas/nueva/', views.cita_nueva, name='cita_nueva'),
    path('citas/<int:id_cita>/', views.cita_detalle, name='cita_detalle'),
    path('citas/<int:id_cita>/cancelar/', views.cita_cancelar, name='cita_cancelar'),
    path('citas/<int:id_cita>/reprogramar/', views.cita_reprogramar, name='cita_reprogramar'),
    path('citas/<int:id_cita>/atender/', views.cita_atender, name='cita_atender'),
    
    # Médicos
    path('medicos/', views.medicos_list, name='medicos_list'),
    path('medicos/<int:id_medico>/', views.medico_detalle, name='medico_detalle'),
    path('medicos/<int:id_medico>/disponibilidad/', views.medico_disponibilidad, name='medico_disponibilidad'),
    path('medicos/<int:id_medico>/horarios/', views.medico_horarios, name='medico_horarios'),
    path('horarios/<int:id_horario>/eliminar/', views.horario_eliminar, name='horario_eliminar'),
    
    # Especialidades
    path('especialidades/', views.especialidades_list, name='especialidades_list'),
    
    # Pacientes (solo para admin)
    path('pacientes/', views.pacientes_list, name='pacientes_list'),
    path('pacientes/<int:id_paciente>/', views.paciente_detalle, name='paciente_detalle'),
    
    # Perfil
    path('perfil/', views.perfil, name='perfil'),
    path('perfil/editar/', views.perfil_editar, name='perfil_editar'),
    
    # Reportes (Admin)
    path('reportes/', views.reportes, name='reportes'),
    
    # Notificaciones
    path('notificaciones/', views.notificaciones, name='notificaciones'),
]
