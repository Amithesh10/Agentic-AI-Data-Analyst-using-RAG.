def run_eda(df):
    column_info = []

    for col in df.columns:
        column_info.append({
            "Column": col,
            "Data Type": str(df[col].dtype),
            "Missing Values": int(df[col].isnull().sum()),
            "Unique Values": int(df[col].nunique())
        })

    eda = {
        "rows": df.shape[0],
        "columns": df.shape[1],
        "missing_values": int(df.isnull().sum().sum()),
        "duplicate_rows": int(df.duplicated().sum()),
        "column_info": column_info,
        "summary": df.describe(include="all").fillna("")
    }

    return eda