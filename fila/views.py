from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.utils import timezone

from .models import Pedido3D, PedidoRouter, PedidoCAD
from .forms import (NovaImpressao3DForm, EdicaoGestor3DForm,
                    NovoRouterForm, EdicaoGestorRouterForm,
                    NovoCADForm, EdicaoGestorCADForm)

# --- FUNÇÃO DO SEGURANÇA ---
def tem_permissao(user, setor):
    if not user.is_authenticated:
        return False
    if user.is_superuser: # O Gestor Geral pode tudo!
        return True
    # Verifica se o usuário pertence ao grupo 'Setor 3D', 'Setor Router', etc.
    return user.groups.filter(name=f'Setor {setor}').exists()

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
        'pode_editar': tem_permissao(request.user, '3D') # <--- Enviando a permissão pro HTML!
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
        'pode_editar': tem_permissao(request.user, 'Router')
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
        'pode_editar': tem_permissao(request.user, 'CAD')
    }
    return render(request, 'fila/lista.html', contexto)


# ==========================================
# VIEWS DA IMPRESSORA 3D
# ==========================================
@login_required
def novo_pedido_3d(request):
    if not tem_permissao(request.user, '3D'):
        messages.error(request, 'Acesso Negado: Você não tem o crachá do Setor 3D.')
        return redirect('lista_fila')

    if request.method == 'POST':
        form = NovaImpressao3DForm(request.POST, request.FILES)
        if form.is_valid():
            pedido = form.save(commit=False)
            pedido.solicitante = request.user.username
            pedido.save()
            return redirect('lista_fila')
    else:
        form = NovaImpressao3DForm()
    return render(request, 'fila/form.html', {'form': form, 'titulo': 'Novo Pedido - 3D'})

@login_required
def editar_pedido_3d(request, id):
    if not tem_permissao(request.user, '3D'): return redirect('lista_fila')
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
    if not tem_permissao(request.user, '3D'): return redirect('lista_fila')
    item = get_object_or_404(Pedido3D, id=id)
    item.delete()
    messages.success(request, 'Pedido removido da fila 3D.')
    return redirect('lista_fila')


# ==========================================
# VIEWS DA ROUTER CNC
# ==========================================
@login_required
def novo_pedido_router(request):
    if not tem_permissao(request.user, 'Router'):
        messages.error(request, 'Acesso Negado: Você não tem o crachá do Setor Router.')
        return redirect('lista_router')

    if request.method == 'POST':
        form = NovoRouterForm(request.POST, request.FILES)
        if form.is_valid():
            pedido = form.save(commit=False)
            pedido.solicitante = request.user.username
            pedido.save()
            return redirect('lista_router')
    else:
        form = NovoRouterForm()
    return render(request, 'fila/form.html', {'form': form, 'titulo': 'Novo Pedido - Router'})

@login_required
def editar_pedido_router(request, id):
    if not tem_permissao(request.user, 'Router'): return redirect('lista_router')
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
    if not tem_permissao(request.user, 'Router'): return redirect('lista_router')
    item = get_object_or_404(PedidoRouter, id=id)
    item.delete()
    messages.success(request, 'Pedido removido da fila Router.')
    return redirect('lista_router')


# ==========================================
# VIEWS DO PROJETO CAD
# ==========================================
@login_required
def novo_pedido_cad(request):
    if not tem_permissao(request.user, 'CAD'):
        messages.error(request, 'Acesso Negado: Você não tem o crachá do Setor CAD.')
        return redirect('lista_cad')

    if request.method == 'POST':
        form = NovoCADForm(request.POST, request.FILES)
        if form.is_valid():
            pedido = form.save(commit=False)
            pedido.solicitante = request.user.username
            pedido.save()
            return redirect('lista_cad')
    else:
        form = NovoCADForm()
    return render(request, 'fila/form.html', {'form': form, 'titulo': 'Novo Pedido - CAD'})

@login_required
def editar_pedido_cad(request, id):
    if not tem_permissao(request.user, 'CAD'): return redirect('lista_cad')
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
    if not tem_permissao(request.user, 'CAD'): return redirect('lista_cad')
    item = get_object_or_404(PedidoCAD, id=id)
    item.delete()
    messages.success(request, 'Projeto removido da fila CAD.')
    return redirect('lista_cad')