# Homework 06 — Data Preprocessing

This homework demonstrates a reproducible data preprocessing workflow using reusable cleaning functions.

## Files

- `homework06_data-preprocessing_submission.ipynb` → main preprocessing notebook
- `src/cleaning.py` → reusable cleaning functions
- `data/raw/sample_data.csv` → original raw dataset
- `data/processed/cleaned_data.csv` → cleaned and processed dataset

## Cleaning Strategy

The preprocessing workflow includes three main steps:

1. Columns with more than 50% missing values are removed because they contain too little reliable information. In this dataset, `extra_data` is removed.

2. Missing values in the numeric columns `age`, `income`, and `score` are filled using the median. Median imputation is used because it is less sensitive to extreme values than the mean.

3. The numeric columns `age`, `income`, and `score` are normalized using Min-Max scaling so that their values fall between 0 and 1.

The `zipcode` and `city` columns are kept unchanged because they are identifier or categorical fields and should not be normalized.

## Reusable Functions

The cleaning logic is implemented in `src/cleaning.py` using:

- `drop_missing()` → removes columns with excessive missing values
- `fill_missing_median()` → fills missing numeric values using the median
- `normalize_data()` → applies Min-Max normalization to selected numeric columns

## Output

The cleaned dataset is saved to:

`data/processed/cleaned_data.csv`

The notebook also compares the original and cleaned datasets by checking:

- Dataset shape
- Missing-value counts
- Removed columns
- Cleaned and normalized values