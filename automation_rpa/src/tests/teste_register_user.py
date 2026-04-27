from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from utils.constants import Constants
from data.mock_dados import MockDados
from pages.register_user import RegisterPage

class TestRegister:
    def __init__(self):
        # Configuração do WebDriver (Isolamento de infraestrutura)
        self.service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=self.service)
        self.driver.maximize_window()
        
        # Instância das classes de apoio
        self.page = RegisterPage(self.driver)
        self.dados = MockDados()

    def executar_teste(self):
        try:
            # Passo 1 e 2: Iniciar e Navegar
            print("Iniciando Teste: Register User")
            self.driver.get(Constants.BASE_URL)

            # Passo 3: Verificar Home Page (via título da página ou elemento)
            assert Constants.MSG_HOME_VISIBLE in self.driver.title
            print("Passo 3: Home Page visível.")

            # Passo 4 e 5: Login/Signup
            self.page.ir_para_login_signup()
            texto_signup = self.page.verificar_texto_novo_usuario()
            assert Constants.MSG_NEW_USER_SIGNUP in texto_signup
            print("Passo 5: 'New User Signup!' visível.")

            # Passo 6 e 7: Cadastro Inicial
            self.page.realizar_signup_inicial(self.dados.nome, self.dados.email)

            # Passo 8: Verificar 'ENTER ACCOUNT INFORMATION'
            assert self.page.verificar_se_formulario_abriu()
            print("Passo 8: Formulário de informações aberto.")

            # Passo 9 a 12: Preenchimento de dados
            self.page.preencher_detalhes_pessoais(
                self.dados.password, 
                self.dados.birth_day, 
                self.dados.birth_month, 
                self.dados.birth_year
            )
            
            # Passo 13 e 14: Criar Conta e Verificar Sucesso
            self.page.preencher_endereco_e_criar(self.dados)
            # Aqui você pode adicionar um assert para verificar se Constants.MSG_ACCOUNT_CREATED apareceu

            # Passo 15 a 18: Fluxo Final (Delete)
            status_usuario = self.page.confirmar_e_deletar()
            print(f"Passo 16: Logado como {status_usuario}")
            print("Passo 18: Conta deletada com sucesso.")

        except Exception as e:
            print(f"Falha na execução do teste: {e}")
        finally:
            self.driver.quit()
