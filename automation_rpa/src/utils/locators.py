from selenium.webdriver.common.by import By

class RegisterLocators:

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

class LoginLocators:

    LOGIN_SECTION_TEXT = (By.XPATH, "//h2[contains(text(), 'Login to your account')]")
    EMAIL_INPUT        = (By.XPATH, "//input[@data-qa='login-email']")
    PASSWORD_INPUT     = (By.XPATH, "//input[@data-qa='login-password']")
    LOGIN_BTN          = (By.XPATH, "//button[@data-qa='login-button']")
    
    LOGGED_IN_TEXT     = (By.XPATH, "//a[contains(text(), 'Logged in as')]")
    DELETE_ACCOUNT_BTN = (By.XPATH, "//a[@href='/delete_account']")
    DELETED_TEXT       = (By.XPATH, "//b[contains(text(), 'Account Deleted!')]")
    CONTINUE_BTN       = (By.XPATH, "//a[@data-qa='continue-button']")

    LOGIN_INCORRET = (By.XPATH, "//p[contains(text(), 'Your email or password is incorrect!')]")
    
    LOGOUT_BTN = (By.XPATH, "//a[@href='/logout']")
    