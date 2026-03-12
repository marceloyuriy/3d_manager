from django.contrib.auth.backends import ModelBackend

class BackendIgnoraInativo(ModelBackend):
    """
    Backend customizado para não penalizar usuários inativos no django-axes.
    """
    def user_can_authenticate(self, user):
        # O padrão do Django retorna False se is_active=False.
        # Ao retornar True, forçamos o sistema a verificar se a senha está correta,
        # evitando que o django-axes conte como tentativa falha de invasão.
        return True