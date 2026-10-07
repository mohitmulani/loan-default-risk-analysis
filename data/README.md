# Loan Default Risk Analysis & Dashboard

An end-to-end data analytics project that analyzes historical loan application data to identify borrower segments with different observed default rates and presents the findings through an interactive Power BI dashboard.

**Workflow:** Kaggle Dataset → Python/Pandas → SQL Server → Power BI

> **Important:** This project is a descriptive/diagnostic analysis of historical outcomes. Observed relationships should not be interpreted as causal evidence or as an individual applicant's predicted probability of default.

## Project Overview

Financial institutions need to understand historical loan default patterns to evaluate portfolio risk and identify borrower segments that may require closer analysis.

This project uses the **Home Credit Default Risk** dataset to examine default behavior across borrower demographics, income, employment experience, education, occupation, credit-to-income ratios, and external risk scores.

The raw dataset was explored and cleaned using Python, transformed into an analysis-ready dataset, loaded into SQL Server for analytical querying, and visualized through a two-page Power BI dashboard.

## Business Problem

Large lending datasets contain hundreds of thousands of applications and many borrower attributes. Reviewing these records manually makes it difficult to identify meaningful risk patterns.

This project addresses questions such as:

- What is the overall historical default rate?
- Which age groups have higher observed default rates?
- How do default rates vary across income groups?
- Does employment experience show different default patterns?
- Which education and occupation groups have higher observed default rates?
- How does the external risk score relate to historical default outcomes?
- How does the credit-to-income ratio vary across borrower segments?
- Can an interactive dashboard make these patterns easier for stakeholders to explore?

## Project Objectives

1. Clean and prepare the raw loan application dataset for analysis.
2. Engineer meaningful borrower and credit-related analytical features.
3. Analyze historical default patterns using SQL Server.
4. Identify borrower segments with higher observed default rates.
5. Build an interactive Power BI dashboard for portfolio and borrower analysis.
6. Present findings in a business-friendly format suitable for risk-oriented analysis.

## Dataset

### Source

**Home Credit Default Risk — Kaggle**

The dataset contains **307,511 applications** with **122 original columns**.

The target variable is:

| TARGET | Meaning |
|---|---|
| `0` | Loan did not default |
| `1` | Loan defaulted |

Download the dataset from:

https://www.kaggle.com/competitions/home-credit-default-risk/data

Place the required file here:

```text
data/application_train.csv
```

The raw dataset should not be committed to GitHub.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Data exploration, cleaning and feature engineering |
| Pandas | Data manipulation and transformation |
| SQL Server | Data storage and analytical SQL |
| T-SQL | Business analysis and segmentation |
| Power BI | Interactive dashboard and visualization |
| DAX | Dashboard measures |
| VS Code | Development environment |
| Git / GitHub | Version control and portfolio |

### Python packages

- pandas
- numpy
- pyodbc
- python-dotenv

## Project Architecture

```text
Kaggle Dataset
      |
      v
application_train.csv
      |
      v
Python / Pandas
  |           |
  |           +--> Cleaning & Feature Engineering
  |
  +--> Exploration & Profiling
      |
      v
Analysis-ready CSV
      |
      v
SQL Server
      |
      v
T-SQL Analysis
      |
      v
Power BI
   /        \
  v          v
Executive   Borrower
Overview    Risk Analysis
```

## Project Structure

```text
Loan_Default_Risk/
|
├── data/
│   └── application_train.csv
|
├── scripts/
│   ├── explore_data.py
│   ├── clean_data.py
│   └── load_data.py
|
├── sql/
│   └── analysis.sql
|
├── powerbi/
│   └── loan_default_risk_dashboard.pbix
|
├── screenshots/
│   ├── executive_overview.png
│   └── borrower_risk_analysis.png
|
├── README.md
├── requirements.txt
└── .gitignore
```

## Data Exploration & Preparation

### Initial Dataset Profile

The original dataset contained:

- **307,511 rows**
- **122 columns**
- **24,825 defaults**
- **282,686 non-defaults**
- **8.07% overall default rate**

Initial checks included:

- Dataset dimensions
- Data types
- Missing-value analysis
- Duplicate rows
- Duplicate application IDs
- Numeric distributions
- Categorical distributions
- Extreme values
- Target distribution

No duplicate application IDs were identified.

### Data Cleaning

The cleaning process was performed using Python and Pandas.

#### Anomalous employment values

The dataset contains `DAYS_EMPLOYED = 365243`, which was treated as a placeholder rather than a realistic employment duration and converted to `NULL`.

