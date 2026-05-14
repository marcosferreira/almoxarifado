from django.test import TestCase
from django.urls import reverse
from django.test.utils import override_settings

from ..models import Produto
from .test_base import _criar_usuario, _criar_produto


@override_settings(
    STORAGES={
        "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"
        },
    }
)
class ProdutoCRUDViewTests(TestCase):
    def setUp(self) -> None:
        self.almoxarife = _criar_usuario("almox2", grupo="Almoxarife")
        self.solicitante = _criar_usuario("solicit", grupo="Solicitante")
        self.produto = _criar_produto("Papel A4", estoque=100)

    def test_produto_list_requer_login(self) -> None:
        resp = self.client.get(reverse("produto_list"))
        self.assertEqual(resp.status_code, 302)
        self.assertIn("/login", resp["Location"])

    def test_produto_list_acessivel_para_almoxarife(self) -> None:
        self.client.login(username="almox2", password="senha12345")
        resp = self.client.get(reverse("produto_list"))
        self.assertEqual(resp.status_code, 200)

    def test_produto_create_negado_para_solicitante(self) -> None:
        self.client.login(username="solicit", password="senha12345")
        resp = self.client.post(reverse("produto_create"), {"nome": "Teste"})
        self.assertEqual(resp.status_code, 302)
        self.assertFalse(Produto.objects.filter(nome="Teste").exists())

    def test_produto_delete_permitido_para_almoxarife(self) -> None:
        self.client.login(username="almox2", password="senha12345")
        pk = self.produto.pk
        resp = self.client.post(reverse("produto_delete", args=[pk]))
        self.assertEqual(resp.status_code, 302)
        self.assertFalse(Produto.objects.filter(pk=pk).exists())
