from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from .models import Pedido3D, PedidoRouter, PedidoCAD
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError


# ==========================================
# FORMULÁRIO DE REGISTRO DE USUÁRIO
# ==========================================
class RegistroUsuarioForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30, required=True, label='Nome',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Seu nome'}),
    )
    last_name = forms.CharField(
        max_length=30, required=True, label='Sobrenome',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Seu sobrenome'}),
    )
    email = forms.EmailField(
        required=True, label='E-mail',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'seu@email.com'}),
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome de utilizador'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Crie uma senha'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Repita a senha'})


# ==========================================
# FORMULÁRIO DE PERFIL DO USUÁRIO
# ==========================================
class PerfilUsuarioForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        labels = {
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'email': 'E-mail',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }


# ==========================================
# FORMULÁRIO DE GESTÃO DE USUÁRIO (ADMIN)
# ==========================================
class GestaoUsuarioForm(forms.ModelForm):
    GRUPOS_FIXOS = ['Setor 3D', 'Setor Router', 'Setor CAD']

    grupos = forms.ModelMultipleChoiceField(
        queryset=Group.objects.none(),  # Será preenchido no __init__
        required=False,
        label='Setores',
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'is_active', 'is_staff'] # <-- Adicione o is_staff aqui
        labels = {
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'email': 'E-mail',
            'is_active': 'Conta ativa (Permite login)',
            'is_staff': 'É Gestor? (Permite editar/excluir pedidos)', # <-- Nova label
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'form-check-input'}), # <-- Novo widget
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Garantir que os 3 grupos fixos existam e filtrar apenas eles
        for nome in self.GRUPOS_FIXOS:
            Group.objects.get_or_create(name=nome)
        self.fields['grupos'].queryset = Group.objects.filter(name__in=self.GRUPOS_FIXOS).order_by('name')
        if self.instance.pk:
            self.fields['grupos'].initial = self.instance.groups.filter(name__in=self.GRUPOS_FIXOS)

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            user.groups.set(self.cleaned_data['grupos'])
        return user

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


class LoginFormCustomizado(AuthenticationForm):
    """
    Formulário de login customizado para dar mensagens amigáveis
    quando o usuário acertar a senha mas a conta estiver aguardando aprovação.
    """
    def confirm_login_allowed(self, user):
        # Esta função do Django só é chamada SE a senha digitada estiver CORRETA.
        if not user.is_active:
            raise ValidationError(
                "A sua conta já foi criada, mas ainda está aguardando a aprovação do gestor. Por favor, aguarde.",
                code='inactive',
            )