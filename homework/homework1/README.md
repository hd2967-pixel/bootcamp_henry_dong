# Technology Stock Risk-Return Analysis

**Stage:** Problem Framing & Scoping (Stage 01)

## Problem Statement

Individual investors often compare technology stocks mainly based on recent price movements, but price performance alone does not show how much risk an investor is taking.

This project will analyze major U.S. technology stocks such as Apple (AAPL), Microsoft (MSFT), and NVIDIA (NVDA) using historical market data to compare their returns, volatility, and downside risk.

The goal is to provide a simple framework that helps investors understand which stock has offered a more attractive risk-return tradeoff. The project will not provide direct buy or sell recommendations, but instead use quantitative metrics and visualizations to support investment decisions.

Success will be measured by whether the analysis can produce a reproducible comparison of historical return, volatility, maximum drawdown, and risk-adjusted return across the selected technology stocks.

## Stakeholder & User

The primary stakeholder is an individual investor who needs to decide how to allocate money among major technology stocks.

The end user may also be a junior investment analyst who uses the analysis to compare securities and communicate their risk-return characteristics.

## Useful Answer & Decision

The initial analysis will be primarily **descriptive**.

Key metrics will include:

- Historical return
- Daily and annualized volatility
- Maximum drawdown
- Risk-adjusted return
- Price trends

The main deliverable will be a Jupyter notebook containing analysis, visualizations, and a comparison summary.

## Assumptions & Constraints

- Historical market data is available through public financial data sources such as Yahoo Finance.
- Historical performance does not guarantee future performance.
- The initial analysis focuses mainly on price and volume data.
- Macroeconomic events and company-specific news may not be fully captured.
- Data quality and API availability may affect the analysis.

## Known Unknowns / Risks

- The selected historical period may significantly affect the results.
- Market conditions may change after the analysis is completed.
- Different risk metrics may produce different rankings.
- Missing or inconsistent market data may need additional cleaning.

## Lifecycle Mapping

Goal → Stage → Deliverable

- Define the investment problem → Problem Framing & Scoping (Stage 01) → Project scope and stakeholder memo
- Collect market data → Data Acquisition → Historical stock-price dataset
- Clean and validate data → Data Preparation → Analysis-ready dataset
- Compare risk and return → Exploratory Data Analysis → Metrics and visualizations
- Communicate findings → Reporting → Final notebook and stakeholder summary

## Repo Plan

The repository will use the following structure:

- `data/` → project datasets
- `src/` → reusable Python code
- `notebooks/` → analysis notebooks
- `docs/` → stakeholder-facing documentation

The repository will be updated as each stage of the project lifecycle is completed.