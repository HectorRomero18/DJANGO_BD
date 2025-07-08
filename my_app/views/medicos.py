from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from my_app.models import Medico
from django.contrib import messages
from my_app.forms import  MedicoForm
from django.urls import reverse_lazy



class MedicoListView(ListView):
    model = Medico
    template_name = 'medicos/list.html'
    context_object_name = 'medicos'

    def get_queryset(self):
        queryset = super().get_queryset()
        q1 = self.request.GET.get('q', '')
        if q1 is not None:
            queryset = queryset.filter(nombre__icontains=q1) | queryset.filter(apellido__icontains=q1) | queryset.filter(cedula__icontains=q1)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('my_app:crear-medico')
        return context



class MedicoCreateView(CreateView):
    model = Medico
    form_class = MedicoForm
    template_name = 'medicos/crear_medico.html'
    success_url = reverse_lazy('my_app:list-medicos')

    def form_valid(self, form):
        messages.success(self.request, 'Médico creado correctamente.')
        return super().form_valid(form)
    

class MedicoUpdateView(UpdateView):
    model = Medico
    form_class = MedicoForm
    template_name = 'medicos/update.html'
    success_url = reverse_lazy('my_app:list-medicos')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Médico actualizado correctamente.')
        return response
    

class MedicoDeleteView(DeleteView):
    model = Medico
    template_name = 'medicos/confirm_delete.html'
    success_url = reverse_lazy('my_app:list-medicos') 

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Médico eliminado correctamente.')
        return super().delete(request, *args, **kwargs)
    
