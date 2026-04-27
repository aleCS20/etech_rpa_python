import time
import os

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from datetime import datetime

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 15)
    
    def find_element(self, locator):
        try:
            return self.wait.until(EC.visibility_of_element_located(locator))
        except TimeoutException:
            print(f"Erro: Elemento com seletor {locator} não foi encontrado!!")
            raise
    
    def click(self, locator):
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()
    
    def write(self, locator, text, slow=False):
        element = self.find_element(locator)
        element.clear()
        if slow:
            for char in text:
                element.send_keys(char)
                time.sleep(0.1)
        else:
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

    def select_dropdown_by_text(self, locator, text):
        from selenium.webdriver.support.ui import Select
        
        select = Select(self.find_element(locator))
        select.select_by_visible_text(text)
    
    def save_screenshot(self, name="erro"):
        """Salva um print da tela atual na pasta /logs caso não exista será criada"""
        
        if not os.path.exists("logs"):
            os.makedirs("logs")
            
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filepath = f"logs/{name}_{timestamp}.png"
        self.driver.save_screenshot(filepath)
        print(f"📸 Screenshot salvo em: {filepath}")

