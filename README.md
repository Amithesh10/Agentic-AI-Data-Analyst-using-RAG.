# Agentic AI Data Analyst using RAG

> **An AI-powered multi-agent analytics platform that automates data analysis, business intelligence, and reporting using Agentic AI, Retrieval-Augmented Generation (RAG), and Groq LLM.**

---

## 🚀 Overview

**IntelliAnalyst** is an intelligent data analytics platform that enables users to upload datasets and optional knowledge-base documents to perform automated data analysis through specialized AI agents.

The application combines **Agentic AI** and **Retrieval-Augmented Generation (RAG)** to generate business insights, KPIs, SQL queries, visualizations, forecasts, and downloadable reports from user-provided data.

Unlike traditional dashboards, IntelliAnalyst acts as an AI Data Analyst capable of understanding both structured datasets and business documents.

---

## ✨ Features

* 📂 Upload CSV and Excel datasets
* 📚 Upload PDF, DOCX, and TXT knowledge-base documents
* 🤖 Multi-Agent AI architecture
* 📊 Automated Exploratory Data Analysis (EDA)
* 📈 Automatic KPI generation
* 💬 Natural language business insights
* 🛢️ SQL query generation from plain English
* 📉 Interactive data visualization
* 🔮 Forecasting using Machine Learning
* 📄 Downloadable PDF reports
* ⚡ Powered by Groq LLM for fast inference
* 🧠 Retrieval-Augmented Generation (RAG) using ChromaDB

---

# 🏗️ Project Architecture

```text
                 User
                  │
                  ▼
       Upload Dataset (CSV/XLSX)
                  │
                  ▼
          Pandas DataFrame
                  │
                  ├───────────────┐
                  │               │
                  ▼               ▼
            EDA Agent        KPI Agent
                  │               │
                  └──────┬────────┘
                         │
                         ▼
               User Business Question
                         │
                         ▼
         Upload Knowledge Base (Optional)
                         │
                         ▼
             Document Loader (PDF/DOCX/TXT)
                         │
                         ▼
                  Text Chunking
                         │
                         ▼
            Sentence Transformer
                         │
                         ▼
                     ChromaDB
                         │
                         ▼
                  Context Retrieval
                         │
                         ▼
                  Groq AI (LLM)
                         │
      ┌────────────┬────────────┬─────────────┬─────────────┐
      ▼            ▼            ▼             ▼             ▼
 Insight Agent   SQL Agent   Chart Agent   Forecast     Report
                                               Agent      Agent
      │            │            │             │            │
      └────────────┴────────────┴─────────────┴────────────┘
                         │
                         ▼
                 AI Generated Outputs
```

---

# 🧠 Agentic AI Workflow

## 1️⃣ Data Upload

The user uploads:

* CSV
* Excel

The system loads the dataset into a Pandas DataFrame.

---

## 2️⃣ Knowledge Base Upload (Optional)

Users can upload company documents such as:

* SOPs
* Business Rules
* Product Catalogs
* Company Policies
* Previous Reports
* Financial Documents

These documents are processed for Retrieval-Augmented Generation (RAG).

---

## 3️⃣ RAG Pipeline

The uploaded documents go through:

```
Documents
      │
      ▼
Text Extraction
      │
      ▼
Chunking
      │
      ▼
Sentence Embeddings
      │
      ▼
ChromaDB
      │
      ▼
Retriever
```

Whenever the user asks a question, the retriever fetches the most relevant document chunks, which are sent to the LLM as additional context.

---

## 4️⃣ AI Agents

### 🔹 EDA Agent

Performs:

* Dataset profiling
* Missing value analysis
* Duplicate detection
* Data type analysis
* Statistical summary

---

### 🔹 KPI Agent

Automatically computes:

* Total
* Average
* Maximum
* Minimum
* Standard Deviation

for every numeric column.

---

### 🔹 Insight Agent

Uses:

* Dataset summary
* User question
* Retrieved RAG context

to generate:

