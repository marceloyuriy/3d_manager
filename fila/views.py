from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.utils import timezone

from .models import Pedido3D, PedidoRouter, PedidoCAD
from .forms import NovaImpressao3DForm, EdicaoGestor3DForm


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
        'setor_ativo': '3D' # <-- Esta etiqueta avisa o HTML para pintar o botão 3D!
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
        'setor_ativo': 'Router' # <-- Etiqueta da Router
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
        'setor_ativo': 'CAD' # <-- Etiqueta do CAD
    }
    return render(request, 'fila/lista.html', contexto)


@login_required
def novo_pedido(request):
    if request.method == 'POST':
        # Substituímos pelo novo formulário da 3D
        form = NovaImpressao3DForm(request.POST, request.FILES)
        if form.is_valid():
            pedido = form.save(commit=False)
            pedido.solicitante = request.user.username
            pedido.save()

            return redirect('lista_fila')
    else:
        form = NovaImpressao3DForm()

    contexto = {
        'form': form,
        'titulo': 'Novo Pedido 3D'
    }
    return render(request, 'fila/form.html', contexto)


@login_required
def editar_pedido(request, id):
    if not request.user.is_staff:
        return redirect('lista_fila')

    # Substituímos ItemFila por Pedido3D
    item = get_object_or_404(Pedido3D, id=id)

    if request.method == 'POST':
        # Substituímos pelo novo formulário de edição da 3D
        form = EdicaoGestor3DForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            item_salvo = form.save(commit=False)

            if item_salvo.status == 'C' and not item_salvo.data_conclusao:
                item_salvo.data_conclusao = timezone.now()
            elif item_salvo.status != 'C':
                item_salvo.data_conclusao = None

            item_salvo.save()

            messages.success(request, f'O pedido "{item_salvo.nome_peca}" foi atualizado com sucesso!')
            return redirect('lista_fila')
    else:
        form = EdicaoGestor3DForm(instance=item)

    return render(request, 'fila/form.html', {'form': form, 'titulo': f'Editando: {item.nome_peca}'})


@login_required
def deletar_pedido(request, id):
    if not request.user.is_staff:
        return redirect('lista_fila')

    # Substituímos ItemFila por Pedido3D
    item = get_object_or_404(Pedido3D, id=id)
    nome = item.nome_peca
    item.delete()

    messages.success(request, f'O pedido "{nome}" foi removido da fila.')
    return redirect('lista_fila')


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