from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.utils import timezone
from .models import ItemFila
from .forms import NovaImpressaoForm, EdicaoGestorForm


def lista_fila(request):
    # 1. EM PRODUÇÃO: Apenas o que está imprimindo agora
    em_producao = ItemFila.objects.filter(status='I').order_by('prazo')

    # 2. FILA DE ESPERA: Apenas o que está aguardando
    fila_espera = ItemFila.objects.filter(status='F').order_by('prazo')

    # 3. PENDENTES: Pendente de informação ou Erro
    pendentes = ItemFila.objects.filter(status__in=['P', 'E']).order_by('-data_criacao')

    # 4. CONCLUÍDOS: Os últimos 10
    concluidos = ItemFila.objects.filter(status='C').order_by('-data_conclusao')[:10]

    # Mandamos as 4 listas para o HTML
    contexto = {
        'em_producao': em_producao,
        'fila_espera': fila_espera,
        'pendentes': pendentes,
        'concluidos': concluidos
    }
    return render(request, 'fila/lista.html', contexto)


def novo_pedido(request):
    if request.method == 'POST':
        form = NovaImpressaoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # MENSAGEM DE SUCESSO!
            messages.success(request, 'Novo pedido adicionado à fila com sucesso!')
            return redirect('lista_fila')
    else:
        form = NovaImpressaoForm()
    return render(request, 'fila/form.html', {'form': form, 'titulo': 'Novo Pedido'})


@login_required
def editar_pedido(request, id):
    if not request.user.is_staff:
        return redirect('lista_fila')

    item = get_object_or_404(ItemFila, id=id)

    if request.method == 'POST':
        form = EdicaoGestorForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            # commit=False salva no Python primeiro, antes de enviar para o banco de dados
            item_salvo = form.save(commit=False)

            # REGRA INTELIGENTE: Se o status for Concluído e não tiver data, preenchemos com o momento atual
            if item_salvo.status == 'C' and not item_salvo.data_conclusao:
                item_salvo.data_conclusao = timezone.now()
            # Se o status não for 'C', limpamos a data de conclusão (caso tenha sido alterado por engano)
            elif item_salvo.status != 'C':
                item_salvo.data_conclusao = None

            item_salvo.save()  # Agora sim, salvamos no banco!

            messages.success(request, f'O pedido "{item_salvo.nome_peca}" foi atualizado com sucesso!')
            return redirect('lista_fila')
    else:
        form = EdicaoGestorForm(instance=item)

    return render(request, 'fila/form.html', {'form': form, 'titulo': f'Editando: {item.nome_peca}'})


@login_required
def deletar_pedido(request, id):
    if not request.user.is_staff:
        return redirect('lista_fila')

    item = get_object_or_404(ItemFila, id=id)
    nome = item.nome_peca  # Guardamos o nome para mostrar na mensagem
    item.delete()

    messages.success(request, f'O pedido "{nome}" foi removido da fila.')
    return redirect('lista_fila')

def registro(request):
    if request.method == 'POST':
        # O Django já tem um formulário seguro e pronto para senhas!
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # Cria o usuário no banco de dados
            messages.success(request, 'Conta criada com sucesso! Agora você pode fazer login.')
            return redirect('login')  # Manda o usuário para a tela de login
    else:
        form = UserCreationForm()

    return render(request, 'fila/registro.html', {'form': form})