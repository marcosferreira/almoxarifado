import io

from django.test import TestCase
from django.urls import reverse
from django.test.utils import override_settings

from .test_base import _criar_usuario, _criar_produto
from ..models import Produto


@override_settings(
    STORAGES={
        "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"
        },
    }
)
class ImportarProdutosViewTests(TestCase):
    def setUp(self) -> None:
        self.user = _criar_usuario("imp", grupo="Almoxarife")
        self.client.login(username="imp", password="senha12345")

    def _criar_xlsx(self, rows: list[list[str]]) -> io.BytesIO:
        from openpyxl import Workbook
        wb = Workbook()
        ws = wb.active
        ws.append(["Nome", "Categoria", "Unidade", "Estoque Mínimo"])
        for row in rows:
            ws.append(row)
        buf = io.BytesIO()
        wb.save(buf)
        buf.seek(0)
        buf.name = "produtos.xlsx"
        return buf

    def test_get_exibe_formulario(self) -> None:
        resp = self.client.get(reverse("importar_produtos"))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Importar Produtos em Lote")

    def test_post_sem_arquivo_exibe_erro(self) -> None:
        resp = self.client.post(reverse("importar_produtos"), {})
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Selecione um arquivo")

    def test_post_preview_exibe_tabela(self) -> None:
        xlsx = self._criar_xlsx([
            ["Papel A4", "Escritório", "RM", "100"],
            ["Caneta Azul", "Escritório", "UN", "50"],
        ])
        resp = self.client.post(reverse("importar_produtos"), {"arquivo": xlsx})
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Pré-visualização")
        self.assertContains(resp, "Papel A4")
        self.assertContains(resp, "Caneta Azul")

    def test_confirmar_importacao_cria_produtos(self) -> None:
        xlsx = self._criar_xlsx([
            ["Papel A4", "Escritório", "RM", "100"],
            ["Caneta Azul", "Escritório", "UN", "50"],
        ])
        self.client.post(reverse("importar_produtos"), {"arquivo": xlsx})
        resp = self.client.post(reverse("importar_produtos"), {"confirmar": "1"}, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Importação concluída")
        self.assertTrue(Produto.objects.filter(nome__iexact="Papel A4").exists())
        self.assertTrue(Produto.objects.filter(nome__iexact="Caneta Azul").exists())

    def test_importacao_skip_duplicados(self) -> None:
        _criar_produto("Papel A4")
        xlsx = self._criar_xlsx([
            ["Papel A4", "Escritório", "RM", "100"],
            ["Caneta Vermelha", "Escritório", "UN", "30"],
        ])
        self.client.post(reverse("importar_produtos"), {"arquivo": xlsx})
        resp = self.client.post(reverse("importar_produtos"), {"confirmar": "1"}, follow=True)
        self.assertContains(resp, "já existente")
        self.assertEqual(Produto.objects.filter(nome__iexact="Papel A4").count(), 1)
        self.assertTrue(Produto.objects.filter(nome__iexact="Caneta Vermelha").exists())

    def test_importacao_planilha_vazia(self) -> None:
        xlsx = self._criar_xlsx([])
        resp = self.client.post(reverse("importar_produtos"), {"arquivo": xlsx})
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Nenhum produto encontrado")

    def test_importacao_negada_solicitante(self) -> None:
        self.client.logout()
        user = _criar_usuario("solicit", grupo="Solicitante")
        self.client.login(username="solicit", password="senha12345")
        resp = self.client.get(reverse("importar_produtos"))
        self.assertEqual(resp.status_code, 302)
