from django import forms
from .models import ItemFila


class NovaImpressaoForm(forms.ModelForm):
    class Meta:
        model = ItemFila
        # O Operador NÃO vê a 'previsao_conclusao', 'prioridade' e 'status'
        fields = ['solicitante', 'nome_peca', 'prazo', 'arquivo_impressao', 'link_fusion']

        widgets = {
            'solicitante': forms.TextInput(attrs={'class': 'form-control'}),
            'nome_peca': forms.TextInput(attrs={'class': 'form-control'}),
            # format='%Y-%m-%d' garante que a data seja salva e lida corretamente pelo navegador
            'prazo': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'type': 'date'}),
            'arquivo_impressao': forms.FileInput(attrs={'class': 'form-control'}),
            'link_fusion': forms.URLInput(attrs={'class': 'form-control'}),
        }


class EdicaoGestorForm(forms.ModelForm):
    class Meta:
        model = ItemFila
        # Incluímos 'previsao_conclusao', 'prioridade' e 'status' para o gestor
        fields = ['solicitante', 'nome_peca', 'prazo', 'previsao_conclusao', 'prioridade', 'status',
                  'arquivo_impressao', 'link_fusion']

        widgets = {
            'solicitante': forms.TextInput(attrs={'class': 'form-control'}),
            'nome_peca': forms.TextInput(attrs={'class': 'form-control'}),

            # format resolve o bug da data sumir. 'readonly': True trava o campo para o Gestor não alterar o pedido original.
            'prazo': forms.DateInput(format='%Y-%m-%d',
                                     attrs={'class': 'form-control', 'type': 'date', 'readonly': True}),

            # Novo campo para o Gestor preencher a previsão real de entrega
            'previsao_conclusao': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'type': 'date'}),

            'prioridade': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'arquivo_impressao': forms.FileInput(attrs={'class': 'form-control'}),
            'link_fusion': forms.URLInput(attrs={'class': 'form-control'}),
        }