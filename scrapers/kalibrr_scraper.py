"""
Kalibrr Job Scraper
Scrapes IT job listings from Kalibrr with manual setup
"""

import time
import random
from datetime import datetime
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import re

from scrapers.base_scraper import BaseScraper
from utils.date_utils import convert_posted_date_kalibrr
from utils.tech_extractor import extract_technologies

class KalibrrScraper(BaseScraper):
    """Kalibrr job scraper implementation with manual setup"""
    
    def __init__(self):
        super().__init__("Kalibrr")
        self.base_url = "https://www.kalibrr.com"
    
    def scrape_manual(self, max_jobs=500):
        """Scrape Kalibrr with manual filter setup"""
        print(f"\nManual Kalibrr IT Jobs Scraping")
        
        with self:
            all_job_urls = []
            
            try:
                # Step 1: Navigate to Kalibrr main page
                print("Navigating to Kalibrr homepage...")
                self.driver.get(self.base_url)
                time.sleep(random.uniform(3, 5))
                
                # Step 2: Wait for manual filter setup
                print("\n" + "="*60)
                print("MANUAL SETUP REQUIRED")
                print("="*60)
                print("Please do the following manually in the browser:")
                print("1. Click the Filter button")
                print("2. Click 'Job function' dropdown")
                print("3. Check the 'IT and Software' checkbox")
                print("4. Click the Search button")
                print("5. Wait for the IT jobs to load completely")
                print("6. Make sure you can see the job listings")
                print("="*60)
                print("When you're ready for scraping to begin, press ENTER...")
                
                # Wait for user confirmation
                input()
                
                print("Starting automated scraping process...")
                print("Waiting for job content to load completely...")
                
                # Give a moment for any final loading
                time.sleep(random.uniform(2, 4))
                
                # First stage: Collect job URLs (simplified - like your original)
                while True:
                    soup = BeautifulSoup(self.driver.page_source, "html.parser")
                    
                    # Extract job links from current page
                    job_links = soup.find_all('a', class_='k-text-black', attrs={'itemprop': 'name'})
                    print(f"Found {len(job_links)} job links on current page")
                    
                    # Add new unique URLs
                    new_urls = []
                    for job_link in job_links:
                        job_url = "https://www.kalibrr.com" + job_link.get('href')
                        if job_url not in all_job_urls:
                            new_urls.append(job_url)
                            all_job_urls.append(job_url)
                    
                    print(f"Added {len(new_urls)} new unique job URLs. Total: {len(all_job_urls)}")
                    
                    # Check if we've reached our target
                    if len(all_job_urls) >= max_jobs:
                        print(f"Target reached! Collected {len(all_job_urls)} jobs (target: {max_jobs})")
                        break
                    
                    # If no new URLs found, check what to do next
                    if len(new_urls) == 0:
                        print("No new job URLs found...")
                        break
                    
                    # Simple break for now - you can add Load More logic later if needed
                    break
                
                print(f"Total unique job URLs collected: {len(all_job_urls)}")
                
                # Ask user if they want to proceed with individual job scraping
                if len(all_job_urls) > 0:
                    print(f"\nReady to scrape {len(all_job_urls)} individual job pages")
                    proceed = input("Do you want to proceed with detailed job scraping? (y/n): ").lower().strip()
                    
                    if proceed != 'y':
                        print("Scraping cancelled by user")
                        return
                else:
                    print("No job URLs collected. Please check the manual setup and try again.")
                    return
                    
            except Exception as e:
                print(f"Error during setup: {e}")
                return
            
            # Second stage: Visit individual job pages for detailed information
            print(f"\nStarting detailed job information extraction...")
            
            for i, job_url in enumerate(all_job_urls, 1):
                print(f"\nProcessing job {i}/{len(all_job_urls)}: {job_url}")
                self._process_job_detail(job_url)
    
    def _normalize_seniority_level(self, seniority_level):
        """Normalize seniority level to Entry Level, Non-Entry Level, or Internship"""
        
        seniority_lower = seniority_level.lower()
        
        # Keep Internship as is
        if 'internship' in seniority_lower:
            return "Internship"
        
        # Check if current seniority level indicates entry level
        entry_level_indicators = [
            'entry level', 'entry-level', 'associate', 'junior', 
            'graduate', 'fresher', 'beginner'
        ]
        
        # If any entry level indicator is found, return Entry Level
        if any(indicator in seniority_lower for indicator in entry_level_indicators):
            return "Entry Level"
        
        # Everything else becomes Non-Entry Level
        return "Non-Entry Level"

    # Update your _process_job_detail method - replace the save_job section:
    def _process_job_detail(self, job_url):
        """Process individual job detail page"""
        try:
            self.driver.get(job_url)
            time.sleep(random.uniform(4, 6))
            soup = BeautifulSoup(self.driver.page_source, "html.parser")

            # Extract company name
            company_elem = soup.find('h2', class_='k-inline-block')
            company_name = company_elem.text.strip() if company_elem else "N/A"

            # Extract job title
            title_elem = soup.find('h1', attrs={'itemprop': 'title'})
            job_title = title_elem.text.strip().replace('\xa0', ' ') if title_elem else "N/A"

            # Extract location
            location_elem = soup.find('span', attrs={'itemscope': True, 'itemtype': 'http://schema.org/PostalAddress'})
            location = location_elem.text.strip() if location_elem else "N/A"

            # Extract employment type
            employment_elem = soup.find('a', class_='k-text-grey-900', href=re.compile(r'/home/t/'))
            employment_type = employment_elem.text.strip() if employment_elem else "Not specified"

            # Extract remote option
            remote_elem = soup.find('span', string=re.compile(r'Remote|Hybrid|On-site'))
            remote_option = remote_elem.text.strip() if remote_elem else "On-site"

            # Extract posted date
            posted_date = None
            try:
                date_elem = soup.find('span', attrs={'itemprop': 'datePosted'})
                if date_elem:
                    date_str = date_elem.text.strip()
                    posted_date = date_str.split('T')[0]  # Extract YYYY-MM-DD part
                else:
                    posted_text_elem = soup.find('p', string=re.compile(r'Posted.*ago'))
                    if posted_text_elem:
                        posted_date = convert_posted_date_kalibrr(posted_text_elem.text.strip())
            except Exception as e:
                print(f"Could not extract posted date: {e}")

            # Extract seniority level
            seniority_elem = soup.find('dd', class_='k-inline-flex k-items-center')
            seniority_level = "Not specified"
            if seniority_elem:
                seniority_link = seniority_elem.find('a')
                if seniority_link:
                    seniority_level = seniority_link.text.strip()

            # Extract salary
            salary = None
            try:
                salary_elem = soup.find('li', class_='md:k-list-disc md:k-ml-7')
                if salary_elem:
                    salary_spans = salary_elem.find_all('span')
                    if len(salary_spans) >= 3:
                        potential_salary = f"{salary_spans[0].text.strip()}{salary_spans[1].text.strip()}{salary_spans[2].text.strip()}"
                    elif len(salary_spans) >= 1:
                        potential_salary = salary_spans[0].text.strip()
                    else:
                        potential_salary = ""
                    
                    if potential_salary and (re.search(r'₱|PHP|php|\d', potential_salary) and 
                                        not potential_salary.upper().strip() in ['FULL_TIME', 'PART_TIME', 'CONTRACT']):
                        salary = potential_salary
                        print(f"Found salary: {salary}")
            except Exception as e:
                print(f"Could not extract salary: {e}")

            # Extract qualifications text
            qualifications_text = ""
            try:
                qualifications_elem = soup.find('div', attrs={'itemprop': 'qualifications'})
                if qualifications_elem:
                    qualifications_text = qualifications_elem.get_text(separator=' ', strip=True)
                    qualifications_text = re.sub(r'\s+', ' ', qualifications_text)
                    print(f"Qualifications extracted: {len(qualifications_text)} characters")
            except Exception as e:
                print(f"Error extracting qualifications: {e}")

            # Extract technologies
            technologies = None
            try:
                combined_text_for_tech = f"{job_title} {qualifications_text}"
                technologies = extract_technologies(combined_text_for_tech)
                
                if technologies:
                    print(f"Technologies found: {technologies}")
                else:
                    print("No technologies detected")
                    
            except Exception as e:
                print(f"Error extracting technologies: {e}")

            # Normalize seniority level
            normalized_seniority = self._normalize_seniority_level(seniority_level)

            # Save job to database
            self.save_job(
                job_title=job_title,
                company_name=company_name,
                location=location,
                job_url=job_url,
                employment_type=employment_type,
                remote_option=remote_option,
                posted_date=posted_date,
                platform=self.platform_name,
                keyword="IT and Software",
                seniority_level=normalized_seniority,  # Use normalized seniority instead
                salary=salary,
                technologies=technologies,
                qualifications=qualifications_text,
                scraped_at=datetime.now()
            )
            
        except Exception as e:
            print(f"Error scraping job details: {e}")