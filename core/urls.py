import robots_txt
from django.contrib import admin
from django.urls import path, include
from django.conf import settings # Importa as configurações (settings.py)
from django.conf.urls.static import static # Ajuda a servir arquivos de mídia
from django.http import HttpResponse


urlpatterns = [
    path('@aeroriver_2026_hub/', admin.site.urls),
    path('', include('fila.urls')),
    path('robots.txt', robots_txt),
]

def robots_txt(request):
    lines = [
        "User-Agent: *",
        "Disallow: /portal-gestor-aero-2026/",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")

# Isso é essencial para que os arquivos (STL/GCODE) possam ser baixados durante o desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
