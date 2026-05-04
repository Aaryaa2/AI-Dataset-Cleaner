def generate_insights(df):

    insights = []

    total_rows = len(df)

    # ---------- Missing Values ----------
    missing = df.isnull().sum()

    for col in df.columns:
        if missing[col] > 0:
            percent = (missing[col] / total_rows) * 100

            if percent > 30:
                insights.append(
                    f"⚠️ {col} has {percent:.1f}% missing values → consider dropping or strong cleaning"
                )
            else:
                insights.append(
                    f"ℹ️ {col} has {percent:.1f}% missing values → fill with mean/median"
                )

    # ---------- Outliers ----------
    numeric_cols = df.select_dtypes(include="number").columns

    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1

        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR

        outliers = ((df[col] < lower) | (df[col] > upper)).sum()

        if outliers > 0:
            insights.append(
                f"⚠️ {col} contains {outliers} outliers → consider removing or capping"
            )

    # ---------- Clean dataset ----------
    if len(insights) == 0:
        insights.append("✅ Dataset looks clean and ready for analysis!")

    return insights