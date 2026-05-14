from typing import Any

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db import transaction
from .models import ItemEntrada, Pedido, PerfilUsuario, Produto


@receiver(post_save, sender=User)
def garantir_perfil_usuario(sender: type[User], instance: User, **kwargs: Any) -> None:
    PerfilUsuario.objects.get_or_create(user=instance)


@receiver(post_save, sender=ItemEntrada)
def atualizar_estoque_entrada(sender: type[ItemEntrada], instance: ItemEntrada, created: bool, **kwargs: Any) -> None:
    if created:
        produto = instance.produto
        produto.estoque_atual += instance.quantidade
        produto.save()


@receiver(pre_save, sender=Pedido)
def gerenciar_fluxo_estoque(sender: type[Pedido], instance: Pedido, **kwargs: Any) -> None:
    if instance.pk:
        old_instance = Pedido.objects.get(pk=instance.pk)

        if old_instance.status != "RESERVADO" and instance.status == "RESERVADO":
            with transaction.atomic():
                for item in instance.itens.all():
                    produto = Produto.objects.select_for_update().get(pk=item.produto_id)
                    if produto.estoque_disponivel < item.quantidade:
                        raise ValueError(f"Estoque insuficiente para {produto.nome}")
                    produto.estoque_reservado += item.quantidade
                    produto.save()

        elif old_instance.status != "ENTREGUE" and instance.status == "ENTREGUE":
            if old_instance.status in ("RESERVADO", "EMPENHADO"):
                with transaction.atomic():
                    for item in instance.itens.all():
                        produto = Produto.objects.select_for_update().get(pk=item.produto_id)
                        produto.estoque_atual -= item.quantidade
                        produto.estoque_reservado -= item.quantidade
                        produto.save()
            else:
                with transaction.atomic():
                    for item in instance.itens.all():
                        produto = Produto.objects.select_for_update().get(pk=item.produto_id)
                        produto.estoque_atual -= item.quantidade
                        produto.save()

        elif (
            old_instance.status in ("RESERVADO", "EMPENHADO")
            and instance.status == "CANCELADO"
        ):
            with transaction.atomic():
                for item in instance.itens.all():
                    produto = Produto.objects.select_for_update().get(pk=item.produto_id)
                    produto.estoque_reservado -= item.quantidade
                    produto.save()

            if old_instance.status == "EMPENHADO" and instance.empenho_anexo:
                instance.empenho_anexo.delete(save=False)
