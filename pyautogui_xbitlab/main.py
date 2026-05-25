from src.pages.navegador_page import NavegadorPage
from src.pages.aim_trainer import AimTrainer

def main():
    url_jogo = 'https://www.xbitlabs.com/aim-trainer/'
    
    navegador = NavegadorPage()
    bot_mira = AimTrainer(
        target_path='assets/alvo.png', 
        start_button_path='assets/start.png'
    )
    
    try:
        navegador.iniciar_jogo(url_jogo)
    
        bot_mira.clicar_start()
        
        bot_mira.executar_treinamento()
        
    except KeyboardInterrupt:
        print("\nAutomação encerrada pelo usuário.")
    finally:
        print("Finalizando processos...")
        navegador.fechar()

if __name__ == "__main__":
    main()

