from django.contrib import admin
from django.urls import path, include
from django.conf import settings # Importa as configurações (settings.py)
from django.conf.urls.static import static # Ajuda a servir arquivos de mídia

urlpatterns = [
    path('gestao-secreta-3d/', admin.site.urls),
    path('', include('fila.urls')),
]

# Isso é essencial para que os arquivos (STL/GCODE) possam ser baixados durante o desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
