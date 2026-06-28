import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression
import numpy as np


def forecast_column(df, column, periods):
    data = df[[column]].dropna().reset_index(drop=True)

    data["time_index"] = range(len(data))

    X = data[["time_index"]]
    y = data[column]

    model = LinearRegression()
    model.fit(X, y)

    future_index = np.arange(len(data), len(data) + periods).reshape(-1, 1)
    predictions = model.predict(future_index)

    forecast_df = pd.DataFrame({
        "Period": range(1, periods + 1),
        "Forecast": predictions
    })

    fig = px.line(
        forecast_df,
        x="Period",
        y="Forecast",
        title=f"Forecast for {column}"
    )

    return forecast_df, fig