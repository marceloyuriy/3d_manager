from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.utils import timezone

from .models import Pedido3D, PedidoRouter, PedidoCAD
from .forms import (
    NovaImpressao3DForm,
    EdicaoGestor3DForm,
    NovoRouterForm,
    EdicaoGestorRouterForm,
    NovoCADForm,
    EdicaoGestorCADForm,
)


SETORES = {
    '3d': {
        'nome': 'Impressão 3D',
        'tag': '3D',
        'model': Pedido3D,
        'novo_form': NovaImpressao3DForm,
        'edicao_form': EdicaoGestor3DForm,
        'lista_url': 'lista_fila',
    },
    'router': {
        'nome': 'Router CNC',
        'tag': 'Router',
        'model': PedidoRouter,
        'novo_form': NovoRouterForm,
        'edicao_form': EdicaoGestorRouterForm,
        'lista_url': 'lista_router',
    },
    'cad': {
        'nome': 'CAD ↔ Manufatura',
        'tag': 'CAD',
        'model': PedidoCAD,
        'novo_form': NovoCADForm,
        'edicao_form': EdicaoGestorCADForm,
        'lista_url': 'lista_cad',
    },
}


def _setor_config(setor):
    return SETORES.get(setor, SETORES['3d'])


# --- 1. VIEW DA FILA 3D ---
def lista_3d(request):
    em_producao = Pedido3D.objects.filter(status='I').order_by('prazo')
    fila_espera = Pedido3D.objects.filter(status='F').order_by('prazo')
    pendentes = Pedido3D.objects.filter(status__in=['P', 'E']).order_by('-data_criacao')
    concluidos = Pedido3D.objects.filter(status='C').order_by('-data_conclusao')[:10]

    contexto = {
        'em_producao': em_producao,
        'fila_espera': fila_espera,
        'pendentes': pendentes,
        'concluidos': concluidos,
        'setor_ativo': '3D',
        'setor_slug': '3d',
    }
    return render(request, 'fila/lista.html', contexto)

# --- 2. VIEW DA FILA ROUTER ---
def lista_router(request):
    # Dica: No futuro colocaremos aqui a trava de segurança (if user in group)
    em_producao = PedidoRouter.objects.filter(status='I').order_by('prazo')
    fila_espera = PedidoRouter.objects.filter(status='F').order_by('prazo')
    pendentes = PedidoRouter.objects.filter(status__in=['P', 'E']).order_by('-data_criacao')
    concluidos = PedidoRouter.objects.filter(status='C').order_by('-data_conclusao')[:10]

    contexto = {
        'em_producao': em_producao,
        'fila_espera': fila_espera,
        'pendentes': pendentes,
        'concluidos': concluidos,
        'setor_ativo': 'Router',
        'setor_slug': 'router',
    }
    return render(request, 'fila/lista.html', contexto)

# --- 3. VIEW DA FILA CAD ---
def lista_cad(request):
    em_producao = PedidoCAD.objects.filter(status='I').order_by('prazo')
    fila_espera = PedidoCAD.objects.filter(status='F').order_by('prazo')
    pendentes = PedidoCAD.objects.filter(status__in=['P', 'E']).order_by('-data_criacao')
    concluidos = PedidoCAD.objects.filter(status='C').order_by('-data_conclusao')[:10]

    contexto = {
        'em_producao': em_producao,
        'fila_espera': fila_espera,
        'pendentes': pendentes,
        'concluidos': concluidos,
        'setor_ativo': 'CAD',
        'setor_slug': 'cad',
    }
    return render(request, 'fila/lista.html', contexto)


@login_required
def novo_pedido(request, setor='3d'):
    config = _setor_config(setor)
    form_class = config['novo_form']

    if request.method == 'POST':
        form = form_class(request.POST, request.FILES)
        if form.is_valid():
            pedido = form.save(commit=False)
            pedido.solicitante = request.user.username
            pedido.save()

            return redirect(config['lista_url'])
    else:
        form = form_class()

    contexto = {
        'form': form,
        'titulo': f"Novo Pedido - {config['nome']}",
        'setor_slug': setor,
        'lista_url': config['lista_url'],
    }
    return render(request, 'fila/form.html', contexto)


@login_required
def editar_pedido(request, setor, id):
    if not request.user.is_staff:
        return redirect('lista_fila')

    config = _setor_config(setor)
    model = config['model']
    form_class = config['edicao_form']

    item = get_object_or_404(model, id=id)

    if request.method == 'POST':
        form = form_class(request.POST, request.FILES, instance=item)
        if form.is_valid():
            item_salvo = form.save(commit=False)

            if item_salvo.status == 'C' and not item_salvo.data_conclusao:
                item_salvo.data_conclusao = timezone.now()
            elif item_salvo.status != 'C':
                item_salvo.data_conclusao = None

            item_salvo.save()

            messages.success(request, f'O pedido "{item_salvo.nome_peca}" foi atualizado com sucesso!')
            return redirect(config['lista_url'])
    else:
        form = form_class(instance=item)

    return render(
        request,
        'fila/form.html',
        {
            'form': form,
            'titulo': f"Editando ({config['nome']}): {item.nome_peca}",
            'setor_slug': setor,
            'lista_url': config['lista_url'],
        },
    )


@login_required
def deletar_pedido(request, setor, id):
    if not request.user.is_staff:
        return redirect('lista_fila')

    config = _setor_config(setor)
    model = config['model']

    item = get_object_or_404(model, id=id)
    nome = item.nome_peca
    item.delete()

    messages.success(request, f'O pedido "{nome}" foi removido da fila.')
    return redirect(config['lista_url'])


def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Conta criada com sucesso! Agora você pode fazer login.')
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'fila/registro.html', {'form': form})
