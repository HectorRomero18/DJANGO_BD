from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from my_app.models import Empleado
from django.contrib import messages
from my_app.forms import  EmpleadoForm
from django.urls import reverse_lazy


# Crear un nuevo Empleado

class EmpleadoListView(ListView):
    model = Empleado
    template_name = 'empleados/list.html'
    context_object_name = 'empleados'

    def get_queryset(self):
        queryset = super().get_queryset()
        q1 = self.request.GET.get('q', '')
        if q1 is not None:
            queryset = queryset.filter(nombre__icontains=q1) | queryset.filter(apellido__icontains=q1) | queryset.filter(cedula__icontains=q1)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('my_app:crear-empleado')
        return context
    
class EmpleadoCreateView(CreateView):
    model = Empleado
    form_class = EmpleadoForm
    template_name = 'empleados/crear_empleado.html'
    success_url = reverse_lazy('my_app:list-empleados')

    def form_valid(self, form):
        messages.success(self.request, 'Empleado creado exitosamente')
        return super().form_valid(form)
    
class EmpleadoUpdateView(UpdateView):
    model = Empleado
    form_class = EmpleadoForm
    template_name = 'empleados/update.html'
    success_url = reverse_lazy('my_app:list-empleados')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Empleado actualizado exitosamente')
        return response
    
class EmpleadoDeleteView(DeleteView):
    model = Empleado
    template_name = 'empleados/confirm_delete.html'
    success_url = reverse_lazy('my_app:list-empleados')
   
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Empleado eliminado exitosamente')
        return super().delete(request, *args, **kwargs)
    
    
