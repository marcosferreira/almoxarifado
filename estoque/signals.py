from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import ItemEntrada, Pedido, PerfilUsuario


@receiver(post_save, sender=User)
def garantir_perfil_usuario(sender, instance, **kwargs):
    PerfilUsuario.objects.get_or_create(user=instance)


@receiver(post_save, sender=ItemEntrada)
def atualizar_estoque_entrada(sender, instance, created, **kwargs):
    if created:
        produto = instance.produto
        produto.estoque_atual += instance.quantidade
        produto.save()


@receiver(pre_save, sender=Pedido)
def gerenciar_fluxo_estoque(sender, instance, **kwargs):
    if instance.pk:
        old_instance = Pedido.objects.get(pk=instance.pk)

        # Se mudou para RESERVADO
        if old_instance.status != "RESERVADO" and instance.status == "RESERVADO":
            for item in instance.itens.all():
                produto = item.produto
                if produto.estoque_disponivel < item.quantidade:
                    raise ValueError(f"Estoque insuficiente para {produto.nome}")
                produto.estoque_reservado += item.quantidade
                produto.save()

        # Se mudou para ENTREGUE
        elif old_instance.status != "ENTREGUE" and instance.status == "ENTREGUE":
            # Se estava RESERVADO antes, remove da reserva e baixa do atual
            if old_instance.status == "RESERVADO" or old_instance.status == "EMPENHADO":
                for item in instance.itens.all():
                    produto = item.produto
                    produto.estoque_atual -= item.quantidade
                    produto.estoque_reservado -= item.quantidade
                    produto.save()
            else:
                # Se não estava reservado (fluxo direto ou pulou etapa), baixa apenas do atual
                for item in instance.itens.all():
                    produto = item.produto
                    produto.estoque_atual -= item.quantidade
                    produto.save()

        # Se foi CANCELADO e estava RESERVADO
        elif (
            old_instance.status in ["RESERVADO", "EMPENHADO"]
            and instance.status == "CANCELADO"
        ):
            for item in instance.itens.all():
                produto = item.produto
                produto.estoque_reservado -= item.quantidade
                produto.save()
