from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from my_app.models import CitaMedica
from django.contrib import messages
from my_app.forms import CitaMedicaForm
from django.urls import reverse_lazy




# Crear una nueva Cita Medica


class CitaMedicaListView(ListView):
    model = CitaMedica
    template_name = 'citas_medicas/list.html'
    context_object_name = 'citas_medicas'

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q')
        if q is not None:
            queryset = queryset.filter(paciente__nombre__icontains=q) | queryset.filter(medico__nombre__icontains=q) | queryset.filter(empleado__nombre__icontains=q)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('my_app:crear-cita')
        return context


class CitaMedicaCreateView(CreateView):
    model = CitaMedica
    form_class = CitaMedicaForm
    template_name = 'citas_medicas/crear_cita_medica.html'
    success_url = reverse_lazy('my_app:list-cita')

    def form_valid(self, form):
        messages.success(self.request, 'Empleado creado exitosamente')
        return super().form_valid(form)
    
class CitaMedicaUpdateView(UpdateView):
    model = CitaMedica
    form_class = CitaMedicaForm
    template_name = 'citas_medicas/update.html'
    success_url = reverse_lazy('my_app:list-cita')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Cita médica actualizada exitosamente')
        return response

class CitaMedicaDeleteView(DeleteView):
    model = CitaMedica
    template_name = 'citas_medicas/confirm_delete.html'
    success_url = reverse_lazy('my_app:list-cita')
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Cita médica eliminada exitosamente')
        return super().delete(request, *args, **kwargs)
    

