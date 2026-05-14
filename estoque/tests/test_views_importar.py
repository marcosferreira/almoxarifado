from io import BytesIO

from django.test import TestCase
from django.urls import reverse
from django.test.utils import override_settings

from openpyxl import Workbook

from ..models import Produto, Fornecedor, Entrada, ItemEntrada
from .test_base import _criar_usuario


@override_settings(
    STORAGES={
        "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"
        },
    }
)
class ImportarLicitacaoViewTests(TestCase):
    def setUp(self) -> None:
        self.user = _criar_usuario("importador", grupo="Almoxarife")
        self.client.login(username="importador", password="senha12345")

    def _arquivo_xlsx_licitacao(self):
        from django.core.files.uploadedfile import SimpleUploadedFile

        wb = Workbook()
        ws = wb.active
        ws.title = "Fornecedor Exemplo"
        ws.append(["PROPONENTE: Fornecedor Exemplo - CNPJ: 12345678000199"])
        ws.append(["Mensagem"])
        ws.append(["Item", "Produto", "Unidade", "Quantidade", "Preco", "Total"])
        ws.append([1, "Arroz Branco", "PCT", 10, 5.5, 55])
        ws.append([None, None, None, None, None, 55])

        output = BytesIO()
        wb.save(output)
        output.seek(0)
        return SimpleUploadedFile(
            "licitacao.xlsx",
            output.getvalue(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

    def test_get_exibe_formulario(self) -> None:
        resp = self.client.get(reverse("importar_licitacao"))
        self.assertEqual(resp.status_code, 200)

    def test_post_sem_arquivo_exibe_erro(self) -> None:
        resp = self.client.post(reverse("importar_licitacao"), {})
        self.assertEqual(resp.status_code, 200)

    def test_post_arquivo_invalido_exibe_erro(self) -> None:
        from django.core.files.uploadedfile import SimpleUploadedFile
        arquivo = SimpleUploadedFile("teste.txt", b"conteudo", content_type="text/plain")
        resp = self.client.post(reverse("importar_licitacao"), {"arquivo": arquivo})
        self.assertEqual(resp.status_code, 200)

    def test_importa_xlsx_em_base_vazia_criando_produto(self) -> None:
        arquivo = self._arquivo_xlsx_licitacao()

        resp_preview = self.client.post(
            reverse("importar_licitacao"),
            {
                "arquivo": arquivo,
                "licitacao_nome": "Pregao 01/2026",
            },
        )

        self.assertEqual(resp_preview.status_code, 200)
        self.assertEqual(Produto.objects.count(), 0)
        self.assertIn("licitacao_importar", self.client.session)

        resp_confirm = self.client.post(
            reverse("importar_licitacao"),
            {
                "confirmar": "1",
                "licitacao_nome": "Pregao 01/2026",
            },
        )

        self.assertEqual(resp_confirm.status_code, 302)
        self.assertEqual(Produto.objects.count(), 1)
        self.assertEqual(Fornecedor.objects.count(), 1)
        self.assertEqual(Entrada.objects.count(), 1)
        self.assertEqual(ItemEntrada.objects.count(), 1)

        item = ItemEntrada.objects.select_related("entrada", "produto").first()
        self.assertEqual(item.produto.nome, "Arroz Branco")
        self.assertEqual(item.entrada.licitacao, "Pregao 01/2026")

    def test_importa_xlsx_com_descricao_longa_sem_estourar_varchar(self) -> None:
        from django.core.files.uploadedfile import SimpleUploadedFile

        nome_muito_longo = "ARROZ " + ("INTEGRAL " * 40)

        wb = Workbook()
        ws = wb.active
        ws.title = "Fornecedor Longo"
        ws.append(["PROPONENTE: Fornecedor Longo - CNPJ: 12345678000199"])
        ws.append(["Mensagem"])
        ws.append(["Item", "Produto", "Unidade", "Quantidade", "Preco", "Total"])
        ws.append([1, nome_muito_longo, "PCT", 2, 7.5, 15])
        ws.append([None, None, None, None, None, 15])

        output = BytesIO()
        wb.save(output)
        output.seek(0)
        arquivo = SimpleUploadedFile(
            "licitacao_longa.xlsx",
            output.getvalue(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

        resp_preview = self.client.post(
            reverse("importar_licitacao"),
            {
                "arquivo": arquivo,
                "licitacao_nome": "Pregao 01/2026",
            },
        )
        self.assertEqual(resp_preview.status_code, 200)

        resp_confirm = self.client.post(
            reverse("importar_licitacao"),
            {
                "confirmar": "1",
                "licitacao_nome": "Pregao 01/2026",
            },
        )
        self.assertEqual(resp_confirm.status_code, 302)

        produto = Produto.objects.first()
        self.assertIsNotNone(produto)
        self.assertLessEqual(len(produto.nome), 200)
        self.assertEqual(ItemEntrada.objects.count(), 1)
