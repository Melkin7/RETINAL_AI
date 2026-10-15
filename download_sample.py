import subprocess
import pandas as pd
from pathlib import Path

df = pd.read_csv("dataset/sample_train.csv")
output_dir = Path("dataset/train_images")
output_dir.mkdir(parents=True, exist_ok=True)

for i, row in enumerate(df.itertuples(index=False), start=1):
    image_id = row.id_code
    image_path = output_dir / f"{image_id}.png"

    if image_path.exists():
        print(f"[{i}/100] Already downloaded: {image_id}")
        continue

    print(f"[{i}/100] Downloading: {image_id}")

    subprocess.run(
        [
            "kaggle", "competitions", "download",
            "-c", "aptos2019-blindness-detection",
            "-f", f"train_images/{image_id}.png",
            "-p", str(output_dir),
        ],
        check=True,
    )

    zip_path = output_dir / f"{image_id}.png.zip"
    if zip_path.exists():
        subprocess.run(
            ["unzip", "-o", str(zip_path), "-d", str(output_dir)],
            check=True,
        )
        zip_path.unlink()

print("\nFinished downloading the selected sample.")
