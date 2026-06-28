import pandas as pd


def load_dataset(file):
    file_name = file.name.lower()

    if file_name.endswith(".csv"):
        return pd.read_csv(file)

    elif file_name.endswith(".xlsx"):
        return pd.read_excel(file)

    else:
        raise ValueError("Unsupported file format")