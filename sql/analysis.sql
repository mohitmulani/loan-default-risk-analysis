USE LoanDefaultRisk;
GO

--Query 1 — Overall portfolio summary

SELECT
    COUNT(*) AS Total_Applications,
    SUM(TARGET) AS Total_Defaults,
    COUNT(*) - SUM(TARGET) AS Non_Defaults,
    CAST(
        SUM(TARGET) * 100.0 / COUNT(*)
        AS DECIMAL(10,2)
    ) AS Default_Rate_Percent
FROM applications_clean;

--Query 2 — Default rate by education

SELECT
    NAME_EDUCATION_TYPE,
    COUNT(*) AS Total_Applications,
    SUM(TARGET) AS Total_Defaults,
    CAST(
        SUM(TARGET) * 100.0 / COUNT(*)
        AS DECIMAL(10,2)
    ) AS Default_Rate_Percent
FROM applications_clean
GROUP BY NAME_EDUCATION_TYPE
ORDER BY Default_Rate_Percent DESC;

--Query 3 — Default rate by age group

SELECT
    AGE_GROUP,
    COUNT(*) AS Total_Applications,
    SUM(TARGET) AS Total_Defaults,
    CAST(
        SUM(TARGET) * 100.0 / COUNT(*)
        AS DECIMAL(10,2)
    ) AS Default_Rate_Percent
FROM applications_clean
GROUP BY AGE_GROUP
ORDER BY Default_Rate_Percent DESC;

--Query 4 — Default rate by income group

SELECT
    INCOME_GROUP,
    COUNT(*) AS Total_Applications,
    SUM(TARGET) AS Total_Defaults,
    CAST(
        SUM(TARGET) * 100.0 / COUNT(*)
        AS DECIMAL(10,2)
    ) AS Default_Rate_Percent
FROM applications_clean
GROUP BY INCOME_GROUP
ORDER BY Default_Rate_Percent DESC;

--Query 5 — High-risk segments

SELECT
    AGE_GROUP,
    INCOME_GROUP,
    NAME_EDUCATION_TYPE,
    COUNT(*) AS Total_Applications,
    SUM(TARGET) AS Total_Defaults,
    CAST(
        SUM(TARGET) * 100.0 / COUNT(*)
        AS DECIMAL(10,2)
    ) AS Default_Rate_Percent
FROM applications_clean
GROUP BY
    AGE_GROUP,
    INCOME_GROUP,
    NAME_EDUCATION_TYPE
HAVING COUNT(*) >= 500
ORDER BY
    Default_Rate_Percent DESC;

--Query 6 — Credit-to-Income Risk

SELECT
    CASE
        WHEN CREDIT_INCOME_RATIO < 1 THEN '< 1'
        WHEN CREDIT_INCOME_RATIO < 2 THEN '1 - 2'
        WHEN CREDIT_INCOME_RATIO < 4 THEN '2 - 4'
        WHEN CREDIT_INCOME_RATIO < 6 THEN '4 - 6'
        WHEN CREDIT_INCOME_RATIO < 10 THEN '6 - 10'
        ELSE '10+'
    END AS Credit_Income_Band,

    COUNT(*) AS Total_Applications,

    SUM(TARGET) AS Total_Defaults,

    CAST(
        SUM(TARGET) * 100.0 / COUNT(*)
        AS DECIMAL(10,2)
    ) AS Default_Rate_Percent

FROM applications_clean

WHERE CREDIT_INCOME_RATIO IS NOT NULL

GROUP BY
    CASE
        WHEN CREDIT_INCOME_RATIO < 1 THEN '< 1'
        WHEN CREDIT_INCOME_RATIO < 2 THEN '1 - 2'
        WHEN CREDIT_INCOME_RATIO < 4 THEN '2 - 4'
        WHEN CREDIT_INCOME_RATIO < 6 THEN '4 - 6'
        WHEN CREDIT_INCOME_RATIO < 10 THEN '6 - 10'
        ELSE '10+'
    END

HAVING COUNT(*) >= 500

ORDER BY
    Default_Rate_Percent DESC;

--Query 7 — Occupation Risk Analysis

SELECT
    OCCUPATION_TYPE,
    COUNT(*) AS Total_Applications,
    SUM(TARGET) AS Total_Defaults,
    CAST(
        SUM(TARGET) * 100.0 / COUNT(*)
        AS DECIMAL(10,2)
    ) AS Default_Rate_Percent
FROM applications_clean
GROUP BY OCCUPATION_TYPE
HAVING COUNT(*) >= 1000
ORDER BY Default_Rate_Percent DESC;

--Query 8 — Young + low-income + occupation

SELECT
    OCCUPATION_TYPE,
    COUNT(*) AS Total_Applications,
    SUM(TARGET) AS Total_Defaults,
    CAST(
        SUM(TARGET) * 100.0 / COUNT(*)
        AS DECIMAL(10,2)
    ) AS Default_Rate_Percent
FROM applications_clean
WHERE AGE_GROUP = '18-25'
  AND INCOME_GROUP = 'Very Low'
  AND OCCUPATION_TYPE <> 'Unknown'
GROUP BY OCCUPATION_TYPE
HAVING COUNT(*) >= 100
ORDER BY Default_Rate_Percent DESC;

--Query 9 - External risk scores

