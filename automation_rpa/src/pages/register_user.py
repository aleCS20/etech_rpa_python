from selenium.webdriver.common.by import By
from .base_page import BasePage

class RegisterPage(BasePage):
    """
    Especialização da página de registro. - Test Case 1
    """
    # --------------------- Seletores da página ---------------------
    SIGNUP_LOGIN_LINK = (By.CSS_SELECTOR, "a[href='/login']")
    NEW_USER_TEXT     = (By.XPATH, "//h2[contains(text(), 'New User Signup!')]")
    
    NAME_FIELD        = (By.XPATH, "//input[@data-qa='signup-name']")
    EMAIL_FIELD       = (By.XPATH, "//input[@data-qa='signup-email']")
    SIGNUP_BTN        = (By.XPATH, "//button[@data-qa='signup-button']")

    ACCOUNT_INFO_TEXT = (By.XPATH, "//b[contains(text(), 'Enter Account Information')]")
    
    GENDER_MR_RADIO   = (By.ID, "id_gender1")
    PASSWORD_FIELD    = (By.ID, "password")
    DAYS_SELECT       = (By.ID, "days")
    MONTHS_SELECT     = (By.ID, "months")
    YEARS_SELECT      = (By.ID, "years")
    NEWSLETTER_CHECK  = (By.ID, "newsletter")
    SPECIAL_OFFERS_CHECK = (By.ID, "optin")

    FIRST_NAME_FIELD  = (By.ID, "first_name")
    LAST_NAME_FIELD   = (By.ID, "last_name")
    COMPANY_FIELD     = (By.ID, "company")
    ADDRESS1_FIELD    = (By.ID, "address1")
    COUNTRY_SELECT    = (By.ID, "country")
    STATE_FIELD       = (By.ID, "state")
    CITY_FIELD        = (By.ID, "city")
    ZIPCODE_FIELD     = (By.ID, "zipcode")
    MOBILE_FIELD      = (By.ID, "mobile_number")
    
    CREATE_ACCOUNT_BTN = (By.XPATH, "//button[@data-qa='create-account']")
    SUCCESS_TEXT       = (By.XPATH, "//b[contains(text(), 'Account Created!')]")
    CONTINUE_BTN       = (By.XPATH, "//a[@data-qa='continue-button']")

    LOGGED_IN_TEXT     = (By.XPATH, "//a[contains(text(), 'Logged in as')]")
    DELETE_ACCOUNT_BTN = (By.XPATH, "//a[@href='/delete_account']")
    DELETED_TEXT       = (By.XPATH, "//b[contains(text(), 'Account Deleted!')]")

    # ------------------ Métodos de Ação  ------------------
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
