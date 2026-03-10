import ipaddress
from django.conf import settings
from django.http import HttpResponseForbidden


class AdminIPAllowlistMiddleware:
    """Restringe acesso ao admin por IP configurado em ADMIN_ALLOWED_IPS."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        admin_path = f"/{settings.ADMIN_SITE_PATH.strip('/')}/"
        if request.path.startswith(admin_path):
            if not self._is_allowed(request):
                return HttpResponseForbidden('Acesso ao admin bloqueado para este IP.')

        return self.get_response(request)

    def _is_allowed(self, request):
        allowed_ranges = getattr(settings, 'ADMIN_ALLOWED_IPS', [])
        if not allowed_ranges:
            return False

        client_ip = self._get_client_ip(request)
        if not client_ip:
            return False

        try:
            ip_obj = ipaddress.ip_address(client_ip)
        except ValueError:
            return False

        for allowed in allowed_ranges:
            try:
                network = ipaddress.ip_network(allowed, strict=False)
                if ip_obj in network:
                    return True
            except ValueError:
                continue

        return False

    @staticmethod
    def _get_client_ip(request):
        # Se estiver atrás de proxy, usa o primeiro IP da cadeia X-Forwarded-For.
        xff = request.META.get('HTTP_X_FORWARDED_FOR')
        if xff:
            return xff.split(',')[0].strip()

        return request.META.get('REMOTE_ADDR')
