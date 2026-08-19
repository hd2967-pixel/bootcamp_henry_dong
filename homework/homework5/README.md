# Homework 05 — Data Storage

## Overview

This homework implements a reproducible data storage workflow using CSV and Parquet formats.

The homework notebook saves, reloads, validates, and manages DataFrames using reusable read and write utilities.

## Folder Structure

Homework 5 uses separate folders for raw and processed data:

- `data/raw/` → raw datasets stored in CSV format
- `data/processed/` → processed datasets stored in Parquet format

The files are stored inside the Homework 5 directory.

## File Formats

CSV is used for raw data because it is:

- Human-readable
- Portable
- Easy to inspect
- Widely supported

Parquet is used for processed data because it:

- Uses storage more efficiently
- Preserves data types more reliably
- Is well suited for analytical workflows

## Environment-Driven Paths

Storage locations are configured using environment variables:

- `DATA_DIR_RAW=data/raw`
- `DATA_DIR_PROCESSED=data/processed`

The notebook reads these values from `.env` rather than hard-coding machine-specific absolute paths.

The paths are interpreted relative to the Homework 5 directory.

## Reusable Utilities

The notebook implements reusable storage functions:

- `detect_format()` → detects CSV or Parquet based on the file suffix
- `write_df()` → writes a DataFrame as CSV or Parquet
- `read_df()` → reads a CSV or Parquet file

The write utility creates missing output directories automatically.

The utilities also provide clear error messages for unsupported file formats, missing files, or unavailable Parquet engines.

## Validation

After saving the data, both CSV and Parquet files are reloaded and validated.

The validation checks confirm that:

- Dataset shapes match
- Required columns are present
- Date columns retain datetime-compatible types
- Price columns retain numeric types
- Ticker columns retain text-compatible types

Parquet operations require a supported engine such as `pyarrow` or `fastparquet`.