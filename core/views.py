from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Sum, Count
from .models import Cliente, Funcionario, Pet, Servico, Agendamento, Produto
from .forms import (
    ClienteForm, ClienteEditForm,
    FuncionarioForm, FuncionarioEditForm,
    PetForm, PetEditForm,
    ServicoForm,
    AgendamentoForm, AgendamentoEditForm,
    ProdutoForm,
)


def home(request):
    context = {
        'total_clientes': Cliente.objects.count(),
        'total_pets': Pet.objects.count(),
        'total_funcionarios': Funcionario.objects.count(),
        'total_servicos': Servico.objects.count(),
        'total_agendamentos': Agendamento.objects.filter(status='Agendado').count(),
        'total_produtos': Produto.objects.count(),
    }
    return render(request, 'core/home.html', context)


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
        if funcionario.agendamentos.exists():
            messages.error(request, f'Não é possível remover o funcionário "{funcionario.nome}" pois possui agendamentos vinculados.')
        else:
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
        if pet.agendamentos.exists():
            messages.error(request, f'Não é possível remover o pet "{pet.nome}" pois possui agendamentos vinculados.')
        else:
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
        if servico.agendamentos.exists():
            messages.error(request, f'Não é possível remover o serviço "{servico.nome}" pois possui agendamentos vinculados.')
        else:
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


# ==================== AGENDAMENTO ====================

def agendamento_listar(request):
    data = request.GET.get('data', '')
    nome_pet = request.GET.get('nome_pet', '')
    nome_cliente = request.GET.get('nome_cliente', '')
    funcionario_id = request.GET.get('funcionario', '')
    status = request.GET.get('status', '')
    agendamentos = Agendamento.objects.select_related('pet', 'pet__cliente', 'servico', 'funcionario').all()
    if data:
        agendamentos = agendamentos.filter(data=data)
    if nome_pet:
        agendamentos = agendamentos.filter(pet__nome__icontains=nome_pet)
    if nome_cliente:
        agendamentos = agendamentos.filter(pet__cliente__nome__icontains=nome_cliente)
    if funcionario_id:
        agendamentos = agendamentos.filter(funcionario_id=funcionario_id)
    if status:
        agendamentos = agendamentos.filter(status=status)
    funcionarios = Funcionario.objects.all()
    return render(request, 'core/agendamento_listar.html', {
        'agendamentos': agendamentos, 'data': data, 'nome_pet': nome_pet,
        'nome_cliente': nome_cliente, 'funcionario_id': funcionario_id,
        'status': status, 'funcionarios': funcionarios,
    })


def agendamento_inserir(request):
    if request.method == 'POST':
        form = AgendamentoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Agendamento cadastrado com sucesso!')
            return redirect('agendamento_listar')
    else:
        form = AgendamentoForm()
    return render(request, 'core/form.html', {
        'form': form, 'titulo': 'Inserir Agendamento', 'voltar_url': 'agendamento_listar'
    })


def agendamento_alterar(request, pk):
    agendamento = get_object_or_404(Agendamento, pk=pk)
    if agendamento.status == 'Realizado':
        messages.error(request, 'Agendamentos com status "Realizado" não podem ser alterados.')
        return redirect('agendamento_listar')
    if request.method == 'POST':
        form = AgendamentoEditForm(request.POST, instance=agendamento)
        if form.is_valid():
            form.save()
            messages.success(request, 'Agendamento alterado com sucesso!')
            return redirect('agendamento_listar')
    else:
        form = AgendamentoEditForm(instance=agendamento)
    return render(request, 'core/form.html', {
        'form': form, 'titulo': f'Alterar Agendamento',
        'voltar_url': 'agendamento_listar',
        'info_extra': f'Pet: {agendamento.pet.nome} | Serviço: {agendamento.servico.nome}'
    })


def agendamento_remover(request, pk):
    agendamento = get_object_or_404(Agendamento, pk=pk)
    if agendamento.status == 'Realizado':
        messages.error(request, 'Agendamentos com status "Realizado" não podem ser removidos.')
        return redirect('agendamento_listar')
    if request.method == 'POST':
        agendamento.delete()
        messages.success(request, 'Agendamento removido com sucesso!')
        return redirect('agendamento_listar')
    return render(request, 'core/confirmar_remocao.html', {
        'objeto': agendamento, 'tipo': 'Agendamento', 'voltar_url': 'agendamento_listar'
    })


