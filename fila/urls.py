from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.lista_fila, name='lista_fila'),
    path('novo/', views.novo_pedido, name='novo_pedido'),
    path('editar/<int:id>/', views.editar_pedido, name='editar_pedido'),
    path('deletar/<int:id>/', views.deletar_pedido, name='deletar_pedido'),

    # Login, Logout e Registro
    path('login/', auth_views.LoginView.as_view(template_name='fila/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='lista_fila'), name='logout'),
    path('registro/', views.registro, name='registro'),

    # Recuperação de Senha (Esqueci a Senha)
    # Usamos as telas padrão do Django para facilitar no MVP
    path('recuperar-senha/', auth_views.PasswordResetView.as_view(template_name='fila/recuperar_senha.html'),
         name='password_reset'),
    path('recuperar-senha/enviado/', auth_views.PasswordResetDoneView.as_view(template_name='fila/senha_enviada.html'),
         name='password_reset_done'),
    path('recuperar-senha/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='fila/nova_senha.html'),
         name='password_reset_confirm'),
    path('recuperar-senha/concluido/',
         auth_views.PasswordResetCompleteView.as_view(template_name='fila/senha_concluida.html'),
         name='password_reset_complete'),
]