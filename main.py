"""
Job Scraper Main Entry Point
Clean, organized job scraping system for Philippine IT jobs
"""

from database.connection import create_jobs_table, clear_scraped_jobs
# from scrapers.indeed_scraper import IndeedScraper
from scrapers.kalibrr_scraper import KalibrrScraper
from scrapers.jobstreet_scraper import JobstreetScraper
from scrapers.linkedin_scraper import LinkedinScraper
from scrapers.foundit_scraper import FounditScraper


if __name__ == "__main__":
    # Initialize database
    print("Initializing PostgreSQL database connection...")
    if create_jobs_table():
        print("Database setup successful!")
        
        # Uncomment the scrapers you want to run:
        clear_scraped_jobs()

        # Run individual scrapers
        # scraper = IndeedScraper()
        # scraper.scrape("software developer")
        
        # scraper = KalibrrScraper()
        #scraper.scrape_manual()
        
        # Add other scrapers as you create them:
        # scraper = JobstreetScraper()  
        # scraper.scrape_manual()

        scraper = LinkedinScraper()
        scraper.scrape_manual()

        scraper = FounditScraper()
        scraper.scrape_manual()

        
        print("Job scraper ready to run!")
        print("Uncomment the scraper functions you want to use.")
    else:
        print("Database setup failed! Please check your PostgreSQL connection.")
        print("Make sure PostgreSQL is running and database 'JobPostings' exists.")