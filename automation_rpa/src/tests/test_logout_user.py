from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from src.utils.constants import Constants
from src.data.mock_dados import MockDados
from src.pages.login_page import LoginPage

class TestLogoutUser:
    def __init__(self):
        self.service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=self.service)
        self.driver.maximize_window()
        
        self.login_page = LoginPage(self.driver)
        self.dados = MockDados()

    def executar_teste_logout(self):
        try:
            print(f"🚀 Acessando: {Constants.BASE_URL}")
            self.driver.get(Constants.BASE_URL)

            assert Constants.MSG_HOME_VISIBLE in self.driver.title
            print("✅ Passo 3: Home Page confirmada.")

            self.login_page.acessar_secao_autenticacao()
            print(f"🔑 Realizando login para logout: {self.dados.email}")
            self.login_page.realizar_login(self.dados.email, self.dados.password, slow=True)

            assert self.dados.nome in self.login_page.validar_usuario_logado()
            print("✅ Passo 8: Usuário logado com sucesso.")

            print("🚪 Realizando logout...")
            self.login_page.realizar_logout()

            assert self.login_page.verificar_se_sessao_login_visivel()
            print("✅ Passo 10: Logout confirmado, redirecionado para Login.")

        except Exception as e:
            self.login_page.save_screenshot("falha_test_case_4")
            print(f"❌ Erro durante o logout: {e}")
            raise e
        
        finally:
            self.driver.quit()

