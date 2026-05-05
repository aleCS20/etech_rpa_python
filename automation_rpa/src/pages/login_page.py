from .base_page import BasePage
from src.utils.locators import LoginLocators, RegisterLocators

class LoginPage(BasePage):
    def acessar_secao_autenticacao(self):
        self.click(RegisterLocators.SIGNUP_LOGIN_LINK)
    
    def verificar_se_sessao_login_visivel(self):
        return self.is_visible(LoginLocators.LOGIN_SECTION_TEXT)

    def realizar_login(self, email, senha, slow=False):
        self.write(LoginLocators.EMAIL_INPUT, email, slow=slow)
        self.write(LoginLocators.PASSWORD_INPUT, senha, slow=slow)
        self.click(LoginLocators.LOGIN_BTN)
    
    def validar_usuario_logado(self):
        return self.get_text(LoginLocators.LOGGED_IN_TEXT)
    
    def deletar_conta(self):
        self.click(LoginLocators.DELETE_ACCOUNT_BTN)
        confirmacao = self.get_text(LoginLocators.DELETED_TEXT)
        return confirmacao
    
    def realizar_logout(self):
        self.click(LoginLocators.LOGOUT_BTN)
    
