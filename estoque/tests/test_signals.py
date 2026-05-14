from decimal import Decimal

from django.test import TestCase
from django.test.utils import override_settings

from ..models import Pedido, ItemPedido
from .test_base import _criar_usuario, _criar_produto, _criar_unidade, _criar_setor


@override_settings(
    STORAGES={
        "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"
        },
    }
)
class EstoqueSignalTests(TestCase):
    def setUp(self) -> None:
        self.user = _criar_usuario("almox", grupo="Almoxarife")
        self.produto = _criar_produto(estoque=20, reservado=0)
        self.unidade = _criar_unidade()
        self.setor = _criar_setor(unidade=self.unidade)

    def _criar_pedido_com_item(self, quantidade: int = 5, status: str = "SOLICITADO") -> Pedido:
        pedido = Pedido.objects.create(
            secretaria=self.unidade,
            setor=self.setor,
            status=status,
        )
        ItemPedido.objects.create(pedido=pedido, produto=self.produto, quantidade=Decimal(str(quantidade)))
        return pedido

    def test_reserva_estoque_ao_mudar_para_reservado(self) -> None:
        pedido = self._criar_pedido_com_item(quantidade=5)
        self.produto.refresh_from_db()
        self.assertEqual(self.produto.estoque_reservado, Decimal("0"))

        pedido.status = "RESERVADO"
        pedido.save()

        self.produto.refresh_from_db()
        self.assertEqual(self.produto.estoque_reservado, Decimal("5"))

    def test_debita_estoque_ao_entregar(self) -> None:
        pedido = self._criar_pedido_com_item(quantidade=5)
        Pedido.objects.filter(pk=pedido.pk).update(status="RESERVADO")
        self.produto.estoque_reservado = Decimal("5")
        self.produto.save()

        pedido.refresh_from_db()
        pedido.status = "ENTREGUE"
        pedido.save()

        self.produto.refresh_from_db()
        self.assertEqual(self.produto.estoque_atual, Decimal("15"))
        self.assertEqual(self.produto.estoque_reservado, Decimal("0"))

    def test_libera_reserva_ao_cancelar(self) -> None:
        pedido = self._criar_pedido_com_item(quantidade=5)
        Pedido.objects.filter(pk=pedido.pk).update(status="RESERVADO")
        self.produto.estoque_reservado = Decimal("5")
        self.produto.save()

        pedido.refresh_from_db()
        pedido.status = "CANCELADO"
        pedido.save()

        self.produto.refresh_from_db()
        self.assertEqual(self.produto.estoque_reservado, Decimal("0"))
        self.assertEqual(self.produto.estoque_atual, Decimal("20"))

    def test_estoque_insuficiente_lanca_excecao(self) -> None:
        pedido = self._criar_pedido_com_item(quantidade=50)
        with self.assertRaises(ValueError):
            pedido.status = "RESERVADO"
            pedido.save()
