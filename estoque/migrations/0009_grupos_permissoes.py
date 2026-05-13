from django.db import migrations


GRUPOS = {
    "Almoxarife": [
        # Produto
        ("estoque", "produto", "view_produto"),
        ("estoque", "produto", "add_produto"),
        ("estoque", "produto", "change_produto"),
        ("estoque", "produto", "delete_produto"),
        # Categoria
        ("estoque", "categoria", "view_categoria"),
        ("estoque", "categoria", "add_categoria"),
        ("estoque", "categoria", "change_categoria"),
        # Fornecedor
        ("estoque", "fornecedor", "view_fornecedor"),
        ("estoque", "fornecedor", "add_fornecedor"),
        ("estoque", "fornecedor", "change_fornecedor"),
        ("estoque", "fornecedor", "delete_fornecedor"),
        # Entrada
        ("estoque", "entrada", "view_entrada"),
        ("estoque", "entrada", "add_entrada"),
        ("estoque", "entrada", "change_entrada"),
        ("estoque", "entrada", "delete_entrada"),
        ("estoque", "itementrada", "view_itementrada"),
        ("estoque", "itementrada", "add_itementrada"),
        ("estoque", "itementrada", "change_itementrada"),
        ("estoque", "itementrada", "delete_itementrada"),
        # Pedido (confirmar entrega)
        ("estoque", "pedido", "view_pedido"),
        ("estoque", "pedido", "change_pedido"),
        ("estoque", "itempedido", "view_itempedido"),
        # Unidade e Setor
        ("estoque", "unidade", "view_unidade"),
        ("estoque", "setor", "view_setor"),
    ],
    "Comprador": [
        # Pedido (criar, empenhar)
        ("estoque", "pedido", "view_pedido"),
        ("estoque", "pedido", "add_pedido"),
        ("estoque", "pedido", "change_pedido"),
        ("estoque", "itempedido", "view_itempedido"),
        ("estoque", "itempedido", "add_itempedido"),
        ("estoque", "itempedido", "change_itempedido"),
        # Produto (consulta)
        ("estoque", "produto", "view_produto"),
        ("estoque", "fornecedor", "view_fornecedor"),
        ("estoque", "unidade", "view_unidade"),
        ("estoque", "setor", "view_setor"),
    ],
    "Solicitante": [
        # Apenas cria e consulta pedidos
        ("estoque", "pedido", "view_pedido"),
        ("estoque", "pedido", "add_pedido"),
        ("estoque", "itempedido", "view_itempedido"),
        ("estoque", "itempedido", "add_itempedido"),
        ("estoque", "produto", "view_produto"),
        ("estoque", "unidade", "view_unidade"),
        ("estoque", "setor", "view_setor"),
    ],
    "Administrador": [],  # superuser; grupos definem apenas via Django admin
}


def criar_grupos(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")
    ContentType = apps.get_model("contenttypes", "ContentType")

    for nome_grupo, permissoes in GRUPOS.items():
        grupo, _ = Group.objects.get_or_create(name=nome_grupo)
        perms = []
        for app_label, model_name, codename in permissoes:
            try:
                ct = ContentType.objects.get(app_label=app_label, model=model_name)
                perm = Permission.objects.get(content_type=ct, codename=codename)
                perms.append(perm)
            except (ContentType.DoesNotExist, Permission.DoesNotExist):
                pass
        grupo.permissions.set(perms)


def remover_grupos(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    for nome_grupo in GRUPOS:
        Group.objects.filter(name=nome_grupo).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("estoque", "0008_setor_cargo_representante_setor_representante_and_more"),
        ("contenttypes", "0002_remove_content_type_name"),
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.RunPython(criar_grupos, remover_grupos),
    ]
