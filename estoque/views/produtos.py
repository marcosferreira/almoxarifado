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
