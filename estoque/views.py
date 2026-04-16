from django.shortcuts import render, redirect, get_object_or_404
from decimal import Decimal

from django.db.models import F, Sum
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from .models import Produto, Pedido, Fornecedor, Entrada, ItemEntrada, ItemPedido
from .forms import (
    ProdutoForm,
    FornecedorForm,
    EntradaForm,
    ItemEntradaFormSet,
    PedidoForm,
    ItemPedidoFormSet,
    AnexoEmpenhoForm,
    PerfilUsuarioForm,
)


def _to_decimal(value):
    return value if value is not None else Decimal("0")


@login_required
def dashboard(request):
    total_produtos = Produto.objects.count()
    pedidos_reservados = Pedido.objects.filter(status="RESERVADO").count()
    entregas_realizadas = Pedido.objects.filter(status="ENTREGUE").count()

    # Produtos com estoque abaixo do mínimo
    estoque_critico = Produto.objects.filter(estoque_atual__lt=F("estoque_minimo"))

    # Pedidos recentes
    pedidos_recentes = Pedido.objects.all().order_by("-data_pedido")[:5]

    entradas_recentes = Entrada.objects.select_related("fornecedor").order_by(
        "-data_entrada"
    )[:5]
    pedidos_pendentes_empenho = Pedido.objects.filter(status="RESERVADO").order_by(
        "-data_pedido"
    )[:6]

    context = {
        "total_produtos": total_produtos,
        "pedidos_reservados": pedidos_reservados,
        "entregas_realizadas": entregas_realizadas,
        "estoque_critico": estoque_critico,
        "pedidos_recentes": pedidos_recentes,
        "entradas_recentes": entradas_recentes,
        "pedidos_pendentes_empenho": pedidos_pendentes_empenho,
    }
    return render(request, "estoque/dashboard.html", context)


# --- PRODUTOS ---
@login_required
def produto_list(request):
    search = request.GET.get("search", "")
    produtos = Produto.objects.all()
    if search:
        produtos = produtos.filter(nome__icontains=search)
    return render(
        request, "estoque/produto_list.html", {"produtos": produtos, "search": search}
    )


@login_required
def produto_create(request):
    form = ProdutoForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Produto cadastrado com sucesso!")
        return redirect("produto_list")
    return render(
        request, "estoque/produto_form.html", {"form": form, "title": "Novo Produto"}
    )


