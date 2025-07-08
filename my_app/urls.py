from django.contrib import admin
from django.urls import path
from my_app.views.medicos import MedicoCreateView, MedicoListView, MedicoUpdateView, MedicoDeleteView
from my_app.views.menu import MenuListView
from my_app.views.paciente import crear_paciente,PacienteListView, PacienteUpdateView, PacienteDeleteView
from my_app.views.empleado import EmpleadoCreateView, EmpleadoListView, EmpleadoUpdateView, EmpleadoDeleteView
from my_app.views.cita_medica import CitaMedicaCreateView, CitaMedicaListView, CitaMedicaDeleteView, CitaMedicaUpdateView
from my_app.views.consultorio import ConsultorioListView, ConsultorioCreateView, ConsultorioUpdateView, ConsultorioDeleteView
from my_app.views.rol import RolCreateView, RolListView, RolUpdateView, RolDeleteView
from my_app.views.ubicacion import UbicacionCreateView, UbicacionListView, UbicacionDeleteView, UbicacionUpdateView
from my_app.views.ciudad import CiudadCreateView, CiudadListView, CiudadDeleteView, CiudadUpdateView

app_name = 'my_app'


urlpatterns = [
    path('', MenuListView.as_view(), name='menu-list'),


    path('pacientes_list/', PacienteListView.as_view(), name='list-pacientes'),
    path('pacientes_create/', crear_paciente, name='crear-paciente'),
    path('pacientes_update/<int:pk>/', PacienteUpdateView.as_view(), name='paciente-update'),
    path('pacientes/<int:pk>/eliminar/', PacienteDeleteView.as_view(), name='paciente-delete'),



    path('medicos_list/', MedicoListView.as_view(), name='list-medicos'),
    path('medicos_create/', MedicoCreateView.as_view(), name='crear-medico'),
    path('medicos_update/<int:pk>/', MedicoUpdateView.as_view(), name='medico-update'),
    path('medicos/<int:pk>/eliminar/', MedicoDeleteView.as_view(), name='medico-delete'),


    path('empleados_list/', EmpleadoListView.as_view(), name='list-empleados'),
    path('empleados/', EmpleadoCreateView.as_view(), name='crear-empleado'),
    path('empleados_update/<int:pk>/', EmpleadoUpdateView.as_view(), name='empleado-update'),
    path('empleados/<int:pk>/eliminar/', EmpleadoDeleteView.as_view(), name='empleado-delete'),


    path('consultorios_list/', ConsultorioListView.as_view(), name='list-consultorios'),
    path('consultorios_create/', ConsultorioCreateView.as_view(), name='crear-consultorio'),
    path('consultorios_update/<int:pk>/', ConsultorioUpdateView.as_view(), name='consultorio-update'),
    path('consultorios/<int:pk>/eliminar/', ConsultorioDeleteView.as_view(), name='consultorio-delete'),



    path('ubicacion_list/', UbicacionListView.as_view(), name='list-ubicacion'),
    path('ubicacion_create/', UbicacionCreateView.as_view(), name='crear-ubicacion'),
    path('ubicacion_update/<int:pk>/', UbicacionUpdateView.as_view(), name='ubicacion-update'),
    path('ubicacion/<int:pk>/eliminar/', UbicacionDeleteView.as_view(), name='ubicacion-delete'),


    path('ciudad_list/', CiudadListView.as_view(), name='list-ciudad'),
    path('ciudad_create/', CiudadCreateView.as_view(), name='crear-ciudad'),
    path('ciudad_update/<int:pk>/', CiudadUpdateView.as_view(), name='ciudad-update'),
    path('ciudad/<int:pk>/eliminar/', CiudadDeleteView.as_view(), name='ciudad-delete'),




    path('rol_list/', RolListView.as_view(), name='list-rol'),
    path('rol_create/', RolCreateView.as_view(), name='crear-rol'),
    path('rol_update/<int:pk>/', RolUpdateView.as_view(), name='rol-update'),
    path('rol/<int:pk>/eliminar/', RolDeleteView.as_view(), name='rol-delete'),


    path('cita_list/', CitaMedicaListView.as_view(), name='list-cita'),
    path('cita_medica_create/', CitaMedicaCreateView.as_view(), name='crear-cita'),
    path('cita_medica_update/<int:pk>/', CitaMedicaUpdateView.as_view(), name='cita-update'),
    path('cita_medica/<int:pk>/eliminar/', CitaMedicaDeleteView.as_view(), name='cita-delete'),
]
