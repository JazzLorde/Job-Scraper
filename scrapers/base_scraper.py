"""
Base Scraper Class
Contains common functionality for all scrapers
"""

import hashlib
from datetime import datetime
from database.connection import get_db_connection
from utils.categorizer import categorize_job_title
from utils.browser import get_chrome_driver

class BaseScraper:
    """Base class for all job scrapers"""
    
    def __init__(self, platform_name):
        self.platform_name = platform_name
        self.driver = None
    
    def save_job(self, **kwargs):
        """Save job to PostgreSQL database"""
        conn = get_db_connection()
        if not conn:
            print("No database connection available")
            return
        
        try:
            # Extract qualifications text for duplicate checking
            qualifications = kwargs.get('qualifications', '')
            job_title = kwargs.get('job_title', '')
            
            if job_title:
                category = categorize_job_title(job_title)
                kwargs['category'] = category
                print(f"Category: {category}")
            
            # Check for duplicates
            if qualifications:
                qualifications_hash = hashlib.md5(qualifications.strip().encode('utf-8')).hexdigest()
                kwargs['qualifications_hash'] = qualifications_hash
                
                cur = conn.cursor()
                cur.execute("SELECT job_title, company_name FROM scraped_jobs WHERE qualifications_hash = %s LIMIT 1", 
                           (qualifications_hash,))
                existing_job = cur.fetchone()
                
                if existing_job:
                    print(f"Duplicate job skipped (same qualifications): {kwargs['job_title']} at {kwargs['company_name']}")
                    print(f"Original job: {existing_job[0]} at {existing_job[1]}")
                    conn.close()
                    return
            
            # Insert new job
            cur = conn.cursor()
            columns = list(kwargs.keys())
            placeholders = ', '.join(['%s'] * len(kwargs))
            columns_str = ', '.join(columns)
            values = list(kwargs.values())
            
            insert_query = f"INSERT INTO scraped_jobs ({columns_str}) VALUES ({placeholders})"
            cur.execute(insert_query, values)
            conn.commit()
            
            print(f"Saved new job: {kwargs['job_title']} at {kwargs['company_name']}")
            if kwargs.get('technologies'):
                print(f"Technologies: {kwargs['technologies']}")
                
        except Exception as e:
            print(f"Database save error: {e}")
            print(f"Data: {kwargs}")
        finally:
            conn.close()
    
    def setup_driver(self):
        """Initialize Chrome driver"""
        if not self.driver:
            self.driver = get_chrome_driver()
        return self.driver
    
    def close_driver(self):
        """Close Chrome driver"""
        if self.driver:
            self.driver.quit()
            self.driver = None
    
    def __enter__(self):
        """Context manager entry"""
        self.setup_driver()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close_driver()