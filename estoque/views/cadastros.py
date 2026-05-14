from django.http import HttpRequest, HttpResponse
from ._base import (
    render, redirect, get_object_or_404,
    messages, ProtectedError,
    login_required, _tem_papel,
    Unidade, Setor, UnidadeForm, SetorForm,
)


@login_required
def unidade_list(request: HttpRequest) -> HttpResponse:
    unidades = Unidade.objects.all().order_by("nome")
    return render(request, "estoque/unidade_list.html", {"unidades": unidades})


@_tem_papel("Almoxarife", "Administrador")
def unidade_create(request: HttpRequest) -> HttpResponse:
    form = UnidadeForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Unidade cadastrada com sucesso!")
        return redirect("unidade_list")
    return render(
        request, "estoque/unidade_form.html", {"form": form, "title": "Nova Unidade"}
    )


@_tem_papel("Almoxarife", "Administrador")
def unidade_update(request: HttpRequest, pk: int) -> HttpResponse:
    unidade = get_object_or_404(Unidade, pk=pk)
    form = UnidadeForm(request.POST or None, instance=unidade)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Unidade atualizada com sucesso!")
        return redirect("unidade_list")
    return render(
        request,
        "estoque/unidade_form.html",
        {"form": form, "title": "Editar Unidade", "unidade": unidade},
    )


@_tem_papel("Almoxarife", "Administrador")
def unidade_delete(request: HttpRequest, pk: int) -> HttpResponse:
    unidade = get_object_or_404(Unidade, pk=pk)
    if request.method == "POST":
        try:
            unidade.delete()
            messages.success(request, "Unidade excluída com sucesso!")
        except ProtectedError:
            messages.error(
                request,
                "Não foi possível excluir a unidade porque ela está vinculada a entradas, pedidos ou setores em uso.",
            )
    return redirect("unidade_list")


@login_required
def setor_list(request: HttpRequest) -> HttpResponse:
    setores = (
        Setor.objects.select_related("unidade").all().order_by("unidade__nome", "nome")
    )
    return render(request, "estoque/setor_list.html", {"setores": setores})


@_tem_papel("Almoxarife", "Administrador")
def setor_create(request: HttpRequest) -> HttpResponse:
    form = SetorForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Setor cadastrado com sucesso!")
        return redirect("setor_list")
    return render(
        request, "estoque/setor_form.html", {"form": form, "title": "Novo Setor"}
    )


@_tem_papel("Almoxarife", "Administrador")
def setor_update(request: HttpRequest, pk: int) -> HttpResponse:
    setor = get_object_or_404(Setor, pk=pk)
    form = SetorForm(request.POST or None, instance=setor)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Setor atualizado com sucesso!")
        return redirect("setor_list")
    return render(
        request,
        "estoque/setor_form.html",
        {"form": form, "title": "Editar Setor", "setor": setor},
    )


@_tem_papel("Almoxarife", "Administrador")
def setor_delete(request: HttpRequest, pk: int) -> HttpResponse:
    setor = get_object_or_404(Setor, pk=pk)
    if request.method == "POST":
        try:
            setor.delete()
            messages.success(request, "Setor excluído com sucesso!")
        except ProtectedError:
            messages.error(
                request,
                "Não foi possível excluir o setor porque ele está vinculado a entradas ou pedidos.",
            )
    return redirect("setor_list")
