import time
from src.tests.test_register_user import TestRegisterUser
from src.tests.test_login_user import TestLoginUser

def orquestrar_automacoes():
    print("--- Iniciando AtividadeTest Case 1 ---")
    registro = TestRegisterUser()
    registro.executar_teste()

    print("⏳ Aguardando 5 segundos para o próximo Test Case ....")
    time.sleep(5)

    print("--- Iniciando Test Case 2 ---")
    login = TestLoginUser()
    login.executar_teste_login_sucesso()

if __name__ == "__main__":
    orquestrar_automacoes()
