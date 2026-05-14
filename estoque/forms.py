from typing import Any

from django import forms
from django.contrib.auth.models import User
from .models import (
    Produto,
    Fornecedor,
    Entrada,
    ItemEntrada,
    Pedido,
    ItemPedido,
    Categoria,
    PerfilUsuario,
    Unidade,
    Setor,
)


class _DynamicSetorFilterMixin:
    unidade_field: str
    setor_field: str = "setor"

    def _init_dynamic_setor_filter(self, unidade_field_name: str, setor_field_name: str = "setor") -> None:
        unidade_queryset = Unidade.objects.order_by("nome")
        self.fields[unidade_field_name].queryset = unidade_queryset  # type: ignore[attr-defined]
        self.fields[setor_field_name].queryset = Setor.objects.none()  # type: ignore[attr-defined]

        unidade_id: Any = None
        if self.is_bound:  # type: ignore[attr-defined]
            unidade_id = self.data.get(unidade_field_name)  # type: ignore[attr-defined]
        elif self.instance and self.instance.pk:  # type: ignore[attr-defined]
            unidade_id = getattr(self.instance, f"{unidade_field_name}_id", None)  # type: ignore[attr-defined]

        if unidade_id:
            self.fields[setor_field_name].queryset = Setor.objects.filter(  # type: ignore[attr-defined]
                unidade_id=unidade_id
            ).order_by("nome")


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ["nome"]


class FornecedorForm(forms.ModelForm):
    class Meta:
        model = Fornecedor
        fields = ["nome_fantasia", "razao_social", "cnpj", "contato", "telefone"]


class UnidadeForm(forms.ModelForm):
    class Meta:
        model = Unidade
        fields = ["nome", "representante", "cargo_representante"]


class SetorForm(forms.ModelForm):
    class Meta:
        model = Setor
        fields = ["unidade", "nome", "representante", "cargo_representante"]


class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = [
            "nome",
            "categoria",
            "fornecedores",
            "unidade_medida",
            "estoque_minimo",
        ]
        widgets = {
            "fornecedores": forms.SelectMultiple(attrs={"size": 6}),
        }


class EntradaForm(_DynamicSetorFilterMixin, forms.ModelForm):
    class Meta:
        model = Entrada
        fields = [
            "numero_nota",
            "data_entrada",
            "numero_pedido",
            "fornecedor",
            "unidade",
            "setor",
            "licitacao",
            "lote",
            "compra_direta",
            "programa",
            "numero_empenho",
            "observacoes",
        ]
        widgets = {
            "data_entrada": forms.DateInput(attrs={"type": "date"}),
            "observacoes": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._init_dynamic_setor_filter("unidade")


class ItemEntradaForm(forms.ModelForm):
    class Meta:
        model = ItemEntrada
        fields = ["produto", "quantidade", "preco_unitario", "licitacao_restante"]


class PedidoForm(_DynamicSetorFilterMixin, forms.ModelForm):
    class Meta:
        model = Pedido
        fields = [
            "secretaria",
            "setor",
            "endereco_entrega",
            "programa",
            "fornecedor",
            "licitacao",
            "numero_empenho",
            "compra_direta",
            "observacoes",
        ]
        widgets = {
            "observacoes": forms.Textarea(attrs={"rows": 2}),
        }

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._init_dynamic_setor_filter("secretaria")


class ItemPedidoForm(forms.ModelForm):
    class Meta:
        model = ItemPedido
        fields = [
            "produto",
            "quantidade",
            "quantidade_licitada",
            "quantidade_atendida",
            "preco_unitario",
        ]


class AnexoEmpenhoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ["empenho_anexo"]


class PerfilUsuarioForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]


class PerfilTemaForm(forms.ModelForm):
    class Meta:
        model = PerfilUsuario
        fields = ["tema_ui"]


ItemEntradaFormSet = forms.inlineformset_factory(
    Entrada, ItemEntrada, form=ItemEntradaForm, extra=1, can_delete=True
)
ItemPedidoFormSet = forms.inlineformset_factory(
    Pedido, ItemPedido, form=ItemPedidoForm, extra=1, can_delete=True
)
