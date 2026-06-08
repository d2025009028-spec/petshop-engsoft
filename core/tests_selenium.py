"""
Testes automatizados com Selenium para o Sistema PawControl.
Testa as operações de Inserir, Listar, Alterar e Remover
para as entidades: Cliente, Funcionário, Pet e Serviço.

Para rodar:
    python manage.py test core.tests_selenium --verbosity=2
"""

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import time


class BaseSeleniumTest(LiveServerTestCase):
    """Classe base com métodos auxiliares para os testes."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = webdriver.ChromeOptions()
        # Remova a linha abaixo se quiser ver o navegador abrindo
        # options.add_argument('--headless')
        cls.driver = webdriver.Chrome(options=options)
        cls.driver.implicitly_wait(5)
        cls.driver.set_window_size(1280, 800)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def preencher_campo(self, name, valor):
        """Preenche um campo de formulário pelo atributo name."""
        campo = self.driver.find_element(By.NAME, name)
        campo.clear()
        campo.send_keys(valor)

    def selecionar_opcao(self, name, valor):
        """Seleciona uma opção em um campo select."""
        select = Select(self.driver.find_element(By.NAME, name))
        select.select_by_visible_text(valor)

    def clicar_botao(self, texto):
        """Clica em um botão pelo texto."""
        botao = self.driver.find_element(By.XPATH, f"//button[contains(text(), '{texto}')]")
        botao.click()

    def clicar_link(self, texto):
        """Clica em um link pelo texto."""
        link = self.driver.find_element(By.LINK_TEXT, texto)
        link.click()

    def verificar_texto_na_pagina(self, texto):
        """Verifica se um texto está presente na página."""
        self.assertIn(texto, self.driver.page_source)

    def verificar_texto_ausente(self, texto):
        """Verifica se um texto NÃO está na página."""
        self.assertNotIn(texto, self.driver.page_source)

    def aguardar_mensagem(self, texto):
        """Aguarda uma mensagem de sucesso/erro aparecer."""
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "alert"))
        )
        self.verificar_texto_na_pagina(texto)


class ClienteTest(BaseSeleniumTest):
    """Testes CRUDES para a entidade Cliente."""

    def test_01_inserir_cliente(self):
        """[RF01] Testa a inserção de um novo cliente."""
        self.driver.get(f"{self.live_server_url}/clientes/inserir/")
        self.preencher_campo('nome', 'João da Silva')
        self.preencher_campo('cpf', '123.456.789-00')
        self.preencher_campo('telefone', '(35) 99999-1234')
        self.preencher_campo('email', 'joao@email.com')
        self.preencher_campo('endereco', 'Rua A, 123 - Itajubá/MG')
        self.clicar_botao('Salvar')
        self.aguardar_mensagem('Cliente cadastrado com sucesso!')

    def test_02_listar_clientes(self):
        """[RF03] Testa a listagem e filtro de clientes."""
        # Inserir cliente para listar
        self.driver.get(f"{self.live_server_url}/clientes/inserir/")
        self.preencher_campo('nome', 'Maria Souza')
        self.preencher_campo('cpf', '987.654.321-00')
        self.preencher_campo('telefone', '(35) 98888-5678')
        self.clicar_botao('Salvar')

        # Listar todos
        self.driver.get(f"{self.live_server_url}/clientes/")
        self.verificar_texto_na_pagina('Maria Souza')

        # Filtrar por nome
        self.preencher_campo('nome', 'Maria')
        self.clicar_botao('Filtrar')
        self.verificar_texto_na_pagina('Maria Souza')

        # Filtrar por CPF
        self.driver.get(f"{self.live_server_url}/clientes/")
        self.preencher_campo('cpf', '987')
        self.clicar_botao('Filtrar')
        self.verificar_texto_na_pagina('987.654.321-00')

    def test_03_alterar_cliente(self):
        """[RF02] Testa a alteração de um cliente existente."""
        # Inserir cliente
        self.driver.get(f"{self.live_server_url}/clientes/inserir/")
        self.preencher_campo('nome', 'Pedro Santos')
        self.preencher_campo('cpf', '111.222.333-44')
        self.preencher_campo('telefone', '(35) 97777-0000')
        self.clicar_botao('Salvar')

        # Alterar
        self.driver.get(f"{self.live_server_url}/clientes/")
        self.clicar_link('Alterar')
        self.preencher_campo('nome', 'Pedro Santos Alterado')
        self.preencher_campo('telefone', '(35) 96666-1111')
        self.clicar_botao('Salvar')
        self.aguardar_mensagem('Cliente alterado com sucesso!')

        # Verificar alteração
        self.driver.get(f"{self.live_server_url}/clientes/")
        self.verificar_texto_na_pagina('Pedro Santos Alterado')

    def test_04_remover_cliente(self):
        """[RF04] Testa a remoção de um cliente."""
        # Inserir cliente
        self.driver.get(f"{self.live_server_url}/clientes/inserir/")
        self.preencher_campo('nome', 'Cliente Para Remover')
        self.preencher_campo('cpf', '555.666.777-88')
        self.preencher_campo('telefone', '(35) 95555-0000')
        self.clicar_botao('Salvar')

        # Remover
        self.driver.get(f"{self.live_server_url}/clientes/")
        self.clicar_link('Remover')
        self.clicar_botao('Sim, Remover')
        self.aguardar_mensagem('removido com sucesso!')

        # Verificar remoção
        self.driver.get(f"{self.live_server_url}/clientes/")
        self.verificar_texto_ausente('Cliente Para Remover')


class FuncionarioTest(BaseSeleniumTest):
    """Testes CRUDES para a entidade Funcionário."""

    def test_01_inserir_funcionario(self):
        """[RF05] Testa a inserção de um novo funcionário."""
        self.driver.get(f"{self.live_server_url}/funcionarios/inserir/")
        self.preencher_campo('nome', 'Ana Veterinária')
        self.preencher_campo('cpf', '222.333.444-55')
        self.selecionar_opcao('cargo', 'Veterinário')
        self.preencher_campo('telefone', '(35) 91111-2222')
        self.preencher_campo('email', 'ana@petshop.com')
        self.preencher_campo('salario', '5000.00')
        self.clicar_botao('Salvar')
        self.aguardar_mensagem('Funcionário cadastrado com sucesso!')

    def test_02_listar_funcionarios(self):
        """[RF07] Testa a listagem e filtro de funcionários."""
        # Inserir
        self.driver.get(f"{self.live_server_url}/funcionarios/inserir/")
        self.preencher_campo('nome', 'Carlos Tosador')
        self.preencher_campo('cpf', '333.444.555-66')
        self.selecionar_opcao('cargo', 'Tosador')
        self.preencher_campo('telefone', '(35) 92222-3333')
        self.preencher_campo('salario', '3000.00')
        self.clicar_botao('Salvar')

        # Listar
        self.driver.get(f"{self.live_server_url}/funcionarios/")
        self.verificar_texto_na_pagina('Carlos Tosador')

        # Filtrar por cargo
        self.selecionar_opcao('cargo', 'Tosador')
        self.clicar_botao('Filtrar')
        self.verificar_texto_na_pagina('Carlos Tosador')

    def test_03_alterar_funcionario(self):
        """[RF06] Testa a alteração de um funcionário."""
        # Inserir
        self.driver.get(f"{self.live_server_url}/funcionarios/inserir/")
        self.preencher_campo('nome', 'Fernanda Banhista')
        self.preencher_campo('cpf', '444.555.666-77')
        self.selecionar_opcao('cargo', 'Banhista')
        self.preencher_campo('telefone', '(35) 93333-4444')
        self.preencher_campo('salario', '2500.00')
        self.clicar_botao('Salvar')

        # Alterar
        self.driver.get(f"{self.live_server_url}/funcionarios/")
        self.clicar_link('Alterar')
        self.preencher_campo('salario', '3500.00')
        self.clicar_botao('Salvar')
        self.aguardar_mensagem('Funcionário alterado com sucesso!')

    def test_04_remover_funcionario(self):
        """[RF08] Testa a remoção de um funcionário."""
        # Inserir
        self.driver.get(f"{self.live_server_url}/funcionarios/inserir/")
        self.preencher_campo('nome', 'Func Para Remover')
        self.preencher_campo('cpf', '666.777.888-99')
        self.selecionar_opcao('cargo', 'Atendente')
        self.preencher_campo('telefone', '(35) 94444-5555')
        self.preencher_campo('salario', '2000.00')
        self.clicar_botao('Salvar')

        # Remover
        self.driver.get(f"{self.live_server_url}/funcionarios/")
        self.clicar_link('Remover')
        self.clicar_botao('Sim, Remover')
        self.aguardar_mensagem('removido com sucesso!')


class PetTest(BaseSeleniumTest):
    """Testes CRUDES para a entidade Pet."""

    def _criar_cliente(self):
        """Cria um cliente para vincular ao pet."""
        self.driver.get(f"{self.live_server_url}/clientes/inserir/")
        self.preencher_campo('nome', 'Dono do Pet')
        self.preencher_campo('cpf', '888.999.000-11')
        self.preencher_campo('telefone', '(35) 95555-6666')
        self.clicar_botao('Salvar')

    def test_01_inserir_pet(self):
        """[RF09] Testa a inserção de um novo pet."""
        self._criar_cliente()
        self.driver.get(f"{self.live_server_url}/pets/inserir/")
        self.preencher_campo('nome', 'Rex')
        self.selecionar_opcao('especie', 'Cachorro')
        self.preencher_campo('raca', 'Labrador')
        self.preencher_campo('peso', '25.5')
        self.preencher_campo('observacoes', 'Dócil e brincalhão')
        self.selecionar_opcao('cliente', 'Dono do Pet - 888.999.000-11')
        self.clicar_botao('Salvar')
        self.aguardar_mensagem('Pet cadastrado com sucesso!')

    def test_02_listar_pets(self):
        """[RF11] Testa a listagem e filtro de pets."""
        self._criar_cliente()
        self.driver.get(f"{self.live_server_url}/pets/inserir/")
        self.preencher_campo('nome', 'Mimi')
        self.selecionar_opcao('especie', 'Gato')
        self.preencher_campo('raca', 'Siamês')
        self.selecionar_opcao('cliente', 'Dono do Pet - 888.999.000-11')
        self.clicar_botao('Salvar')

        self.driver.get(f"{self.live_server_url}/pets/")
        self.verificar_texto_na_pagina('Mimi')

        self.preencher_campo('nome_pet', 'Mimi')
        self.clicar_botao('Filtrar')
        self.verificar_texto_na_pagina('Siamês')

    def test_03_alterar_pet(self):
        """[RF10] Testa a alteração de um pet."""
        self._criar_cliente()
        self.driver.get(f"{self.live_server_url}/pets/inserir/")
        self.preencher_campo('nome', 'Bolinha')
        self.selecionar_opcao('especie', 'Cachorro')
        self.preencher_campo('peso', '10.0')
        self.selecionar_opcao('cliente', 'Dono do Pet - 888.999.000-11')
        self.clicar_botao('Salvar')

        self.driver.get(f"{self.live_server_url}/pets/")
        self.clicar_link('Alterar')
        self.preencher_campo('peso', '12.5')
        self.clicar_botao('Salvar')
        self.aguardar_mensagem('Pet alterado com sucesso!')

    def test_04_remover_pet(self):
        """[RF12] Testa a remoção de um pet."""
        self._criar_cliente()
        self.driver.get(f"{self.live_server_url}/pets/inserir/")
        self.preencher_campo('nome', 'Pet Para Remover')
        self.selecionar_opcao('especie', 'Roedor')
        self.selecionar_opcao('cliente', 'Dono do Pet - 888.999.000-11')
        self.clicar_botao('Salvar')

        self.driver.get(f"{self.live_server_url}/pets/")
        self.clicar_link('Remover')
        self.clicar_botao('Sim, Remover')
        self.aguardar_mensagem('removido com sucesso!')


class ServicoTest(BaseSeleniumTest):
    """Testes CRUDES para a entidade Serviço."""

    def test_01_inserir_servico(self):
        """[RF13] Testa a inserção de um novo serviço."""
        self.driver.get(f"{self.live_server_url}/servicos/inserir/")
        self.preencher_campo('nome', 'Banho Completo')
        self.preencher_campo('descricao', 'Banho com shampoo especial e secagem')
        self.preencher_campo('preco', '80.00')
        self.preencher_campo('duracao_estimada', '60')
        self.clicar_botao('Salvar')
        self.aguardar_mensagem('Serviço cadastrado com sucesso!')

    def test_02_listar_servicos(self):
        """[RF15] Testa a listagem e filtro de serviços."""
        self.driver.get(f"{self.live_server_url}/servicos/inserir/")
        self.preencher_campo('nome', 'Tosa Higiênica')
        self.preencher_campo('preco', '50.00')
        self.preencher_campo('duracao_estimada', '30')
        self.clicar_botao('Salvar')

        self.driver.get(f"{self.live_server_url}/servicos/")
        self.verificar_texto_na_pagina('Tosa Higiênica')

        self.preencher_campo('nome', 'Tosa')
        self.clicar_botao('Filtrar')
        self.verificar_texto_na_pagina('Tosa Higiênica')

    def test_03_alterar_servico(self):
        """[RF14] Testa a alteração de um serviço."""
        self.driver.get(f"{self.live_server_url}/servicos/inserir/")
        self.preencher_campo('nome', 'Consulta Veterinária')
        self.preencher_campo('preco', '120.00')
        self.preencher_campo('duracao_estimada', '45')
        self.clicar_botao('Salvar')

        self.driver.get(f"{self.live_server_url}/servicos/")
        self.clicar_link('Alterar')
        self.preencher_campo('preco', '150.00')
        self.clicar_botao('Salvar')
        self.aguardar_mensagem('Serviço alterado com sucesso!')

    def test_04_remover_servico(self):
        """[RF16] Testa a remoção de um serviço."""
        self.driver.get(f"{self.live_server_url}/servicos/inserir/")
        self.preencher_campo('nome', 'Servico Para Remover')
        self.preencher_campo('preco', '30.00')
        self.preencher_campo('duracao_estimada', '15')
        self.clicar_botao('Salvar')

        self.driver.get(f"{self.live_server_url}/servicos/")
        self.clicar_link('Remover')
        self.clicar_botao('Sim, Remover')
        self.aguardar_mensagem('removido com sucesso!')
