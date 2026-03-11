from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.utils import timezone

from .models import Pedido3D, PedidoRouter, PedidoCAD
from .forms import (NovaImpressao3DForm, EdicaoGestor3DForm,
                    NovoRouterForm, EdicaoGestorRouterForm,
                    NovoCADForm, EdicaoGestorCADForm,
                    RegistroUsuarioForm, PerfilUsuarioForm,
                    GestaoUsuarioForm)

# --- Os 3 grupos fixos do sistema ---
GRUPOS_FIXOS = ['Setor 3D', 'Setor Router', 'Setor CAD']

# --- FUNÇÕES DE SEGURANÇA ---
def pode_adicionar(user, setor):
    """Verifica se o usuário pode adicionar pedidos (Operador do Setor)"""
    if not user.is_authenticated: return False
    if user.is_superuser: return True
    return user.groups.filter(name=f'Setor {setor}').exists()

def pode_gerenciar(user, setor):
    """Verifica se o usuário pode editar/excluir pedidos (Gestor do Setor)"""
    if not user.is_authenticated: return False
    if user.is_superuser: return True
    # Tem que pertencer ao setor E ter a flag de staff (Gestor)
    return user.is_staff and user.groups.filter(name=f'Setor {setor}').exists()


# ==========================================
# VIEWS DO HUB (LISTAGEM)
# ==========================================
@login_required
def lista_3d(request):
    em_producao = Pedido3D.objects.filter(status='I').order_by('prazo')
    fila_espera = Pedido3D.objects.filter(status='F').order_by('prazo')
    pendentes = Pedido3D.objects.filter(status__in=['P', 'E']).order_by('-data_criacao')
    concluidos = Pedido3D.objects.filter(status='C').order_by('-data_conclusao')[:10]

    contexto = {
        'em_producao': em_producao, 'fila_espera': fila_espera,
        'pendentes': pendentes, 'concluidos': concluidos,
        'setor_ativo': '3D',
        'pode_adicionar': pode_adicionar(request.user, '3D'),
        'pode_editar': pode_gerenciar(request.user, '3D'),
    }
    return render(request, 'fila/lista.html', contexto)

@login_required
def lista_router(request):
    em_producao = PedidoRouter.objects.filter(status='I').order_by('prazo')
    fila_espera = PedidoRouter.objects.filter(status='F').order_by('prazo')
    pendentes = PedidoRouter.objects.filter(status__in=['P', 'E']).order_by('-data_criacao')
    concluidos = PedidoRouter.objects.filter(status='C').order_by('-data_conclusao')[:10]

    contexto = {
        'em_producao': em_producao, 'fila_espera': fila_espera,
        'pendentes': pendentes, 'concluidos': concluidos,
        'setor_ativo': 'Router',
        'pode_adicionar': pode_adicionar(request.user, 'Router'),
        'pode_editar': pode_gerenciar(request.user, 'Router'),
    }
    return render(request, 'fila/lista.html', contexto)

@login_required
def lista_cad(request):
    em_producao = PedidoCAD.objects.filter(status='I').order_by('prazo')
    fila_espera = PedidoCAD.objects.filter(status='F').order_by('prazo')
    pendentes = PedidoCAD.objects.filter(status__in=['P', 'E']).order_by('-data_criacao')
    concluidos = PedidoCAD.objects.filter(status='C').order_by('-data_conclusao')[:10]

    contexto = {
        'em_producao': em_producao, 'fila_espera': fila_espera,
        'pendentes': pendentes, 'concluidos': concluidos,
        'setor_ativo': 'CAD',
        'pode_adicionar': pode_adicionar(request.user, 'CAD'),
        'pode_editar': pode_gerenciar(request.user, 'CAD'),
    }
    return render(request, 'fila/lista.html', contexto)


