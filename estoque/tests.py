from django.test import TestCase
from django.contrib.auth.models import User, Group
from django.urls import reverse
from django.test.utils import override_settings
from decimal import Decimal
from io import BytesIO

from openpyxl import Workbook

from .models import (
    PerfilUsuario,
    Produto,
    Categoria,
    Fornecedor,
    Unidade,
    Setor,
    Pedido,
    ItemPedido,
    Entrada,
    ItemEntrada,
)


def _criar_usuario(username="teste", password="senha12345", grupo=None):
    user = User.objects.create_user(username=username, password=password)
    if grupo:
        g, _ = Group.objects.get_or_create(name=grupo)
        user.groups.add(g)
    return user


def _criar_produto(nome="Caneta", estoque=10, estoque_min=2, reservado=0):
    cat, _ = Categoria.objects.get_or_create(nome="Escritório")
    return Produto.objects.create(
        nome=nome,
        categoria=cat,
        unidade_medida="UN",
        estoque_atual=Decimal(str(estoque)),
        estoque_reservado=Decimal(str(reservado)),
        estoque_minimo=Decimal(str(estoque_min)),
    )


def _criar_unidade(nome="Secretaria de Educação"):
    return Unidade.objects.get_or_create(nome=nome)[0]


def _criar_setor(nome="TI", unidade=None):
    if unidade is None:
        unidade = _criar_unidade()
    return Setor.objects.get_or_create(nome=nome, unidade=unidade)[0]


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


# ---------------------------------------------------------------------------
# Signals: mutações de estoque via pedido
# ---------------------------------------------------------------------------
@override_settings(
    STORAGES={
        "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"
        },
    }
)
class EstoqueSignalTests(TestCase):
    def setUp(self):
        self.user = _criar_usuario("almox", grupo="Almoxarife")
        self.produto = _criar_produto(estoque=20, reservado=0)
        self.unidade = _criar_unidade()
        self.setor = _criar_setor(unidade=self.unidade)

    def _criar_pedido_com_item(self, quantidade=5, status="SOLICITADO"):
        pedido = Pedido.objects.create(
            secretaria=self.unidade,
            setor=self.setor,
            status=status,
        )
        ItemPedido.objects.create(pedido=pedido, produto=self.produto, quantidade=Decimal(str(quantidade)))
        return pedido

    def test_reserva_estoque_ao_mudar_para_reservado(self):
        pedido = self._criar_pedido_com_item(quantidade=5)
        self.produto.refresh_from_db()
        self.assertEqual(self.produto.estoque_reservado, Decimal("0"))

        pedido.status = "RESERVADO"
        pedido.save()

        self.produto.refresh_from_db()
        self.assertEqual(self.produto.estoque_reservado, Decimal("5"))

    def test_debita_estoque_ao_entregar(self):
        pedido = self._criar_pedido_com_item(quantidade=5)
        # Simular estado reservado diretamente no banco sem trigger do signal
        Pedido.objects.filter(pk=pedido.pk).update(status="RESERVADO")
        self.produto.estoque_reservado = Decimal("5")
        self.produto.save()

        pedido.refresh_from_db()
        pedido.status = "ENTREGUE"
        pedido.save()

        self.produto.refresh_from_db()
        self.assertEqual(self.produto.estoque_atual, Decimal("15"))
        self.assertEqual(self.produto.estoque_reservado, Decimal("0"))

    def test_libera_reserva_ao_cancelar(self):
        pedido = self._criar_pedido_com_item(quantidade=5)
        Pedido.objects.filter(pk=pedido.pk).update(status="RESERVADO")
        self.produto.estoque_reservado = Decimal("5")
        self.produto.save()

        pedido.refresh_from_db()
        pedido.status = "CANCELADO"
        pedido.save()

        self.produto.refresh_from_db()
        self.assertEqual(self.produto.estoque_reservado, Decimal("0"))
        self.assertEqual(self.produto.estoque_atual, Decimal("20"))  # não debitou

    def test_estoque_insuficiente_lanca_excecao(self):
        pedido = self._criar_pedido_com_item(quantidade=50)  # mais do que o estoque
        with self.assertRaises(ValueError):
            pedido.status = "RESERVADO"
            pedido.save()


