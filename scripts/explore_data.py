import pandas as pd

df = pd.read_csv("data/application_train.csv")

print("DATASET SHAPE")
print(df.shape)

print("\nTARGET DISTRIBUTION")
print(df["TARGET"].value_counts())

print("\nTARGET PERCENTAGE")
print((df["TARGET"].value_counts(normalize=True) * 100).round(2))

print("\nTOP 20 MISSING VALUE COLUMNS")
missing = df.isnull().sum().sort_values(ascending=False)
print(missing.head(20))

print("\nDEFAULT RATE BY EDUCATION")

education_analysis = (
    df.groupby("NAME_EDUCATION_TYPE")
    .agg(
        total_applications = ("TARGET","count"),
        total_defaults = ("TARGET","sum")
    )
)

education_analysis["default_rate"] = (
    education_analysis["total_defaults"]
    / education_analysis["total_applications"]
    * 100
)

print(
    education_analysis
    .sort_values("default_rate", ascending=False)
    .round(2)
)

# -----------------------------------
# DERIVED VARIABLES
# -----------------------------------
# Age in years
df["AGE_YEARS"]=(
df["DAYS_BIRTH"].abs()/365.25
).round(1)

# Fix anomalous employment value
df["DAYS_EMPLOYED"] = df["DAYS_EMPLOYED"].replace(
    365243,
    pd.NA
)

# Employment duration in years
df["EMPLOYMENT_YEARS"] = (
    df["DAYS_EMPLOYED"].abs() / 365.25
)

# Age groups
df["AGE_GROUP"] = pd.cut(
    df["AGE_YEARS"],
    bins=[0, 25, 35, 45, 55, 100],
    labels=[
        "18-25",
        "26-35",
        "36-45",
        "46-55",
        "56+"
    ]
)

# Income groups
df["INCOME_GROUP"] = pd.qcut(
    df["AMT_INCOME_TOTAL"],
    q=5,
    labels=[
        "Very Low",
        "Low",
        "Medium",
        "High",
        "Very High"
    ],
    duplicates="drop"
)

print("\nDEFAULT RATE BY AGE GROUP")

age_analysis = (
    df.groupby("AGE_GROUP", observed=True)
      .agg(
          total_applications=("TARGET", "count"),
          total_defaults=("TARGET", "sum")
      )
)

age_analysis["default_rate"] = (
    age_analysis["total_defaults"]
    / age_analysis["total_applications"]
    * 100
)

print(age_analysis.round(2))


print("\nDEFAULT RATE BY INCOME GROUP")

income_analysis = (
    df.groupby("INCOME_GROUP", observed=True)
      .agg(
          total_applications=("TARGET", "count"),
          total_defaults=("TARGET", "sum")
      )
)

income_analysis["default_rate"] = (
    income_analysis["total_defaults"]
    / income_analysis["total_applications"]
    * 100
)

print(income_analysis.round(2))

# -----------------------------------
# MISSING VALUE HANDLING
# -----------------------------------

# Categorical missing values
df["OCCUPATION_TYPE"] = df["OCCUPATION_TYPE"].fillna("Unknown")

# -----------------------------------
# ADDITIONAL RISK VARIABLES
# -----------------------------------

# Average external risk score
df["EXT_SOURCE_AVG"] = df[
    ["EXT_SOURCE_1", "EXT_SOURCE_2", "EXT_SOURCE_3"]
].mean(axis=1)

# Credit-to-income ratio
df["CREDIT_INCOME_RATIO"] = (
    df["AMT_CREDIT"] / df["AMT_INCOME_TOTAL"]
).round(2)

# -----------------------------------
# VALIDATION
# -----------------------------------

print("\nDATASET SHAPE AFTER TRANSFORMATION")
print(df.shape)

print("\nDAYS_EMPLOYED 365243 CHECK")
print(
    (df["DAYS_EMPLOYED"] == 365243).sum()
)

print("\nMISSING OCCUPATION VALUES")
print(
    df["OCCUPATION_TYPE"].isnull().sum()
)

print("\nDERIVED VARIABLES")
print(
    df[
        [
            "AGE_YEARS",
            "EMPLOYMENT_YEARS",
            "EXT_SOURCE_AVG",
            "CREDIT_INCOME_RATIO"
        ]
    ].describe()
)

# -----------------------------------
# OUTLIER INVESTIGATION
# -----------------------------------
print("\nINCOME STATISTICS")
print(
    df["AMT_INCOME_TOTAL"].describe(
        percentiles=[0.01, 0.05, 0.25, 0.50, 0.75, 0.95, 0.99]
    )
)

print("\nCREDIT STATISTICS")
print(
    df["AMT_CREDIT"].describe(
        percentiles=[0.01, 0.05, 0.25, 0.50, 0.75, 0.95, 0.99]
    )
)

print("\nCREDIT-INCOME RATIO STATISTICS")
print(
    df["CREDIT_INCOME_RATIO"].describe(
        percentiles=[0.01, 0.05, 0.25, 0.50, 0.75, 0.95, 0.99]
    )
)

print("\nTOP 10 HIGHEST INCOME APPLICATIONS")

print(
    df[
        [
            "SK_ID_CURR",
            "AMT_INCOME_TOTAL",
            "AMT_CREDIT",
            "TARGET"
        ]
    ]
    .sort_values("AMT_INCOME_TOTAL", ascending=False)
    .head(10)
)

print("\nTOP 10 HIGHEST CREDIT APPLICATIONS")

print(
    df[
        [
            "SK_ID_CURR",
            "AMT_INCOME_TOTAL",
            "AMT_CREDIT",
            "CREDIT_INCOME_RATIO",
            "TARGET"
        ]
    ]
    .sort_values("AMT_CREDIT", ascending=False)
    .head(10)
)