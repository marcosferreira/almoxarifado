from typing import Any

from django.db.models import Q, OuterRef, Subquery, DecimalField
from django.http import HttpRequest, JsonResponse
from ._base import (
    login_required,
    Produto, Setor, Entrada, Pedido, ItemEntrada,
)


@login_required
def produtos_por_fornecedor(request: HttpRequest) -> JsonResponse:
    fornecedor_id = request.GET.get("fornecedor_id")
    if not fornecedor_id:
        return JsonResponse({"produtos": []})

    preco_unitario_subquery = (
        ItemEntrada.objects.filter(
            produto_id=OuterRef("pk"),
            entrada__fornecedor_id=fornecedor_id,
        )
        .order_by("-entrada__data_entrada", "-id")
        .values("preco_unitario")[:1]
    )

    produtos = Produto.objects.filter(
        Q(fornecedores__id=fornecedor_id)
        | Q(itementrada__entrada__fornecedor_id=fornecedor_id)
    ).annotate(
        preco_unitario=Subquery(
            preco_unitario_subquery,
            output_field=DecimalField(max_digits=10, decimal_places=2),
        )
    ).distinct().order_by("nome")
    payload = [
        {
            "id": p.id,
            "nome": p.nome,
            "unidade_medida": p.unidade_medida,
            "preco_unitario": str(p.preco_unitario) if p.preco_unitario is not None else "",
        }
        for p in produtos
    ]
    return JsonResponse({"produtos": payload})


@login_required
def licitacoes_por_fornecedor(request: HttpRequest) -> JsonResponse:
    fornecedor_id = request.GET.get("fornecedor_id")
    if not fornecedor_id:
        return JsonResponse({"licitacoes": []})

    entradas_qs = (
        Entrada.objects
        .filter(fornecedor_id=fornecedor_id)
        .exclude(licitacao="")
        .values_list("licitacao", flat=True)
        .distinct()
    )
    pedidos_qs = (
        Pedido.objects
        .filter(fornecedor_id=fornecedor_id)
        .exclude(licitacao="")
        .values_list("licitacao", flat=True)
        .distinct()
    )

    licitacoes = sorted(
        set(entradas_qs) | set(pedidos_qs),
        key=lambda v: v,
    )
    return JsonResponse({"licitacoes": licitacoes})


@login_required
def setores_por_unidade(request: HttpRequest) -> JsonResponse:
    unidade_id = request.GET.get("unidade_id")
    if not unidade_id:
        return JsonResponse({"setores": []})

    setores = Setor.objects.filter(unidade_id=unidade_id).order_by("nome")
    payload = [{"id": s.id, "nome": s.nome} for s in setores]
    return JsonResponse({"setores": payload})
