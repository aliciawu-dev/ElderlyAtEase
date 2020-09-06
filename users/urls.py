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
from users import urls as users_urls
from . import views as users_views 

urlpatterns = [
    path('accounts/profile/', users_views.ProfileView.as_view(), name="profile"),
    path('accounts/verify/', users_views.VerificationView.as_view(), name="verify_setup"),
    path('accounts/verify/token', users_views.VerificationTokenView.as_view(), name="verify_otp"),
    path('accounts/verify/success', users_views.VerificationSuccessView.as_view(), name="verify_success"),
    path('accounts/profile/<int:user_id>/', users_views.ProfileView.as_view(), name="profile_other"),
    path('accounts/profile/edit/<int:pk>/', users_views.ProfileEditView.as_view(), name="profile_edit"),
    path('connect/find/', users_views.ConnectionsView.as_view(), name="connect_find"),
    path('connect/add/<int:user_id>/', users_views.ConnectionsView.add, name="add"),
    path('connect/reject/<int:user_id>/', users_views.ConnectionsView.reject, name="reject"),
]
