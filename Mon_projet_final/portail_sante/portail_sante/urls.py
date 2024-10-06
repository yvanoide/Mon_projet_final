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

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('connexion_reussie/', views.connexion_reussie, name='connexion_reussie'),
    path('test/', views.test, name='test'),
    path('monitoring/', views.service_monitoring, name='service_monitoring'),
    path('equipe/', views.equipe_view, name='equipe'),
    path('directeur/', views.directeur, name='directeur'),
    path('directeur_reussi/', views.directeur_reussi, name='directeur_reussi'),  # Pas de paramètre ici
    path('inscription/', views.inscription, name='register'),
    path('inscription-reussie/', views.inscription_reussie, name='inscription_reussie'),
    path('directeur_reussi/', views.directeur_reussi, name='directeur_reussi'),  # Assurez-vous que cette ligne est ici
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('directeur/', views.directeur, name='directeur'),  # Assurez-vous que cette route existe
    path('directeur_reussi/', views.directeur_reussi, name='directeur_reussi'),
]
