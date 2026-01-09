import psycopg2
from psycopg2 import sql

DB_PARAMS = {
    "host": "localhost",
    "port": "5432",
    "database": "art_newsletter",
    "user": "postgres",
    "password": "postgres"
}

def check_db():
    print(f"Connecting to {DB_PARAMS['database']} on {DB_PARAMS['host']}...")
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cur = conn.cursor()
        
        # Check Tables
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        tables = cur.fetchall()
        print("\n--- TABLES FOUND ---")
        for t in tables:
            print(f"- {t[0]}")
            
        if not tables:
            print("NO TABLES FOUND! Migrations have not run.")
            
        # Check Alembic Version
        try:
            cur.execute("SELECT version_num FROM alembic_version")
            version = cur.fetchone()
            print(f"\n--- ALEMBIC VERSION ---: {version[0] if version else 'None'}")
        except psycopg2.errors.UndefinedTable:
            print("\n--- ALEMBIC VERSION ---: Table 'alembic_version' does not exist.")
            conn.rollback()

        conn.close()
        
    except Exception as e:
        print(f"\nERROR CONNECTING TO DB: {e}")
        print("Ensure 'db' container is UP and exposing port 5432.")

if __name__ == "__main__":
    check_db()
