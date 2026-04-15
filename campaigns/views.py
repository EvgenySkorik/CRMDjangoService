from django.db.models import Count
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy

from .forms import CampaignForm
from .models import Campaign


class CampaignListView(ListView):
    template_name = 'campaigns/campaign-list.html'
    model = Campaign
    context_object_name = 'campaigns'


class CampaignDetailView(DetailView):
    template_name = 'campaigns/campaign-detail.html'
    model = Campaign
    context_object_name = 'campaign'


class CampaignCreateView(CreateView):
    model = Campaign
    form_class = CampaignForm
    template_name = 'campaigns/campaign-create.html'
    success_url = reverse_lazy('campaigns:list')


class CampaignUpdateView(UpdateView):
    model = Campaign
    form_class = CampaignForm
    template_name = 'campaigns/campaign-update.html'
    success_url = reverse_lazy('campaigns:list')


class CampaignDeleteView(DeleteView):
    model = Campaign
    template_name = 'campaigns/campaign-delete.html'
    success_url = reverse_lazy('campaigns:list')


class CampaignStatisticView(ListView):
    model = Campaign
    template_name = 'campaigns/campaign-statistic.html'
    context_object_name = 'campaigns'

    # def get_queryset(self):
    #     return Campaign.objects.annotate(
    #         leads_count=Count('leads'),
    #         customers_count=Count('leads', filter=Q(leads__is_active=True))
    #     )