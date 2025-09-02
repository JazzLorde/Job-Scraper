"""
Database Configuration
Contains all database-related settings and configurations
"""

# PostgreSQL Database Configuration
DATABASE_CONFIG = {
    'host': 'localhost',
    'database': 'JobPostings',
    'user': 'postgres',
    'password': 'admin123',
    'port': 5432
}

# Database table schema
CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS scraped_jobs (
    id SERIAL PRIMARY KEY,
    job_title VARCHAR(500),
    company_name VARCHAR(300),
    location VARCHAR(200),
    job_url TEXT,
    employment_type VARCHAR(50),
    remote_option VARCHAR(20),
    posted_date DATE,
    platform VARCHAR(50),
    keyword VARCHAR(100),
    seniority_level VARCHAR(100),
    salary TEXT,
    technologies TEXT,
    qualifications TEXT,
    qualifications_hash VARCHAR(32),
    category VARCHAR(100),
    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""