from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # --- HUB MULTI-FILAS ---
    path('', views.lista_3d, name='lista_fila'),
    path('router/', views.lista_router, name='lista_router'),
    path('cad/', views.lista_cad, name='lista_cad'),

    # --- AÇÕES POR SETOR ---
    path('<slug:setor>/novo/', views.novo_pedido, name='novo_pedido'),
    path('<slug:setor>/editar/<int:id>/', views.editar_pedido, name='editar_pedido'),
    path('<slug:setor>/deletar/<int:id>/', views.deletar_pedido, name='deletar_pedido'),

    # --- LOGIN, LOGOUT E REGISTRO ---
    path('login/', auth_views.LoginView.as_view(template_name='fila/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='lista_fila'), name='logout'),
    path('registro/', views.registro, name='registro'),

    # --- RECUPERAÇÃO DE SENHA ---
    path('recuperar-senha/', auth_views.PasswordResetView.as_view(template_name='fila/recuperar_senha.html'), name='password_reset'),
    path('recuperar-senha/enviado/', auth_views.PasswordResetDoneView.as_view(template_name='fila/senha_enviada.html'), name='password_reset_done'),
    path('recuperar-senha/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='fila/nova_senha.html'), name='password_reset_confirm'),
    path('recuperar-senha/concluido/', auth_views.PasswordResetCompleteView.as_view(template_name='fila/senha_concluida.html'), name='password_reset_complete'),
]
