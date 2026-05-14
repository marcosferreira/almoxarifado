from django.test import TestCase
from django.urls import reverse
from django.test.utils import override_settings

from .test_base import _criar_usuario, _criar_produto


@override_settings(
    STORAGES={
        "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"
        },
    }
)
class RelatorioViewTests(TestCase):
    def setUp(self) -> None:
        self.user = _criar_usuario("relat", grupo="Almoxarife")
        self.client.login(username="relat", password="senha12345")
        _criar_produto("Produto CSV", estoque=5)

    def test_relatorio_estoque_retorna_200(self) -> None:
        resp = self.client.get(reverse("relatorio_estoque"))
        self.assertEqual(resp.status_code, 200)

    def test_relatorio_estoque_export_csv(self) -> None:
        resp = self.client.get(reverse("relatorio_estoque"), {"export": "csv"})
        self.assertEqual(resp.status_code, 200)
        self.assertIn("text/csv", resp["Content-Type"])

    def test_relatorio_estoque_export_xlsx(self) -> None:
        resp = self.client.get(reverse("relatorio_estoque"), {"export": "xlsx"})
        self.assertEqual(resp.status_code, 200)
        self.assertIn("spreadsheetml", resp["Content-Type"])

    def test_relatorio_pedidos_retorna_200(self) -> None:
        resp = self.client.get(reverse("relatorio_pedidos"))
        self.assertEqual(resp.status_code, 200)

    def test_relatorio_movimento_retorna_200(self) -> None:
        resp = self.client.get(reverse("relatorio_movimento"))
        self.assertEqual(resp.status_code, 200)
