from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from src.utils.constants import Constants
from src.data.mock_dados import MockDados
from src.pages.register_user import RegisterPage

class TestRegister:
    def __init__(self):
        # Configuração do WebDriver
        self.service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=self.service)
        self.driver.maximize_window()
        
        self.page = RegisterPage(self.driver)
        self.dados = MockDados()

    def executar_teste(self):
        try:
            # Iniciar o navegador
            print("Iniciando Teste: Register User")
            self.driver.get(Constants.URL)
            
            # Verificar a Home Page se abriu corretamente
            assert Constants.MSG_HOME_VISIBLE in self.driver.title
            print("Passo 3: Home Page visível.")

            # Ativar/clicar em Login/Signup
            self.page.ir_para_login_signup()
            texto_signup = self.page.verificar_texto_novo_usuario()
            assert Constants.MSG_NEW_USER_SIGNUP in texto_signup
            print("Passo 5: 'New User Signup!' visível.")

            # Pré-Cadastro Inicial com nome e e-mail
            self.page.realizar_signup_inicial(self.dados.nome, self.dados.email, slow=True)

            # Verificar erro de -> 'ENTER ACCOUNT INFORMATION'
            assert self.page.verificar_se_formulario_abriu()
            print("Passo 8: Formulário de informações aberto.")

            # Preenchimento de dados do formulário
            self.page.preencher_detalhes_pessoais(
                self.dados.password, 
                self.dados.birth_day, 
                self.dados.birth_month, 
                self.dados.birth_year
            )
            
            # Criar Conta e Verificar se tudo ocorreu com Sucesso
            self.page.preencher_endereco_e_criar(self.dados)

            # Finalizar conta -> (Delete)
            status_usuario = self.page.confirmar_e_deletar()
            print(f"Passo 16: Logado como {status_usuario}")
            print("Passo 18: Conta deletada com sucesso.")

        except Exception as e:
            self.page.save_screenshot("falha_teste_register")
            print(f"Falha na execução do teste: {e}")
        finally:
            self.driver.quit()
