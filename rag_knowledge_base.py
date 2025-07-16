import psycopg2
from sentence_transformers import SentenceTransformer

DB_CONFIG = {
    'host': '10.10.10.15',
    'dbname': 'mydb',
    'user': 'nlguser',
    'password': 'nlgPassword2025',
    'port': 5432
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
    (template_title, embedding, template_curl)
)

conn.commit()
cur.close()
conn.close()

print("✅ Динамический шаблон успешно добавлен!")
