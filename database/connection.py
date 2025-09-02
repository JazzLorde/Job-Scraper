"""
Database Connection Module
Handles PostgreSQL connections and basic database operations
"""

import psycopg2
from psycopg2.extras import RealDictCursor
from config.database import DATABASE_CONFIG, CREATE_TABLE_SQL

def get_db_connection():
    """Create and return database connection"""
    try:
        conn = psycopg2.connect(**DATABASE_CONFIG)
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

def create_jobs_table():
    """Create the jobs table if it doesn't exist"""
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        cur = conn.cursor()
        cur.execute(CREATE_TABLE_SQL)
        conn.commit()
        print("Jobs table created/verified successfully")
        return True
    except Exception as e:
        print(f"Error creating table: {e}")
        return False
    finally:
        conn.close()

def clear_scraped_jobs():
    """Clear all scraped jobs from database"""
    conn = get_db_connection()
    if not conn:
        return
    
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM scraped_jobs")
        deleted_count = cur.rowcount
        conn.commit()
        print(f"Cleared {deleted_count} existing job entries from the database.")
    except Exception as e:
        print(f"Failed to clear job data: {e}")
    finally:
        conn.close()