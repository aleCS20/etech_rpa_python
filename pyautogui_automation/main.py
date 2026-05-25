import pyautogui
from time import sleep

def main():
    while True:
        try:
            ball = pyautogui.locateOnScreen('assets/blue_ball.png', confidence=0.8, grayscale=True)
            pyautogui.mouseDown(ball, duration=1)
            print('encontrou o elemento')
        except:
            print('elemento não encontrado')

        sleep(1)

if __name__ == "__main__":
    main()
