from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import QuerySet
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .forms import LeadForm
from .models import Lead


class LeadListView(PermissionRequiredMixin, ListView):
    permission_required = 'leads.view_lead'
    template_name = 'leads/leads-list.html'
    model = Lead
    context_object_name = 'leads'

    def get_queryset(self) -> QuerySet[Lead]:
        return Lead.objects.select_related('campaign')


class LeadDetailView(PermissionRequiredMixin, DetailView):
    permission_required = 'leads.view_lead'
    template_name = 'leads/lead-detail.html'
    model = Lead
    context_object_name = 'lead'


class LeadCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'leads.add_lead'
    model = Lead
    form_class = LeadForm
    template_name = 'leads/lead-create.html'
    success_url = reverse_lazy('leads:list')


class LeadUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'leads.change_lead'
    model = Lead
    form_class = LeadForm
    template_name = 'leads/lead-update.html'
    success_url = reverse_lazy('leads:list')


class LeadDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = 'leads.delete_lead'
    model = Lead
    template_name = 'leads/lead-delete.html'
    success_url = reverse_lazy('leads:list')
