import psycopg2
from sentence_transformers import SentenceTransformer
import json

# PostgreSQL connection config
DB_CONFIG = {
    'host': 'localhost',
    'dbname': 'Boombom',
    'user': 'postgres',
    'password': 'admin',
    'port': 5432
}

queries = [
    {
        "title": "Top N Messages per Experiment",
        "curl": "curl 'https://nlg-api-dev.cslash.io/api/v1.0/report?experimentId={{experimentId}}&number={{number}}&channel={{channel}}&startDate={{startDate}}&endDate={{endDate}}'",
        "json_payload": {
            "experimentId": "{{experimentId}}",
            "number": "{{number}}",
            "channel": "{{channel}}",
            "startDate": "{{startDate}}",
            "endDate": "{{endDate}}"
        }
    },
    {
        "title": "Full Report per Experiment",
        "curl": "curl 'https://nlg-api-dev.cslash.io/api/v1.0/report/full?experimentId=272' ...",
        "json_payload": {}
    },
    {
        "title": "Best Performing Content per Experiment",
        "curl": "curl 'https://nlg-api-dev.cslash.io/api/v1.0/report?experimentId=272&number=1' ...",
        "json_payload": {}
    }
]

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Connect to database
conn = psycopg2.connect(**DB_CONFIG)
cur = conn.cursor()

# Insert queries with json_payload
for q in queries:
    embedding = model.encode(q["title"]).tolist()
    cur.execute(
        "INSERT INTO rag_knowledge_base (title, embedding, curl, json_payload) VALUES (%s, %s, %s, %s)",
        (q["title"], embedding, q["curl"], json.dumps(q["json_payload"]))
    )

conn.commit()
cur.close()
conn.close()

print("✅ RAG knowledge base with JSON payload successfully populated.")
