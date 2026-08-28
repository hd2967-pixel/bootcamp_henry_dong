"""Stage 15 — one pipeline task refactored into a CLI-callable function with logging.

Runs the *clean* step of the factor-model pipeline as a standalone, idempotent task.

Usage (from the project root):

    python src/run_step.py --input data/raw/factor_returns.csv \
                           --output data/processed/cleaned_data.csv
"""

import argparse
import logging
import sys

from src import cleaning, outliers, utils


def clean_task(input_path, output_path):
    """Read raw data, fill missing ``value``, winsorize ``momentum`` outliers, write."""
    logging.info("[clean] start  input=%s", input_path)
    df = utils.load_dataframe(input_path)
    n_in = len(df)

    df = cleaning.fill_missing_median(df, columns=["value"])
    df["momentum"] = outliers.winsorize_series(df["momentum"], lower=0.01, upper=0.99)

    utils.save_dataframe(df, output_path)
    logging.info("[clean] done  rows_in=%d rows_out=%d output=%s", n_in, len(df), output_path)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Clean step of the factor-model pipeline")
    parser.add_argument("--input", required=True, help="raw CSV/Parquet to clean")
    parser.add_argument("--output", required=True, help="cleaned CSV/Parquet to write")
    args = parser.parse_args(argv)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )
    clean_task(args.input, args.output)


if __name__ == "__main__":
    main()
