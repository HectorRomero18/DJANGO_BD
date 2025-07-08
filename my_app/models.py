from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.exceptions import ValidationError
from datetime import date
# Create your models here.

class Menu(models.Model):
    name = models.CharField(verbose_name='Nombre', max_length=150, unique=True)
    icon = models.CharField(verbose_name='Icono', max_length=100, default='bi bi-calendar-x-fill')
    order = models.PositiveSmallIntegerField(verbose_name='Orden', default=0)

   
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'sgm_m_menu'
        verbose_name = 'Menu'
        verbose_name_plural = 'Menus'
        ordering = ['order', 'name']

class Module(models.Model):
    url = models.CharField(verbose_name='Url', max_length=100, unique=True)
    name = models.CharField(verbose_name='Nombre', max_length=100)
    menu = models.ForeignKey(Menu, on_delete=models.PROTECT, verbose_name='Menu', related_name='modules')
    description = models.CharField(verbose_name='Descripción', max_length=200, null=True, blank=True)
    icon = models.CharField(verbose_name='Icono', max_length=100, default='bi bi-x-octagon')
    is_active = models.BooleanField(verbose_name='Es activo', default=True)
    order = models.PositiveSmallIntegerField(verbose_name='Orden', default=0)

    def __str__(self):
        return f'{self.name} [{self.url}]'

    class Meta:
        verbose_name = 'Módulo'
        db_table = 'sgm_m_module'
        verbose_name_plural = 'Módulos'
        ordering = ['menu', 'order', 'name']


def validar_cedula_ecuatoriana(value):
    if len(value) != 10 or not value.isdigit():
        raise ValidationError('La cédula debe tener 10 dígitos numéricos.')

    provincia = int(value[0:2])
    if provincia < 1 or provincia > 24:
        raise ValidationError('Los dos primeros dígitos no corresponden a ninguna provincia de Ecuador.')

    coeficientes = [2,1,2,1,2,1,2,1,2]
    suma = 0
    for i in range(9):
        mult = int(value[i]) * coeficientes[i]
        if mult >= 10:
            mult -= 9
        suma += mult
    verificador = 10 - (suma % 10) if suma % 10 != 0 else 0
    if verificador != int(value[9]):
        raise ValidationError('La cédula ecuatoriana no es válida.')

telefono_regex = RegexValidator(
    regex=r'^\+?593?\d{9}$',  # Acepta números como +593987654321 o 0987654321
    message="El número de teléfono debe estar en formato válido ecuatoriano, por ejemplo: 0987654321 o +593987654321."
)

GENERO_CHOICES = [
    ('M', 'Masculino'),
    ('F', 'Femenino'),
]

class User(AbstractUser):
    is_patient = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)
    is_empleado = models.BooleanField(default=False)

class Paciente(models.Model):
    nombre = models.CharField(max_length=100, null=True, blank=True)
    apellido = models.CharField(max_length=100, null=True, blank=True)
    cedula = models.CharField(max_length=10, 
                              validators=[validar_cedula_ecuatoriana], 
                              unique=True)
    telefono = models.CharField(max_length=20, validators=[telefono_regex])

    genero = models.CharField(max_length=1, choices=GENERO_CHOICES)
    direccion = models.CharField(max_length=200)
    fecha_nacimiento = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set', 
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_set',  
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    @property
    def edad(self):
        today = date.today()
        if self.fecha_nacimiento:
            edad = today.year - self.fecha_nacimiento.year - ((today.month, today.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day))
        return edad

    class Meta:
        db_table = 'sgm_m_paciente'

    def __str__(self):
        return f"{self.nombre} - {self.cedula}"


