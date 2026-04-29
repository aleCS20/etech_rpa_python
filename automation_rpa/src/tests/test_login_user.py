from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from src.utils.constants import Constants
from src.data.mock_dados import MockDados
from src.pages.login_page import LoginPage

class TestLoginUser:
    def __init__(self):
        self.service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=self.service)
        self.driver.maximize_window()
    
        self.login_page = LoginPage(self.driver)
        self.dados = MockDados()
    
    def executar_teste_login_sucesso(self):

        try:
            print(f"🚀 Acessando: {Constants.BASE_URL}")
            self.driver.get(Constants.BASE_URL)

            assert Constants.MSG_HOME_VISIBLE in self.driver.title
            print("✅ Passo 3: Home Page confirmada.")

            self.login_page.acessar_secao_autenticacao()

            assert self.login_page.verificar_se_sessao_login_visivel()
            print("✅ Passo 5: Seção de Login visível.")

            print(f"🔑 Realizando login para: {self.dados.email}")
            self.login_page.realizar_login(
                self.dados.email, 
                self.dados.password, 
                slow=True
            )

            status_usuario = self.login_page.validar_usuario_logado()
            assert self.dados.nome in status_usuario
            print(f"✅ Passo 8: Confirmado - {status_usuario}")

            print("🗑️ Iniciando exclusão da conta...")
            msg_delecao = self.login_page.deletar_conta()
            assert Constants.MSG_ACCOUNT_DELETED.upper() in msg_delecao.upper()
            print("🏆 Test Case 2 concluído com sucesso!")

        except Exception as e:
            self.login_page.save_screenshot("falha_test_case_2")
            print(f"❌ Erro durante a execução: {e}")
            raise e
        
        finally:
            # Encerramento do driver
            self.driver.quit()
        
if __name__ == "__main__":
    teste = TestLoginUser()
    teste.executar_teste_login_sucesso()