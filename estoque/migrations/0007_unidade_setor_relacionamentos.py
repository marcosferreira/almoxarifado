from django.db import migrations, models
import django.db.models.deletion


def _normalizar_texto(valor):
    if not valor:
        return ""
    return " ".join(str(valor).strip().split())


def popular_unidades_setores(apps, schema_editor):
    Unidade = apps.get_model("estoque", "Unidade")
    Setor = apps.get_model("estoque", "Setor")
    Entrada = apps.get_model("estoque", "Entrada")
    Pedido = apps.get_model("estoque", "Pedido")

    unidades_cache = {}
    setores_cache = {}

    def obter_unidade(nome):
        nome_limpo = _normalizar_texto(nome)
        if not nome_limpo:
            return None
        if nome_limpo in unidades_cache:
            return unidades_cache[nome_limpo]
        unidade, _ = Unidade.objects.get_or_create(nome=nome_limpo)
        unidades_cache[nome_limpo] = unidade
        return unidade

    def obter_setor(unidade, nome):
        nome_limpo = _normalizar_texto(nome)
        if not unidade or not nome_limpo:
            return None
        chave = (unidade.id, nome_limpo)
        if chave in setores_cache:
            return setores_cache[chave]
        setor, _ = Setor.objects.get_or_create(unidade=unidade, nome=nome_limpo)
        setores_cache[chave] = setor
        return setor

    for entrada in Entrada.objects.all().iterator():
        unidade = obter_unidade(getattr(entrada, "unidade", ""))
        setor = obter_setor(unidade, getattr(entrada, "setor", ""))
        entrada.unidade_fk_id = unidade.id if unidade else None
        entrada.setor_fk_id = setor.id if setor else None
        entrada.save(update_fields=["unidade_fk", "setor_fk"])

    for pedido in Pedido.objects.all().iterator():
        unidade = obter_unidade(getattr(pedido, "secretaria", ""))
        setor = obter_setor(unidade, getattr(pedido, "setor", ""))
        pedido.secretaria_fk_id = unidade.id if unidade else None
        pedido.setor_fk_id = setor.id if setor else None
        pedido.save(update_fields=["secretaria_fk", "setor_fk"])


class Migration(migrations.Migration):
    dependencies = [
        ("estoque", "0006_produto_fornecedores"),
    ]

    operations = [
        migrations.CreateModel(
            name="Unidade",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "nome",
                    models.CharField(
                        max_length=200, unique=True, verbose_name="Unidade/Secretaria"
                    ),
                ),
            ],
            options={
                "verbose_name": "Unidade",
                "verbose_name_plural": "Unidades",
            },
        ),
        migrations.CreateModel(
            name="Setor",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nome", models.CharField(max_length=200)),
                (
                    "unidade",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="setores",
                        to="estoque.unidade",
                        verbose_name="Unidade",
                    ),
                ),
            ],
            options={
                "verbose_name": "Setor",
                "verbose_name_plural": "Setores",
                "constraints": [
                    models.UniqueConstraint(
                        fields=("unidade", "nome"), name="unique_setor_por_unidade"
                    )
                ],
            },
        ),
        migrations.AddField(
            model_name="entrada",
            name="setor_fk",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="entradas",
                to="estoque.setor",
                verbose_name="Setor",
            ),
        ),
        migrations.AddField(
            model_name="entrada",
            name="unidade_fk",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="entradas",
                to="estoque.unidade",
                verbose_name="Unidade",
            ),
        ),
        migrations.AddField(
            model_name="pedido",
            name="secretaria_fk",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="pedidos",
                to="estoque.unidade",
                verbose_name="Unidade/Secretaria",
            ),
        ),
        migrations.AddField(
            model_name="pedido",
            name="setor_fk",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="pedidos",
                to="estoque.setor",
                verbose_name="Setor/Departamento",
            ),
        ),
        migrations.RunPython(popular_unidades_setores, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name="entrada",
            name="unidade",
        ),
        migrations.RemoveField(
            model_name="entrada",
            name="setor",
        ),
        migrations.RemoveField(
            model_name="pedido",
            name="secretaria",
        ),
        migrations.RemoveField(
            model_name="pedido",
            name="setor",
        ),
        migrations.RenameField(
            model_name="entrada",
            old_name="unidade_fk",
            new_name="unidade",
        ),
        migrations.RenameField(
            model_name="entrada",
            old_name="setor_fk",
            new_name="setor",
        ),
        migrations.RenameField(
            model_name="pedido",
            old_name="secretaria_fk",
            new_name="secretaria",
        ),
        migrations.RenameField(
            model_name="pedido",
            old_name="setor_fk",
            new_name="setor",
        ),
    ]
