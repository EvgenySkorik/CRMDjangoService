from django.urls import path
from django.contrib.auth import views as auth_views
from .views import dashboard, logout_view

app_name = 'users'

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', logout_view, name='logout'),
]
