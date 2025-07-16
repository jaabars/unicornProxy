
import os
import psycopg2
from sentence_transformers import SentenceTransformer

DB_CONFIG = {
    'host': '10.10.10.15',
    'dbname': 'mydb',
    'user': 'nlguser',
    'password': 'nlgPassword2025'
}

DOCUMENTS_DIR = "docs"
CHUNK_SIZE = 500
model = SentenceTransformer("all-MiniLM-L6-v2")

def chunk_text(text, max_length=CHUNK_SIZE):
    paragraphs = text.split('\n')
    chunks, current = [], ""
    for para in paragraphs:
        if len(current) + len(para) < max_length:
            current += " " + para
        else:
            chunks.append(current.strip())
            current = para
    if current:
        chunks.append(current.strip())
    return chunks

conn = psycopg2.connect(**DB_CONFIG)
cur = conn.cursor()

for filename in os.listdir(DOCUMENTS_DIR):
    if not filename.endswith(".txt"):
        continue
    filepath = os.path.join(DOCUMENTS_DIR, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    chunks = chunk_text(content)
    embeddings = model.encode(chunks)
    for chunk, embedding in zip(chunks, embeddings):
        cur.execute(
            "INSERT INTO documents (chunk_text, embedding) VALUES (%s, %s)",
            (chunk, [float(x) for x in embedding])
        )

conn.commit()
cur.close()
conn.close()
print("✅ Documentation loaded successfully.")
