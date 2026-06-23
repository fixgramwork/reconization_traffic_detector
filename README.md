# 악성 트래픽 나이브 베이즈 분류기

네트워크 트래픽 레코드를 정상(`benign`) 또는 악성(`malicious`)으로 분류하는
나이브 베이즈 기반 실험 프로젝트입니다.

CSV 데이터로 모델을 학습하고, 학습된 모델을 `joblib` 파일로 저장한 뒤,
다른 CSV 데이터에 대한 예측 결과를 생성할 수 있습니다. 포함된 샘플 데이터는
파이프라인 확인용 합성 데이터입니다.

## 프로젝트 구조

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

## 로컬 설정

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install -e .
```

## 학습

```bash
python -m traffic_nb.train \
  --data data/sample_traffic.csv \
  --label-column label \
  --model-out artifacts/traffic_nb.joblib
```

다른 CSV 파일을 사용하려면 `--data` 경로를 바꾸면 됩니다.

```bash
python -m traffic_nb.train \
  --data data/raw/your_dataset.csv \
  --label-column label \
  --model-out artifacts/traffic_nb.joblib
```

## 예측

```bash
python -m traffic_nb.predict \
  --model artifacts/traffic_nb.joblib \
  --data data/sample_traffic.csv \
  --output predictions.csv
```

입력 CSV에 실제 라벨 컬럼이 있으면, 예측 결과 파일에 정답 비교용 컬럼도 함께
저장됩니다.

## 테스트

```bash
pytest
```

## GitHub에 처음 올리기

빈 GitHub 저장소를 만든 뒤 아래 명령어를 실행합니다.

```bash
git remote add origin https://github.com/YOUR_USERNAME/malicious-traffic-naive-bayes.git
git branch -M main
git push -u origin main
```

이슈와 커밋 흐름 예시는 [docs/github-workflow.md](docs/github-workflow.md)를 참고합니다.
