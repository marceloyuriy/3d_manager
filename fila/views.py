from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages  # <-- IMPORTAÇÃO PARA OS AVISOS
from django.utils import timezone  # <-- IMPORTAÇÃO PARA PEGAR A HORA ATUAL
from .models import ItemFila
from .forms import NovaImpressaoForm, EdicaoGestorForm


def lista_fila(request):
    fila_ativa = ItemFila.objects.filter(status__in=['F', 'I']).order_by('prazo')
    pendentes = ItemFila.objects.filter(status__in=['P', 'E']).order_by('-data_criacao')
    concluidos = ItemFila.objects.filter(status='C').order_by('-data_conclusao')[
        :10]  # Mudamos a ordenação para a conclusão mais recente!

    contexto = {'fila_ativa': fila_ativa, 'pendentes': pendentes, 'concluidos': concluidos}
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