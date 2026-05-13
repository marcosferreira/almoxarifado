from ._base import (
    render, redirect, get_object_or_404,
    messages,
    login_required, _tem_papel, _render_pdf,
    Produto, Pedido, ItemEntrada, ItemPedido,
)


@login_required
def pedido_pdf(request, pk):
    pedido = get_object_or_404(
        Pedido.objects.select_related("secretaria").prefetch_related("itens__produto"),
        pk=pk,
    )
    return _render_pdf(
        "estoque/pedido_pdf.html",
        {"pedido": pedido},
        f"pedido_{pedido.pk}.pdf",
    )


@login_required
def produto_ficha_pdf(request, pk):
    produto = get_object_or_404(Produto.objects.select_related("categoria"), pk=pk)
    entradas = (
        ItemEntrada.objects.filter(produto=produto)
        .select_related("entrada")
        .order_by("-entrada__data_entrada")[:50]
    )
    saidas = (
        ItemPedido.objects.filter(produto=produto)
        .select_related("pedido__secretaria")
        .order_by("-pedido__data_pedido")[:50]
    )
    return _render_pdf(
        "estoque/produto_ficha_pdf.html",
        {"produto": produto, "entradas": entradas, "saidas": saidas},
        f"ficha_{produto.pk}.pdf",
    )
