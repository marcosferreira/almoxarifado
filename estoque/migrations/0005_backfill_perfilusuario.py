from django.conf import settings
from django.db import migrations


def criar_perfis_faltantes(apps, schema_editor):
    perfil_model = apps.get_model("estoque", "PerfilUsuario")
    user_model = apps.get_model(*settings.AUTH_USER_MODEL.split("."))

    for user in user_model.objects.all().only("id"):
        perfil_model.objects.get_or_create(user_id=user.id)


class Migration(migrations.Migration):
    dependencies = [
        ("estoque", "0004_perfilusuario"),
    ]

    operations = [
        migrations.RunPython(criar_perfis_faltantes, migrations.RunPython.noop),
    ]
