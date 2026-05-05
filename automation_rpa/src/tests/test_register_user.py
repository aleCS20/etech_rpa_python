from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from .test_base import BaseTest

from src.utils.constants import Constants
from src.data.mock_dados import MockDados
from src.pages.register_user import RegisterPage

class TestRegisterUser(BaseTest):
    def __init__(self):
        super().__init__()
        self.page = RegisterPage(self.driver)

    def executar_teste(self, deletar_ao_final=True):
        try:
            print("\n--- Iniciando Teste: Register User ---")
            self.driver.get(Constants.BASE_URL)
            
            assert Constants.MSG_HOME_VISIBLE in self.driver.title
            print("✅ Passo 3: Home Page visível.")

            self.page.ir_para_login_signup()
            texto_signup = self.page.verificar_texto_novo_usuario()
            assert Constants.MSG_NEW_USER_SIGNUP in texto_signup
            print("✅ Passo 5: 'New User Signup!' visível.")

            self.page.realizar_signup_inicial(self.dados.nome, self.dados.email, slow=True)

            assert self.page.verificar_se_formulario_abriu()
            print("✅ Passo 8: Formulário de informações aberto.")

            self.page.preencher_detalhes_pessoais(
                self.dados.password, 
                self.dados.birth_day, 
                self.dados.birth_month, 
                self.dados.birth_year,
                slow=True
            )
            
            self.page.preencher_endereco_e_criar(self.dados, slow=True)
            print("✅ Passo 14: Conta criada com sucesso.")

            if deletar_ao_final:
                status_usuario = self.page.confirmar_e_deletar()
                print(f"✅ Passo 16: Logado como {status_usuario}")
                print("✅ Passo 18: Conta deletada com sucesso.")
            else:
                from src.utils.locators import LoginLocators
                self.page.click(LoginLocators.CONTINUE_BTN)
                print("ℹ️ Conta mantida para os próximos testes.")

            return True

        except Exception as e:
            self.page.save_screenshot("falha_teste_register")
            print(f"❌ Falha na execução do teste: {e}")
            return False
