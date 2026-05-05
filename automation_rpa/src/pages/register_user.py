from selenium.webdriver.common.by import By
from .base_page import BasePage
from src.utils.locators import RegisterLocators

class RegisterPage(BasePage):
    
    def ir_para_login_signup(self):
        self.click(RegisterLocators.SIGNUP_LOGIN_LINK)

    def verificar_texto_novo_usuario(self):
        return self.get_text(RegisterLocators.NEW_USER_TEXT)

    def realizar_signup_inicial(self, nome, email, slow=False):
        self.write(RegisterLocators.NAME_FIELD, nome, slow=False)
        self.write(RegisterLocators.EMAIL_FIELD, email, slow=False)
        self.click(RegisterLocators.SIGNUP_BTN)

    def verificar_se_formulario_abriu(self):
        return self.is_visible(RegisterLocators.ACCOUNT_INFO_TEXT)

    def preencher_detalhes_pessoais(self, senha, dia, mes, ano):
        self.click(RegisterLocators.GENDER_MR_RADIO)
        self.write(RegisterLocators.PASSWORD_FIELD, senha)
        self.select_dropdown_by_value(RegisterLocators.DAYS_SELECT, dia)
        self.select_dropdown_by_text(RegisterLocators.MONTHS_SELECT, mes)
        self.select_dropdown_by_value(RegisterLocators.YEARS_SELECT, ano)
        #self.click(RegisterLocators.NEWSLETTER_CHECK)
        #self.click(RegisterLocators.SPECIAL_OFFERS_CHECK)

        self.force_click(RegisterLocators.NEWSLETTER_CHECK)
        self.force_click(RegisterLocators.SPECIAL_OFFERS_CHECK)


    def preencher_endereco_e_criar(self, mock):
        self.write(RegisterLocators.FIRST_NAME_FIELD, mock.first_name)
        self.write(RegisterLocators.LAST_NAME_FIELD, mock.last_name)
        self.write(RegisterLocators.COMPANY_FIELD, mock.company)
        self.write(RegisterLocators.ADDRESS1_FIELD, mock.address1)
        self.select_dropdown_by_value(RegisterLocators.COUNTRY_SELECT, mock.country)
        self.write(RegisterLocators.STATE_FIELD, mock.state)
        self.write(RegisterLocators.CITY_FIELD, mock.city)
        self.write(RegisterLocators.ZIPCODE_FIELD, mock.zipcode)
        self.write(RegisterLocators.MOBILE_FIELD, mock.mobile_number)
        self.click(RegisterLocators.CREATE_ACCOUNT_BTN)

    def confirmar_e_deletar(self):
        self.click(RegisterLocators.CONTINUE_BTN)
        
        user_status = self.get_text(RegisterLocators.LOGGED_IN_TEXT)
        self.click(RegisterLocators.DELETE_ACCOUNT_BTN)
        return user_status
