from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse


# Esta é uma função simples, não um módulo externo
def robots_txt(request):
    lines = [
        "User-Agent: *",
        "Disallow: /portal-gestor-aero-2026/",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


urlpatterns = [
    # A sua nova porta secreta
    path('portal-gestor-aero-2026/', admin.site.urls),

    # O robots.txt para esconder a porta dos motores de busca
    path('robots.txt', robots_txt),

    # A ligação com o resto do sistema
    path('', include('fila.urls')),
]