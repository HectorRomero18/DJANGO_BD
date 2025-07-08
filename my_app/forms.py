from django import forms
from .models import Paciente, Medico, Empleado, CitaMedica, Consultorio, Rol, Ciudad, Ubicacion

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        exclude = ['groups', 'user_permissions', 'created_at', 'updated_at']

class MedicoForm(forms.ModelForm):
    class Meta:
        model = Medico
        exclude = ['created_at', 'updated_at']

class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = '__all__'


class RolForm(forms.ModelForm):
    class Meta:
        model = Rol
        fields = ['nombre', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre del rol',
                'maxlength': 100,
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese una descripción para el rol',
                'rows': 4,
            }),
        }

class ConsultorioForm(forms.ModelForm):
    class Meta:
        model = Consultorio
        fields = ['numero', 'ubicacion']


class CiudadForm(forms.ModelForm):
    class Meta:
        model = Ciudad
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre de la ciudad',
                'maxlength': 100,
                'required': True,
            }),
        }


class UbicacionForm(forms.ModelForm):
    class Meta:
        model = Ubicacion
        fields = ['descripcion', 'ciudad', 'piso']
        widgets = {
            'descripcion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese la descripción de la ubicación',
                'maxlength': 200,
                'required': True,
            }),
            'ciudad': forms.Select(attrs={
                'class': 'form-control',
                'required': True,
            }),
            'piso': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'required': False,
            }),
        }

class CitaMedicaForm(forms.ModelForm):
    class Meta:
        model = CitaMedica
        fields = ['medico', 'paciente', 'empleado', 'consultorio', 'estado', 'fecha', 'hora', 'tarifa']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'hora': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'tarifa': forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control'}),
        }