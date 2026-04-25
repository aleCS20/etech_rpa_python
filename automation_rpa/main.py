import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from py_compile import main

from src.modules.user import main as user_register_main

'''user = User()
user.getElementPage()
user.insertNewUser("Alessandro", "exemplo2@email.com")
user.fillFormNewUser("Alessandro", "Barbosa de Oliveira", "Rua 16, n 37", "Canada", "AM", "Manaus", 22, "921111-0000")
'''

user_register_main()

if __name__ == "__main__":
    main()

