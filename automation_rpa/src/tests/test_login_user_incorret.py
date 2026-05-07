from .test_base import TestBase
from src.pages.login_incorrect_page import LoginIncorrectPage
from src.utils.constants import Constants

class TestLoginUserIncorrect(TestBase):
    def __init__(self):
        super().__init__()
        self.login_page = LoginIncorrectPage(self.driver)

    def executar_teste_login_email_incorreto(self):
        print(f"\n--- Iniciando Test Case 3: Login Incorreto ---")
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
        
        return True
    