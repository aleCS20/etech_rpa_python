import time

from src.tests.test_register_user import TestRegisterUser
from src.tests.test_login_user import TestLoginUser
from src.tests.test_login_user_incorret import TestLoginUserIncorrect
from src.tests.test_logout_user import TestLogoutUser
from src.tests.test_base import TestBase

def orquestrar_automacoes():
    sucesso_etapa = True
    driver = TestBase.get_driver()

    try:
        if sucesso_etapa:
            print("\n--- [1] Iniciando Registro ---")
            tc1 = TestRegisterUser()
            sucesso_etapa = tc1.executar_teste(deletar_ao_final=False)

        if sucesso_etapa:
            print("\n--- [4] Testando Logout ---")
            tc4 = TestLogoutUser()
            sucesso_etapa = tc4.executar_teste_logout()
            time.sleep(2)

        if sucesso_etapa:
            print("\n--- [2] Testando Login com Sucesso ---")
            tc2 = TestLoginUser()
            sucesso_etapa = tc2.executar_teste_login_sucesso(deletar_ao_final=False)

        print("\n--- [3] Testando Login Incorreto ---")
        tc3 = TestLoginUserIncorrect()
        tc3.executar_teste_login_email_incorreto()

        if sucesso_etapa:
            print("\n--- [LIMPEZA] Deletando conta de teste ---")
            from src.pages.login_page import LoginPage
            lp = LoginPage(driver)
            lp.deletar_conta()

    except Exception as e:
        print(f"🛑 Fluxo interrompido por erro crítico: {e}")
    finally:
        print("🏁 Finalizando WebDriver...")
        driver.quit()
    
if __name__ == "__main__":
    orquestrar_automacoes()

