from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Menu, Medico, Empleado, CitaMedica
from django.contrib import messages
from .forms import PacienteForm, MedicoForm, EmpleadoForm, CitaMedicaForm
from django.urls import reverse_lazy

# Create your views here.
class MenuListView(ListView):
    model = Menu
    template_name = 'home/home.html'  # tu plantilla
    context_object_name = 'menus'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        menu_id = self.request.GET.get('menu_id')

        if menu_id:
            try:
                menu_seleccionado = Menu.objects.get(pk=menu_id)
                context['selected_menu'] = menu_seleccionado
                context['modules'] = menu_seleccionado.modules.filter(is_active=True)
            except Menu.DoesNotExist:
                context['selected_menu'] = None
                context['modules'] = []
        else:
            context['selected_menu'] = None
            context['modules'] = []

        return context


# Crear un nuevo Paciente

def crear_paciente(request):
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Paciente creado correctamente.')
            return redirect('my_app:menu-list')
    else:
        form = PacienteForm()

    context = {
        'paciente_form': form,
    }
    return render(request, 'pacientes/crear_pacientes.html', context)


# Crear un nuevo Medico

class MedicoCreateView(CreateView):
    model = Medico
    form_class = MedicoForm
    template_name = 'medicos/crear_medico.html'
    success_url = reverse_lazy('my_app:menu-list')

    def form_valid(self, form):
        messages.success(self.request, 'Médico creado correctamente.')
        return super().form_valid(form)
    
# Crear un nuevo Empleado
    
class EmpleadoCreateView(CreateView):
    model = Empleado
    form_class = EmpleadoForm
    template_name = 'empleados/crear_empleado.html'
    success_url = reverse_lazy('my_app:menu-list')

    def form_valid(self, form):
        messages.success(self.request, 'Empleado creado exitosamente')
        return super().form_valid(form)
    


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

