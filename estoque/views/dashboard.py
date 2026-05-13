from ._base import (
    render, login_required, F,
    Produto, Pedido, Entrada,
)


@login_required
def dashboard(request):
    total_produtos = Produto.objects.count()
    pedidos_reservados = Pedido.objects.filter(status="RESERVADO").count()
    entregas_realizadas = Pedido.objects.filter(status="ENTREGUE").count()
    estoque_critico = Produto.objects.filter(estoque_atual__lt=F("estoque_minimo"))
    pedidos_recentes = (
        Pedido.objects.select_related("secretaria").all().order_by("-data_pedido")[:5]
    )
    entradas_recentes = Entrada.objects.select_related("fornecedor").order_by(
        "-data_entrada"
    )[:5]
    pedidos_pendentes_empenho = (
        Pedido.objects.select_related("secretaria")
        .filter(status="RESERVADO")
        .order_by("-data_pedido")[:6]
    )
    return render(
        request,
        "estoque/dashboard.html",
        {
            "total_produtos": total_produtos,
            "pedidos_reservados": pedidos_reservados,
            "entregas_realizadas": entregas_realizadas,
            "estoque_critico": estoque_critico,
            "pedidos_recentes": pedidos_recentes,
            "entradas_recentes": entradas_recentes,
            "pedidos_pendentes_empenho": pedidos_pendentes_empenho,
        },
    )
