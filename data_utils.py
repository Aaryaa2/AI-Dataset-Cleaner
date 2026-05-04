import pandas as pd

def missing_values_table(df):
    missing = df.isnull().sum()
    percent = (missing / len(df)) * 100

    table = pd.DataFrame({
        "Missing Values": missing,
        "Percentage (%)": percent
    })

    table = table[table["Missing Values"] > 0]

    return table.sort_values("Percentage (%)", ascending=False)

import numpy as np

def detect_outliers_iqr(df):
    numeric_cols = df.select_dtypes(include=np.number).columns
    result = {}

    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1

        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR

        count = ((df[col] < lower) | (df[col] > upper)).sum()

        result[col] = {
            "outliers": int(count),
            "lower_bound": float(lower),
            "upper_bound": float(upper)
        }

    return result


def remove_outliers(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1

    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR

    return df[(df[column] >= lower) & (df[column] <= upper)]


def cap_outliers(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1

    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR

    df[column] = df[column].clip(lower, upper)
    return df


def fill_missing(df, column, method):
    if method == "Mean":
        df[column] = df[column].fillna(df[column].mean())
    elif method == "Median":
        df[column] = df[column].fillna(df[column].median())
    elif method == "Mode":
        df[column] = df[column].fillna(df[column].mode()[0])

    return df 

def auto_clean(df):
    df = df.copy()

    # Fill missing values
    for col in df.columns:
        if df[col].isnull().sum() > 0:
            if df[col].dtype != "object":
                df[col] = df[col].fillna(df[col].median())
            else:
                df[col] = df[col].fillna(df[col].mode()[0])

    # Remove outliers (IQR)
    numeric_cols = df.select_dtypes(include="number").columns

    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1

        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR

        df = df[(df[col] >= lower) & (df[col] <= upper)]

    return df