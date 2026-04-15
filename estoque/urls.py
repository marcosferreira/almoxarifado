from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Auth
    path("login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="login"), name="logout"),
    
    # Dashboard
    path("", views.dashboard, name="dashboard"),
    
    # Produtos
    path("produtos/", views.produto_list, name="produto_list"),
    path("produtos/novo/", views.produto_create, name="produto_create"),
    path("produtos/<int:pk>/editar/", views.produto_update, name="produto_update"),
    
    # Fornecedores
    path("fornecedores/", views.fornecedor_list, name="fornecedor_list"),
    path("fornecedores/novo/", views.fornecedor_create, name="fornecedor_create"),
    
    # Entradas
    path("entradas/", views.entrada_list, name="entrada_list"),
    path("entradas/nova/", views.entrada_create, name="entrada_create"),
    
    # Pedidos
    path("pedidos/", views.pedido_list, name="pedido_list"),
    path("pedidos/novo/", views.pedido_create, name="pedido_create"),
    path("pedidos/<int:pk>/", views.pedido_detail, name="pedido_detail"),
    
    # Relatórios
    path("relatorios/", views.relatorios, name="relatorios"),
]
