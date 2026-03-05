from django.contrib import admin
from .models import ItemFila # Importa o modelo que criamos

# Registra o modelo no painel de administração
@admin.register(ItemFila)
class ItemFilaAdmin(admin.ModelAdmin):
    # Essa linha define quais colunas vão aparecer na lista do painel para facilitar a visualização
    list_display = ('nome_peca', 'solicitante', 'prioridade', 'status', 'prazo')
    # Adiciona filtros laterais super úteis
    list_filter = ('status', 'prioridade')