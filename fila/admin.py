from django.contrib import admin
from .models import Pedido3D, PedidoRouter, PedidoCAD

# --- ADMIN DA IMPRESSÃO 3D ---
@admin.register(Pedido3D)
class Pedido3DAdmin(admin.ModelAdmin):
    list_display = ('nome_peca', 'solicitante', 'prioridade', 'status', 'prazo')
    list_filter = ('status', 'prioridade')

# --- ADMIN DA ROUTER CNC ---
@admin.register(PedidoRouter)
class PedidoRouterAdmin(admin.ModelAdmin):
    list_display = ('nome_peca', 'solicitante', 'prioridade', 'status', 'prazo')
    list_filter = ('status', 'prioridade')

# --- ADMIN DO CAD ---
@admin.register(PedidoCAD)
class PedidoCADAdmin(admin.ModelAdmin):
    list_display = ('nome_peca', 'solicitante', 'prioridade', 'status', 'prazo')
    list_filter = ('status', 'prioridade')