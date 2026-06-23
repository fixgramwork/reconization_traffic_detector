from pathlib import Path

import joblib

from traffic_nb.predict import predict
from traffic_nb.train import train_model


def test_train_and_predict_round_trip(tmp_path: Path) -> None:
    model_path = tmp_path / "traffic_nb.joblib"
    output_path = tmp_path / "predictions.csv"

    train_model(
        data_path=Path("data/sample_traffic.csv"),
        label_column="label",
        model_out=model_path,
        test_size=0.25,
        random_state=42,
    )

    model_bundle = joblib.load(model_path)
    assert model_bundle["label_column"] == "label"
    assert "pipeline" in model_bundle

    predict(
        model_path=model_path,
        data_path=Path("data/sample_traffic.csv"),
        output_path=output_path,
    )

    assert output_path.exists()
    assert "prediction" in output_path.read_text()
