from django.db import transaction
from django.http import HttpRequest, HttpResponse

from ._base import (
    render, redirect, get_object_or_404,
    messages,
    login_required, _tem_papel,
    Entrada, EntradaForm, ItemEntradaFormSet,
)

@login_required
def entrada_list(request: HttpRequest) -> HttpResponse:
    entradas = (
        Entrada.objects.select_related("fornecedor", "unidade", "setor", "criado_por")
        .all()
        .order_by("-data_entrada", "-id")
    )
    return render(request, "estoque/entrada_list.html", {"entradas": entradas})


@_tem_papel("Almoxarife", "Administrador")
def entrada_create(request: HttpRequest) -> HttpResponse:
    entrada_form = EntradaForm(request.POST or None)
    formset = ItemEntradaFormSet(request.POST or None)
    if request.method == "POST":
        if entrada_form.is_valid() and formset.is_valid():
            with transaction.atomic():
                entrada = entrada_form.save(commit=False)
                entrada.criado_por = request.user
                entrada.save()
                formset.instance = entrada
                formset.save()
            messages.success(request, "Entrada de estoque registrada com sucesso!")
            return redirect("entrada_list")
    return render(
        request,
        "estoque/entrada_form.html",
        {"entrada_form": entrada_form, "formset": formset},
    )


@_tem_papel("Almoxarife", "Administrador")
def entrada_update(request: HttpRequest, pk: int) -> HttpResponse:
    entrada = get_object_or_404(Entrada, pk=pk)
    form = EntradaForm(request.POST or None, instance=entrada)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Entrada atualizada com sucesso!")
        return redirect("entrada_list")
    return render(
        request,
        "estoque/entrada_form.html",
        {
            "entrada_form": form,
            "formset": None,
            "is_edit": True,
            "entrada": entrada,
        },
    )


@_tem_papel("Almoxarife", "Administrador")
def entrada_delete(request: HttpRequest, pk: int) -> HttpResponse:
    entrada = get_object_or_404(Entrada, pk=pk)
    if request.method == "POST":
        with transaction.atomic():
            for item in entrada.itens.select_related("produto"):
                produto = item.produto
                produto.estoque_atual -= item.quantidade
                produto.save()
            entrada.delete()
        messages.success(request, "Entrada excluída e estoque estornado com sucesso!")
    return redirect("entrada_list")
