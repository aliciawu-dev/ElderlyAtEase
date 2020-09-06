"""medhacks URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from . import views as bases_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', bases_views.LandingView.as_view(), name="landing"),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='bases/login.html'), name="login"),
    path('accounts/logout/', auth_views.LogoutView.as_view(template_name='bases/logout.html'), name='logout'),
    path('accounts/register/', bases_views.RegisterView.as_view(), name="register")
]
