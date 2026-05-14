from django.http import HttpRequest, HttpResponse
from ._base import (
    render, redirect,
    messages,
    login_required,
    PerfilUsuario, PerfilUsuarioForm, PerfilTemaForm,
    PasswordChangeForm, update_session_auth_hash,
)


@login_required
def profile(request: HttpRequest) -> HttpResponse:
    perfil_usuario, _ = PerfilUsuario.objects.get_or_create(user=request.user)
    perfil_form = PerfilUsuarioForm(request.POST or None, instance=request.user)
    tema_form = PerfilTemaForm(request.POST or None, instance=perfil_usuario)
    senha_form = PasswordChangeForm(user=request.user, data=request.POST or None)

    if request.method == "POST":
        acao = request.POST.get("acao")
        if acao == "dados":
            if perfil_form.is_valid() and tema_form.is_valid():
                perfil_form.save()
                tema_form.save()
                messages.success(request, "Perfil atualizado com sucesso.")
                return redirect("profile")
            messages.error(request, "Revise os dados do perfil e tente novamente.")

        elif acao == "senha":
            if senha_form.is_valid():
                user = senha_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, "Senha alterada com sucesso.")
                return redirect("profile")
            messages.error(request, "Não foi possível alterar a senha.")

    return render(
        request,
        "registration/profile.html",
        {
            "perfil_form": perfil_form,
            "tema_form": tema_form,
            "senha_form": senha_form,
        },
    )
