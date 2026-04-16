from django.db.models import QuerySet
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .forms import ContractForm
from .models import Contract


class ContractListView(ListView):
    template_name = 'contracts/contracts-list.html'
    model = Contract
    context_object_name = 'contracts'

    def get_queryset(self) -> QuerySet[Contract]:
        return Contract.objects.select_related('service')


class ContractDetailView(DetailView):
    template_name = 'contracts/contract-detail.html'
    model = Contract
    context_object_name = 'contract'


class ContractCreateView(CreateView):
    model = Contract
    form_class = ContractForm
    template_name = 'contracts/contract-create.html'
    success_url = reverse_lazy('contracts:list')


class ContractUpdateView(UpdateView):
    model = Contract
    form_class = ContractForm
    template_name = 'contracts/contract-update.html'
    success_url = reverse_lazy('contracts:list')


class ContractDeleteView(DeleteView):
    model = Contract
    template_name = 'contracts/contract-delete.html'
    success_url = reverse_lazy('contracts:list')
