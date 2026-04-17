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


class EntradaForm(forms.ModelForm):
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["unidade"].queryset = Unidade.objects.order_by("nome")
        self.fields["setor"].queryset = Setor.objects.none()

        unidade_id = None
        if self.is_bound:
            unidade_id = self.data.get("unidade")
        elif self.instance and self.instance.pk and self.instance.unidade_id:
            unidade_id = self.instance.unidade_id

        if unidade_id:
            self.fields["setor"].queryset = Setor.objects.filter(
                unidade_id=unidade_id
            ).order_by("nome")


class ItemEntradaForm(forms.ModelForm):
    class Meta:
        model = ItemEntrada
        fields = ["produto", "quantidade", "preco_unitario", "licitacao_restante"]


class PedidoForm(forms.ModelForm):
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["secretaria"].queryset = Unidade.objects.order_by("nome")
        self.fields["setor"].queryset = Setor.objects.none()

        unidade_id = None
        if self.is_bound:
            unidade_id = self.data.get("secretaria")
        elif self.instance and self.instance.pk and self.instance.secretaria_id:
            unidade_id = self.instance.secretaria_id

        if unidade_id:
            self.fields["setor"].queryset = Setor.objects.filter(
                unidade_id=unidade_id
            ).order_by("nome")


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
