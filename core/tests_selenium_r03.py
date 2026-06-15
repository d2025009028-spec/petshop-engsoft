"""
Testes automatizados com Selenium - PawControl Release 03.
Para rodar: python manage.py test core.tests_selenium_r03 --verbosity=2
"""

import time
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC


DELAY = 1.0  # segundos entre ações (ajuste pra apresentação)


class BaseTest(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-search-engine-choice-screen')
        cls.driver = webdriver.Chrome(options=options)
        cls.driver.implicitly_wait(10)
        cls.driver.set_window_size(1280, 900)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def abrir(self, path):
        self.driver.get(f"{self.live_server_url}{path}")
        time.sleep(0.5)

    def preencher(self, name, valor):
        campo = self.driver.find_element(By.NAME, name)
        campo.clear()
        campo.send_keys(valor)
        time.sleep(DELAY)

    def selecionar(self, name, texto):
        select = Select(self.driver.find_element(By.NAME, name))
        select.select_by_visible_text(texto)
        time.sleep(DELAY)

    def selecionar_primeiro(self, name):
        """Seleciona a primeira opção não vazia de um select."""
        select = Select(self.driver.find_element(By.NAME, name))
        for i, option in enumerate(select.options):
            if option.get_attribute('value') and option.text.strip() != '---------':
                select.select_by_index(i)
                break
        time.sleep(DELAY)

    def clicar(self, texto):
        el = self.driver.find_element(By.XPATH,
            f"//button[contains(text(), '{texto}')] | //a[contains(text(), '{texto}')]")
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
        time.sleep(0.3)
        self.driver.execute_script("arguments[0].click();", el)
        time.sleep(DELAY)

    def clicar_btn_tabela(self, texto, linha=0):
        """Clica no botão de uma linha específica da tabela."""
        links = self.driver.find_elements(By.LINK_TEXT, texto)
        if links and linha < len(links):
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", links[linha])
            time.sleep(0.3)
            self.driver.execute_script("arguments[0].click();", links[linha])
            time.sleep(DELAY)

    def tem_texto(self, texto):
        self.assertIn(texto, self.driver.page_source)

    def nao_tem_texto(self, texto):
        self.assertNotIn(texto, self.driver.page_source)

    def tem_mensagem(self, texto):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "alert"))
        )
        self.tem_texto(texto)

    # ---- Criadores de dados auxiliares ----

    def criar_cliente(self, nome='Dono Teste', cpf='111.111.111-11'):
        self.abrir('/clientes/inserir/')
        self.preencher('nome', nome)
        self.preencher('cpf', cpf)
        self.preencher('telefone', '(35) 99999-0000')
        self.clicar('Salvar')
        time.sleep(0.5)

    def criar_funcionario(self, nome='Func Teste', cpf='222.222.222-22'):
        self.abrir('/funcionarios/inserir/')
        self.preencher('nome', nome)
        self.preencher('cpf', cpf)
        self.selecionar('cargo', 'Banhista')
        self.preencher('telefone', '(35) 98888-0000')
        self.preencher('salario', '3000.00')
        self.clicar('Salvar')
        time.sleep(0.5)

    def criar_pet(self, nome='Rex Teste'):
        self.abrir('/pets/inserir/')
        self.preencher('nome', nome)
        self.selecionar('especie', 'Cachorro')
        self.selecionar_primeiro('cliente')
        self.clicar('Salvar')
        time.sleep(0.5)

    def criar_servico(self, nome='Banho Teste', preco='80.00'):
        self.abrir('/servicos/inserir/')
        self.preencher('nome', nome)
        self.selecionar('categoria', 'Estética')
        self.preencher('preco', preco)
        self.preencher('duracao_estimada', '60')
        self.clicar('Salvar')
        time.sleep(0.5)

    def criar_tudo(self):
        self.criar_cliente()
        self.criar_funcionario()
        self.criar_pet()
        self.criar_servico()


