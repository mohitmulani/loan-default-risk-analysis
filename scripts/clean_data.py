import pandas as pd

# ==========================================
# 1. LOAD RAW DATA
# ==========================================

INPUT_FILE = "data/application_train.csv"
OUTPUT_FILE = "data/application_train_clean.csv"

df = pd.read_csv(INPUT_FILE)

print(f"Raw dataset shape: {df.shape}")


# ==========================================
# 2. SELECT REQUIRED COLUMNS
# ==========================================

columns_to_keep = [
    "SK_ID_CURR",
    "TARGET",

    # Loan information
    "NAME_CONTRACT_TYPE",
    "AMT_INCOME_TOTAL",
    "AMT_CREDIT",
    "AMT_ANNUITY",
    "AMT_GOODS_PRICE",

    # Borrower information
    "NAME_INCOME_TYPE",
    "NAME_EDUCATION_TYPE",
    "NAME_FAMILY_STATUS",
    "NAME_HOUSING_TYPE",
    "OCCUPATION_TYPE",
    "CNT_CHILDREN",
    "CNT_FAM_MEMBERS",
    "FLAG_OWN_CAR",
    "FLAG_OWN_REALTY",

    # Age / employment
    "DAYS_BIRTH",
    "DAYS_EMPLOYED",

    # External risk indicators
    "EXT_SOURCE_1",
    "EXT_SOURCE_2",
    "EXT_SOURCE_3",

    # Regional indicators
    "REGION_RATING_CLIENT",
    "REGION_RATING_CLIENT_W_CITY",

    # Social / credit behavior
    "OBS_30_CNT_SOCIAL_CIRCLE",
    "DEF_30_CNT_SOCIAL_CIRCLE",
    "OBS_60_CNT_SOCIAL_CIRCLE",
    "DEF_60_CNT_SOCIAL_CIRCLE",
    "AMT_REQ_CREDIT_BUREAU_YEAR"
]

df = df[columns_to_keep].copy()

print(f"After column selection: {df.shape}")


# ==========================================
# 3. FIX KNOWN DATA ANOMALY
# ==========================================

df["DAYS_EMPLOYED"] = df["DAYS_EMPLOYED"].replace(
    365243,
    pd.NA
)


# ==========================================
# 4. CREATE AGE
# ==========================================

df["AGE_YEARS"] = (
    df["DAYS_BIRTH"].abs() / 365.25
).round(1)


# ==========================================
# 5. CREATE EMPLOYMENT YEARS
# ==========================================

df["EMPLOYMENT_YEARS"] = (
    df["DAYS_EMPLOYED"].abs() / 365.25
)

# ==========================================
# 6. HANDLE CATEGORICAL MISSING VALUES
# ==========================================

df["OCCUPATION_TYPE"] = (
    df["OCCUPATION_TYPE"]
    .fillna("Unknown")
)


# ==========================================
# 7. EXTERNAL SOURCE AVERAGE
# ==========================================

df["EXT_SOURCE_AVG"] = df[
    [
        "EXT_SOURCE_1",
        "EXT_SOURCE_2",
        "EXT_SOURCE_3"
    ]
].mean(axis=1)


# ==========================================
# 8. CREDIT-TO-INCOME RATIO
# ==========================================

df["CREDIT_INCOME_RATIO"] = (
    df["AMT_CREDIT"] /
    df["AMT_INCOME_TOTAL"]
).round(2)


# ==========================================
# 9. AGE GROUP
# ==========================================

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


# ==========================================
# 10. INCOME GROUP
# ==========================================

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


# ==========================================
# 11. VALIDATION
# ==========================================

print("\n========== VALIDATION ==========")

print("\nFinal shape:")
print(df.shape)

print("\nDuplicate application IDs:")
print(df["SK_ID_CURR"].duplicated().sum())

print("\nTARGET values:")
print(df["TARGET"].value_counts())

print("\nRemaining 365243 values:")
print((df["DAYS_EMPLOYED"] == 365243).sum())

print("\nMissing occupation values:")
print(df["OCCUPATION_TYPE"].isna().sum())

print("\nAge statistics:")
print(df["AGE_YEARS"].describe())

print("\nEmployment statistics:")
print(df["EMPLOYMENT_YEARS"].describe())


# ==========================================
# 12. SAVE CLEAN DATA
# ==========================================

df.to_csv(
    OUTPUT_FILE,
    index=False
)

print(f"\nClean dataset saved to: {OUTPUT_FILE}")