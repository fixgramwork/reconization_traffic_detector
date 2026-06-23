# Malicious Traffic Naive Bayes Classifier

Naive Bayes baseline for classifying network traffic records as benign or malicious.

The project is intentionally small: it trains from a CSV file, saves a model artifact,
and can generate predictions for another CSV file. The included sample dataset is
synthetic and only exists to verify the pipeline.

## Project Layout

```text
.
├── data/
│   └── sample_traffic.csv
├── docs/
│   └── github-workflow.md
├── src/
│   └── traffic_nb/
│       ├── predict.py
│       └── train.py
├── tests/
│   └── test_pipeline.py
├── pyproject.toml
└── requirements.txt
```

## Local Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install -e .
```

## Train

```bash
python -m traffic_nb.train \
  --data data/sample_traffic.csv \
  --label-column label \
  --model-out artifacts/traffic_nb.joblib
```

Use your own dataset by passing a different CSV path:

```bash
python -m traffic_nb.train \
  --data data/raw/your_dataset.csv \
  --label-column label \
  --model-out artifacts/traffic_nb.joblib
```

## Predict

```bash
python -m traffic_nb.predict \
  --model artifacts/traffic_nb.joblib \
  --data data/sample_traffic.csv \
  --output predictions.csv
```

If the input CSV includes the label column, prediction output will keep it for comparison.

## Test

```bash
pytest
```

## First GitHub Push

After creating an empty GitHub repository, run:

```bash
git remote add origin https://github.com/YOUR_USERNAME/malicious-traffic-naive-bayes.git
git branch -M main
git push -u origin main
```

See [docs/github-workflow.md](docs/github-workflow.md) for suggested issues and commits.
