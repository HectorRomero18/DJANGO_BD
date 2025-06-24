from django import forms
from .models import Paciente, Medico, Empleado, CitaMedica

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


class CitaMedicaForm(forms.ModelForm):
    class Meta:
        model = CitaMedica
        fields = ['medico', 'paciente', 'empleado', 'consultorio', 'estado', 'fecha', 'hora', 'tarifa']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'hora': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'tarifa': forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control'}),
        }