class AgendamentoTest(BaseTest):

    def test_01_inserir_agendamento(self):
        """[RF17] Inserir agendamento."""
        self.criar_tudo()
        self.abrir('/agendamentos/inserir/')
        self.preencher('data', '2026-07-15')
        self.preencher('hora', '10:00')
        self.selecionar_primeiro('pet')
        self.selecionar_primeiro('servico')
        self.selecionar_primeiro('funcionario')
        self.clicar('Salvar')
        self.tem_mensagem('Agendamento cadastrado com sucesso!')

    def test_02_listar_agendamentos(self):
        """[RF19] Listar e filtrar agendamentos."""
        self.criar_tudo()
        self.abrir('/agendamentos/inserir/')
        self.preencher('data', '2026-08-20')
        self.preencher('hora', '14:00')
        self.selecionar_primeiro('pet')
        self.selecionar_primeiro('servico')
        self.selecionar_primeiro('funcionario')
        self.clicar('Salvar')

        self.abrir('/agendamentos/')
        self.tem_texto('Rex Teste')
        self.tem_texto('Agendado')

        self.selecionar('status', 'Agendado')
        self.clicar('Filtrar')
        self.tem_texto('Agendado')

    def test_03_alterar_agendamento(self):
        """[RF18] Alterar agendamento."""
        self.criar_tudo()
        self.abrir('/agendamentos/inserir/')
        self.preencher('data', '2026-09-10')
        self.preencher('hora', '09:00')
        self.selecionar_primeiro('pet')
        self.selecionar_primeiro('servico')
        self.selecionar_primeiro('funcionario')
        self.clicar('Salvar')

        self.abrir('/agendamentos/')
        self.clicar_btn_tabela('Alterar')
        self.selecionar('status', 'Realizado')
        self.clicar('Salvar')
        self.tem_mensagem('Agendamento alterado com sucesso!')

    def test_04_remover_agendamento(self):
        """[RF20] Remover agendamento."""
        self.criar_tudo()
        self.abrir('/agendamentos/inserir/')
        self.preencher('data', '2026-10-05')
        self.preencher('hora', '16:00')
        self.selecionar_primeiro('pet')
        self.selecionar_primeiro('servico')
        self.selecionar_primeiro('funcionario')
        self.clicar('Salvar')

        self.abrir('/agendamentos/')
        self.clicar_btn_tabela('Remover')
        self.clicar('Sim, Remover')
        self.tem_mensagem('Agendamento removido com sucesso!')


class ProdutoTest(BaseTest):

    def test_01_inserir_produto(self):
        """[RF21] Inserir produto."""
        self.abrir('/produtos/inserir/')
        self.preencher('nome', 'Ração Premium 15kg')
        self.selecionar('categoria', 'Ração')
        self.preencher('descricao', 'Ração premium para cães adultos')
        self.preencher('preco', '189.90')
        self.preencher('quantidade_estoque', '25')
        self.clicar('Salvar')
        self.tem_mensagem('Produto cadastrado com sucesso!')

    def test_02_listar_produtos(self):
        """[RF23] Listar e filtrar produtos."""
        self.abrir('/produtos/inserir/')
        self.preencher('nome', 'Shampoo Antipulgas')
        self.selecionar('categoria', 'Higiene')
        self.preencher('preco', '35.90')
        self.preencher('quantidade_estoque', '50')
        self.clicar('Salvar')

        self.abrir('/produtos/')
        self.tem_texto('Shampoo Antipulgas')

        self.selecionar('categoria', 'Higiene')
        self.clicar('Filtrar')
        self.tem_texto('Shampoo Antipulgas')

    def test_03_alterar_produto(self):
        """[RF22] Alterar produto."""
        self.abrir('/produtos/inserir/')
        self.preencher('nome', 'Bola de Borracha')
        self.selecionar('categoria', 'Brinquedo')
        self.preencher('preco', '15.00')
        self.preencher('quantidade_estoque', '100')
        self.clicar('Salvar')

        self.abrir('/produtos/')
        self.clicar_btn_tabela('Alterar')
        self.preencher('preco', '19.90')
        self.clicar('Salvar')
        self.tem_mensagem('Produto alterado com sucesso!')

    def test_04_remover_produto(self):
        """[RF24] Remover produto."""
        self.abrir('/produtos/inserir/')
        self.preencher('nome', 'Produto Remover')
        self.selecionar('categoria', 'Acessório')
        self.preencher('preco', '10.00')
        self.preencher('quantidade_estoque', '5')
        self.clicar('Salvar')

        self.abrir('/produtos/')
        self.clicar_btn_tabela('Remover')
        self.clicar('Sim, Remover')
        self.tem_mensagem('removido com sucesso!')


class RelatorioTest(BaseTest):

    def test_01_relatorio_servicos_periodo(self):
        """[RF25] Relatório de serviços por período."""
        self.criar_tudo()
        self.abrir('/agendamentos/inserir/')
        self.preencher('data', '2026-07-10')
        self.preencher('hora', '10:00')
        self.selecionar_primeiro('pet')
        self.selecionar_primeiro('servico')
        self.selecionar_primeiro('funcionario')
        self.selecionar('status', 'Realizado')
        self.clicar('Salvar')

        self.abrir('/relatorios/servicos/')
        self.preencher('data_inicio', '2026-07-01')
        self.preencher('data_fim', '2026-07-31')
        self.clicar('Gerar')
        self.tem_texto('Rex Teste')
        self.tem_texto('Banho Teste')

    def test_02_relatorio_faturamento_mensal(self):
        """[RF26] Relatório de faturamento mensal."""
        self.criar_tudo()
        self.abrir('/agendamentos/inserir/')
        self.preencher('data', '2026-07-10')
        self.preencher('hora', '10:00')
        self.selecionar_primeiro('pet')
        self.selecionar_primeiro('servico')
        self.selecionar_primeiro('funcionario')
        self.selecionar('status', 'Realizado')
        self.clicar('Salvar')

        self.abrir('/relatorios/faturamento/')
        self.selecionar('mes', 'Julho')
        self.preencher('ano', '2026')
        self.clicar('Gerar')
        self.tem_texto('Banho Teste')
        self.tem_texto('Total Geral')