#### Missing values

Missing numerical values were generally preserved as `NULL` rather than automatically replacing them with zero. This avoids incorrectly implying that a missing financial or risk value represents an actual zero.

#### Occupation

Missing occupation values were categorized as `Unknown`.

#### Extreme values

Legitimate extreme income and credit values were retained rather than automatically removed. Ratios and analytical bands were used where appropriate.

## Feature Engineering

The project created analytical features including:

- `AGE_YEARS`
- `EMPLOYMENT_YEARS`
- `EXT_SOURCE_AVG`
- `CREDIT_INCOME_RATIO`
- `AGE_GROUP`
- `INCOME_GROUP`
- `CREDIT_INCOME_BAND`
- `EMPLOYMENT_BAND`
- `EXT_SOURCE_BAND`

### Age

```text
AGE_YEARS = ABS(DAYS_BIRTH) / 365.25
```

### Employment Experience

```text
EMPLOYMENT_YEARS = ABS(DAYS_EMPLOYED) / 365.25
```

after replacing the anomalous `365243` value with `NULL`.

### Credit-to-Income Ratio

```text
CREDIT_INCOME_RATIO = AMT_CREDIT / AMT_INCOME_TOTAL
```

### Age Groups

- 18–25
- 26–35
- 36–45
- 46–55
- 56+

### Income Groups

- Very Low
- Low
- Medium
- High
- Very High

### Credit-to-Income Bands

- `<1`
- `1–2`
- `2–4`
- `4–6`
- `6–10`
- `10+`
- `Unknown`

### Employment Bands

- `<1 year`
- `1–3 years`
- `3–5 years`
- `5–10 years`
- `10+ years`
- `Unknown`

### External Risk Score Bands

- Very Low
- Low
- Medium
- High
- Very High
- Unknown

## SQL Server Analysis

The cleaned dataset was loaded into:

```text
Database: LoanDefaultRisk
Table: applications_clean
```

SQL analysis was used to calculate:

- Application counts
- Default counts
- Default rates
- Segment comparisons
- Occupation-level default rates
- Age-level default rates
- Income-level default rates
- Education-level default rates
- Employment-level default rates
- Credit-to-income analysis
- External risk score analysis
- Combined borrower segments

Sample-size thresholds were used for certain segment analyses to avoid overinterpreting groups with very few applications.

## Key Findings

### Overall Portfolio

- **307,511 applications**
- **24,825 defaults**
- **8.07% overall default rate**

### External Risk Score

| External Risk Band | Applications | Defaults | Default Rate |
|---|---:|---:|---:|
| Very Low | 10,448 | 2,951 | **28.24%** |
| Low | 58,950 | 9,510 | **16.13%** |
| Medium | 143,723 | 9,601 | **6.68%** |
| High | 93,581 | 2,738 | **2.93%** |
| Very High | 637 | 11 | **1.73%** |

The Very Low external risk score band had a **28.24% observed default rate**, compared with the overall portfolio rate of **8.07%**.

### Age

The 18–25 age group had the highest observed default rate among the analyzed age groups:

**12.27%**

### Income

Default rates varied across income groups. The Very High income group had the lowest observed default rate at:

**6.52%**

### Employment Experience

| Employment Band | Default Rate |
|---|---:|
| 1–3 years | **11.07%** |
| <1 year | **10.97%** |
| 3–5 years | **9.67%** |
| 5–10 years | **7.37%** |
| 10+ years | **5.19%** |

The `Unknown` group is not interpreted as a safer employment category because it represents missing/anomalous employment information.

### Occupation

Among occupation groups meeting the minimum sample-size threshold:

- Low-skill laborers — **17.15%**
- Drivers — **11.33%**
- Waiters/barmen staff — **11.28%**

### High-Risk Segment Analysis

One analyzed borrower segment combined:

- Age: **18–25**
- Income: **Low**
- Education: **Secondary / Secondary Special**

Results:

- **2,854 applications**
- **452 defaults**
- **15.84% default rate**

This was approximately **1.96× the overall portfolio default rate**.

## Power BI Dashboard

The final Power BI dashboard contains two analytical pages.

### Page 1 — Executive Risk Overview

Provides a portfolio-level view of historical default patterns.

**KPIs**
- Total Applications
- Total Defaults
- Default Rate
- Average Credit Amount

**Visuals**
- Default Rate by External Risk Score
- Default Rate by Age Group
- Default Rate by Income Group
- Default Rate by Employment Experience
- Default Rate by Education

