from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse


def robots_txt(request):
    lines = [
        "User-Agent: *",
        "Disallow: /portal-gestor-aero-2026/",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


urlpatterns = [
    # A porta secreta voltou!
    path('portal-gestor-aero-2026/', admin.site.urls),

    # Bloqueio de indexação do Google
    path('robots.txt', robots_txt),

    # Resto do sistema
    path('', include('fila.urls')),
]