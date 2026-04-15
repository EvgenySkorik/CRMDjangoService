from django.urls import path
from .views import (
    CampaignListView,
    CampaignDetailView,
    CampaignCreateView,
    CampaignUpdateView,
    CampaignDeleteView,
    CampaignStatisticView,
)

app_name = 'campaigns'

urlpatterns = [
    path('', CampaignListView.as_view(), name='list'),
    path('create/', CampaignCreateView.as_view(), name='create'),
    path('<int:pk>/', CampaignDetailView.as_view(), name='detail'),
    path('<int:pk>/update/', CampaignUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', CampaignDeleteView.as_view(), name='delete'),
    path('statistic/', CampaignStatisticView.as_view(), name='statistic'),
]
