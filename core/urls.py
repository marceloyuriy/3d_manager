from django.conf import settings
from django.contrib import admin
from django.http import HttpResponse
from django.urls import include, path


def robots_txt(request):
    lines = [
        'User-Agent: *',
        f"Disallow: /{settings.ADMIN_SITE_PATH.strip('/')}/",
    ]
    return HttpResponse('\n'.join(lines), content_type='text/plain')


urlpatterns = [
    path(f"{settings.ADMIN_SITE_PATH.strip('/')}/", admin.site.urls),
    path('robots.txt', robots_txt),
    path('', include('fila.urls')),
]
