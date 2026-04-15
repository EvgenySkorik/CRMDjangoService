from django.urls import path

from .views import (
    ContractListView,
    ContractCreateView,
    ContractDetailView,
    ContractDeleteView,
    ContractUpdateView
)


app_name = 'contracts'

urlpatterns = [
    path('', ContractListView.as_view(), name='list'),
    path('create/', ContractCreateView.as_view(), name='create'),
    path('<int:pk>/', ContractDetailView.as_view(), name='detail'),
    path('<int:pk>/update/', ContractUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', ContractDeleteView.as_view(), name='delete'),
]
