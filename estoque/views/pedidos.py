from django.http import HttpRequest, HttpResponse
from ._base import (
    render, redirect, get_object_or_404,
    messages, Decimal,
    login_required, _tem_papel, _to_decimal,
    Pedido, PedidoForm, ItemPedidoFormSet, AnexoEmpenhoForm,
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
