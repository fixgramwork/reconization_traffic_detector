from __future__ import annotations

import argparse
from pathlib import Path

import joblib
import pandas as pd


def predict(model_path: Path, data_path: Path, output_path: Path) -> None:
    model_bundle = joblib.load(model_path)
    pipeline = model_bundle["pipeline"]
    label_column = model_bundle["label_column"]
    feature_columns = model_bundle["feature_columns"]

    data = pd.read_csv(data_path)
    missing_columns = [column for column in feature_columns if column not in data.columns]
    if missing_columns:
        raise ValueError(f"Input data is missing required columns: {missing_columns}")

    features = data[feature_columns]
    output = data.copy()
    output["prediction"] = pipeline.predict(features)

    if label_column in output.columns:
        output["is_correct"] = output[label_column] == output["prediction"]

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output.to_csv(output_path, index=False)
    print(f"Saved predictions to {output_path}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Predict labels with a saved traffic classifier.")
    parser.add_argument("--model", type=Path, required=True, help="Saved model artifact path.")
    parser.add_argument("--data", type=Path, required=True, help="CSV file to classify.")
    parser.add_argument("--output", type=Path, default=Path("predictions.csv"), help="Output CSV path.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    predict(model_path=args.model, data_path=args.data, output_path=args.output)


if __name__ == "__main__":
    main()
