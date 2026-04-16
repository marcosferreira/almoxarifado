from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.test.utils import override_settings

from .models import PerfilUsuario


@override_settings(
    STORAGES={
        "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"
        },
    }
)
class PerfilUsuarioTemaTests(TestCase):
    def test_cria_perfil_automaticamente_para_novo_usuario(self):
        user = User.objects.create_user(username="joao", password="senha12345")

        self.assertTrue(PerfilUsuario.objects.filter(user=user).exists())
        self.assertEqual(user.perfil_usuario.tema_ui, PerfilUsuario.TEMA_CLASSIC)

    def test_salva_tema_no_perfil(self):
        user = User.objects.create_user(username="maria", password="senha12345")
        self.client.login(username="maria", password="senha12345")

        response = self.client.post(
            reverse("profile"),
            {
                "acao": "dados",
                "first_name": "Maria",
                "last_name": "Silva",
                "email": "maria@example.com",
                "tema_ui": PerfilUsuario.TEMA_MODERN,
            },
        )

        self.assertEqual(response.status_code, 302)
        user.refresh_from_db()
        self.assertEqual(user.perfil_usuario.tema_ui, PerfilUsuario.TEMA_MODERN)

    def test_renderiza_tema_escolhido_no_body(self):
        user = User.objects.create_user(username="carlos", password="senha12345")
        perfil = user.perfil_usuario
        perfil.tema_ui = PerfilUsuario.TEMA_MODERN
        perfil.save()

        self.client.login(username="carlos", password="senha12345")
        response = self.client.get(reverse("dashboard"))

        self.assertContains(response, 'data-theme="modern"')
