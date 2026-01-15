# bug-fix-minicase

Reproducible bug-fix mini case based on a common real-world issue: a CSV ingestion pipeline that breaks on delimiter mismatches, inconsistent date formats, currency/decimal variations, missing values, and invalid numeric fields.

This repo includes:
- `broken/`: a naive implementation that fails on real-world edge cases
- `fixed/`: a robust implementation with safe parsing + normalization
- `sample_data/`: messy input CSV to reproduce the bug
- `tests/`: pytest tests that verify before/after behavior

## Problem
A CSV pipeline that assumes:
- comma delimiter
- consistent date formats
- numeric values without currency symbols or decimal commas
- no missing / invalid fields

In practice, the pipeline crashes when the input contains mixed delimiters, nulls, currency strings, and invalid numeric values.

## How to run
From the repo root:

``bash
python broken/pipeline.py
python fixed/pipeline.py

## How to test
Install dependencies:
pip install -r requirements.txt

## run test
pytest -q

## Expected behavior
- `python broken/pipeline.py` fails due to real-world CSV issues (delimiter mismatch, mixed numeric formats, missing values, and invalid integers).
- `python fixed/pipeline.py` runs successfully, normalizes the input, and writes `output/clean_sales.csv`.
- `pytest -q` passes:
  - one test asserts the broken script returns a non-zero exit code
  - one test asserts the fixed script produces a valid CSV with the expected headers and row count

```bash
pip install -r requirements.txt

