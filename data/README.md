# Data

`sample_traffic.csv` is synthetic and only exists for local testing.

Recommended structure for real datasets:

```text
data/
├── sample_traffic.csv
├── raw/
│   └── real_dataset.csv
└── external/
```

Keep large or license-restricted datasets out of Git. Place them under `data/raw/`
or `data/external/`, which are ignored by `.gitignore`.
