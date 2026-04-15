from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('services/', include('services.urls')),
    path('campaigns/', include('campaigns.urls')),
    path('leads/', include('leads.urls')),
]
