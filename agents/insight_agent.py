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
        st.error("GROQ_API_KEY not found. Add it in .env or Streamlit Secrets.")
        st.stop()

    return Groq(api_key=api_key)


def generate_insight(df, question, context):
    client = get_groq_client()

    dataset_preview = df.head(10).to_string()
    dataset_summary = df.describe(include="all").fillna("").to_string()

    system_prompt = """
You are an Agentic AI Data Analyst.
Analyze the dataset and retrieved knowledge base context.
Give accurate, clear, business-focused answers.
Do not hallucinate.
If the data is insufficient, clearly say that.
"""

    user_prompt = f"""
User Question:
{question}

Dataset Preview:
{dataset_preview}

Dataset Summary:
{dataset_summary}

Retrieved Knowledge Base Context:
{context}

Answer in this format:

1. Direct Answer
2. Evidence from Data
3. Business Explanation
4. Recommendations
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.2,
        max_tokens=1500
    )

    return response.choices[0].message.content