from gemini_service import ask_gemini


def smart_ai_analyzer(df, dataset_type):

    # Convert small sample of data
    sample_data = df.head(10).to_string()

    columns = list(df.columns)

    prompt = f"""
You are a senior data scientist AI.

Analyze this dataset and act like an expert analyst.

Dataset Type (system detected): {dataset_type}

Columns:
{columns}

Sample Data:
{sample_data}

Your tasks:

1. Identify what this dataset represents
2. Find key patterns
3. Detect anomalies or unusual values
4. Give business insights
5. Suggest actions or decisions
6. Explain in simple language for non-technical users

Be specific and practical.
"""

    return ask_gemini(prompt)