* Business insights
* Trend analysis
* Explanations
* Recommendations

---

### 🔹 SQL Agent

Converts natural language into SQL queries.

Example:

**Question**

> Show top 5 products by revenue.

Generated SQL:

```sql
SELECT Product,
SUM(Revenue) AS Total_Revenue
FROM uploaded_data
GROUP BY Product
ORDER BY Total_Revenue DESC
LIMIT 5;
```

---

### 🔹 Chart Agent

Creates:

* Bar Charts
* Line Charts
* Scatter Plots
* Histograms
* Box Plots

---

### 🔹 Forecast Agent

Performs forecasting on selected numeric columns using machine learning.

---

### 🔹 Report Agent

Generates downloadable PDF reports containing:

* Dataset overview
* EDA summary
* KPI summary
* AI-generated insights

---

# 📸 Application Workflow

```text
Upload Dataset
       │
       ▼
Upload Knowledge Base (Optional)
       │
       ▼
Data Processing
       │
       ▼
EDA + KPI Generation
       │
       ▼
Retrieve Relevant Context (RAG)
       │
       ▼
Groq LLM
       │
       ▼
AI Agents
       │
       ├── Business Insights
       ├── SQL Generation
       ├── Charts
       ├── Forecast
       └── PDF Report
       │
       ▼
Interactive Dashboard
```

---

# 💻 Tech Stack

| Category            | Technology                       |
| ------------------- | -------------------------------- |
| Frontend            | Streamlit                        |
| LLM                 | Groq (Llama 3.3 70B)             |
| Agentic AI          | Multi-Agent Architecture         |
| RAG                 | ChromaDB + Sentence Transformers |
| Embeddings          | all-MiniLM-L6-v2                 |
| Data Processing     | Pandas, NumPy                    |
| Machine Learning    | Scikit-learn                     |
| Visualization       | Plotly                           |
| PDF Generation      | ReportLab                        |
| Document Processing | PyPDF, python-docx               |
| Deployment          | Streamlit Community Cloud        |

---

# 📁 Project Structure

```text
IntelliAnalyst/
│
├── agents/
│   ├── eda_agent.py
│   ├── kpi_agent.py
│   ├── insight_agent.py
│   ├── sql_agent.py
│   └── forecast_agent.py
│
├── rag/
│   ├── document_loader.py
│   ├── retriever.py
│   └── vector_store.py
│
├── utils/
│   ├── charts.py
│   ├── data_loader.py
│   └── report_generator.py
│
├── app.py
├── requirements.txt
├── .env.example
└── README.md
```

---

# ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/IntelliAnalyst.git
```

Navigate to the project:

```bash
cd IntelliAnalyst
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
```

Run the application:

```bash
streamlit run app.py
```

---

# 🌐 Deployment

The application is designed for deployment on **Streamlit Community Cloud**.

Add the following secret in **App Settings → Secrets**:

```toml
GROQ_API_KEY = "your_groq_api_key"
```

---

# 🎯 Sample Use Cases

* Business Intelligence
* Sales Analytics
* Financial Analysis
* Inventory Monitoring
* KPI Reporting
* Executive Dashboards
* SQL Query Assistant
* AI Data Exploration
* Decision Support Systems

---

# 📈 Future Enhancements

* Multi-dataset analysis
* Real-time database connectivity (MySQL, PostgreSQL, SQL Server)
* Power BI and Tableau integration
* Conversational AI dashboard
* Role-based authentication
* Advanced forecasting models (ARIMA, Prophet, LSTM)
* Dashboard export (PPT, Excel)
* Scheduled report generation
* Multi-language support

---

# 👨‍💻 Author

**Amithesh T S**

* GitHub: [https://github.com/Amithesh10](https://github.com/Amithesh10)
* LinkedIn:[ www.linkedin.com/in/amithesh-ts]( www.linkedin.com/in/amithesh-ts)

---

## ⭐ If you found this project useful, consider giving it a star on GitHub!
