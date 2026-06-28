def generate_kpis(df):
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    kpis = {}

    for col in numeric_cols:
        kpis[col] = {
            "Total": round(df[col].sum(), 2),
            "Average": round(df[col].mean(), 2),
            "Maximum": round(df[col].max(), 2),
            "Minimum": round(df[col].min(), 2),
            "Standard Deviation": round(df[col].std(), 2)
        }

    return kpis