from .test_base import TestBase
from src.utils.constants import Constants
from src.pages.login_page import LoginPage

class TestLoginUser(TestBase):
    def __init__(self):
        super().__init__()
        self.login_page = LoginPage(self.driver)

    def executar_teste_login_sucesso(self, deletar_ao_final=True):
        print(f"\n--- Iniciando Test Case 2: Login Sucesso ---")
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

        if deletar_ao_final:
            print("🗑️ Iniciando exclusão da conta...")
            msg_delecao = self.login_page.deletar_conta()
            assert Constants.MSG_ACCOUNT_DELETED.upper() in msg_delecao.upper()
            print("🏆 Test Case 2 concluído com sucesso (ambiente limpo).")
        else:
            print("ℹ️ Login validado. Mantendo sessão ativa.")

        return True
