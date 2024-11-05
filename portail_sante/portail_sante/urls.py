"""portail_sante URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path
from auth_app import views

from django.urls import path
from auth_app import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('connexion_reussie/', views.connexion_reussie, name='connexion_reussie'),
    path('test/', views.test, name='test'),
    path('monitoring/', views.service_monitoring, name='service_monitoring'),
    path('equipe/', views.equipe_view, name='equipe'),  # Nouvelle route pour la page Équipe
    path('directeur/', views.directeur, name='directeur'),

    
]