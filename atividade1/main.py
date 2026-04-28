import logging
import time
from queue import Queue, Empty
from threading import Thread, Lock

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


URL = "https://digital.detran.am.gov.br/site/apps/veiculo/filtroplacarenavam-consultaveiculo.jsp"
MAX_RETRY = 2
NUM_WORKERS = 1


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

queue = Queue()
results = []
results_lock = Lock()


vehicles = [
    {"placa": "JXG5062", "renavam": "00910227160"},
    {"placa": "ABC1234", "renavam": "12345678901"},
]


def create_task(placa: str, renavam: str) -> dict:
    return {
        "placa": placa,
        "renavam": renavam,
        "status": "PENDING",
        "attempts": 0,
        "error": None,
        "result": None,
    }


def create_driver():
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless=new")  # descomente depois, quando quiser rodar sem abrir janela
    return webdriver.Chrome(service=service, options=options)


def fill_and_submit(driver, placa: str, renavam: str):
    driver.get(URL)

    wait = WebDriverWait(driver, 20)

    placa_input = wait.until(
        EC.presence_of_element_located((By.XPATH, "//input[contains(@name,'placa') or contains(@id,'placa')]"))
    )
    renavam_input = wait.until(
        EC.presence_of_element_located((By.XPATH, "//input[contains(@name,'renavam') or contains(@id,'renavam')]"))
    )
    consultar_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//input[@value='Consultar'] | //button[contains(., 'Consultar')]"))
    )

    placa_input.clear()
    placa_input.send_keys(placa)

    renavam_input.clear()
    renavam_input.send_keys(renavam)

    consultar_button.click()


    return {
        "title": driver.title,
        "current_url": driver.current_url,
    }


def process_task(driver, task: dict):
    logging.info(f"Processando placa={task['placa']} renavam={task['renavam']}")
    task["status"] = "PROCESSING"

    result = fill_and_submit(driver, task["placa"], task["renavam"])

    task["status"] = "DONE"
    task["result"] = result
    logging.info(f"Concluído: {task['placa']}")


def worker(worker_id: int):
    driver = create_driver()

    try:
        while True:
            try:
                task = queue.get(timeout=1)
            except Empty:
                return

            try:
                process_task(driver, task)

                with results_lock:
                    results.append(task)

            except Exception as e:
                task["attempts"] += 1
                task["error"] = str(e)

                logging.error(
                    f"Erro no worker={worker_id} placa={task['placa']} tentativa={task['attempts']} erro={e}"
                )

                if task["attempts"] <= MAX_RETRY:
                    task["status"] = "RETRY"
                    queue.put(task)
                    logging.info(f"Reenfileirada: {task['placa']}")
                else:
                    task["status"] = "FAILED"
                    with results_lock:
                        results.append(task)
                    logging.error(f"Falha definitiva: {task['placa']}")

            finally:
                queue.task_done()

    finally:
        driver.quit()


def main():
    for v in vehicles:
        queue.put(create_task(v["placa"], v["renavam"]))

    threads = []
    for i in range(NUM_WORKERS):
        t = Thread(target=worker, args=(i + 1,), daemon=True)
        t.start()
        threads.append(t)

    queue.join()

    print("\n=== RESULTADOS FINAIS ===")
    for item in results:
        print(
            item["placa"],
            item["renavam"],
            item["status"],
            f"tentativas={item['attempts']}",
            f"erro={item['error']}"
        )


if __name__ == "__main__":
    main()