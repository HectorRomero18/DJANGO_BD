from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from my_app.forms import PacienteForm
from my_app.models import Paciente
from django.urls import reverse_lazy




class PacienteListView(ListView):
    model = Paciente
    template_name = 'pacientes/list.html'
    context_object_name = 'pacientes'
    paginate_by = 10  # Número de pacientes por página
    
    def get_queryset(self):
        queryset = super().get_queryset()
        q1 = self.request.GET.get('q', '')
        if q1 is not None:
            queryset = queryset.filter(nombre__icontains=q1) | queryset.filter(apellido__icontains=q1) | queryset.filter(cedula__icontains=q1)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('my_app:crear-paciente')
        return context
    



# Crear un nuevo Paciente

def crear_paciente(request):
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Paciente creado correctamente.')
            return redirect('my_app:list-pacientes')
    else:
        form = PacienteForm()

    context = {
        'paciente_form': form,
    }
    return render(request, 'pacientes/crear_pacientes.html', context)


class PacienteUpdateView(UpdateView):
    model = Paciente
    form_class = PacienteForm
    template_name = 'pacientes/update.html'
    success_url = reverse_lazy('my_app:list-pacientes')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Paciente actualizado correctamente.')
        return response


class PacienteDeleteView(DeleteView):
    model = Paciente
    template_name = 'pacientes/confirm_delete.html'
    success_url = reverse_lazy('my_app:list-pacientes')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Paciente eliminado correctamente.')
        return super().delete(request, *args, **kwargs)