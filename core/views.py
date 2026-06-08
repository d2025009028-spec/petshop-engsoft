from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Cliente, Funcionario, Pet, Servico
from .forms import (
    ClienteForm, ClienteEditForm,
    FuncionarioForm, FuncionarioEditForm,
    PetForm, PetEditForm,
    ServicoForm,
)


def home(request):
    return render(request, 'core/home.html')


# ==================== CLIENTE ====================

def cliente_listar(request):
    nome = request.GET.get('nome', '')
    cpf = request.GET.get('cpf', '')
    clientes = Cliente.objects.all()
    if nome:
        clientes = clientes.filter(nome__icontains=nome)
    if cpf:
        clientes = clientes.filter(cpf__icontains=cpf)
    return render(request, 'core/cliente_listar.html', {'clientes': clientes, 'nome': nome, 'cpf': cpf})


def cliente_inserir(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente cadastrado com sucesso!')
            return redirect('cliente_listar')
    else:
        form = ClienteForm()
    return render(request, 'core/form.html', {
        'form': form, 'titulo': 'Inserir Cliente', 'voltar_url': 'cliente_listar'
    })


def cliente_alterar(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        form = ClienteEditForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente alterado com sucesso!')
            return redirect('cliente_listar')
    else:
        form = ClienteEditForm(instance=cliente)
    return render(request, 'core/form.html', {
        'form': form, 'titulo': f'Alterar Cliente: {cliente.nome}',
        'voltar_url': 'cliente_listar', 'cpf_readonly': cliente.cpf
    })


def cliente_remover(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        if cliente.pets.exists():
            messages.error(request, f'Não é possível remover o cliente "{cliente.nome}" pois possui pets cadastrados.')
        else:
            nome = cliente.nome
            cliente.delete()
            messages.success(request, f'Cliente "{nome}" removido com sucesso!')
        return redirect('cliente_listar')
    return render(request, 'core/confirmar_remocao.html', {
        'objeto': cliente, 'tipo': 'Cliente', 'voltar_url': 'cliente_listar'
    })


def cliente_detalhar(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    return render(request, 'core/cliente_detalhar.html', {'cliente': cliente})


# ==================== FUNCIONÁRIO ====================

def funcionario_listar(request):
    nome = request.GET.get('nome', '')
    cargo = request.GET.get('cargo', '')
    funcionarios = Funcionario.objects.all()
    if nome:
        funcionarios = funcionarios.filter(nome__icontains=nome)
    if cargo:
        funcionarios = funcionarios.filter(cargo=cargo)
    cargos = Funcionario.CARGO_CHOICES
    return render(request, 'core/funcionario_listar.html', {
        'funcionarios': funcionarios, 'nome': nome, 'cargo': cargo, 'cargos': cargos
    })


def funcionario_inserir(request):
    if request.method == 'POST':
        form = FuncionarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Funcionário cadastrado com sucesso!')
            return redirect('funcionario_listar')
    else:
        form = FuncionarioForm()
    return render(request, 'core/form.html', {
        'form': form, 'titulo': 'Inserir Funcionário', 'voltar_url': 'funcionario_listar'
    })


def funcionario_alterar(request, pk):
    funcionario = get_object_or_404(Funcionario, pk=pk)
    if request.method == 'POST':
        form = FuncionarioEditForm(request.POST, instance=funcionario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Funcionário alterado com sucesso!')
            return redirect('funcionario_listar')
    else:
        form = FuncionarioEditForm(instance=funcionario)
    return render(request, 'core/form.html', {
        'form': form, 'titulo': f'Alterar Funcionário: {funcionario.nome}',
        'voltar_url': 'funcionario_listar', 'cpf_readonly': funcionario.cpf
    })


def funcionario_remover(request, pk):
    funcionario = get_object_or_404(Funcionario, pk=pk)
    if request.method == 'POST':
        nome = funcionario.nome
        funcionario.delete()
        messages.success(request, f'Funcionário "{nome}" removido com sucesso!')
        return redirect('funcionario_listar')
    return render(request, 'core/confirmar_remocao.html', {
        'objeto': funcionario, 'tipo': 'Funcionário', 'voltar_url': 'funcionario_listar'
    })


def funcionario_detalhar(request, pk):
    funcionario = get_object_or_404(Funcionario, pk=pk)
    return render(request, 'core/funcionario_detalhar.html', {'funcionario': funcionario})


# ==================== PET ====================

def pet_listar(request):
    nome_pet = request.GET.get('nome_pet', '')
    nome_cliente = request.GET.get('nome_cliente', '')
    pets = Pet.objects.select_related('cliente').all()
    if nome_pet:
        pets = pets.filter(nome__icontains=nome_pet)
    if nome_cliente:
        pets = pets.filter(cliente__nome__icontains=nome_cliente)
    return render(request, 'core/pet_listar.html', {
        'pets': pets, 'nome_pet': nome_pet, 'nome_cliente': nome_cliente
    })


def pet_inserir(request):
    if request.method == 'POST':
        form = PetForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pet cadastrado com sucesso!')
            return redirect('pet_listar')
    else:
        form = PetForm()
    return render(request, 'core/form.html', {
        'form': form, 'titulo': 'Inserir Pet', 'voltar_url': 'pet_listar'
    })


def pet_alterar(request, pk):
    pet = get_object_or_404(Pet, pk=pk)
    if request.method == 'POST':
        form = PetEditForm(request.POST, instance=pet)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pet alterado com sucesso!')
            return redirect('pet_listar')
    else:
        form = PetEditForm(instance=pet)
    return render(request, 'core/form.html', {
        'form': form, 'titulo': f'Alterar Pet: {pet.nome}',
        'voltar_url': 'pet_listar', 'info_extra': f'Cliente: {pet.cliente.nome}'
    })


def pet_remover(request, pk):
    pet = get_object_or_404(Pet, pk=pk)
    if request.method == 'POST':
        nome = pet.nome
        pet.delete()
        messages.success(request, f'Pet "{nome}" removido com sucesso!')
        return redirect('pet_listar')
    return render(request, 'core/confirmar_remocao.html', {
        'objeto': pet, 'tipo': 'Pet', 'voltar_url': 'pet_listar'
    })


def pet_detalhar(request, pk):
    pet = get_object_or_404(Pet, pk=pk)
    return render(request, 'core/pet_detalhar.html', {'pet': pet})


# ==================== SERVIÇO ====================

def servico_listar(request):
    nome = request.GET.get('nome', '')
    servicos = Servico.objects.all()
    if nome:
        servicos = servicos.filter(nome__icontains=nome)
    return render(request, 'core/servico_listar.html', {'servicos': servicos, 'nome': nome})


def servico_inserir(request):
    if request.method == 'POST':
        form = ServicoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Serviço cadastrado com sucesso!')
            return redirect('servico_listar')
    else:
        form = ServicoForm()
    return render(request, 'core/form.html', {
        'form': form, 'titulo': 'Inserir Serviço', 'voltar_url': 'servico_listar'
    })


def servico_alterar(request, pk):
    servico = get_object_or_404(Servico, pk=pk)
    if request.method == 'POST':
        form = ServicoForm(request.POST, instance=servico)
        if form.is_valid():
            form.save()
            messages.success(request, 'Serviço alterado com sucesso!')
            return redirect('servico_listar')
    else:
        form = ServicoForm(instance=servico)
    return render(request, 'core/form.html', {
        'form': form, 'titulo': f'Alterar Serviço: {servico.nome}',
        'voltar_url': 'servico_listar'
    })


def servico_remover(request, pk):
    servico = get_object_or_404(Servico, pk=pk)
    if request.method == 'POST':
        nome = servico.nome
        servico.delete()
        messages.success(request, f'Serviço "{nome}" removido com sucesso!')
        return redirect('servico_listar')
    return render(request, 'core/confirmar_remocao.html', {
        'objeto': servico, 'tipo': 'Serviço', 'voltar_url': 'servico_listar'
    })


def servico_detalhar(request, pk):
    servico = get_object_or_404(Servico, pk=pk)
    return render(request, 'core/servico_detalhar.html', {'servico': servico})
