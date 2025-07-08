from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from my_app.models import Menu
from django.contrib import messages
from django.urls import reverse_lazy

# Create your views here.
class MenuListView(ListView):
    model = Menu
    template_name = 'home/home.html'
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
