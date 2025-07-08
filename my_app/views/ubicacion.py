from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from my_app.models import Ubicacion, Ciudad
from django.contrib import messages
from my_app.forms import  UbicacionForm
from django.urls import reverse_lazy

class UbicacionListView(ListView):
    model = Ubicacion
    template_name = 'ubicaciones/list.html'
    context_object_name = 'ubicaciones'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        q1 = self.request.GET.get('q', '')
        if q1 is not None:
            queryset = queryset.filter(descripcion__icontains=q1) | queryset.filter(ciudad__nombre__icontains=q1)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('my_app:crear-ubicacion')
        return context

class UbicacionCreateView(CreateView):
    model = Ubicacion
    form_class = UbicacionForm
    template_name = 'ubicaciones/crear_ubicacion.html'
    success_url = reverse_lazy('my_app:list-ubicacion')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ciudades'] = Ciudad.objects.all()
        return context

    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Ubicación creada correctamente.')
        return response
    
class UbicacionUpdateView(UpdateView):
    model = Ubicacion
    form_class = UbicacionForm
    template_name = 'ubicaciones/update.html'
    success_url = reverse_lazy('my_app:list-ubicacion')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ciudades'] = Ciudad.objects.all()
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Ubicación actualizada correctamente.')
        return response
    
class UbicacionDeleteView(DeleteView):
    model = Ubicacion
    template_name = 'ubicaciones/confirm_delete.html'
    success_url = reverse_lazy('my_app:list-ubicacion')
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Ubicación eliminada correctamente.')
        return super().delete(request, *args, **kwargs)
    
    