import csv
import os
import subprocess
import sys


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def test_fixed_pipeline_creates_output():
    result = run([sys.executable, "fixed/pipeline.py"])
    assert result.returncode == 0, result.stderr

    assert os.path.exists("output/clean_sales.csv")

    with open("output/clean_sales.csv", "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    assert len(rows) == 6
    assert set(rows[0].keys()) == {
        "order_id",
        "order_date",
        "customer",
        "product",
        "amount",
        "quantity",
    }


def test_broken_pipeline_fails():
    result = run([sys.executable, "broken/pipeline.py"])
    assert result.returncode != 0
