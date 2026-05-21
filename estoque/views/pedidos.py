from django.http import HttpRequest, HttpResponse
from ._base import (
    render, redirect, get_object_or_404,
    messages, Decimal,
    login_required, _tem_papel, _to_decimal,
    Pedido, PedidoForm, ItemPedidoFormSet, AnexoEmpenhoForm, ItemEntrada,
)


@login_required
def pedido_list(request: HttpRequest) -> HttpResponse:
    status_filter = request.GET.get("status")
    pedidos = (
        Pedido.objects.select_related("secretaria", "setor")
        .all()
        .order_by("-data_pedido")
    )
    if status_filter:
        pedidos = pedidos.filter(status=status_filter)
    return render(
        request,
        "estoque/pedido_list.html",
        {"pedidos": pedidos, "status_filter": status_filter},
    )


@_tem_papel("Almoxarife", "Comprador", "Solicitante", "Administrador")
def pedido_create(request: HttpRequest) -> HttpResponse:
    pode_editar_preco_unitario = (
        request.user.is_superuser
        or request.user.groups.filter(name="Administrador").exists()
    )

    def _preco_recente_fornecedor_produto(fornecedor_id: int, produto_id: int):
        return (
            ItemEntrada.objects.filter(
                entrada__fornecedor_id=fornecedor_id,
                produto_id=produto_id,
            )
            .order_by("-entrada__data_entrada", "-id")
            .values_list("preco_unitario", flat=True)
            .first()
        )

    pedido_form = PedidoForm(request.POST or None)
    formset = ItemPedidoFormSet(request.POST or None)

    if not pode_editar_preco_unitario:
        for item_form in formset.forms:
            if "preco_unitario" in item_form.fields:
                item_form.fields["preco_unitario"].widget.attrs["readonly"] = "readonly"
            if "quantidade_licitada" in item_form.fields:
                item_form.fields["quantidade_licitada"].widget.attrs["readonly"] = "readonly"

    if request.method == "POST":
        if pedido_form.is_valid() and formset.is_valid():
            pedido = pedido_form.save()
            formset.instance = pedido

            if not pode_editar_preco_unitario:
                for item_form in formset.forms:
                    cleaned = item_form.cleaned_data
                    if not cleaned or cleaned.get("DELETE"):
                        continue
                    produto = cleaned.get("produto")
                    if not produto:
                        continue
                    preco_base = _preco_recente_fornecedor_produto(
                        pedido.fornecedor_id,
                        produto.id,
                    ) if pedido.fornecedor_id else None
                    item_form.instance.preco_unitario = preco_base if preco_base is not None else Decimal("0")
                    item_form.instance.quantidade_licitada = item_form.instance.quantidade

            formset.save()
            messages.success(request, "Pedido solicitado com sucesso!")
            return redirect("pedido_list")
    return render(
        request,
        "estoque/pedido_form.html",
        {
            "pedido_form": pedido_form,
            "formset": formset,
            "pode_editar_preco_unitario": pode_editar_preco_unitario,
        },
    )


@login_required
def pedido_detail(request: HttpRequest, pk: int) -> HttpResponse:
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
