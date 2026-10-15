
from huggingface_hub import hf_hub_download
from pathlib import Path
import shutil

REPO_ID = "Melkin07/retinal-ai-dr-classifier"
FILENAME = "classifier_improved.pt"

PROJECT_DIR = Path(__file__).resolve().parent
DESTINATION = PROJECT_DIR / FILENAME


def download_model():
    print("Downloading Retinal AI model...")

    downloaded_file = hf_hub_download(
        repo_id=REPO_ID,
        filename=FILENAME,
        repo_type="model",
    )

    if Path(downloaded_file).resolve() != DESTINATION.resolve():
        shutil.copy2(downloaded_file, DESTINATION)

    print(f"Model saved to: {DESTINATION}")


if __name__ == "__main__":
    download_model()