# ==========================================
# VIEWS DA IMPRESSORA 3D
# ==========================================
@login_required
def novo_pedido_3d(request):
    if not pode_adicionar(request.user, '3D'):
        messages.error(request, 'Acesso Negado: Você não pertence ao Setor 3D.')
        return redirect('lista_fila')

    if request.method == 'POST':
        form = NovaImpressao3DForm(request.POST, request.FILES)
        if form.is_valid():
            pedido = form.save(commit=False)
            pedido.solicitante = request.user.username
            pedido.save()
            messages.success(request, 'Pedido 3D adicionado à fila!')
            return redirect('lista_fila')
    else:
        form = NovaImpressao3DForm()
    return render(request, 'fila/form.html', {'form': form, 'titulo': 'Novo Pedido - Impressão 3D'})

@login_required
def editar_pedido_3d(request, id):
    if not pode_gerenciar(request.user, '3D'):
        messages.error(request, 'Acesso Negado: Apenas gestores do Setor 3D podem editar pedidos.')
        return redirect('lista_fila')
    item = get_object_or_404(Pedido3D, id=id)
    if request.method == 'POST':
        form = EdicaoGestor3DForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            item_salvo = form.save(commit=False)
            if item_salvo.status == 'C' and not item_salvo.data_conclusao:
                item_salvo.data_conclusao = timezone.now()
            elif item_salvo.status != 'C':
                item_salvo.data_conclusao = None
            item_salvo.save()
            messages.success(request, f'Pedido "{item_salvo.nome_peca}" atualizado!')
            return redirect('lista_fila')
    else:
        form = EdicaoGestor3DForm(instance=item)
    return render(request, 'fila/form.html', {'form': form, 'titulo': f'Editando 3D: {item.nome_peca}'})

@login_required
def deletar_pedido_3d(request, id):
    if not pode_gerenciar(request.user, '3D'):
        messages.error(request, 'Acesso Negado: Apenas gestores do Setor 3D podem excluir pedidos.')
        return redirect('lista_fila')
    item = get_object_or_404(Pedido3D, id=id)
    item.delete()
    messages.success(request, 'Pedido removido da fila 3D.')
    return redirect('lista_fila')


# ==========================================
# VIEWS DA ROUTER CNC
# ==========================================
@login_required
def novo_pedido_router(request):
    if not pode_adicionar(request.user, 'Router'):
        messages.error(request, 'Acesso Negado: Você não pertence ao Setor Router.')
        return redirect('lista_router')

    if request.method == 'POST':
        form = NovoRouterForm(request.POST, request.FILES)
        if form.is_valid():
            pedido = form.save(commit=False)
            pedido.solicitante = request.user.username
            pedido.save()
            messages.success(request, 'Pedido Router adicionado à fila!')
            return redirect('lista_router')
    else:
        form = NovoRouterForm()
    return render(request, 'fila/form.html', {'form': form, 'titulo': 'Novo Pedido - Router CNC'})

@login_required
def editar_pedido_router(request, id):
    if not pode_gerenciar(request.user, 'Router'):
        messages.error(request, 'Acesso Negado: Apenas gestores do Setor Router podem editar pedidos.')
        return redirect('lista_router')
    item = get_object_or_404(PedidoRouter, id=id)
    if request.method == 'POST':
        form = EdicaoGestorRouterForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            item_salvo = form.save(commit=False)
            if item_salvo.status == 'C' and not item_salvo.data_conclusao: item_salvo.data_conclusao = timezone.now()
            elif item_salvo.status != 'C': item_salvo.data_conclusao = None
            item_salvo.save()
            messages.success(request, f'Pedido "{item_salvo.nome_peca}" atualizado!')
            return redirect('lista_router')
    else:
        form = EdicaoGestorRouterForm(instance=item)
    return render(request, 'fila/form.html', {'form': form, 'titulo': f'Editando Router: {item.nome_peca}'})

@login_required
def deletar_pedido_router(request, id):
    if not pode_gerenciar(request.user, 'Router'):
        messages.error(request, 'Acesso Negado: Apenas gestores do Setor Router podem excluir pedidos.')
        return redirect('lista_router')
    item = get_object_or_404(PedidoRouter, id=id)
    item.delete()
    messages.success(request, 'Pedido removido da fila Router.')
    return redirect('lista_router')


