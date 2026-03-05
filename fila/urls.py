from django.urls import path
from django.contrib.auth import views as auth_views  # Importa o sistema de login do Django
from . import views

urlpatterns = [
    path('', views.lista_fila, name='lista_fila'),
    path('novo/', views.novo_pedido, name='novo_pedido'),

    # Rotas para os Gestores
    path('editar/<int:id>/', views.editar_pedido, name='editar_pedido'),
    path('deletar/<int:id>/', views.deletar_pedido, name='deletar_pedido'),

    # Rotas de Login/Logout padrão do Django
    path('login/', auth_views.LoginView.as_view(template_name='fila/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='lista_fila'), name='logout'),
]