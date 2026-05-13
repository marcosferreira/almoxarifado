"""
Pacote views do app estoque.
Re-exporta todas as views para compatibilidade com urls.py.
"""
from .api import produtos_por_fornecedor, setores_por_unidade
from .dashboard import dashboard
from .produtos import produto_list, produto_create, produto_update, produto_delete
from .fornecedores import (
    fornecedor_list,
    fornecedor_create,
    fornecedor_update,
    fornecedor_delete,
)
from .cadastros import (
    unidade_list,
    unidade_create,
    unidade_update,
    unidade_delete,
    setor_list,
    setor_create,
    setor_update,
    setor_delete,
)
from .entradas import entrada_list, entrada_create, entrada_update, entrada_delete
from .pedidos import pedido_list, pedido_create, pedido_detail
from .relatorios import (
    relatorios,
    relatorio_movimento,
    relatorio_estoque,
    relatorio_pedidos,
    importar_licitacao,
)
from .pdf import pedido_pdf, produto_ficha_pdf
from .auth import profile

__all__ = [
    "produtos_por_fornecedor",
    "setores_por_unidade",
    "dashboard",
    "produto_list",
    "produto_create",
    "produto_update",
    "produto_delete",
    "fornecedor_list",
    "fornecedor_create",
    "fornecedor_update",
    "fornecedor_delete",
    "unidade_list",
    "unidade_create",
    "unidade_update",
    "unidade_delete",
    "setor_list",
    "setor_create",
    "setor_update",
    "setor_delete",
    "entrada_list",
    "entrada_create",
    "entrada_update",
    "entrada_delete",
    "pedido_list",
    "pedido_create",
    "pedido_detail",
    "relatorios",
    "relatorio_movimento",
    "relatorio_estoque",
    "relatorio_pedidos",
    "importar_licitacao",
    "pedido_pdf",
    "produto_ficha_pdf",
    "profile",
]
