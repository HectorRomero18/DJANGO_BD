from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from my_app.forms import RolForm
from my_app.models import Rol
from django.urls import reverse_lazy

class RolListView(ListView):
    model = Rol
    template_name = 'roles/list.html'
    context_object_name = 'roles'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        q1 = self.request.GET.get('q', '')
        if q1 is not None:
            queryset = queryset.filter(nombre__icontains=q1) | queryset.filter(descripcion__icontains=q1)
        return queryset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('my_app:crear-rol')
        return context

class RolCreateView(CreateView):
    model = Rol
    form_class = RolForm
    template_name = 'roles/crear_rol.html'
    success_url = reverse_lazy('my_app:list-rol')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Rol creado correctamente.')
        return response
    
class RolUpdateView(UpdateView):
    model = Rol
    form_class = RolForm
    template_name = 'roles/update.html'
    success_url = reverse_lazy('my_app:list-rol')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Rol actualizado correctamente.')
        return response

class RolDeleteView(DeleteView):
    model = Rol
    template_name = 'roles/confirm_delete.html'
    success_url = reverse_lazy('my_app:list-rol')
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Rol eliminado correctamente.')
        return super().delete(request, *args, **kwargs)
    