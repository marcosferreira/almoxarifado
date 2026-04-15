from django.contrib import admin
from .models import Categoria, Fornecedor, Produto, Entrada, ItemEntrada, Pedido, ItemPedido

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nome",)
    search_fields = ("nome",)

@admin.register(Fornecedor)
class FornecedorAdmin(admin.ModelAdmin):
    list_display = ("nome_fantasia", "cnpj", "telefone")
    search_fields = ("nome_fantasia", "cnpj")

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ("nome", "categoria", "unidade_medida", "estoque_atual", "estoque_reservado", "estoque_disponivel", "estoque_minimo")
    list_filter = ("categoria", "unidade_medida")
    search_fields = ("nome",)

class ItemEntradaInline(admin.TabularInline):
    model = ItemEntrada
    extra = 1

@admin.register(Entrada)
class EntradaAdmin(admin.ModelAdmin):
    list_display = ("id", "fornecedor", "data_entrada", "numero_nota")
    inlines = [ItemEntradaInline]
    list_filter = ("fornecedor", "data_entrada")

class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 1

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ("id", "secretaria", "status", "data_pedido")
    inlines = [ItemPedidoInline]
    list_filter = ("status", "secretaria")
    search_fields = ("secretaria",)
