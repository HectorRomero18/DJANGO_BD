from django.contrib import admin
from django.urls import path
from .views import MenuListView, crear_paciente, MedicoCreateView, EmpleadoCreateView, CitaMedicaCreateView, CitaMedicaListView
app_name = 'my_app'


urlpatterns = [
    path('', MenuListView.as_view(), name='menu-list'),
    path('pacientes_create/', crear_paciente, name='crear-paciente'),
    path('medicos_create/', MedicoCreateView.as_view(), name='crear-medico'),
    path('empleados/', EmpleadoCreateView.as_view(), name='crear-empleado'),
    path('cita_medica_create/', CitaMedicaCreateView.as_view(), name='crear-cita'),
    path('cita_list/', CitaMedicaListView.as_view(), name='list-cita')
]
