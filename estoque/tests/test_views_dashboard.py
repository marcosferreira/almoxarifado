import json
from datetime import date
from decimal import Decimal

from django.test import TestCase
from django.urls import reverse
from django.test.utils import override_settings

from .test_base import _criar_usuario, _criar_produto, _criar_unidade
from ..models import Pedido, ItemPedido


@override_settings(
    STORAGES={
        "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"
        },
    }
)
class DashboardViewTests(TestCase):
    def setUp(self) -> None:
        self.user = _criar_usuario("dash", grupo="Almoxarife")
        self.client.login(username="dash", password="senha12345")

    def test_dashboard_retorna_200(self) -> None:
        resp = self.client.get(reverse("dashboard"))
        self.assertEqual(resp.status_code, 200)

    def test_dashboard_mostra_banner_critico(self) -> None:
        _criar_produto("Produto Critico", estoque=0, estoque_min=10)
        resp = self.client.get(reverse("dashboard"))
        self.assertContains(resp, "abaixo do estoque mínimo")
        self.assertNotContains(resp, "Estoque regular")

    def test_dashboard_mostra_banner_regular(self) -> None:
        _criar_produto("Produto OK", estoque=20, estoque_min=10)
        resp = self.client.get(reverse("dashboard"))
        self.assertContains(resp, "Estoque regular")
        self.assertNotContains(resp, "abaixo do estoque mínimo")

    def test_dashboard_renderiza_chart_data(self) -> None:
        produto = _criar_produto("Produto Consumo", estoque=50)
        unidade = _criar_unidade("Secretaria X")

        pedido = Pedido.objects.create(
            secretaria=unidade,
            status="ENTREGUE",
            data_pedido=date.today(),
        )
        ItemPedido.objects.create(
            pedido=pedido,
            produto=produto,
            quantidade=Decimal("15"),
            preco_unitario=Decimal("2.50"),
        )

        resp = self.client.get(reverse("dashboard"))
        self.assertEqual(resp.status_code, 200)

        chart_consumo = resp.context.get("chart_consumo_json", "{}")
        chart_categoria = resp.context.get("chart_categoria_json", "{}")

        parsed_consumo = json.loads(chart_consumo)
        self.assertIn("labels", parsed_consumo)
        self.assertIn("datasets", parsed_consumo)

        parsed_categoria = json.loads(chart_categoria)
        self.assertIn("labels", parsed_categoria)
        self.assertIn("data", parsed_categoria)
        self.assertTrue(len(parsed_categoria["data"]) > 0)

    def test_kpi_variance_no_crash(self) -> None:
        resp = self.client.get(reverse("dashboard"))
        kpi = resp.context.get("kpi_variance", [])
        self.assertEqual(len(kpi), 3)
        for item in kpi:
            self.assertIn("label", item)
            self.assertIn("direction", item)
            self.assertIn("percent", item)
            self.assertIn("current", item)
            self.assertIn("previous", item)