@login_required
def produto_update(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    form = ProdutoForm(request.POST or None, instance=produto)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Produto atualizado com sucesso!")
        return redirect("produto_list")
    return render(
        request, "estoque/produto_form.html", {"form": form, "title": "Editar Produto"}
    )


# --- FORNECEDORES ---
@login_required
def fornecedor_list(request):
    fornecedores = Fornecedor.objects.all()
    return render(
        request, "estoque/fornecedor_list.html", {"fornecedores": fornecedores}
    )


@login_required
def fornecedor_create(request):
    form = FornecedorForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Fornecedor cadastrado com sucesso!")
        return redirect("fornecedor_list")
    return render(
        request,
        "estoque/fornecedor_form.html",
        {"form": form, "title": "Novo Fornecedor"},
    )


# --- ENTRADAS ---
@login_required
def entrada_list(request):
    entradas = (
        Entrada.objects.select_related("fornecedor")
        .all()
        .order_by("-data_entrada", "-id")
    )
    return render(request, "estoque/entrada_list.html", {"entradas": entradas})


@login_required
def entrada_create(request):
    entrada_form = EntradaForm(request.POST or None)
    formset = ItemEntradaFormSet(request.POST or None)
    if request.method == "POST":
        if entrada_form.is_valid() and formset.is_valid():
            entrada = entrada_form.save()
            formset.instance = entrada
            formset.save()
            messages.success(request, "Entrada de estoque registrada com sucesso!")
            return redirect("entrada_list")
    return render(
        request,
        "estoque/entrada_form.html",
        {"entrada_form": entrada_form, "formset": formset},
    )


# --- PEDIDOS ---
@login_required
def pedido_list(request):
    status_filter = request.GET.get("status")
    pedidos = Pedido.objects.all().order_by("-data_pedido")
    if status_filter:
        pedidos = pedidos.filter(status=status_filter)
    return render(
        request,
        "estoque/pedido_list.html",
        {
            "pedidos": pedidos,
            "status_filter": status_filter,
        },
    )


@login_required
def pedido_create(request):
    pedido_form = PedidoForm(request.POST or None)
    formset = ItemPedidoFormSet(request.POST or None)
    if request.method == "POST":
        if pedido_form.is_valid() and formset.is_valid():
            pedido = pedido_form.save()
            formset.instance = pedido
            formset.save()
            messages.success(request, "Pedido solicitado com sucesso!")
            return redirect("pedido_list")
    return render(
        request,
        "estoque/pedido_form.html",
        {"pedido_form": pedido_form, "formset": formset},
    )


@login_required
def pedido_detail(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    empenho_form = AnexoEmpenhoForm(
        request.POST or None, request.FILES or None, instance=pedido
    )

    itens = list(pedido.itens.select_related("produto", "produto__categoria"))

    total_geral = Decimal("0")
    total_atendido = Decimal("0")
    total_licitado = Decimal("0")
    total_restante = Decimal("0")
    for item in itens:
        total_geral += _to_decimal(item.total_pedido)
        total_atendido += _to_decimal(item.total_atendido)
        total_licitado += _to_decimal(item.quantidade_licitada)
        total_restante += _to_decimal(item.restante_licitacao)

    if request.method == "POST":
        if "reservar" in request.POST:
            try:
                pedido.status = "RESERVADO"
                pedido.save()
                messages.success(request, "Pedido reservado com sucesso!")
            except ValueError as e:
                messages.error(request, str(e))

        elif "anexar_empenho" in request.POST and empenho_form.is_valid():
            empenho_form.save()
            pedido.status = "EMPENHADO"
            pedido.save()
            messages.success(request, "Empenho anexado e status atualizado!")

        elif "confirmar_entrega" in request.POST:
            pedido.status = "ENTREGUE"
            pedido.save()
            messages.success(request, "Entrega confirmada e estoque baixado!")

        return redirect("pedido_detail", pk=pk)

    return render(
        request,
        "estoque/pedido_detail.html",
        {
            "pedido": pedido,
            "itens": itens,
            "empenho_form": empenho_form,
            "total_geral": total_geral,
            "total_atendido": total_atendido,
            "total_licitado": total_licitado,
            "total_restante": total_restante,
        },
    )


# --- RELATÓRIOS ---
@login_required
def relatorios(request):
    # Inventário Atual
    produtos = Produto.objects.all().order_by("categoria__nome", "nome")

    # Consumo por Secretaria (Simples)
    consumo_secretaria = (
        ItemPedido.objects.filter(pedido__status="ENTREGUE")
        .values("pedido__secretaria")
        .annotate(total_itens=Sum("quantidade"))
        .order_by("-total_itens")
    )

    entradas_por_grupo = (
        ItemEntrada.objects.values("produto__categoria__nome")
        .annotate(total_quantidade=Sum("quantidade"))
        .order_by("-total_quantidade")
    )

    return render(
        request,
        "estoque/relatorios.html",
        {
            "produtos": produtos,
            "consumo_secretaria": consumo_secretaria,
            "entradas_por_grupo": entradas_por_grupo,
        },
    )


@login_required
def importar_licitacao(request):
    if request.method == "POST":
        messages.success(request, "Arquivo recebido para processamento de importação.")
        return redirect("importar_licitacao")
    return render(request, "estoque/importar_licitacao.html")


@login_required
def profile(request):
    perfil_form = PerfilUsuarioForm(request.POST or None, instance=request.user)
    senha_form = PasswordChangeForm(user=request.user, data=request.POST or None)

    if request.method == "POST":
        acao = request.POST.get("acao")
        if acao == "dados":
            if perfil_form.is_valid():
                perfil_form.save()
                messages.success(request, "Perfil atualizado com sucesso.")
                return redirect("profile")
            messages.error(request, "Revise os dados do perfil e tente novamente.")

        elif acao == "senha":
            if senha_form.is_valid():
                user = senha_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, "Senha alterada com sucesso.")
                return redirect("profile")
            messages.error(request, "Não foi possível alterar a senha.")

    return render(
        request,
        "registration/profile.html",
        {
            "perfil_form": perfil_form,
            "senha_form": senha_form,
        },
    )
