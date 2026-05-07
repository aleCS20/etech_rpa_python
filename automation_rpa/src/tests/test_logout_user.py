from .test_base import TestBase
from src.utils.constants import Constants
from src.pages.login_page import LoginPage

class TestLogoutUser(TestBase):
    def __init__(self):
        super().__init__()
        self.login_page = LoginPage(self.driver)

    def executar_teste_logout(self):
        print(f"\n--- Iniciando Test Case 4: Logout ---")
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
        
        return True
