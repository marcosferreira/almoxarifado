from decimal import Decimal

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


@override_settings(
    STORAGES={
        "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"
        },
    }
)
class ProdutoLoteEstoqueTests(TestCase):
    def setUp(self) -> None:
        self.user = _criar_usuario("lotetest", grupo="Almoxarife")
        self.client.login(username="lotetest", password="senha12345")
        self.p1 = _criar_produto("Produto A", estoque=10, estoque_min=2)
        self.p2 = _criar_produto("Produto B", estoque=20, estoque_min=5)

    def test_atualiza_estoque_minimo_em_lote(self) -> None:
        resp = self.client.post(
            reverse("produto_lote_estoque"),
            {"ids": f"{self.p1.pk},{self.p2.pk}", "estoque_minimo": "15"},
            follow=True,
        )
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "atualizado para 2")
        self.p1.refresh_from_db()
        self.p2.refresh_from_db()
        self.assertEqual(self.p1.estoque_minimo, Decimal("15"))
        self.assertEqual(self.p2.estoque_minimo, Decimal("15"))

    def test_sem_produtos_selecionados_exibe_warning(self) -> None:
        resp = self.client.post(
            reverse("produto_lote_estoque"),
            {"ids": "", "estoque_minimo": "10"},
            follow=True,
        )
        self.assertContains(resp, "Nenhum produto selecionado")

    def test_negado_para_solicitante(self) -> None:
        self.client.logout()
        user = _criar_usuario("sol2", grupo="Solicitante")
        self.client.login(username="sol2", password="senha12345")
        resp = self.client.post(
            reverse("produto_lote_estoque"),
            {"ids": str(self.p1.pk), "estoque_minimo": "10"},
        )
        self.assertEqual(resp.status_code, 302)
