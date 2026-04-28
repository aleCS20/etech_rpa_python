import csv
import os

class DataPersistence:
    @staticmethod
    def save_to_csv(data, folder_name, filename):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.abspath(os.path.join(current_dir, ".."))
        target_folder = os.path.join(project_root, folder_name)

        if (not os.path.exists(target_folder)):
            os.makedirs(target_folder)
            
        target_path = os.path.join(target_folder, filename)
        
        fieldnames = ["id", "nome", "preco", "link"]
        
        with open(target_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
            
        print(f"✅ Arquivo salvo com sucesso em: {target_path}")


