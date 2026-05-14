from decimal import Decimal
from typing import Optional

from django.contrib.auth.models import User, Group

from ..models import (
    Produto,
    Categoria,
    Unidade,
    Setor,
)


def _criar_usuario(username: str = "teste", password: str = "senha12345", grupo: Optional[str] = None) -> User:
    user = User.objects.create_user(username=username, password=password)
    if grupo:
        g, _ = Group.objects.get_or_create(name=grupo)
        user.groups.add(g)
    return user


def _criar_produto(
    nome: str = "Caneta",
    estoque: int = 10,
    estoque_min: int = 2,
    reservado: int = 0,
) -> Produto:
    cat, _ = Categoria.objects.get_or_create(nome="Escritório")
    return Produto.objects.create(
        nome=nome,
        categoria=cat,
        unidade_medida="UN",
        estoque_atual=Decimal(str(estoque)),
        estoque_reservado=Decimal(str(reservado)),
        estoque_minimo=Decimal(str(estoque_min)),
    )


def _criar_unidade(nome: str = "Secretaria de Educação") -> Unidade:
    return Unidade.objects.get_or_create(nome=nome)[0]


def _criar_setor(nome: str = "TI", unidade: Optional[Unidade] = None) -> Setor:
    if unidade is None:
        unidade = _criar_unidade()
    return Setor.objects.get_or_create(nome=nome, unidade=unidade)[0]
