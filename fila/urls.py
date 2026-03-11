from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path('', views.lista_3d, name='lista_fila'),
    path('router/', views.lista_router, name='lista_router'),
    path('cad/', views.lista_cad, name='lista_cad'),

    path('3d/novo/', views.novo_pedido_3d, name='novo_pedido_3d'),
    path('3d/editar/<int:id>/', views.editar_pedido_3d, name='editar_pedido_3d'),
    path('3d/deletar/<int:id>/', views.deletar_pedido_3d, name='deletar_pedido_3d'),

    path('router/novo/', views.novo_pedido_router, name='novo_pedido_router'),
    path('router/editar/<int:id>/', views.editar_pedido_router, name='editar_pedido_router'),
    path('router/deletar/<int:id>/', views.deletar_pedido_router, name='deletar_pedido_router'),

    path('cad/novo/', views.novo_pedido_cad, name='novo_pedido_cad'),
    path('cad/editar/<int:id>/', views.editar_pedido_cad, name='editar_pedido_cad'),
    path('cad/deletar/<int:id>/', views.deletar_pedido_cad, name='deletar_pedido_cad'),

    path('registro/', views.registro, name='registro'),

    path('gestao/usuarios/pendentes/', views.lista_usuarios_pendentes, name='usuarios_pendentes'),
    path('gestao/usuarios/aprovar/<int:user_id>/', views.aprovar_usuario, name='aprovar_usuario'),
    path('gestao/usuarios/rejeitar/<int:user_id>/', views.rejeitar_usuario, name='rejeitar_usuario'),

    path('login/', auth_views.LoginView.as_view(template_name='fila/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    path('alterar-senha/', auth_views.PasswordChangeView.as_view(template_name='fila/alterar_senha.html'), name='password_change'),
    path('alterar-senha/concluido/', auth_views.PasswordChangeDoneView.as_view(template_name='fila/alterar_senha_concluido.html'), name='password_change_done'),

    path(
        'recuperar-senha/',
        auth_views.PasswordResetView.as_view(
            template_name='fila/recuperar_senha.html',
            email_template_name='fila/emails/password_reset_email.txt',
            subject_template_name='fila/emails/password_reset_subject.txt',
            html_email_template_name='fila/emails/password_reset_email.html',
        ),
        name='password_reset',
    ),
    path('recuperar-senha/enviado/', auth_views.PasswordResetDoneView.as_view(template_name='fila/senha_enviada.html'), name='password_reset_done'),
    path('recuperar-senha/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='fila/nova_senha.html'), name='password_reset_confirm'),
    path('recuperar-senha/concluido/', auth_views.PasswordResetCompleteView.as_view(template_name='fila/senha_concluida.html'), name='password_reset_complete'),
]
