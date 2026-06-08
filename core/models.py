from django.db import models


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

    nome = models.CharField(max_length=100)
    especie = models.CharField(max_length=20, choices=ESPECIE_CHOICES)
    raca = models.CharField(max_length=100, blank=True, null=True, verbose_name='Raça')
    data_nascimento = models.DateField(blank=True, null=True, verbose_name='Data de Nascimento')
    peso = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name='Peso (kg)')
    observacoes = models.TextField(max_length=500, blank=True, null=True, verbose_name='Observações')
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='pets')

    def __str__(self):
        return f"{self.nome} ({self.especie}) - Dono: {self.cliente.nome}"

    class Meta:
        ordering = ['nome']


class Servico(models.Model):
    nome = models.CharField(max_length=150, unique=True)
    descricao = models.TextField(max_length=500, blank=True, null=True, verbose_name='Descrição')
    preco = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Preço')
    duracao_estimada = models.PositiveIntegerField(verbose_name='Duração Estimada (min)')

    def __str__(self):
        return f"{self.nome} - R${self.preco}"

    class Meta:
        ordering = ['nome']
        verbose_name = 'Serviço'
        verbose_name_plural = 'Serviços'
