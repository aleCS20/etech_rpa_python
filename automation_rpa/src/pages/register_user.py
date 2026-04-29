from selenium.webdriver.common.by import By
from .base_page import BasePage

class RegisterPage(BasePage):
    
    def ir_para_login_signup(self):
        self.click(self.SIGNUP_LOGIN_LINK)

    def verificar_texto_novo_usuario(self):
        return self.get_text(self.NEW_USER_TEXT)

    def realizar_signup_inicial(self, nome, email):
        self.write(self.NAME_FIELD, nome)
        self.write(self.EMAIL_FIELD, email)
        self.click(self.SIGNUP_BTN)

    def verificar_se_formulario_abriu(self):
        return self.is_visible(self.ACCOUNT_INFO_TEXT)

    def preencher_detalhes_pessoais(self, senha, dia, mes, ano):
        self.click(self.GENDER_MR_RADIO)
        self.write(self.PASSWORD_FIELD, senha)
        self.select_dropdown_by_value(self.DAYS_SELECT, dia)
        self.select_dropdown_by_text(self.MONTHS_SELECT, mes)
        self.select_dropdown_by_value(self.YEARS_SELECT, ano)
        self.click(self.NEWSLETTER_CHECK)
        self.click(self.SPECIAL_OFFERS_CHECK)

    def preencher_endereco_e_criar(self, mock):
        self.write(self.FIRST_NAME_FIELD, mock.first_name)
        self.write(self.LAST_NAME_FIELD, mock.last_name)
        self.write(self.COMPANY_FIELD, mock.company)
        self.write(self.ADDRESS1_FIELD, mock.address1)
        self.select_dropdown_by_value(self.COUNTRY_SELECT, mock.country)
        self.write(self.STATE_FIELD, mock.state)
        self.write(self.CITY_FIELD, mock.city)
        self.write(self.ZIPCODE_FIELD, mock.zipcode)
        self.write(self.MOBILE_FIELD, mock.mobile_number)
        self.click(self.CREATE_ACCOUNT_BTN)

    def confirmar_e_deletar(self):
        self.click(self.CONTINUE_BTN)
        
        user_status = self.get_text(self.LOGGED_IN_TEXT)
        self.click(self.DELETE_ACCOUNT_BTN)
        return user_status