def agendamento_detalhar(request, pk):
    agendamento = get_object_or_404(Agendamento, pk=pk)
    return render(request, 'core/agendamento_detalhar.html', {'agendamento': agendamento})


# ==================== PRODUTO ====================

def produto_listar(request):
    nome = request.GET.get('nome', '')
    categoria = request.GET.get('categoria', '')
    produtos = Produto.objects.all()
    if nome:
        produtos = produtos.filter(nome__icontains=nome)
    if categoria:
        produtos = produtos.filter(categoria=categoria)
    categorias = Produto.CATEGORIA_CHOICES
    return render(request, 'core/produto_listar.html', {
        'produtos': produtos, 'nome': nome, 'categoria': categoria, 'categorias': categorias
    })


def produto_inserir(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produto cadastrado com sucesso!')
            return redirect('produto_listar')
    else:
        form = ProdutoForm()
    return render(request, 'core/form.html', {
        'form': form, 'titulo': 'Inserir Produto', 'voltar_url': 'produto_listar'
    })


def produto_alterar(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    if request.method == 'POST':
        form = ProdutoForm(request.POST, instance=produto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produto alterado com sucesso!')
            return redirect('produto_listar')
    else:
        form = ProdutoForm(instance=produto)
    return render(request, 'core/form.html', {
        'form': form, 'titulo': f'Alterar Produto: {produto.nome}',
        'voltar_url': 'produto_listar'
    })


def produto_remover(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    if request.method == 'POST':
        nome = produto.nome
        produto.delete()
        messages.success(request, f'Produto "{nome}" removido com sucesso!')
        return redirect('produto_listar')
    return render(request, 'core/confirmar_remocao.html', {
        'objeto': produto, 'tipo': 'Produto', 'voltar_url': 'produto_listar'
    })


def produto_detalhar(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    return render(request, 'core/produto_detalhar.html', {'produto': produto})


# ==================== RELATÓRIOS ====================

def relatorio_servicos_periodo(request):
    data_inicio = request.GET.get('data_inicio', '')
    data_fim = request.GET.get('data_fim', '')
    funcionario_id = request.GET.get('funcionario', '')
    servico_id = request.GET.get('servico', '')
    agendamentos = None
    total_servicos = 0
    valor_total = 0

    if data_inicio and data_fim:
        agendamentos = Agendamento.objects.filter(
            status='Realizado',
            data__gte=data_inicio,
            data__lte=data_fim
        ).select_related('pet', 'pet__cliente', 'servico', 'funcionario')

        if funcionario_id:
            agendamentos = agendamentos.filter(funcionario_id=funcionario_id)
        if servico_id:
            agendamentos = agendamentos.filter(servico_id=servico_id)

        total_servicos = agendamentos.count()
        valor_total = sum(a.servico.preco for a in agendamentos)

    funcionarios = Funcionario.objects.all()
    servicos = Servico.objects.all()

    return render(request, 'core/relatorio_servicos.html', {
        'agendamentos': agendamentos, 'data_inicio': data_inicio,
        'data_fim': data_fim, 'funcionario_id': funcionario_id,
        'servico_id': servico_id, 'funcionarios': funcionarios,
        'servicos': servicos, 'total_servicos': total_servicos,
        'valor_total': valor_total,
    })


def relatorio_faturamento_mensal(request):
    mes = request.GET.get('mes', '')
    ano = request.GET.get('ano', '')
    dados = None
    total_geral = 0

    if mes and ano:
        agendamentos = Agendamento.objects.filter(
            status='Realizado',
            data__month=int(mes),
            data__year=int(ano)
        ).select_related('servico')

        dados = agendamentos.values(
            'servico__nome', 'servico__preco'
        ).annotate(
            quantidade=Count('id'),
            subtotal=Sum('servico__preco')
        ).order_by('servico__nome')

        total_geral = sum(d['subtotal'] for d in dados) if dados else 0

    meses = [
        (1, 'Janeiro'), (2, 'Fevereiro'), (3, 'Março'), (4, 'Abril'),
        (5, 'Maio'), (6, 'Junho'), (7, 'Julho'), (8, 'Agosto'),
        (9, 'Setembro'), (10, 'Outubro'), (11, 'Novembro'), (12, 'Dezembro'),
    ]

    return render(request, 'core/relatorio_faturamento.html', {
        'dados': dados, 'mes': mes, 'ano': ano,
        'meses': meses, 'total_geral': total_geral,
    })
