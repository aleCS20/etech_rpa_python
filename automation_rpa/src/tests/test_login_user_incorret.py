from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from src.data.mock_dados import MockDados
from src.pages.login_page import LoginPage
from src.utils.constants import Constants
from src.pages.login_incorrect_page import LoginIncorrectPage

class TestLoginUserIncorrect:
    def __init__(self):
        self.service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=self.service)
        self.driver.maximize_window()
    
        self.login_page = LoginIncorrectPage(self.driver)
        self.dados = MockDados()

    def executar_teste_login_email_incorreto(self):
        try:
            print(f"🚀 Acessando: {Constants.BASE_URL}")
            self.driver.get(Constants.BASE_URL)

            assert Constants.MSG_HOME_VISIBLE in self.driver.title
            print("✅ Passo 3: Home Page confirmada.")

            self.login_page.acessar_secao_autenticacao()
            
            print(f"🔑 Tentando login incorreto com: {self.dados.email_incorret}")
            self.login_page.realizar_login(
                self.dados.email_incorret, 
                self.dados.password_incorret, 
                slow=True
            )

            msg_erro = self.login_page.verificar_mensagem_erro_email_senha()
            assert Constants.MSG_INCORRECT_LOGIN in msg_erro
            print(f"✅ Passo 7: Mensagem de erro validada: {msg_erro}")

        except Exception as e:
            self.login_page.save_screenshot("falha_test_case_3")
            print(f"❌ Erro durante a execução: {e}")
            raise e
            
        finally:
            self.driver.quit()



