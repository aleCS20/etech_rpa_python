import pyautogui
import time

class AimTrainer:
    def __init__(self, target_path: str = 'assets/alvo.png', start_button_path: str = 'assets/start.png'):
        self.target_path = target_path
        self.start_button_path = start_button_path
        
        pyautogui.PAUSE = 0.001

    def clicar_start(self, tentativas: int = 10) -> bool:
        print("Procurando botão 'Start' na tela...")
        for _ in range(tentativas):
            try:
                start_pos = pyautogui.locateCenterOnScreen(self.start_button_path, confidence=0.8)
                if start_pos is not None:
                    pyautogui.click(start_pos)
                    print("Botão Start clicado! O jogo vai começar...")
                    time.sleep(0.5)
                    return True
            except Exception:
                pass
            time.sleep(0.5)
        
        print("Aviso: Botão Start não detectado por imagem. Tentando prosseguir...")
        return False

    def executar_treinamento(self):
        print("Modo Master Ativado! Pressione CTRL+C para parar manualmente.")
        
        while True:
            try:
                alvo = pyautogui.locateCenterOnScreen(
                    self.target_path, 
                    confidence=0.75, 
                    grayscale=True
                )
                
                if alvo is not None:
                    pyautogui.click(alvo, alvo)
                    
            except (pyautogui.ImageNotFoundException, KeyboardInterrupt):
                pass
            except Exception:
                pass

