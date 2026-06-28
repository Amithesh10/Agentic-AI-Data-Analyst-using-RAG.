import plotly.express as px


def create_chart(df, chart_type, x_col, y_col):
    if chart_type == "Bar Chart":
        return px.bar(df, x=x_col, y=y_col, title=f"{y_col} by {x_col}")

    elif chart_type == "Line Chart":
        return px.line(df, x=x_col, y=y_col, title=f"{y_col} trend by {x_col}")

    elif chart_type == "Scatter Plot":
        return px.scatter(df, x=x_col, y=y_col, title=f"{x_col} vs {y_col}")

    elif chart_type == "Histogram":
        return px.histogram(df, x=x_col, title=f"Distribution of {x_col}")

    elif chart_type == "Box Plot":
        return px.box(df, x=x_col, y=y_col, title=f"Box Plot of {y_col} by {x_col}")

    else:
        return px.scatter(df, x=x_col, y=y_col)