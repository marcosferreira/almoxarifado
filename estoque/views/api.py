from typing import Any

from django.db.models import Q
from django.http import HttpRequest, JsonResponse
from ._base import (
    login_required,
    Produto, Setor, Entrada, Pedido,
)


@login_required
def produtos_por_fornecedor(request: HttpRequest) -> JsonResponse:
    fornecedor_id = request.GET.get("fornecedor_id")
    if not fornecedor_id:
        return JsonResponse({"produtos": []})

    produtos = Produto.objects.filter(
        Q(fornecedores__id=fornecedor_id)
        | Q(itementrada__entrada__fornecedor_id=fornecedor_id)
    ).distinct().order_by("nome")
    payload = [
        {"id": p.id, "nome": p.nome, "unidade_medida": p.unidade_medida}
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
