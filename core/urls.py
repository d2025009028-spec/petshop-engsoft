from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    # Cliente
    path('clientes/', views.cliente_listar, name='cliente_listar'),
    path('clientes/inserir/', views.cliente_inserir, name='cliente_inserir'),
    path('clientes/<int:pk>/alterar/', views.cliente_alterar, name='cliente_alterar'),
    path('clientes/<int:pk>/remover/', views.cliente_remover, name='cliente_remover'),
    path('clientes/<int:pk>/', views.cliente_detalhar, name='cliente_detalhar'),

    # Funcionário
    path('funcionarios/', views.funcionario_listar, name='funcionario_listar'),
    path('funcionarios/inserir/', views.funcionario_inserir, name='funcionario_inserir'),
    path('funcionarios/<int:pk>/alterar/', views.funcionario_alterar, name='funcionario_alterar'),
    path('funcionarios/<int:pk>/remover/', views.funcionario_remover, name='funcionario_remover'),
    path('funcionarios/<int:pk>/', views.funcionario_detalhar, name='funcionario_detalhar'),

    # Pet
    path('pets/', views.pet_listar, name='pet_listar'),
    path('pets/inserir/', views.pet_inserir, name='pet_inserir'),
    path('pets/<int:pk>/alterar/', views.pet_alterar, name='pet_alterar'),
    path('pets/<int:pk>/remover/', views.pet_remover, name='pet_remover'),
    path('pets/<int:pk>/', views.pet_detalhar, name='pet_detalhar'),

    # Serviço
    path('servicos/', views.servico_listar, name='servico_listar'),
    path('servicos/inserir/', views.servico_inserir, name='servico_inserir'),
    path('servicos/<int:pk>/alterar/', views.servico_alterar, name='servico_alterar'),
    path('servicos/<int:pk>/remover/', views.servico_remover, name='servico_remover'),
    path('servicos/<int:pk>/', views.servico_detalhar, name='servico_detalhar'),
]