# ==========================================
# VIEWS DO PROJETO CAD
# ==========================================
@login_required
def novo_pedido_cad(request):
    if not pode_adicionar(request.user, 'CAD'):
        messages.error(request, 'Acesso Negado: Você não pertence ao Setor CAD.')
        return redirect('lista_cad')

    if request.method == 'POST':
        form = NovoCADForm(request.POST, request.FILES)
        if form.is_valid():
            pedido = form.save(commit=False)
            pedido.solicitante = request.user.username
            pedido.save()
            messages.success(request, 'Projeto CAD adicionado à fila!')
            return redirect('lista_cad')
    else:
        form = NovoCADForm()
    return render(request, 'fila/form.html', {'form': form, 'titulo': 'Novo Pedido - Projeto CAD'})

@login_required
def editar_pedido_cad(request, id):
    if not pode_gerenciar(request.user, 'CAD'):
        messages.error(request, 'Acesso Negado: Apenas gestores do Setor CAD podem editar pedidos.')
        return redirect('lista_cad')
    item = get_object_or_404(PedidoCAD, id=id)
    if request.method == 'POST':
        form = EdicaoGestorCADForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            item_salvo = form.save(commit=False)
            if item_salvo.status == 'C' and not item_salvo.data_conclusao: item_salvo.data_conclusao = timezone.now()
            elif item_salvo.status != 'C': item_salvo.data_conclusao = None
            item_salvo.save()
            messages.success(request, f'Projeto "{item_salvo.nome_peca}" atualizado!')
            return redirect('lista_cad')
    else:
        form = EdicaoGestorCADForm(instance=item)
    return render(request, 'fila/form.html', {'form': form, 'titulo': f'Editando CAD: {item.nome_peca}'})

@login_required
def deletar_pedido_cad(request, id):
    if not pode_gerenciar(request.user, 'CAD'):
        messages.error(request, 'Acesso Negado: Apenas gestores do Setor CAD podem excluir pedidos.')
        return redirect('lista_cad')
    item = get_object_or_404(PedidoCAD, id=id)
    item.delete()
    messages.success(request, 'Projeto removido da fila CAD.')
    return redirect('lista_cad')


# ==========================================
# VIEWS DE GESTÃO DE USUÁRIOS
# ==========================================
def registro(request):
    if request.user.is_authenticated:
        return redirect('lista_fila')

    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            messages.success(request, 'Conta criada com sucesso! Aguarde a aprovação do gestor para aceder ao sistema.')
            return redirect('login')
    else:
        form = RegistroUsuarioForm()
    return render(request, 'fila/registro.html', {'form': form})


@login_required
def lista_usuarios_pendentes(request):
    if not request.user.is_superuser:
        messages.error(request, 'Acesso restrito ao gestor.')
        return redirect('lista_fila')

    pendentes = User.objects.filter(is_active=False).order_by('-date_joined')
    return render(request, 'fila/usuarios_pendentes.html', {'pendentes': pendentes})


@login_required
def aprovar_usuario(request, user_id):
    if not request.user.is_superuser:
        return redirect('lista_fila')

    user = get_object_or_404(User, id=user_id, is_active=False)
    user.is_active = True
    user.save()
    messages.success(request, f'Utilizador "{user.username}" aprovado com sucesso!')
    return redirect('usuarios_pendentes')


@login_required
def rejeitar_usuario(request, user_id):
    if not request.user.is_superuser:
        return redirect('lista_fila')

    user = get_object_or_404(User, id=user_id, is_active=False)
    username = user.username
    user.delete()
    messages.success(request, f'Solicitação de "{username}" foi rejeitada.')
    return redirect('usuarios_pendentes')


