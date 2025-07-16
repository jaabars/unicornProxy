import psycopg2
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
import os
import json

load_dotenv()

DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'dbname': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USERNAME'),
    'password': os.getenv('DB_PASSWORD'),
    'port': os.getenv('DB_PORT')
}

model = SentenceTransformer("all-MiniLM-L6-v2")

template_title = "Top N Messages by Channel and Date"
template_curl = (
    "curl 'https://nlg-api-dev.cslash.io/api/v1.0/report?"
    "experimentId={{experimentId}}&number={{number}}&channel={{channel}}"
    "&startDate={{startDate}}&endDate={{endDate}}'"
)

embedding = model.encode(template_title).tolist()

conn = psycopg2.connect(**DB_CONFIG)
cur = conn.cursor()

cur.execute(
    "INSERT INTO rag_knowledge_base (title, embedding, curl) VALUES (%s, %s, %s)",
    (template_title, json.dumps(embedding), template_curl)
)

conn.commit()
cur.close()
conn.close()

print("✅ Dynamic template successfully added!")
