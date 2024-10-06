from django.contrib import admin
from django.urls import path, include  # Ajoutez 'include'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('auth_app.urls')),  # Incluez les URLs de auth_app
]