@login_required
def perfil(request):
    if request.method == 'POST':
        form = PerfilUsuarioForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('perfil')
    else:
        form = PerfilUsuarioForm(instance=request.user)

    # Montar info dos setores do usuário
    user_groups = request.user.groups.values_list('name', flat=True)
    setores_info = []
    for grupo_nome in GRUPOS_FIXOS:
        setor_nome = grupo_nome.replace('Setor ', '')
        pertence = grupo_nome in user_groups
        eh_gestor = request.user.is_staff and pertence
        setores_info.append({
            'nome': setor_nome,
            'pertence': pertence,
            'eh_gestor': eh_gestor,
        })

    return render(request, 'fila/perfil.html', {
        'form': form,
        'grupos': user_groups,
        'setores_info': setores_info,
    })


@login_required
def lista_usuarios(request):
    if not request.user.is_superuser:
        messages.error(request, 'Acesso restrito ao gestor.')
        return redirect('lista_fila')

    usuarios = User.objects.filter(is_active=True).order_by('username')
    pendentes_count = User.objects.filter(is_active=False).count()
    return render(request, 'fila/gestao_usuarios.html', {
        'usuarios': usuarios,
        'pendentes_count': pendentes_count,
    })


@login_required
def editar_usuario(request, user_id):
    if not request.user.is_superuser:
        return redirect('lista_fila')

    user = get_object_or_404(User, id=user_id)
    if user.is_superuser and user != request.user:
        messages.error(request, 'Não é possível editar outro superuser.')
        return redirect('lista_usuarios')

    if request.method == 'POST':
        form = GestaoUsuarioForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, f'Utilizador "{user.username}" atualizado!')
            return redirect('lista_usuarios')
    else:
        form = GestaoUsuarioForm(instance=user)

    return render(request, 'fila/editar_usuario.html', {
        'form': form,
        'usuario': user,
    })


@login_required
def desativar_usuario(request, user_id):
    if not request.user.is_superuser:
        return redirect('lista_fila')

    user = get_object_or_404(User, id=user_id)
    if user.is_superuser:
        messages.error(request, 'Não é possível desativar um superuser.')
        return redirect('lista_usuarios')

    user.is_active = False
    user.save()
    messages.success(request, f'Utilizador "{user.username}" foi desativado.')
    return redirect('lista_usuarios')


# ==========================================
# VIEWS DE GESTÃO DE GRUPOS/SETORES
# ==========================================
@login_required
def lista_grupos(request):
    if not request.user.is_superuser:
        messages.error(request, 'Acesso restrito ao gestor.')
        return redirect('lista_fila')

    # Auto-criar os 3 grupos fixos se não existirem
    for nome in GRUPOS_FIXOS:
        Group.objects.get_or_create(name=nome)

    grupos = Group.objects.filter(name__in=GRUPOS_FIXOS).order_by('name')
    grupos_info = []
    for grupo in grupos:
        membros = grupo.user_set.filter(is_active=True).order_by('username')
        grupos_info.append({
            'grupo': grupo,
            'membros_count': membros.count(),
            'membros': membros,
            'membros_gestores': membros.filter(is_staff=True),
            'membros_operadores': membros.filter(is_staff=False),
        })

    pendentes_count = User.objects.filter(is_active=False).count()
    return render(request, 'fila/gestao_grupos.html', {
        'grupos_info': grupos_info,
        'pendentes_count': pendentes_count,
    })


@login_required
def criar_grupo(request):
    """Mantida por compatibilidade mas os grupos agora são fixos"""
    if not request.user.is_superuser:
        return redirect('lista_fila')
    messages.info(request, 'Os grupos do sistema são fixos: Setor 3D, Setor Router e Setor CAD.')
    return redirect('lista_grupos')


@login_required
def eliminar_grupo(request, group_id):
    """Não permite eliminar os grupos fixos"""
    if not request.user.is_superuser:
        return redirect('lista_fila')
    messages.error(request, 'Os grupos do sistema são fixos e não podem ser eliminados.')
    return redirect('lista_grupos')
