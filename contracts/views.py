from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import QuerySet
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .forms import ContractForm
from .models import Contract


class ContractListView(PermissionRequiredMixin, ListView):
    permission_required = 'contracts.view_contract'
    template_name = 'contracts/contracts-list.html'
    model = Contract
    context_object_name = 'contracts'

    def get_queryset(self) -> QuerySet[Contract]:
        return Contract.objects.select_related('service')


class ContractDetailView(PermissionRequiredMixin, DetailView):
    permission_required = 'contracts.view_contract'
    template_name = 'contracts/contract-detail.html'
    model = Contract
    context_object_name = 'contract'


class ContractCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'contracts.add_contract'
    model = Contract
    form_class = ContractForm
    template_name = 'contracts/contract-create.html'
    success_url = reverse_lazy('contracts:list')


class ContractUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'contracts.change_contract'
    model = Contract
    form_class = ContractForm
    template_name = 'contracts/contract-update.html'
    success_url = reverse_lazy('contracts:list')


class ContractDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = 'contracts.delete_contract'
    model = Contract
    template_name = 'contracts/contract-delete.html'
    success_url = reverse_lazy('contracts:list')
