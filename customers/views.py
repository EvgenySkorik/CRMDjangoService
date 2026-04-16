from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from leads.models import Lead
from .forms import CustomerForm
from .models import Customer


class CustomerCreateView(CreateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'customers/customer-create.html'
    success_url = reverse_lazy('customers:list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if 'lead_pk' in self.kwargs:
            form.fields['lead'].disabled = True
            form.fields['lead'].label = 'Клиент для активации'
        return form

    def get_initial(self):
        initial = super().get_initial()
        lead_pk = self.kwargs.get('lead_pk')
        if lead_pk:
            initial['lead'] = Lead.objects.get(pk=lead_pk)
        return initial


class CustomerListView(ListView):
    model = Customer
    template_name = 'customers/customers-list.html'
    context_object_name = 'customers'


class CustomerDetailView(DetailView):
    model = Customer
    template_name = 'customers/customer-detail.html'
    context_object_name = 'customer'


class CustomerUpdateView(UpdateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'customers/customer-update.html'
    context_object_name = 'customer'
    success_url = reverse_lazy('customers:list')


class CustomerDeleteView(DeleteView):
    model = Customer
    template_name = 'customers/customer-delete.html'
    context_object_name = 'customer'
    success_url = reverse_lazy('customers:list')
