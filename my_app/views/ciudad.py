from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from my_app.models import Ciudad
from django.contrib import messages
from my_app.forms import  CiudadForm
from django.urls import reverse_lazy


class CiudadListView(ListView):
    model = Ciudad
    template_name = 'ciudades/list.html'
    context_object_name = 'ciudades'
    def get_queryset(self):
        queryset = super().get_queryset()
        q1 = self.request.GET.get('q', '')
        if q1 is not None:
            queryset = queryset.filter(nombre__icontains=q1)
        return queryset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('my_app:crear-ciudad')
        return context

class CiudadCreateView(CreateView):
    model = Ciudad
    form_class = CiudadForm
    template_name = 'ciudades/crear_ciudad.html'
    success_url = reverse_lazy('my_app:list-ciudad')
   
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Ciudad creada correctamente.')
        return response
    
class CiudadUpdateView(UpdateView):
    model = Ciudad
    form_class = CiudadForm
    template_name = 'ciudades/update.html'
    success_url = reverse_lazy('my_app:list-ciudad')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Ciudad actualizada correctamente.')
        return response

class CiudadDeleteView(DeleteView):
    model = Ciudad
    template_name = 'ciudades/confirm_delete.html'
    success_url = reverse_lazy('my_app:list-ciudad')
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Ciudad eliminada correctamente.')
        return super().delete(request, *args, **kwargs)
    