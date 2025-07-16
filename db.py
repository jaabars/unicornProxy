import psycopg2

DB_CONFIG = {
    'host': 'localhost',
    'dbname': 'Boombom',
    'user': 'postgres',
    'password': 'admin',
    'port': 5432
}

def get_connection():
    return psycopg2.connect(**DB_CONFIG)
