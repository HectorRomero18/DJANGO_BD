from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from my_app.models import Consultorio, Ubicacion
from django.contrib import messages
from my_app.forms import  ConsultorioForm
from django.urls import reverse_lazy

class ConsultorioListView(ListView):
    model = Consultorio
    template_name = 'consultorios/list.html'
    context_object_name = 'consultorios'

    def get_queryset(self):
        queryset = super().get_queryset()
        q1 = self.request.GET.get('q', '')
        if q1 is not None:
            queryset = queryset.filter(numero__icontains=q1) | queryset.filter(ubicacion__descripcion__icontains=q1)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('my_app:crear-consultorio')
        return context
    
class ConsultorioCreateView(CreateView):
    model = Consultorio
    form_class = ConsultorioForm
    template_name = 'consultorios/crear_consultorio.html'
    success_url = reverse_lazy('my_app:list-consultorios')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ubicaciones'] = Ubicacion.objects.filter(
            id__in=Consultorio.objects.values_list('ubicacion_id', flat=True).distinct()
        ).select_related('ciudad')
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Consultorio creado correctamente.')
        return response
    
class ConsultorioUpdateView(UpdateView):
    model = Consultorio
    form_class = ConsultorioForm
    template_name = 'consultorios/update.html'
    success_url = reverse_lazy('my_app:list-consultorios')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ubicaciones'] = Ubicacion.objects.filter(
            id__in=Consultorio.objects.values_list('ubicacion_id', flat=True).distinct()
        ).select_related('ciudad')
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Consultorio actualizado correctamente.')
        return response
    
class ConsultorioDeleteView(DeleteView):
    model = Consultorio
    template_name = 'consultorios/confirm_delete.html'
    success_url = reverse_lazy('my_app:list-consultorios')
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Consultorio eliminado correctamente.')
        return super().delete(request, *args, **kwargs)
    