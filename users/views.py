from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from campaigns.models import Campaign
from customers.models import Customer
from leads.models import Lead
from services.models import Service


@login_required
def dashboard(request):
    context = {
        'services_count': Service.objects.count(),
        'campaigns_count': Campaign.objects.count(),
        'leads_count': Lead.objects.count(),
        'customers_count': Customer.objects.count(),
    }
    return render(request, 'users/index.html', context)


def logout_view(request):
    logout(request)
    return redirect('/login/')
