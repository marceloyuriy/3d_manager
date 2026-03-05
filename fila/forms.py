from django import forms
from .models import ItemFila


# ---------------------------------------------------------
# FORMULÁRIO 1: Para Usuários Comuns (Novo Pedido)
# ---------------------------------------------------------
class NovaImpressaoForm(forms.ModelForm):
    class Meta:
        model = ItemFila
        # Removemos 'prioridade' e 'status' desta lista
        fields = ['solicitante', 'nome_peca', 'prazo', 'arquivo_impressao', 'link_fusion']

        widgets = {
            'solicitante': forms.TextInput(attrs={'class': 'form-control'}),
            'nome_peca': forms.TextInput(attrs={'class': 'form-control'}),
            'prazo': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'arquivo_impressao': forms.FileInput(attrs={'class': 'form-control'}),
            'link_fusion': forms.URLInput(attrs={'class': 'form-control'}),
        }


# ---------------------------------------------------------
# FORMULÁRIO 2: Para Gestores (Edição de Pedido)
# ---------------------------------------------------------
class EdicaoGestorForm(forms.ModelForm):
    class Meta:
        model = ItemFila
        # Incluímos 'prioridade' e 'status' para o gestor poder alterar
        fields = ['solicitante', 'nome_peca', 'prazo', 'prioridade', 'status', 'arquivo_impressao', 'link_fusion']

        widgets = {
            'solicitante': forms.TextInput(attrs={'class': 'form-control'}),
            'nome_peca': forms.TextInput(attrs={'class': 'form-control'}),
            'prazo': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            # Adicionamos o visual (Bootstrap) para as caixas de seleção
            'prioridade': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'arquivo_impressao': forms.FileInput(attrs={'class': 'form-control'}),
            'link_fusion': forms.URLInput(attrs={'class': 'form-control'}),
        }