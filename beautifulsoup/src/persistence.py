import csv
import os

class DataPersistence:
    @staticmethod
    def save_to_csv(data, folder_name, filename):
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        target_dir = os.path.join(base_path, folder_name)

        os.makedirs(target_dir, exist_ok=True)
        path = os.path.join(target_dir, filename)

        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["id", "nome", "preco", "link"])
            writer.writeheader()
            writer.writerows(data)
        
        print(f" Dados salvos com sucesso: {path}")


