# GitHub Workflow

## Suggested Issues

Start with small issues that each produce one clear change.

1. Project bootstrap
   - Goal: create package layout, dependency files, README, and sample data.
   - Done when: a new contributor can install dependencies and run tests.

2. Baseline training pipeline
   - Goal: load CSV data, preprocess numeric and categorical columns, train GaussianNB.
   - Done when: training prints accuracy, a classification report, and saves a model.

3. Prediction command
   - Goal: load the saved model and write predictions to CSV.
   - Done when: the command works on the sample dataset.

4. Real dataset integration
   - Goal: document the selected public dataset and map its columns into this pipeline.
   - Done when: local training works on the real dataset without committing large raw files.

5. Evaluation report
   - Goal: save metrics and confusion matrix output under `reports/`.
   - Done when: model quality can be compared across runs.

6. CI for tests
   - Goal: run `pytest` in GitHub Actions on every push and pull request.
   - Done when: GitHub shows a passing test check.

## Suggested Commits

Use one commit per meaningful step. Good commit messages are short and explain the change.

```text
chore: bootstrap python traffic classifier project
feat: add naive bayes training pipeline
feat: add prediction command
test: cover train and predict round trip
docs: document setup and github workflow
ci: run tests in github actions
```

## Branch Naming

```text
main
feature/training-pipeline
feature/prediction-command
docs/setup-guide
ci/pytest
```

## Practical Rules

- Keep raw traffic datasets out of Git unless they are tiny and redistributable.
- Commit source code, configuration, small sample data, and documentation.
- Do not commit `.venv/`, model artifacts, prediction outputs, or large reports.
- Mention the issue number in commits or pull requests after you create GitHub issues.

Example:

```text
feat: add baseline training pipeline

Closes #2
```
