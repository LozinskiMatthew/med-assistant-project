import shutil
import os
import subprocess

from rag.config.paths import DOCTOR_DIALOGUE_PATH
from rag.src.general_exceptions import GeneralException
from rag.src.logger import get_logger
import zipfile




logger = get_logger(__name__)

class DataSourcing:
    def __init__(self, path=DOCTOR_DIALOGUE_PATH, target_folder="../datasets/doctor_dialogue"):
        self.path = path
        self.target_folder = target_folder

    def download_data_and_prepare_to_move(self):

        os.environ["KAGGLE_CONFIG_DIR"] = r"C:\Users\lozin\Desktop\RAG_Task_Solver\RAG" # Should put it in .env in future

        dataset_slug = "xuehaihe/medical-dialogue-dataset"
        zip_filename = "medical-dialogue-dataset.zip"
        temp_path = "temp_medical_dialogue"

        kaggle_path = r"C:\Users\lozin\anaconda3\envs\ML_REST\Scripts\kaggle.exe"

        subprocess.run([
            kaggle_path, "datasets", "download", "-d", dataset_slug
        ], check=True)

        os.makedirs(temp_path, exist_ok=True)

        with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
            zip_ref.extractall(temp_path)

        logger.info("Data was downloaded and extracted to temp folder.")
        return temp_path

    def move_and_remove(self):
        temp_path = self.download_data_and_prepare_to_move()
        os.makedirs(self.target_folder, exist_ok=True)

        for folder in os.listdir(temp_path):
            folder_path = os.path.join(temp_path, folder)
            if os.path.isdir(folder_path):
                for item in os.listdir(folder_path):
                    source = os.path.join(folder_path, item)
                    destination = os.path.join(self.target_folder, item)
                    if os.path.isdir(source):
                        shutil.copytree(source, destination, dirs_exist_ok=True)
                    else:
                        shutil.copy2(source, destination)
            else:
                source = folder_path
                destination = os.path.join(self.target_folder, folder)
                shutil.copy2(source, destination)

        shutil.rmtree(temp_path)
        if os.path.exists("medical-dialogue-dataset.zip"):
            os.remove("medical-dialogue-dataset.zip")

        logger.info(f"Dataset now only exists in: {os.path.abspath(self.target_folder)}")

    def run(self):
        try:
            logger.info("Data source started...")
            self.move_and_remove()
        except Exception as e:
            logger.error("Error while downloading and moving the data", e)
            raise GeneralException("Failed to properly download, and move the data to target destination {e}")

if __name__ == "__main__":
    data_source = DataSourcing()
    data_source.run()