SELECT
    CASE
        WHEN EXT_SOURCE_AVG < 0.2 THEN 'Very Low'
        WHEN EXT_SOURCE_AVG < 0.4 THEN 'Low'
        WHEN EXT_SOURCE_AVG < 0.6 THEN 'Medium'
        WHEN EXT_SOURCE_AVG < 0.8 THEN 'High'
        ELSE 'Very High'
    END AS External_Score_Band,

    COUNT(*) AS Total_Applications,

    SUM(TARGET) AS Total_Defaults,

    CAST(
        SUM(TARGET) * 100.0 / COUNT(*)
        AS DECIMAL(10,2)
    ) AS Default_Rate_Percent

FROM applications_clean
WHERE EXT_SOURCE_AVG IS NOT NULL
GROUP BY
    CASE
        WHEN EXT_SOURCE_AVG < 0.2 THEN 'Very Low'
        WHEN EXT_SOURCE_AVG < 0.4 THEN 'Low'
        WHEN EXT_SOURCE_AVG < 0.6 THEN 'Medium'
        WHEN EXT_SOURCE_AVG < 0.8 THEN 'High'
        ELSE 'Very High'
    END
HAVING COUNT(*) >= 500
ORDER BY Default_Rate_Percent DESC;

--Query 10 - Default rate by employment duration

SELECT
    CASE
        WHEN EMPLOYMENT_YEARS IS NULL THEN 'Unknown'
        WHEN EMPLOYMENT_YEARS < 1 THEN '< 1 year'
        WHEN EMPLOYMENT_YEARS < 3 THEN '1 - 3 years'
        WHEN EMPLOYMENT_YEARS < 5 THEN '3 - 5 years'
        WHEN EMPLOYMENT_YEARS < 10 THEN '5 - 10 years'
        ELSE '10+ years'
    END AS Employment_Band,

    COUNT(*) AS Total_Applications,

    SUM(TARGET) AS Total_Defaults,

    CAST(
        SUM(TARGET) * 100.0 / COUNT(*)
        AS DECIMAL(10,2)
    ) AS Default_Rate_Percent

FROM applications_clean

GROUP BY
    CASE
        WHEN EMPLOYMENT_YEARS IS NULL THEN 'Unknown'
        WHEN EMPLOYMENT_YEARS < 1 THEN '< 1 year'
        WHEN EMPLOYMENT_YEARS < 3 THEN '1 - 3 years'
        WHEN EMPLOYMENT_YEARS < 5 THEN '3 - 5 years'
        WHEN EMPLOYMENT_YEARS < 10 THEN '5 - 10 years'
        ELSE '10+ years'
    END

HAVING COUNT(*) >= 500

ORDER BY Default_Rate_Percent DESC;

--Altering table and creating income and employment bands

ALTER TABLE applications_clean
ADD
    CREDIT_INCOME_BAND VARCHAR(20),
    EMPLOYMENT_BAND VARCHAR(20);
GO

UPDATE applications_clean
SET CREDIT_INCOME_BAND =
    CASE
        WHEN CREDIT_INCOME_RATIO IS NULL THEN 'Unknown'
        WHEN CREDIT_INCOME_RATIO < 1 THEN '< 1'
        WHEN CREDIT_INCOME_RATIO < 2 THEN '1 - 2'
        WHEN CREDIT_INCOME_RATIO < 4 THEN '2 - 4'
        WHEN CREDIT_INCOME_RATIO < 6 THEN '4 - 6'
        WHEN CREDIT_INCOME_RATIO < 10 THEN '6 - 10'
        ELSE '10+'
    END;
GO

UPDATE applications_clean
SET EMPLOYMENT_BAND =
    CASE
        WHEN EMPLOYMENT_YEARS IS NULL THEN 'Unknown'
        WHEN EMPLOYMENT_YEARS < 1 THEN '< 1 year'
        WHEN EMPLOYMENT_YEARS < 3 THEN '1 - 3 years'
        WHEN EMPLOYMENT_YEARS < 5 THEN '3 - 5 years'
        WHEN EMPLOYMENT_YEARS < 10 THEN '5 - 10 years'
        ELSE '10+ years'
    END;
GO

--Verifying income and employment bands

SELECT
    CREDIT_INCOME_BAND,
    COUNT(*) AS Applications,
    SUM(TARGET) AS Defaults,
    CAST(
        SUM(TARGET) * 100.0 / COUNT(*)
        AS DECIMAL(10,2)
    ) AS Default_Rate
FROM applications_clean
GROUP BY CREDIT_INCOME_BAND
ORDER BY Default_Rate DESC;

SELECT
    EMPLOYMENT_BAND,
    COUNT(*) AS Applications,
    SUM(TARGET) AS Defaults,
    CAST(
        SUM(TARGET) * 100.0 / COUNT(*)
        AS DECIMAL(10,2)
    ) AS Default_Rate
FROM applications_clean
GROUP BY EMPLOYMENT_BAND
ORDER BY Default_Rate DESC;

--Adding External Score Band

ALTER TABLE applications_clean
ADD EXT_SOURCE_BAND VARCHAR(20);
GO

UPDATE applications_clean
SET EXT_SOURCE_BAND =
    CASE
        WHEN EXT_SOURCE_AVG IS NULL THEN 'Unknown'
        WHEN EXT_SOURCE_AVG < 0.2 THEN 'Very Low'
        WHEN EXT_SOURCE_AVG < 0.4 THEN 'Low'
        WHEN EXT_SOURCE_AVG < 0.6 THEN 'Medium'
        WHEN EXT_SOURCE_AVG < 0.8 THEN 'High'
        ELSE 'Very High'
    END;
GO