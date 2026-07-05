import os
import json

from dotenv import load_dotenv
from google import genai

from profiler import full_profile

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def smart_ai_analyzer(df, dataset_type):

    profile = full_profile(df)

    prompt = f"""
You are a world-class Senior Data Analyst.

Analyze the following dataset profile.

Dataset Type:
{dataset_type}

Dataset Profile:
{json.dumps(profile, indent=2)}

Return your answer in markdown with the following sections.

# Executive Summary

# Key Insights

# Important Trends

# Risks

# Recommendations

# Business Opportunities

# Overall Data Quality

Keep the response under 500 words.
"""

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:

        return f"""
# AI Analysis Error

Unable to analyze this dataset.

Reason:

{str(e)}
"""