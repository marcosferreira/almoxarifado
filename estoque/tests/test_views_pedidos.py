from datetime import date
from decimal import Decimal

from django.test import TestCase
from django.urls import reverse
from django.test.utils import override_settings

from ..models import Fornecedor, Entrada, ItemEntrada, ItemPedido, Pedido
from .test_base import _criar_produto, _criar_usuario


@override_settings(
    STORAGES={
        "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"
        },
    }
)
class PedidoViewsTests(TestCase):
    def setUp(self) -> None:
        self.fornecedor = Fornecedor.objects.create(
            nome_fantasia="Fornecedor A",
            razao_social="Fornecedor A LTDA",
            cnpj="12345678000199",
            contato="Contato",
            telefone="83999999999",
        )
        self.produto = _criar_produto("Caderno", estoque=50)
        self.produto.fornecedores.add(self.fornecedor)

        entrada_antiga = Entrada.objects.create(
            fornecedor=self.fornecedor,
            data_entrada=date(2026, 1, 10),
        )
        ItemEntrada.objects.create(
            entrada=entrada_antiga,
            produto=self.produto,
            quantidade=Decimal("10"),
            preco_unitario=Decimal("8.90"),
            licitacao_restante=Decimal("10"),
        )

        entrada_recente = Entrada.objects.create(
            fornecedor=self.fornecedor,
            data_entrada=date(2026, 2, 10),
        )
        ItemEntrada.objects.create(
            entrada=entrada_recente,
            produto=self.produto,
            quantidade=Decimal("10"),
            preco_unitario=Decimal("9.99"),
            licitacao_restante=Decimal("10"),
        )

    def _payload_pedido(self, preco_unitario: str, quantidade_licitada: str = "2"):
        return {
            "secretaria": "",
            "setor": "",
            "endereco_entrega": "Rua A",
            "programa": "",
            "fornecedor": str(self.fornecedor.id),
            "licitacao": "",
            "numero_empenho": "",
            "observacoes": "",
            "itens-TOTAL_FORMS": "1",
            "itens-INITIAL_FORMS": "0",
            "itens-MIN_NUM_FORMS": "0",
            "itens-MAX_NUM_FORMS": "1000",
            "itens-0-id": "",
            "itens-0-produto": str(self.produto.id),
            "itens-0-quantidade": "2",
            "itens-0-quantidade_licitada": quantidade_licitada,
            "itens-0-quantidade_atendida": "0",
            "itens-0-preco_unitario": preco_unitario,
            "itens-0-DELETE": "",
        }

    def test_api_produtos_por_fornecedor_retorna_preco_mais_recente(self) -> None:
        user = _criar_usuario("comprador-api", grupo="Comprador")
        self.client.login(username=user.username, password="senha12345")

        resposta = self.client.get(
            reverse("produtos_por_fornecedor"),
            {"fornecedor_id": self.fornecedor.id},
        )

        self.assertEqual(resposta.status_code, 200)
        produtos = resposta.json().get("produtos", [])
        self.assertEqual(len(produtos), 1)
        self.assertEqual(Decimal(str(produtos[0]["preco_unitario"])), Decimal("9.99"))

    def test_usuario_nao_admin_nao_consegue_alterar_preco_unitario(self) -> None:
        user = _criar_usuario("comprador-preco", grupo="Comprador")
        self.client.login(username=user.username, password="senha12345")

        resposta = self.client.post(
            reverse("pedido_create"),
            self._payload_pedido(preco_unitario="1.00", quantidade_licitada="999"),
        )

        self.assertEqual(resposta.status_code, 302)
        pedido = Pedido.objects.latest("id")
        item = ItemPedido.objects.get(pedido=pedido)
        self.assertEqual(item.preco_unitario, Decimal("9.99"))
        self.assertEqual(item.quantidade_licitada, Decimal("2"))

    def test_usuario_admin_pode_informar_preco_unitario_manual(self) -> None:
        user = _criar_usuario("admin-preco", grupo="Administrador")
        self.client.login(username=user.username, password="senha12345")

        resposta = self.client.post(
            reverse("pedido_create"),
            self._payload_pedido(preco_unitario="1.00"),
        )

        self.assertEqual(resposta.status_code, 302)
        pedido = Pedido.objects.latest("id")
        item = ItemPedido.objects.get(pedido=pedido)
        self.assertEqual(item.preco_unitario, Decimal("1.00"))

    def test_rejeita_quantidade_pedida_decimal(self) -> None:
        user = _criar_usuario("comprador-int-qtd", grupo="Comprador")
        self.client.login(username=user.username, password="senha12345")

        resposta = self.client.post(
            reverse("pedido_create"),
            self._payload_pedido(preco_unitario="1.00") | {"itens-0-quantidade": "2.5"},
        )

        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(Pedido.objects.count(), 0)

    def test_rejeita_quantidade_atendida_decimal(self) -> None:
        user = _criar_usuario("comprador-int-atd", grupo="Comprador")
        self.client.login(username=user.username, password="senha12345")

        resposta = self.client.post(
            reverse("pedido_create"),
            self._payload_pedido(preco_unitario="1.00") | {"itens-0-quantidade_atendida": "1.7"},
        )

        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(Pedido.objects.count(), 0)
