from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from src.data.mock_dados import MockDados

class TestBase:
    _driver = None

    @classmethod
    def get_driver(cls):
        if cls._driver is None:
            service = Service(ChromeDriverManager().install())
            cls._driver = webdriver.Chrome(service=service)
            cls._driver.maximize_window()
        return cls._driver

    def __init__(self):
        self.driver = self.get_driver()
        self.dados = MockDados()