# ---------------------------------------------------------------------------
# Views: CRUD de Produto (permissões)
# ---------------------------------------------------------------------------
@override_settings(
    STORAGES={
        "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"
        },
    }
)
class ProdutoCRUDViewTests(TestCase):
    def setUp(self):
        self.almoxarife = _criar_usuario("almox2", grupo="Almoxarife")
        self.solicitante = _criar_usuario("solicit", grupo="Solicitante")
        self.produto = _criar_produto("Papel A4", estoque=100)

    def test_produto_list_requer_login(self):
        resp = self.client.get(reverse("produto_list"))
        self.assertEqual(resp.status_code, 302)
        self.assertIn("/login", resp["Location"])

    def test_produto_list_acessivel_para_almoxarife(self):
        self.client.login(username="almox2", password="senha12345")
        resp = self.client.get(reverse("produto_list"))
        self.assertEqual(resp.status_code, 200)

    def test_produto_create_negado_para_solicitante(self):
        self.client.login(username="solicit", password="senha12345")
        resp = self.client.post(reverse("produto_create"), {"nome": "Teste"})
        # Deve redirecionar para dashboard (sem permissão)
        self.assertEqual(resp.status_code, 302)
        self.assertFalse(Produto.objects.filter(nome="Teste").exists())

    def test_produto_delete_permitido_para_almoxarife(self):
        self.client.login(username="almox2", password="senha12345")
        pk = self.produto.pk
        resp = self.client.post(reverse("produto_delete", args=[pk]))
        self.assertEqual(resp.status_code, 302)
        self.assertFalse(Produto.objects.filter(pk=pk).exists())


# ---------------------------------------------------------------------------
# Views: Relatórios com filtro e export
# ---------------------------------------------------------------------------
@override_settings(
    STORAGES={
        "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"
        },
    }
)
class RelatorioViewTests(TestCase):
    def setUp(self):
        self.user = _criar_usuario("relat", grupo="Almoxarife")
        self.client.login(username="relat", password="senha12345")
        _criar_produto("Produto CSV", estoque=5)

    def test_relatorio_estoque_retorna_200(self):
        resp = self.client.get(reverse("relatorio_estoque"))
        self.assertEqual(resp.status_code, 200)

    def test_relatorio_estoque_export_csv(self):
        resp = self.client.get(reverse("relatorio_estoque"), {"export": "csv"})
        self.assertEqual(resp.status_code, 200)
        self.assertIn("text/csv", resp["Content-Type"])

    def test_relatorio_estoque_export_xlsx(self):
        resp = self.client.get(reverse("relatorio_estoque"), {"export": "xlsx"})
        self.assertEqual(resp.status_code, 200)
        self.assertIn("spreadsheetml", resp["Content-Type"])

    def test_relatorio_pedidos_retorna_200(self):
        resp = self.client.get(reverse("relatorio_pedidos"))
        self.assertEqual(resp.status_code, 200)

    def test_relatorio_movimento_retorna_200(self):
        resp = self.client.get(reverse("relatorio_movimento"))
        self.assertEqual(resp.status_code, 200)


# ---------------------------------------------------------------------------
# Importar licitação
# ---------------------------------------------------------------------------
@override_settings(
    STORAGES={
        "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"
        },
    }
)
class ImportarLicitacaoViewTests(TestCase):
    def setUp(self):
        self.user = _criar_usuario("importador", grupo="Almoxarife")
        self.client.login(username="importador", password="senha12345")

    def _arquivo_xlsx_licitacao(self):
        from django.core.files.uploadedfile import SimpleUploadedFile

        wb = Workbook()
        ws = wb.active
        ws.title = "Fornecedor Exemplo"
        ws.append(["PROPONENTE: Fornecedor Exemplo - CNPJ: 12345678000199"])  # linha 1
        ws.append(["Mensagem"])  # linha 2
        ws.append(["Item", "Produto", "Unidade", "Quantidade", "Preco", "Total"])  # linha 3
        ws.append([1, "Arroz Branco", "PCT", 10, 5.5, 55])  # linha 4
        ws.append([None, None, None, None, None, 55])  # linha total/fim

        output = BytesIO()
        wb.save(output)
        output.seek(0)
        return SimpleUploadedFile(
            "licitacao.xlsx",
            output.getvalue(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

    def test_get_exibe_formulario(self):
        resp = self.client.get(reverse("importar_licitacao"))
        self.assertEqual(resp.status_code, 200)

    def test_post_sem_arquivo_exibe_erro(self):
        resp = self.client.post(reverse("importar_licitacao"), {})
        self.assertEqual(resp.status_code, 200)

    def test_post_arquivo_invalido_exibe_erro(self):
        from django.core.files.uploadedfile import SimpleUploadedFile
        arquivo = SimpleUploadedFile("teste.txt", b"conteudo", content_type="text/plain")
        resp = self.client.post(reverse("importar_licitacao"), {"arquivo": arquivo})
        self.assertEqual(resp.status_code, 200)

    def test_importa_xlsx_em_base_vazia_criando_produto(self):
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

    def test_importa_xlsx_com_descricao_longa_sem_estourar_varchar(self):
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

