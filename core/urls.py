from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Acesso direto e limpo para o admin
    path('admin/', admin.site.urls),

    # A ligação com o resto do sistema
    path('', include('fila.urls')),
]