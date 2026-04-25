import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from py_compile import main
from utils_constants.constants import URL
from src.data.mock_dados import dados

class User:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://automationexercise.com/")
        
    def getElementPage(self):
        element = self.driver.find_element(By.XPATH, "/html/body/header/div/div/div/div[1]/div/a/img")
        time.sleep(3)
        print("A página foi carregada corretamente!")
        login = self.getLoginClik()

    def getLoginClik(self):
        element = self.driver.find_element(By.XPATH, "/html/body/header/div/div/div/div[2]/div/ul/li[4]/a")
        time.sleep(2)
        print(element.text)
        element.click()
        capture = self.verifyNewUserVisible()

    def verifyNewUserVisible(self):
        element = self.driver.find_element(By.XPATH, "/html/body/section/div/div/div[3]/div/h2")
        time.sleep(2)
        print(element.text)
    
    def insertNewUser(self, name, email):
        input_name = self.driver.find_element(By.XPATH, "/html/body/section/div/div/div[3]/div/form/input[2]")
        input_name.send_keys(name)

        input_email = self.driver.find_element(By.XPATH, "/html/body/section/div/div/div[3]/div/form/input[3]")
        input_email.send_keys(email)

        time.sleep(2)
        print(name, email)
        input_button = self.driver.find_element(By.XPATH, "/html/body/section/div/div/div[3]/div/form/button").click()
    
    def fillFormNewUser(self, name, last_name, endereco, pais, estado, cidade, codigo, numberTel):
        element = self.driver.find_element(By.XPATH, "/html/body/section/div/div/div/div/h2/b")
        time.sleep(2)
        print(element.text)

        time.sleep(2)
        password = self.driver.find_element(By.XPATH, '//*[@id="password"]')
        password.send_keys("ja097-12")

        first_name = self.driver.find_element(By.XPATH, '//*[@id="first_name"]')
        first_name.send_keys(name)

        last_name = self.driver.find_element(By.XPATH, '//*[@id="last_name"]')
        last_name.send_keys("Barbosa de Oliveira")

        address = self.driver.find_element(By.XPATH, '//*[@id="address1"]')
        address.send_keys(endereco)

        find_country = self.driver.find_element(By.ID, "country")
        
        
        state = self.driver.find_element(By.ID, "state")
        state.send_keys(estado)

        city = self.driver.find_element(By.ID, "city")
        city.send_keys(cidade)

        codigo = self.driver.find_element(By.ID, "zipcode")
        codigo.send_keys(codigo)

        Telephone = self.driver.find_element(By.ID, "mobile_number")
        Telephone.send_keys(numberTel)

        input_button = self.driver.find_element(By.XPATH, '/html/body/section/div/div/div/div/form/button').click()

        time.sleep(3)

user = User()
user.getElementPage()

if __name__ == "__main__":
    main()

