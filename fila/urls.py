from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # --- HUB MULTI-FILAS ---
    path('', views.lista_3d, name='lista_fila'),
    path('router/', views.lista_router, name='lista_router'),
    path('cad/', views.lista_cad, name='lista_cad'),

    # --- AÇÕES SETOR 3D ---
    path('3d/novo/', views.novo_pedido_3d, name='novo_pedido_3d'),
    path('3d/editar/<int:id>/', views.editar_pedido_3d, name='editar_pedido_3d'),
    path('3d/deletar/<int:id>/', views.deletar_pedido_3d, name='deletar_pedido_3d'),

    # --- AÇÕES SETOR ROUTER ---
    path('router/novo/', views.novo_pedido_router, name='novo_pedido_router'),
    path('router/editar/<int:id>/', views.editar_pedido_router, name='editar_pedido_router'),
    path('router/deletar/<int:id>/', views.deletar_pedido_router, name='deletar_pedido_router'),

    # --- AÇÕES SETOR CAD ---
    path('cad/novo/', views.novo_pedido_cad, name='novo_pedido_cad'),
    path('cad/editar/<int:id>/', views.editar_pedido_cad, name='editar_pedido_cad'),
    path('cad/deletar/<int:id>/', views.deletar_pedido_cad, name='deletar_pedido_cad'),

    # --- LOGIN E REGISTRO ---
    path('login/', auth_views.LoginView.as_view(template_name='fila/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='lista_fila'), name='logout'),

    # --- RECUPERAÇÃO DE SENHA ---
    path('recuperar-senha/', auth_views.PasswordResetView.as_view(template_name='fila/recuperar_senha.html'), name='password_reset'),
    path('recuperar-senha/enviado/', auth_views.PasswordResetDoneView.as_view(template_name='fila/senha_enviada.html'), name='password_reset_done'),
    path('recuperar-senha/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='fila/nova_senha.html'), name='password_reset_confirm'),
    path('recuperar-senha/concluido/', auth_views.PasswordResetCompleteView.as_view(template_name='fila/senha_concluida.html'), name='password_reset_complete'),
]