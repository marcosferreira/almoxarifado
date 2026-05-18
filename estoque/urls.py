from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Auth
    path(
        "accounts/login/",
        auth_views.LoginView.as_view(template_name="registration/login.html"),
        name="login",
    ),
    path(
        "accounts/logout/",
        auth_views.LogoutView.as_view(next_page="login"),
        name="logout",
    ),
    path("accounts/profile/", views.profile, name="profile"),
    # Dashboard
    path("", views.dashboard, name="dashboard"),
    # Produtos
    path("produtos/", views.produto_list, name="produto_list"),
    path("produtos/novo/", views.produto_create, name="produto_create"),
    path("produtos/<int:pk>/editar/", views.produto_update, name="produto_update"),
    path("produtos/<int:pk>/excluir/", views.produto_delete, name="produto_delete"),
    path("produtos/lote-estoque-minimo/", views.produto_lote_estoque, name="produto_lote_estoque"),
    path(
        "api/setores-por-unidade/",
        views.setores_por_unidade,
        name="setores_por_unidade",
    ),
    path(
        "api/produtos-por-fornecedor/",
        views.produtos_por_fornecedor,
        name="produtos_por_fornecedor",
    ),
    # Fornecedores
    path("fornecedores/", views.fornecedor_list, name="fornecedor_list"),
    path("fornecedores/novo/", views.fornecedor_create, name="fornecedor_create"),
    path("fornecedores/<int:pk>/editar/", views.fornecedor_update, name="fornecedor_update"),
    path("fornecedores/<int:pk>/excluir/", views.fornecedor_delete, name="fornecedor_delete"),
    # Unidades
    path("unidades/", views.unidade_list, name="unidade_list"),
    path("unidades/nova/", views.unidade_create, name="unidade_create"),
    path("unidades/<int:pk>/editar/", views.unidade_update, name="unidade_update"),
    path("unidades/<int:pk>/excluir/", views.unidade_delete, name="unidade_delete"),
    # Setores
    path("setores/", views.setor_list, name="setor_list"),
    path("setores/novo/", views.setor_create, name="setor_create"),
    path("setores/<int:pk>/editar/", views.setor_update, name="setor_update"),
    path("setores/<int:pk>/excluir/", views.setor_delete, name="setor_delete"),
    # Entradas
    path("entradas/", views.entrada_list, name="entrada_list"),
    path("entradas/nova/", views.entrada_create, name="entrada_create"),
    path("entradas/<int:pk>/editar/", views.entrada_update, name="entrada_update"),
    path("entradas/<int:pk>/excluir/", views.entrada_delete, name="entrada_delete"),
    # Pedidos
    path("pedidos/", views.pedido_list, name="pedido_list"),
    path("pedidos/novo/", views.pedido_create, name="pedido_create"),
    path("pedidos/<int:pk>/", views.pedido_detail, name="pedido_detail"),
    # Relatórios
    path("relatorios/", views.relatorios, name="relatorios"),
    path(
        "relatorios/movimento/",
        views.relatorio_movimento,
        name="relatorio_movimento",
    ),
    path("relatorios/estoque/", views.relatorio_estoque, name="relatorio_estoque"),
    path("relatorios/pedidos/", views.relatorio_pedidos, name="relatorio_pedidos"),
    path("importar-licitacao/", views.importar_licitacao, name="importar_licitacao"),
    path("importar-produtos/", views.importar_produtos, name="importar_produtos"),
    # PDF
    path("pedidos/<int:pk>/pdf/", views.pedido_pdf, name="pedido_pdf"),
    path("produtos/<int:pk>/ficha-pdf/", views.produto_ficha_pdf, name="produto_ficha_pdf"),
]