class Especialidad(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'sgm_p_especialidad'

    

DIAS_SEMANA = [
    ('Lun', 'Lunes'),
    ('Mar', 'Martes'),
    ('Mie', 'Miércoles'),
    ('Jue', 'Jueves'),
    ('Vie', 'Viernes'),
    ('Sab', 'Sábado'),
    ('Dom', 'Domingo'),
]

class Horario(models.Model):
    dia_semana = models.CharField(max_length=3, choices=DIAS_SEMANA)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    def clean(self):
        super().clean()
        if self.hora_fin <= self.hora_inicio:
            raise ValidationError('La hora de fin debe ser mayor que la hora de inicio.')

    def __str__(self):
        return f"{self.get_dia_semana_display()} ({self.hora_inicio} a {self.hora_fin})"

    class Meta:
        db_table = 'sgm_p_horario'




class Medico(models.Model):
    nombre = models.CharField(max_length=100, null=True, blank=True)
    apellido = models.CharField(max_length=100, null=True, blank=True)
    cedula = models.CharField(max_length=10, validators=[validar_cedula_ecuatoriana], unique=True)
    telefono = models.CharField(max_length=20, validators=[telefono_regex])
    especialidad = models.ForeignKey(Especialidad, on_delete=models.CASCADE, related_name='medicos')
    genero = models.CharField(max_length=1, choices=GENERO_CHOICES)
    direccion = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    horarios = models.ManyToManyField(Horario, related_name='medicos', blank=True)


    # @property
    # def edad(self):
    #     today = date.today()
    #     if self.fecha_nacimiento:
    #         edad = today.year - self.fecha_nacimiento.year - ((today.month, today.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day))
    #     return edad

    def __str__(self):
        return f"{self.nombre} - {self.cedula}"

    class Meta:
        db_table = 'sgm_m_medico'



class Rol(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre
    
    class Meta:
        db_table = 'sgm_p_rol'

class Empleado(models.Model):
    nombre = models.CharField(max_length=100, null=True, blank=True)
    apellido = models.CharField(max_length=100, null=True, blank=True)
    cedula = models.CharField(max_length=10, validators=[validar_cedula_ecuatoriana], unique=True)
    telefono = models.CharField(max_length=20, validators=[telefono_regex])
    genero = models.CharField(max_length=1, choices=GENERO_CHOICES)
    direccion = models.CharField(max_length=200)
    rol = models.ForeignKey(Rol, on_delete=models.SET_NULL, null=True, related_name='empleados')

    class Meta:
        db_table = 'sgm_m_empleado'


    def __str__(self):
        return f"{self.nombre} - {self.cedula}"


class Ciudad(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre
    
    class Meta:
        db_table = 'sgm_p_ciudad'


class Ubicacion(models.Model):
    descripcion = models.CharField(max_length=200)
    ciudad = models.ForeignKey(Ciudad, on_delete=models.CASCADE, related_name='ubicaciones')
    piso = models.IntegerField(default='1', blank=True)

    def __str__(self):
        return f"{self.descripcion} en {self.ciudad}"

    class Meta:
        db_table = 'sgm_p_ubicacion'



class Consultorio(models.Model):
    numero = models.CharField(max_length=10)
    ubicacion = models.ForeignKey(Ubicacion, on_delete=models.CASCADE, related_name='consultorios')
    class Meta:
        db_table = 'sgm_m_consultorio'
        unique_together = ('numero', 'ubicacion')

    def __str__(self):
        return f"Consultorio {self.numero} - {self.ubicacion.descripcion} ({self.ubicacion.ciudad.nombre})"
    


class CitaMedica(models.Model):
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE, related_name='citas')
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='citas')
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, related_name='citas')
    consultorio = models.ForeignKey(Consultorio, on_delete=models.CASCADE, related_name='citas')

    ESTADO_CITA_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('cancelada', 'Cancelada'),
        ('atendida', 'Atendida'),
    ]

    estado = models.CharField(max_length=15, choices=ESTADO_CITA_CHOICES, default='pendiente')
    fecha = models.DateField()
    hora = models.TimeField()
    tarifa = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'sgm_t_cita_medica'