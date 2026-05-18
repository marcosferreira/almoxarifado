import json
from datetime import date, timedelta
from decimal import Decimal

from django.http import HttpRequest, HttpResponse
from django.db.models.functions import TruncMonth
from django.utils import timezone
from ._base import (
    render, login_required, F, Sum, Count,
    Produto, Pedido, ItemPedido, Entrada,
)


def _six_months_start() -> date:
    """First day of the month 5 months before today (for 6-month window)."""
    today = date.today()
    month = today.month - 5
    year = today.year
    while month <= 0:
        month += 12
        year -= 1
    return date(year, month, 1)


def _meses_labels(start: date, count: int = 6) -> list[str]:
    """Generate month labels in 'mmm/YY' format for the last `count` months."""
    months_pt = ["jan", "fev", "mar", "abr", "mai", "jun",
                 "jul", "ago", "set", "out", "nov", "dez"]
    labels: list[str] = []
    current = date(start.year, start.month, 1)
    for _ in range(count):
        labels.append(f"{months_pt[current.month - 1]}/{str(current.year)[2:]}")
        month = current.month + 1
        year = current.year
        if month > 12:
            month = 1
            year += 1
        current = date(year, month, 1)
    return labels


def _chart_consumo_secretaria() -> str:
    """Bar chart data: monthly consumption by secretaria (last 6 months)."""
    inicio = _six_months_start()
    labels = _meses_labels(inicio, count=6)

    qs = (
        ItemPedido.objects
        .filter(
            pedido__status="ENTREGUE",
            pedido__data_pedido__date__gte=inicio,
        )
        .annotate(mes=TruncMonth("pedido__data_pedido"))
        .values("mes", "pedido__secretaria__nome")
        .annotate(total=Sum("quantidade"))
        .order_by("mes")
    )

    secretarias: dict[str, dict[str, Decimal]] = {}
    for row in qs:
        nome = row["pedido__secretaria__nome"] or "Sem secretaria"
        label = _meses_labels(row["mes"].date(), count=1)[0]
        if nome not in secretarias:
            secretarias[nome] = {lbl: Decimal("0") for lbl in labels}
        secretarias[nome][label] = row["total"] or Decimal("0")

    datasets = [
        {
            "label": nome,
            "data": [float(secretarias[nome].get(lbl, 0)) for lbl in labels],
        }
        for nome in secretarias
    ]

    if not datasets:
        return "{}"

    return json.dumps({"labels": labels, "datasets": datasets})


def _chart_consumo_categoria() -> str:
    """Pie chart data: consumption distribution by category."""
    qs = (
        ItemPedido.objects
        .filter(pedido__status="ENTREGUE")
        .values("produto__categoria__nome")
        .annotate(total=Sum("quantidade"))
        .order_by("-total")
    )

    labels: list[str] = []
    data: list[float] = []
    for row in qs:
        labels.append(row["produto__categoria__nome"] or "Sem categoria")
        data.append(float(row["total"] or 0))

    if not labels:
        return "{}"

    return json.dumps({"labels": labels, "data": data})


def _kpi_variance() -> list[dict[str, object]]:
    """KPI indicators comparing current month vs previous month."""
    today = date.today()
    current_start = today.replace(day=1)
    prev_start = (current_start - timedelta(days=1)).replace(day=1)
    current_end = today  # up to today for current month
    prev_end = current_start - timedelta(days=1)  # last day of previous month

    # Pedidos created this month vs last month
    pedidos_current = Pedido.objects.filter(
        data_pedido__date__gte=current_start,
        data_pedido__date__lte=current_end,
    ).count()
    pedidos_prev = Pedido.objects.filter(
        data_pedido__date__gte=prev_start,
        data_pedido__date__lte=prev_end,
    ).count()

    # Entradas created this month vs last month
    entradas_current = Entrada.objects.filter(
        data_entrada__gte=current_start,
        data_entrada__lte=current_end,
    ).count()
    entradas_prev = Entrada.objects.filter(
        data_entrada__gte=prev_start,
        data_entrada__lte=prev_end,
    ).count()

    # Items consumed (entregue) this month vs last month
    itens_current = ItemPedido.objects.filter(
        pedido__status="ENTREGUE",
        pedido__data_pedido__date__gte=current_start,
        pedido__data_pedido__date__lte=current_end,
    ).aggregate(total=Sum("quantidade"))["total"] or 0
    itens_prev = ItemPedido.objects.filter(
        pedido__status="ENTREGUE",
        pedido__data_pedido__date__gte=prev_start,
        pedido__data_pedido__date__lte=prev_end,
    ).aggregate(total=Sum("quantidade"))["total"] or 0

    def _pct(current: int | Decimal, previous: int | Decimal) -> int:
        cur = int(current) if isinstance(current, Decimal) else current
        prev = int(previous) if isinstance(previous, Decimal) else previous
        if prev == 0:
            return 100 if cur > 0 else 0
        return round((cur - prev) / prev * 100)

    def _dir(current: int | Decimal, previous: int | Decimal) -> str:
        cur = int(current) if isinstance(current, Decimal) else current
        prev = int(previous) if isinstance(previous, Decimal) else previous
        if cur > prev:
            return "up"
        if cur < prev:
            return "down"
        return "neutral"

    return [
        {
            "label": "Pedidos no Mês",
            "current": pedidos_current,
            "previous": pedidos_prev,
            "direction": _dir(pedidos_current, pedidos_prev),
            "percent": _pct(pedidos_current, pedidos_prev),
        },
        {
            "label": "Entradas no Mês",
            "current": entradas_current,
            "previous": entradas_prev,
            "direction": _dir(entradas_current, entradas_prev),
            "percent": _pct(entradas_current, entradas_prev),
        },
        {
            "label": "Itens Consumidos",
            "current": int(itens_current),
            "previous": int(itens_prev),
            "direction": _dir(itens_current, itens_prev),
            "percent": _pct(itens_current, itens_prev),
        },
    ]


@login_required
def dashboard(request: HttpRequest) -> HttpResponse:
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
            "estoque_critico_count": estoque_critico.count(),
            "pedidos_recentes": pedidos_recentes,
            "entradas_recentes": entradas_recentes,
            "pedidos_pendentes_empenho": pedidos_pendentes_empenho,
            "chart_consumo_json": _chart_consumo_secretaria(),
            "chart_categoria_json": _chart_consumo_categoria(),
            "kpi_variance": _kpi_variance(),
        },
    )
