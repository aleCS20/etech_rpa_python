from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 15)
    
    def find_element(self, locator):
        try:
            return self.wait.until(EC.visibility_of_element_located(locator))
        except TimeoutException:
            print(f"Erro: Elemento com seletor {locator} não foi encontrado no tempo esperado.")
            raise
    
    def click(self, locator):
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()
    
    def write(self, locator, text):
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)
    
    def get_text(self, locator):
        return self.find_element(locator).text

    def is_visible(self, locator):
        try:
            return self.find_element(locator).is_displayed()
        except:
            return False
    
    def select_dropdown_by_value(self, locator, value):
        from selenium.webdriver.support.ui import Select
        
        select = Select(self.find_element(locator))
        select.select_by_value(value)
    
