import pandas as pd
import torch
from pathlib import Path
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
)
from model import load_model, inference, CLASSES

LABELS_PATH = Path("dataset/evaluation_labels.csv")
IMAGE_DIR = Path("dataset/evaluation_images")
OUTPUT_PATH = Path("evaluation_results.csv")

def main():
    labels = pd.read_csv(LABELS_PATH)
    model = load_model()

    actual = []
    predicted = []
    rows = []

    for i, row in enumerate(labels.itertuples(index=False), start=1):
        image_id = row.id_code
        true_label = int(row.diagnosis)
        image_path = IMAGE_DIR / f"{image_id}.png"

        if not image_path.is_file():
            raise FileNotFoundError(f"Missing image: {image_path}")

        severity, prediction, probability = inference(model, str(image_path))

        actual.append(true_label)
        predicted.append(severity)
        rows.append({
            "id_code": image_id,
            "actual_grade": true_label,
            "predicted_grade": severity,
            "predicted_class": prediction,
            "predicted_probability": probability,
            "correct": true_label == severity,
        })

        if i % 25 == 0 or i == len(labels):
            print(f"Evaluated {i}/{len(labels)} images")

    accuracy = accuracy_score(actual, predicted)

    print("\n========== EVALUATION RESULTS ==========")
    print(f"Images evaluated: {len(actual)}")
    print(f"Accuracy: {accuracy:.2%}")

    print("\nClassification report:")
    print(classification_report(
        actual,
        predicted,
        labels=list(range(len(CLASSES))),
        target_names=CLASSES,
        zero_division=0,
        digits=4,
    ))

    print("Confusion matrix (rows = actual, columns = predicted):")
    print(confusion_matrix(actual, predicted, labels=list(range(len(CLASSES)))))

    pd.DataFrame(rows).to_csv(OUTPUT_PATH, index=False)
    print(f"\nIndividual predictions saved to: {OUTPUT_PATH}")
    print("\nNote: This is an experimental model evaluation, not clinical validation.")

if __name__ == "__main__":
    main()