### Page 2 — Borrower Risk Analysis

Provides interactive borrower segmentation.

**Filters**
- Age Group
- Income Group
- Education
- Occupation

**KPIs**
- Selected Applications
- Selected Defaults
- Selected Default Rate

**Visuals**
- Default Rate by Occupation
- Default Rate by Credit-to-Income Band
- Applications by Employment Experience
- Credit Amount vs Applicant Income

## DAX Measures

```DAX
Total Applications =
COUNTROWS(Applications_clean)
```

```DAX
Total Defaults =
CALCULATE(
    COUNTROWS(Applications_clean),
    Applications_clean[TARGET] = 1
)
```

```DAX
Default Rate % =
DIVIDE(
    [Total Defaults],
    [Total Applications]
)
```

```DAX
Average Credit Amount =
AVERAGE(Applications_clean[AMT_CREDIT])
```

For interactive segmentation:

```DAX
Selected Applications =
COUNTROWS(Applications_clean)
```

```DAX
Selected Defaults =
CALCULATE(
    COUNTROWS(Applications_clean),
    Applications_clean[TARGET] = 1
)
```

```DAX
Selected Default Rate % =
DIVIDE(
    [Selected Defaults],
    [Selected Applications]
)
```

## Business Insights

### 1. External risk score shows the strongest observed differentiation

Applicants in the Very Low external risk score band had a substantially higher observed default rate than the overall portfolio.

### 2. Younger applicants showed higher observed default rates

The 18–25 age group had the highest observed default rate among the analyzed age groups.

### 3. Shorter employment history showed higher observed default rates

Applicants with less than three years of employment experience showed higher observed rates than applicants with longer employment histories.

### 4. Some occupations showed elevated historical default rates

Low-skill laborers, drivers, and waiters/barmen staff showed relatively high observed rates among sufficiently large occupation groups.

### 5. Combined segmentation provides additional context

Combining demographic and financial characteristics can reveal borrower segments whose observed default rate differs substantially from the portfolio average.

## Limitations

- This is a historical descriptive analysis, not a predictive credit model.
- Higher default rates do not prove causation.
- Missing values exist in several source variables.
- Findings are specific to the Home Credit dataset and may not generalize to other lenders, geographies, or time periods.
- The project does not make individual applicant-level credit decisions.

## Getting Started

### 1. Clone the repository

```bash
git clone <your-github-repository-url>
cd Loan_Default_Risk
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Download the dataset

Download `application_train.csv` from Kaggle and place it in:

```text
data/application_train.csv
```

### 4. Explore the dataset

```bash
python scripts/explore_data.py
```

### 5. Clean and transform the dataset

```bash
python scripts/clean_data.py
```

### 6. Load the cleaned data into SQL Server

Configure the SQL Server connection in `load_data.py` and run:

```bash
python scripts/load_data.py
```

The project uses:

```text
Database: LoanDefaultRisk
Table: applications_clean
```

### 7. Run SQL analysis

Open:

```text
sql/analysis.sql
```

in SQL Server Management Studio or another SQL Server-compatible client.

### 8. Open the Power BI dashboard

Open:

```text
powerbi/loan_default_risk_dashboard.pbix
```

Update the SQL Server data source if necessary and refresh the dataset.

## Requirements

- Python 3.x
- SQL Server
- SQL Server Management Studio or equivalent SQL client
- Power BI Desktop
- Git
- Kaggle account for dataset download

## Future Improvements

Potential extensions include:

- Building a machine-learning default prediction model
- Adding ROC-AUC, precision, recall, and other model evaluation metrics
- Adding additional Home Credit datasets such as previous applications and bureau information
- Creating a formal risk-scoring framework
- Adding automated data validation checks
- Publishing the dashboard through Power BI Service

## Disclaimer

> Default rates in this project represent observed historical outcomes in the dataset and should not be interpreted as causal evidence, credit decisions, or individual applicant-level predicted probabilities of default.

This project is intended for **data analytics learning, portfolio demonstration, and educational purposes**.

## Author

**Mohit**

Aspiring Data Analyst | SQL | Python | Power BI | Excel | Tableau

This project demonstrates practical skills in:

- Data cleaning
- Exploratory data analysis
- Feature engineering
- SQL analysis
- Data segmentation
- Dashboard development
- Business insight generation

## Dataset Attribution

The underlying Home Credit Default Risk dataset is provided by Kaggle/Home Credit and remains subject to its applicable terms and conditions.
