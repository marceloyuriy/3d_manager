from django import forms
from .models import Pedido3D, PedidoRouter, PedidoCAD

# ==========================================
# FORMULÁRIOS DA IMPRESSORA 3D
# ==========================================
class NovaImpressao3DForm(forms.ModelForm):
    class Meta:
        model = Pedido3D
        fields = ['nome_peca', 'prazo', 'arquivo_impressao', 'link_fusion']
        widgets = {
            'nome_peca': forms.TextInput(attrs={'class': 'form-control'}),
            'prazo': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'type': 'date'}),
            'arquivo_impressao': forms.FileInput(attrs={'class': 'form-control'}),
            'link_fusion': forms.URLInput(attrs={'class': 'form-control'}),
        }

class EdicaoGestor3DForm(forms.ModelForm):
    class Meta:
        model = Pedido3D
        fields = ['solicitante', 'nome_peca', 'prazo', 'previsao_conclusao', 'prioridade', 'status', 'arquivo_impressao', 'link_fusion']
        widgets = {
            'solicitante': forms.TextInput(attrs={'class': 'form-control'}),
            'nome_peca': forms.TextInput(attrs={'class': 'form-control'}),
            'prazo': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'type': 'date', 'readonly': True}),
            'previsao_conclusao': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'type': 'date'}),
            'prioridade': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'arquivo_impressao': forms.FileInput(attrs={'class': 'form-control'}),
            'link_fusion': forms.URLInput(attrs={'class': 'form-control'}),
        }

# ==========================================
# FORMULÁRIOS DA ROUTER CNC
# ==========================================
class NovoRouterForm(forms.ModelForm):
    class Meta:
        model = PedidoRouter
        fields = ['nome_peca', 'prazo', 'arquivo_impressao', 'link_fusion']
        widgets = {
            'nome_peca': forms.TextInput(attrs={'class': 'form-control'}),
            'prazo': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'type': 'date'}),
            'arquivo_impressao': forms.FileInput(attrs={'class': 'form-control'}),
            'link_fusion': forms.URLInput(attrs={'class': 'form-control'}),
        }

class EdicaoGestorRouterForm(forms.ModelForm):
    class Meta:
        model = PedidoRouter
        fields = ['solicitante', 'nome_peca', 'prazo', 'previsao_conclusao', 'prioridade', 'status', 'arquivo_impressao', 'link_fusion']
        widgets = {
            'solicitante': forms.TextInput(attrs={'class': 'form-control'}),
            'nome_peca': forms.TextInput(attrs={'class': 'form-control'}),
            'prazo': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'type': 'date', 'readonly': True}),
            'previsao_conclusao': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'type': 'date'}),
            'prioridade': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'arquivo_impressao': forms.FileInput(attrs={'class': 'form-control'}),
            'link_fusion': forms.URLInput(attrs={'class': 'form-control'}),
        }

# ==========================================
# FORMULÁRIOS DO CAD
# ==========================================
class NovoCADForm(forms.ModelForm):
    class Meta:
        model = PedidoCAD
        fields = ['nome_peca', 'prazo', 'arquivo_impressao', 'link_fusion']
        widgets = {
            'nome_peca': forms.TextInput(attrs={'class': 'form-control'}),
            'prazo': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'type': 'date'}),
            'arquivo_impressao': forms.FileInput(attrs={'class': 'form-control'}),
            'link_fusion': forms.URLInput(attrs={'class': 'form-control'}),
        }

class EdicaoGestorCADForm(forms.ModelForm):
    class Meta:
        model = PedidoCAD
        fields = ['solicitante', 'nome_peca', 'prazo', 'previsao_conclusao', 'prioridade', 'status', 'arquivo_impressao', 'link_fusion']
        widgets = {
            'solicitante': forms.TextInput(attrs={'class': 'form-control'}),
            'nome_peca': forms.TextInput(attrs={'class': 'form-control'}),
            'prazo': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'type': 'date', 'readonly': True}),
            'previsao_conclusao': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'type': 'date'}),
            'prioridade': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'arquivo_impressao': forms.FileInput(attrs={'class': 'form-control'}),
            'link_fusion': forms.URLInput(attrs={'class': 'form-control'}),
        }