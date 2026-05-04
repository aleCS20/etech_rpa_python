import time
from src.tests.test_register_user import TestRegisterUser
from src.tests.test_login_user import TestLoginUser
from src.tests.test_login_user_incorret import TestLoginUserIncorrect
from src.tests.test_logout_user import TestLogoutUser
def orquestrar_automacoes():
    print("--- Iniciando AtividadeTest Case 1 ---")
    registro = TestRegisterUser()
    registro.executar_teste()

    print("⏳ Aguardando 5 segundos para o próximo Test Case ....")
    time.sleep(5)

    print("--- Iniciando Test Case 2 ---")
    login = TestLoginUser()
    login.executar_teste_login_sucesso()

    print("⏳ Aguardando 5 segundos para o próximo Test Case ....")
    time.sleep(5)

    print("--- Iniciando Test Case 3 ---")
    login_incoreto = TestLoginUserIncorrect()
    login_incoreto.executar_teste_login_email_incorreto()

    print("⏳ Aguardando 5 segundos para o próximo Test Case ....")
    time.sleep(5)

    print("--- Iniciando Test Case 4: Logout ---")
    logout_test = TestLogoutUser()
    logout_test.executar_teste_logout()
    
if __name__ == "__main__":
    orquestrar_automacoes()

