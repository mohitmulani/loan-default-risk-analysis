import pandas as pd
import pyodbc

# ==========================================
# CONFIGURATION
# ==========================================

INPUT_FILE = "data/application_train_clean.csv"

SERVER = r"localhost"
DATABASE = "LoanDefaultRisk"

TABLE_NAME = "applications_clean"

# ==========================================
# READ CSV
# ==========================================

print("Reading cleaned dataset...")

df = pd.read_csv(INPUT_FILE)

print(f"Rows loaded: {len(df):,}")
print(f"Columns loaded: {len(df.columns)}")

# ==========================================
# SQL SERVER CONNECTION
# ==========================================

connection_string = (
    "DRIVER={ODBC Driver 18 for SQL Server};"
    f"SERVER={SERVER};"
    f"DATABASE={DATABASE};"
    "Trusted_Connection=yes;"
    "TrustServerCertificate=yes;"
)

conn = pyodbc.connect(connection_string)
cursor = conn.cursor()

print("Connected to SQL Server.")

# ==========================================
# DROP EXISTING TABLE
# ==========================================

cursor.execute(f"""
IF OBJECT_ID('{TABLE_NAME}', 'U') IS NOT NULL
    DROP TABLE {TABLE_NAME}
""")

conn.commit()


# ==========================================
# CREATE TABLE
# ==========================================

create_table_sql = f"""
CREATE TABLE {TABLE_NAME} (

    SK_ID_CURR INT,
    TARGET INT,

    NAME_CONTRACT_TYPE VARCHAR(50),
    AMT_INCOME_TOTAL FLOAT,
    AMT_CREDIT FLOAT,
    AMT_ANNUITY FLOAT,
    AMT_GOODS_PRICE FLOAT,

    NAME_INCOME_TYPE VARCHAR(100),
    NAME_EDUCATION_TYPE VARCHAR(100),
    NAME_FAMILY_STATUS VARCHAR(100),
    NAME_HOUSING_TYPE VARCHAR(100),
    OCCUPATION_TYPE VARCHAR(100),

    CNT_CHILDREN INT,
    CNT_FAM_MEMBERS FLOAT,

    FLAG_OWN_CAR VARCHAR(5),
    FLAG_OWN_REALTY VARCHAR(5),

    DAYS_BIRTH INT,
    DAYS_EMPLOYED FLOAT,

    EXT_SOURCE_1 FLOAT,
    EXT_SOURCE_2 FLOAT,
    EXT_SOURCE_3 FLOAT,

    REGION_RATING_CLIENT INT,
    REGION_RATING_CLIENT_W_CITY INT,

    OBS_30_CNT_SOCIAL_CIRCLE FLOAT,
    DEF_30_CNT_SOCIAL_CIRCLE FLOAT,
    OBS_60_CNT_SOCIAL_CIRCLE FLOAT,
    DEF_60_CNT_SOCIAL_CIRCLE FLOAT,

    AMT_REQ_CREDIT_BUREAU_YEAR FLOAT,

    AGE_YEARS FLOAT,
    EMPLOYMENT_YEARS FLOAT,
    EXT_SOURCE_AVG FLOAT,
    CREDIT_INCOME_RATIO FLOAT,

    AGE_GROUP VARCHAR(20),
    INCOME_GROUP VARCHAR(20)
)
"""

cursor.execute(create_table_sql)
conn.commit()

print("Table created.")


# ==========================================
# PREPARE DATA
# ==========================================

# Convert dataframe to object type first.
# This allows missing values to become Python None.
df = df.astype(object)

# Convert all Pandas missing values to Python None.
df = df.where(pd.notnull(df), None)


# Convert categorical columns to strings
categorical_columns = [
    "NAME_CONTRACT_TYPE",
    "NAME_INCOME_TYPE",
    "NAME_EDUCATION_TYPE",
    "NAME_FAMILY_STATUS",
    "NAME_HOUSING_TYPE",
    "OCCUPATION_TYPE",
    "FLAG_OWN_CAR",
    "FLAG_OWN_REALTY",
    "AGE_GROUP",
    "INCOME_GROUP"
]

for column in categorical_columns:
    df[column] = df[column].apply(
        lambda x: str(x) if x is not None else None
    )

# ==========================================
# INSERT DATA
# ==========================================

columns = list(df.columns)

column_list = ", ".join(columns)

placeholders = ", ".join(["?"] * len(columns))

insert_sql = f"""
INSERT INTO {TABLE_NAME}
({column_list})
VALUES ({placeholders})
"""

data = list(df.itertuples(index=False, name=None))

print("Starting data insertion...")

cursor.fast_executemany = True

batch_size = 5000

for start in range(0, len(data), batch_size):

    batch = data[start:start + batch_size]

    cursor.executemany(
        insert_sql,
        batch
    )

    conn.commit()

    print(
        f"Inserted {min(start + batch_size, len(data)):,}"
        f" / {len(data):,}"
    )


# ==========================================
# CLOSE CONNECTION
# ==========================================

cursor.close()
conn.close()

print("\nData loading completed successfully.")