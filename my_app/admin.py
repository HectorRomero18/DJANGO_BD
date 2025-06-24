from django.contrib import admin
from .models import (
    User, Paciente, Medico, Horario, Especialidad,
    Empleado, Rol, Ciudad, Ubicacion, Consultorio, CitaMedica, Module, Menu
)

# Inlines
class HorarioInline(admin.TabularInline):
    model = Horario
    extra = 1

# Admins personalizados
@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon', 'order')
    search_fields = ('name',)
    ordering = ('order', 'name')

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'menu', 'icon', 'is_active', 'order')
    search_fields = ('name', 'url')
    list_filter = ('menu', 'is_active')
    ordering = ('menu', 'order', 'name')

@admin.register(CitaMedica)
class CitaMedicaAdmin(admin.ModelAdmin):
    list_display = ('paciente', 'medico', 'empleado', 'consultorio', 'fecha', 'hora', 'estado', 'tarifa')
    search_fields = (
        'paciente__user__first_name', 'paciente__user__last_name',
        'medico__user__first_name', 'medico__user__last_name',
        'empleado__user__first_name', 'empleado__user__last_name',
        'consultorio__numero'
    )
    list_filter = ('estado', 'fecha', 'medico', 'consultorio')
    ordering = ('-fecha', '-hora')


@admin.register(Medico)
class MedicoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'cedula', 'especialidad', 'telefono', 'genero', 'direccion', 'created_at')
    search_fields = ('user__first_name', 'user__last_name', 'cedula', 'especialidad__nombre')
    list_filter = ('especialidad', 'genero')
    inlines = [HorarioInline]

@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'cedula', 'telefono', 'genero', 'direccion', 'fecha_nacimiento', 'created_at')
    search_fields = ('user__first_name', 'user__last_name', 'cedula')
    list_filter = ('genero',)

@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'cedula', 'telefono', 'genero', 'direccion', 'rol')
    search_fields = ('user__first_name', 'user__last_name', 'cedula', 'rol__nombre')
    list_filter = ('rol', 'genero')

@admin.register(Especialidad)
class EspecialidadAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'activo')
    search_fields = ('nombre',)
    list_filter = ('activo',)

@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

@admin.register(Ciudad)
class CiudadAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

@admin.register(Ubicacion)
class UbicacionAdmin(admin.ModelAdmin):
    list_display = ('descripcion', 'ciudad')
    search_fields = ('descripcion', 'ciudad__nombre')
    list_filter = ('ciudad',)

@admin.register(Consultorio)
class ConsultorioAdmin(admin.ModelAdmin):
    list_display = ('numero', 'ubicacion')
    search_fields = ('numero', 'ubicacion__descripcion', 'ubicacion__ciudad__nombre')
    list_filter = ('ubicacion__ciudad',)

# Si quieres administrar usuarios personalizados:
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_patient', 'is_doctor', 'is_empleado', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email')
    list_filter = ('is_patient', 'is_doctor', 'is_empleado', 'is_staff', 'is_superuser')