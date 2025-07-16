from fastapi import FastAPI, Request
from sentence_transformers import SentenceTransformer
from datetime import datetime, timedelta
import openai
import httpx
import json
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
model = SentenceTransformer("all-MiniLM-L6-v2")

# Securely load the API key
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.post("/custom-report")
async def custom_report(request: Request):
    body = await request.body()
    user_query = body.decode("utf-8").strip()

    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return {"error": "Missing or invalid Authorization header"}

    bearer_token = auth_header.split(" ")[1]

    params = await extract_parameters_from_openai(user_query)
    if not params:
        return {"error": "Failed to extract parameters"}

    url = build_custom_url(params)
    data = await fetch_report_data(url, bearer_token)

    return {"url": url, "data": data}


def build_custom_url(params: dict) -> str:
    base_url = "https://nlg-api-dev.cslash.io/api/v1.0/report/custom?"
    query_string = '&'.join(f"{k}={v}" for k, v in params.items())
    return base_url + query_string


async def fetch_report_data(url: str, token: str) -> dict:
    try:
        headers = {
            "Authorization": f"Bearer {token}",
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)

            print("🔗 URL:", url)
            print("📦 Status Code:", response.status_code)
            print("📥 Response Text:", response.text)

            response.raise_for_status()
            return response.json()

    except Exception as e:
        print("HTTP Request Error:", e)
        return {"error": str(e)}


async def extract_parameters_from_openai(user_prompt: str):
    try:
        today = datetime.today()
        today_str = today.strftime("%Y-%m-%d")
        last_week_start = (today - timedelta(days=7)).strftime("%Y-%m-%d")
        last_month_start = (today - timedelta(days=30)).strftime("%Y-%m-%d")
        yesterday = (today - timedelta(days=1)).strftime("%Y-%m-%d")

        system_prompt = f"""
You are an assistant that extracts structured API parameters from natural language user input.

Return ONLY raw JSON (no explanation).
Do NOT wrap with markdown like ```json.

Extract these keys if mentioned:
- startDate (format: YYYY-MM-DD)
- endDate (format: YYYY-MM-DD)
- channel (e.g., YOUTUBE, SMS, FACEBOOK)
- kpi (default: "percentage")
- number (top N count)
- experimentId (default: 3)

Today is {today_str}.
Use these rules if user says:
- "last week" = startDate: {last_week_start}, endDate: {today_str}
- "last month" = startDate: {last_month_start}, endDate: {today_str}
- "yesterday" = startDate & endDate: {yesterday}
"""

        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.2,
            max_tokens=300
        )

        content = response.choices[0].message.content.strip()
        print("🧠 OpenAI JSON:", content)
        return json.loads(content)

    except Exception as e:
        print("OpenAI Error:", e)
        return None
