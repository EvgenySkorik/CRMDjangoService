from django.urls import path

from customers.views import (
    CustomerCreateView,
    CustomerListView,
    CustomerDetailView,
    CustomerUpdateView,
    CustomerDeleteView,
)

app_name = 'customers'

urlpatterns = [
    path('', CustomerListView.as_view(), name='list'),
    path('create/', CustomerCreateView.as_view(), name='create'),
    path('create/<int:lead_pk>/', CustomerCreateView.as_view(), name='create_from_lead'),
    path('<int:pk>/', CustomerDetailView.as_view(), name='detail'),
    path('<int:pk>/update/', CustomerUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', CustomerDeleteView.as_view(), name='delete'),
]
