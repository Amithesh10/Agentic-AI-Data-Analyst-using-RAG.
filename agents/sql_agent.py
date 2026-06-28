import os
import streamlit as st
from groq import Groq

MODEL_NAME = "llama-3.3-70b-versatile"


def get_groq_client():
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        try:
            api_key = st.secrets["GROQ_API_KEY"]
        except Exception:
            api_key = None

    if not api_key:
        st.error("GROQ_API_KEY not found.")
        st.stop()

    return Groq(api_key=api_key)


def generate_sql(df, question):
    client = get_groq_client()

    columns = list(df.columns)

    system_prompt = """
You are a SQL Agent.
Generate an SQLite query for the user's question.
Use only the table name uploaded_data.
Use only the given columns.
Return the SQL query first, then a short explanation.
"""

    user_prompt = f"""
Table Name:
uploaded_data

Columns:
{columns}

User Question:
{question}
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.1,
        max_tokens=800
    )

    return response.choices[0].message.content