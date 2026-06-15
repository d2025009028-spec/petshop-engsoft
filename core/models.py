from django.db import models
from datetime import date


class Cliente(models.Model):
    nome = models.CharField(max_length=150)
    cpf = models.CharField(max_length=14, unique=True)
    telefone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    endereco = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self):
        return f"{self.nome} - {self.cpf}"

    class Meta:
        ordering = ['nome']


class Funcionario(models.Model):
    CARGO_CHOICES = [
        ('Veterinário', 'Veterinário'),
        ('Tosador', 'Tosador'),
        ('Banhista', 'Banhista'),
        ('Atendente', 'Atendente'),
    ]

    nome = models.CharField(max_length=150)
    cpf = models.CharField(max_length=14, unique=True)
    cargo = models.CharField(max_length=20, choices=CARGO_CHOICES)
    telefone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    salario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.nome} - {self.cargo}"

    class Meta:
        ordering = ['nome']
        verbose_name = 'Funcionário'
        verbose_name_plural = 'Funcionários'


class Pet(models.Model):
    ESPECIE_CHOICES = [
        ('Cachorro', 'Cachorro'),
        ('Gato', 'Gato'),
        ('Ave', 'Ave'),
        ('Roedor', 'Roedor'),
        ('Outro', 'Outro'),
    ]

    PORTE_CHOICES = [
        ('Pequeno', 'Pequeno'),
        ('Médio', 'Médio'),
        ('Grande', 'Grande'),
    ]

    nome = models.CharField(max_length=100)
    especie = models.CharField(max_length=20, choices=ESPECIE_CHOICES)
    porte = models.CharField(max_length=10, choices=PORTE_CHOICES, default='Médio', verbose_name='Porte')
    raca = models.CharField(max_length=100, blank=True, null=True, verbose_name='Raça')
    data_nascimento = models.DateField(blank=True, null=True, verbose_name='Data de Nascimento')
    peso = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name='Peso (kg)')
    observacoes = models.TextField(max_length=500, blank=True, null=True, verbose_name='Observações')
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='pets')

    @property
    def idade(self):
        if self.data_nascimento:
            hoje = date.today()
            anos = hoje.year - self.data_nascimento.year
            if (hoje.month, hoje.day) < (self.data_nascimento.month, self.data_nascimento.day):
                anos -= 1
            return anos
        return None

    def __str__(self):
        return f"{self.nome} ({self.especie}) - Dono: {self.cliente.nome}"

    class Meta:
        ordering = ['nome']


class Servico(models.Model):
    CATEGORIA_CHOICES = [
        ('Estética', 'Estética'),
        ('Saúde', 'Saúde'),
        ('Hospedagem', 'Hospedagem'),
        ('Outros', 'Outros'),
    ]

    nome = models.CharField(max_length=150, unique=True)
    descricao = models.TextField(max_length=500, blank=True, null=True, verbose_name='Descrição')
    preco = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Preço')
    duracao_estimada = models.PositiveIntegerField(verbose_name='Duração Estimada (min)')
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES, default='Outros', verbose_name='Categoria')

    @property
    def preco_formatado(self):
        return f"R$ {self.preco:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

    @property
    def duracao_formatada(self):
        if self.duracao_estimada >= 60:
            horas = self.duracao_estimada // 60
            minutos = self.duracao_estimada % 60
            if minutos > 0:
                return f"{horas}h{minutos}min"
            return f"{horas}h"
        return f"{self.duracao_estimada} min"

    def __str__(self):
        return f"{self.nome} - {self.preco_formatado}"

    class Meta:
        ordering = ['nome']
        verbose_name = 'Serviço'
        verbose_name_plural = 'Serviços'


class Agendamento(models.Model):
    STATUS_CHOICES = [
        ('Agendado', 'Agendado'),
        ('Realizado', 'Realizado'),
        ('Cancelado', 'Cancelado'),
    ]

    data = models.DateField(verbose_name='Data')
    hora = models.TimeField(verbose_name='Hora')
    pet = models.ForeignKey(Pet, on_delete=models.PROTECT, related_name='agendamentos')
    servico = models.ForeignKey(Servico, on_delete=models.PROTECT, related_name='agendamentos', verbose_name='Serviço')
    funcionario = models.ForeignKey(Funcionario, on_delete=models.PROTECT, related_name='agendamentos', verbose_name='Funcionário')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Agendado')
    observacoes = models.TextField(max_length=500, blank=True, null=True, verbose_name='Observações')

    @property
    def valor(self):
        return self.servico.preco

    @property
    def valor_formatado(self):
        return self.servico.preco_formatado

    def __str__(self):
        return f"{self.data.strftime('%d/%m/%Y')} {self.hora.strftime('%H:%M')} - {self.pet.nome} - {self.servico.nome}"

    class Meta:
        ordering = ['-data', '-hora']
        verbose_name = 'Agendamento'
        verbose_name_plural = 'Agendamentos'


class Produto(models.Model):
    CATEGORIA_CHOICES = [
        ('Ração', 'Ração'),
        ('Brinquedo', 'Brinquedo'),
        ('Higiene', 'Higiene'),
        ('Medicamento', 'Medicamento'),
        ('Acessório', 'Acessório'),
    ]

    nome = models.CharField(max_length=150, unique=True)
    descricao = models.TextField(max_length=500, blank=True, null=True, verbose_name='Descrição')
    preco = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Preço')
    quantidade_estoque = models.PositiveIntegerField(verbose_name='Quantidade em Estoque')
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES, verbose_name='Categoria')

    @property
    def preco_formatado(self):
        return f"R$ {self.preco:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

    @property
    def estoque_baixo(self):
        return self.quantidade_estoque <= 5

    def __str__(self):
        return f"{self.nome} - {self.preco_formatado} ({self.quantidade_estoque} un.)"

    class Meta:
        ordering = ['nome']
