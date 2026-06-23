from __future__ import annotations

import argparse
from pathlib import Path

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


def build_pipeline(features: pd.DataFrame) -> Pipeline:
    numeric_columns = features.select_dtypes(include=["number", "bool"]).columns.tolist()
    categorical_columns = [column for column in features.columns if column not in numeric_columns]

    transformers = []
    if numeric_columns:
        transformers.append(
            (
                "numeric",
                Pipeline(
                    steps=[
                        ("imputer", SimpleImputer(strategy="median")),
                        ("scaler", StandardScaler()),
                    ]
                ),
                numeric_columns,
            )
        )
    if categorical_columns:
        transformers.append(
            (
                "categorical",
                Pipeline(
                    steps=[
                        ("imputer", SimpleImputer(strategy="most_frequent")),
                        ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
                    ]
                ),
                categorical_columns,
            )
        )

    if not transformers:
        raise ValueError("No usable feature columns found.")

    return Pipeline(
        steps=[
            ("preprocess", ColumnTransformer(transformers=transformers)),
            ("classifier", GaussianNB()),
        ]
    )


def load_dataset(path: Path, label_column: str) -> tuple[pd.DataFrame, pd.Series]:
    data = pd.read_csv(path)
    if label_column not in data.columns:
        raise ValueError(f"Label column '{label_column}' was not found in {path}.")

    features = data.drop(columns=[label_column])
    labels = data[label_column]
    return features, labels


def train_model(
    data_path: Path,
    label_column: str,
    model_out: Path,
    test_size: float,
    random_state: int,
) -> None:
    features, labels = load_dataset(data_path, label_column)

    stratify = labels if labels.nunique() > 1 else None
    train_features, test_features, train_labels, test_labels = train_test_split(
        features,
        labels,
        test_size=test_size,
        random_state=random_state,
        stratify=stratify,
    )

    pipeline = build_pipeline(train_features)
    pipeline.fit(train_features, train_labels)

    predictions = pipeline.predict(test_features)
    print(f"Accuracy: {accuracy_score(test_labels, predictions):.4f}")
    print("\nClassification report:")
    print(classification_report(test_labels, predictions, zero_division=0))
    print("Confusion matrix:")
    print(confusion_matrix(test_labels, predictions))

    model_out.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(
        {
            "pipeline": pipeline,
            "label_column": label_column,
            "feature_columns": features.columns.tolist(),
        },
        model_out,
    )
    print(f"\nSaved model to {model_out}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train a Naive Bayes traffic classifier.")
    parser.add_argument("--data", type=Path, required=True, help="Training CSV path.")
    parser.add_argument("--label-column", default="label", help="Name of the label column.")
    parser.add_argument(
        "--model-out",
        type=Path,
        default=Path("artifacts/traffic_nb.joblib"),
        help="Path for the saved model artifact.",
    )
    parser.add_argument("--test-size", type=float, default=0.25, help="Validation split ratio.")
    parser.add_argument("--random-state", type=int, default=42, help="Random seed.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    train_model(
        data_path=args.data,
        label_column=args.label_column,
        model_out=args.model_out,
        test_size=args.test_size,
        random_state=args.random_state,
    )


if __name__ == "__main__":
    main()
