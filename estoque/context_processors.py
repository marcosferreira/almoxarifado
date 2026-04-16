from .models import PerfilUsuario


def tema_ui_context(request):
    tema = "classic"
    if request.user.is_authenticated:
        try:
            perfil = request.user.perfil_usuario
        except PerfilUsuario.DoesNotExist:
            perfil = PerfilUsuario.objects.create(user=request.user)
        if perfil.tema_ui:
            tema = perfil.tema_ui
    return {"current_theme": tema}
