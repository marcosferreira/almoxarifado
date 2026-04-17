from django.db import migrations, models


def popular_produto_fornecedores(apps, schema_editor):
    Produto = apps.get_model("estoque", "Produto")

    for produto in Produto.objects.all():
        fornecedor_ids = set(
            produto.itementrada_set.values_list("entrada__fornecedor_id", flat=True)
        )
        fornecedor_ids.update(
            produto.itempedido_set.values_list("pedido__fornecedor_id", flat=True)
        )
        fornecedor_ids.discard(None)
        if fornecedor_ids:
            produto.fornecedores.add(*fornecedor_ids)


class Migration(migrations.Migration):
    dependencies = [
        ("estoque", "0005_backfill_perfilusuario"),
    ]

    operations = [
        migrations.AddField(
            model_name="produto",
            name="fornecedores",
            field=models.ManyToManyField(
                blank=True,
                related_name="produtos",
                to="estoque.fornecedor",
                verbose_name="Fornecedores",
            ),
        ),
        migrations.RunPython(popular_produto_fornecedores, migrations.RunPython.noop),
    ]
