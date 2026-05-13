from ._base import (
    render, redirect, get_object_or_404,
    messages, ProtectedError,
    login_required, _tem_papel,
    Fornecedor, FornecedorForm,
)


@login_required
def fornecedor_list(request):
    fornecedores = Fornecedor.objects.all()
    return render(
        request, "estoque/fornecedor_list.html", {"fornecedores": fornecedores}
    )


@_tem_papel("Almoxarife", "Comprador", "Administrador")
def fornecedor_create(request):
    form = FornecedorForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Fornecedor cadastrado com sucesso!")
        return redirect("fornecedor_list")
    return render(
        request,
        "estoque/fornecedor_form.html",
        {"form": form, "title": "Novo Fornecedor"},
    )


@_tem_papel("Almoxarife", "Comprador", "Administrador")
def fornecedor_update(request, pk):
    fornecedor = get_object_or_404(Fornecedor, pk=pk)
    form = FornecedorForm(request.POST or None, instance=fornecedor)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Fornecedor atualizado com sucesso!")
        return redirect("fornecedor_list")
    return render(
        request,
        "estoque/fornecedor_form.html",
        {"form": form, "title": "Editar Fornecedor"},
    )


@_tem_papel("Almoxarife", "Administrador")
def fornecedor_delete(request, pk):
    fornecedor = get_object_or_404(Fornecedor, pk=pk)
    if request.method == "POST":
        try:
            fornecedor.delete()
            messages.success(request, "Fornecedor excluído com sucesso!")
        except ProtectedError:
            messages.error(
                request,
                "Não foi possível excluir o fornecedor porque ele está vinculado a entradas ou pedidos.",
            )
    return redirect("fornecedor_list")
