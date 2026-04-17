from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from services.forms import ServiceForm
from services.models import Service


class ServiceListView(PermissionRequiredMixin, ListView):
    permission_required = 'services.view_service'
    template_name = 'services/service-list.html'
    model = Service
    context_object_name = 'services'


class ServiceDetailView(PermissionRequiredMixin, DetailView):
    permission_required = 'services.view_service'
    template_name = 'services/service-detail.html'
    model = Service
    context_object_name = 'service'


class ServiceCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'services.add_service'
    model = Service
    form_class = ServiceForm
    template_name = 'services/service-create.html'
    success_url = reverse_lazy('services:list')


class ServiceUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'services.change_service'
    model = Service
    form_class = ServiceForm
    template_name = 'services/service-update.html'
    success_url = reverse_lazy('services:list')


class ServiceDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = 'services.delete_service'
    model = Service
    template_name = 'services/service-delete.html'
    success_url = reverse_lazy('services:list')
