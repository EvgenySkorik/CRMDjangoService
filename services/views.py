from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from services.forms import ServiceForm
from services.models import Service


class ServiceListView(ListView):
    template_name = 'services/service-list.html'
    model = Service
    context_object_name = 'services'


class ServiceDetailView(DetailView):
    template_name = 'services/service-detail.html'
    model = Service
    context_object_name = 'service'


class ServiceCreateView(CreateView):
    model = Service
    form_class = ServiceForm
    template_name = 'services/service-create.html'
    success_url = reverse_lazy('services:list')


class ServiceUpdateView(UpdateView):
    model = Service
    form_class = ServiceForm
    template_name = 'services/service-update.html'
    success_url = reverse_lazy('services:list')


class ServiceDeleteView(DeleteView):
    model = Service
    template_name = 'services/service-delete.html'
    success_url = reverse_lazy('services:list')
