from django.conf import settings
from django.contrib.auth.models import User
from django.core import mail
from django.test import Client, TestCase, override_settings
from django.urls import reverse


@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
class PasswordResetFlowTests(TestCase):
    def setUp(self):
        User.objects.create_user(
            username='usuario_teste',
            email='teste@empresa.com',
            password='SenhaForte123!'
        )

    def test_password_reset_envia_email_com_link(self):
        response = self.client.post(reverse('password_reset'), {'email': 'teste@empresa.com'})

        self.assertRedirects(response, reverse('password_reset_done'))
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('Recuperação de senha', mail.outbox[0].subject)
        self.assertIn('/recuperar-senha/', mail.outbox[0].body)


class AdminIPAllowlistTests(TestCase):
    def test_admin_bloqueia_ip_fora_da_allowlist(self):
        client = Client(REMOTE_ADDR='10.0.0.55')

        response = client.get(f"/{settings.ADMIN_SITE_PATH}/")

        self.assertEqual(response.status_code, 403)

    @override_settings(ADMIN_ALLOWED_IPS=['127.0.0.1'])
    def test_admin_permite_ip_da_allowlist(self):
        client = Client(REMOTE_ADDR='127.0.0.1')

        response = client.get(f"/{settings.ADMIN_SITE_PATH}/")

        self.assertEqual(response.status_code, 302)
