from decimal import Decimal

from django.http import HttpRequest, HttpResponse
from ._base import (
    render, redirect, get_object_or_404,
    messages, ProtectedError,
    login_required, _tem_papel,
    Produto, ProdutoForm,
)


@login_required
def produto_list(request: HttpRequest) -> HttpResponse:
    search = request.GET.get("search", "")
    produtos = Produto.objects.all()
    if search:
        produtos = produtos.filter(nome__icontains=search)
    return render(
        request, "estoque/produto_list.html", {"produtos": produtos, "search": search}
    )


@_tem_papel("Almoxarife", "Administrador")
def produto_create(request: HttpRequest) -> HttpResponse:
    form = ProdutoForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Produto cadastrado com sucesso!")
        return redirect("produto_list")
    return render(
        request, "estoque/produto_form.html", {"form": form, "title": "Novo Produto"}
    )


@_tem_papel("Almoxarife", "Administrador")
def produto_update(request: HttpRequest, pk: int) -> HttpResponse:
    produto = get_object_or_404(Produto, pk=pk)
    form = ProdutoForm(request.POST or None, instance=produto)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Produto atualizado com sucesso!")
        return redirect("produto_list")
    return render(
        request, "estoque/produto_form.html", {"form": form, "title": "Editar Produto"}
    )


@_tem_papel("Almoxarife", "Administrador")
def produto_delete(request: HttpRequest, pk: int) -> HttpResponse:
    produto = get_object_or_404(Produto, pk=pk)
    if request.method == "POST":
        try:
            produto.delete()
            messages.success(request, "Produto excluído com sucesso!")
        except ProtectedError:
            messages.error(
                request,
                "Não foi possível excluir o produto porque ele está vinculado a entradas ou pedidos.",
            )
    return redirect("produto_list")


@_tem_papel("Almoxarife", "Comprador", "Administrador")
def produto_lote_estoque(request: HttpRequest) -> HttpResponse:
    if request.method != "POST":
        return redirect("produto_list")

    ids_str = request.POST.get("ids", "")
    if not ids_str:
        messages.warning(request, "Nenhum produto selecionado.")
        return redirect("produto_list")

    try:
        ids = [int(x) for x in ids_str.split(",") if x.strip().isdigit()]
    except (ValueError, TypeError):
        messages.error(request, "IDs inválidos.")
        return redirect("produto_list")

    if not ids:
        messages.warning(request, "Nenhum produto selecionado.")
        return redirect("produto_list")

    estoque_min_raw = request.POST.get("estoque_minimo", "0")
    try:
        novo_minimo = Decimal(estoque_min_raw)
    except Exception:
        messages.error(request, "Valor inválido para estoque mínimo.")
        return redirect("produto_list")

    if novo_minimo < 0:
        messages.error(request, "Estoque mínimo não pode ser negativo.")
        return redirect("produto_list")

    atualizados = Produto.objects.filter(pk__in=ids).update(estoque_minimo=novo_minimo)
    messages.success(
        request,
        f"Estoque mínimo atualizado para {atualizados} produto(s).",
    )
    return redirect("produto_list")
