from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class PerfilUsuario(models.Model):
    TEMA_CLASSIC = "classic"
    TEMA_MODERN = "modern"
    TEMA_CHOICES = [
        (TEMA_CLASSIC, "Classico (ERP)"),
        (TEMA_MODERN, "Moderno"),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="perfil_usuario",
        verbose_name="Usuario",
    )
    tema_ui = models.CharField(
        max_length=20,
        choices=TEMA_CHOICES,
        default=TEMA_CLASSIC,
        verbose_name="Tema da Interface",
    )

    class Meta:
        verbose_name = "Perfil de Usuario"
        verbose_name_plural = "Perfis de Usuario"

    def __str__(self):
        return f"Perfil de {self.user.username}"


class Categoria(models.Model):
    nome = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"

    def __str__(self):
        return self.nome


class Fornecedor(models.Model):
    nome_fantasia = models.CharField(max_length=200)
    razao_social = models.CharField(max_length=200, blank=True)
    cnpj = models.CharField(max_length=18, unique=True, verbose_name="CNPJ")
    contato = models.CharField(max_length=100, blank=True)
    telefone = models.CharField(max_length=20, blank=True)

    class Meta:
        verbose_name = "Fornecedor"
        verbose_name_plural = "Fornecedores"

    def __str__(self):
        return self.nome_fantasia


class Produto(models.Model):
    UNIDADES_MEDIDA = [
        ("UN", "Unidade"),
        ("CX", "Caixa"),
        ("KG", "Quilo"),
        ("LT", "Litro"),
        ("PCT", "Pacote"),
        ("RM", "Resma"),
    ]
    nome = models.CharField(max_length=200)
    categoria = models.ForeignKey(
        Categoria, on_delete=models.PROTECT, related_name="produtos"
    )
    unidade_medida = models.CharField(
        max_length=3, choices=UNIDADES_MEDIDA, default="UN"
    )
    estoque_atual = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    estoque_reservado = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    estoque_minimo = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    @property
    def estoque_disponivel(self):
        return self.estoque_atual - self.estoque_reservado

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"

    def __str__(self):
        return f"{self.nome} ({self.unidade_medida})"


class Entrada(models.Model):
    fornecedor = models.ForeignKey(
        Fornecedor, on_delete=models.CASCADE, related_name="entradas"
    )
    data_entrada = models.DateField(default=timezone.now, verbose_name="Data")
    numero_nota = models.CharField(
        max_length=50, blank=True, verbose_name="Número da Nota"
    )
    numero_pedido = models.CharField(
        max_length=50, blank=True, verbose_name="Núm. Pedido"
    )
    unidade = models.CharField(max_length=200, blank=True, verbose_name="Unidade")
    setor = models.CharField(max_length=200, blank=True, verbose_name="Setor")
    licitacao = models.CharField(max_length=200, blank=True, verbose_name="Licitação")
    lote = models.CharField(max_length=100, blank=True, verbose_name="Lote")
    compra_direta = models.BooleanField(default=False, verbose_name="Compra Direta?")
    programa = models.CharField(max_length=100, blank=True, verbose_name="Programa")
    numero_empenho = models.CharField(
        max_length=50, blank=True, verbose_name="Nº Empenho"
    )
    observacoes = models.TextField(blank=True)

    class Meta:
        verbose_name = "Entrada"
        verbose_name_plural = "Entradas"

    def __str__(self):
        return f"Entrada {self.id} - {self.fornecedor.nome_fantasia}"


class ItemEntrada(models.Model):
    entrada = models.ForeignKey(Entrada, on_delete=models.CASCADE, related_name="itens")
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
    quantidade = models.DecimalField(max_digits=10, decimal_places=2)
    preco_unitario = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Preço Unitário"
    )
    licitacao_restante = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, verbose_name="Licit. Rest."
    )

    class Meta:
        verbose_name = "Item de Entrada"
        verbose_name_plural = "Itens de Entrada"


class Pedido(models.Model):
    STATUS_CHOICES = [
        ("SOLICITADO", "Solicitado"),
        ("RESERVADO", "Reservado"),
        ("EMPENHADO", "Empenhado"),
        ("ENTREGUE", "Entregue"),
        ("CANCELADO", "Cancelado"),
    ]
    # Cabeçalho Principal (ERP-like)
    secretaria = models.CharField(max_length=200, verbose_name="Unidade/Secretaria")
    setor = models.CharField(
        max_length=200, blank=True, verbose_name="Setor/Departamento"
    )
    data_pedido = models.DateTimeField(auto_now_add=True, verbose_name="Data/Hora")
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="SOLICITADO"
    )

    # Informações Complementares
    endereco_entrega = models.CharField(
        max_length=300, blank=True, verbose_name="Endereço de Entrega"
    )
    programa = models.CharField(
        max_length=100, blank=True, verbose_name="Programa/Convênio"
    )
    fornecedor = models.ForeignKey(
        Fornecedor,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="pedidos",
    )
    licitacao = models.CharField(
        max_length=200, blank=True, verbose_name="Licitação/Contrato"
    )
    numero_empenho = models.CharField(
        max_length=50, blank=True, verbose_name="Nº Empenho"
    )
    empenho_anexo = models.FileField(
        upload_to="empenhos/", blank=True, null=True, verbose_name="Anexo de Empenho"
    )
    compra_direta = models.BooleanField(default=False, verbose_name="Compra Direta?")
    observacoes = models.TextField(blank=True, verbose_name="Observação")

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"

    def __str__(self):
        return f"Pedido {self.id} - {self.secretaria} ({self.get_status_display()})"


class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name="itens")
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
    quantidade = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Qt. Pedida"
    )
    quantidade_licitada = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, verbose_name="Qt. Licitada"
    )
    quantidade_atendida = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, verbose_name="Qt. Atendida"
    )
    preco_unitario = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, verbose_name="Preço Unit."
    )

    @property
    def total_pedido(self):
        return self.quantidade * self.preco_unitario

    @property
    def total_atendido(self):
        return self.quantidade_atendida * self.preco_unitario

    @property
    def restante_licitacao(self):
        return self.quantidade_licitada - self.quantidade_atendida

    @property
    def percentual_licitado(self):
        if self.quantidade_licitada <= 0:
            return 0
        return (self.quantidade_atendida / self.quantidade_licitada) * 100

    class Meta:
        verbose_name = "Item de Pedido"
        verbose_name_plural = "Itens de Pedido"
