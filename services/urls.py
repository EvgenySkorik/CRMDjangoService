from django.urls import path
from .views import (
    ServiceListView,
    ServiceDetailView,
    ServiceCreateView,
    ServiceUpdateView,
    ServiceDeleteView
)

app_name = 'services'

urlpatterns = [
    path('', ServiceListView.as_view(), name='list'),
    path('create/', ServiceCreateView.as_view(), name='create'),
    path('<int:pk>/', ServiceDetailView.as_view(), name='detail'),
    path('<int:pk>/update/', ServiceUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', ServiceDeleteView.as_view(), name='delete'),
]
