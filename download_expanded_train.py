import subprocess
import pandas as pd
from pathlib import Path

labels = pd.read_csv("dataset/expanded_train_labels.csv")
output_dir = Path("dataset/expanded_train_images")
output_dir.mkdir(parents=True, exist_ok=True)

for i, row in enumerate(labels.itertuples(index=False), start=1):
    image_id = row.id_code
    image_path = output_dir / f"{image_id}.png"

    if image_path.exists() and image_path.stat().st_size > 0:
        print(f"[{i}/{len(labels)}] Already downloaded: {image_id}")
        continue

    if image_path.exists():
        image_path.unlink()

    print(f"[{i}/{len(labels)}] Downloading: {image_id}", flush=True)

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
            stdout=subprocess.DEVNULL,
        )
        zip_path.unlink()

    if not image_path.exists() or image_path.stat().st_size == 0:
        raise RuntimeError(f"Download failed or empty image: {image_id}")

print(f"\nFinished. Requested images: {len(labels)}")
print(f"Output folder: {output_dir}")
