"""
JobStreet Job Scraper
Scrapes IT job listings from JobStreet with manual setup
"""

import time
import random
from datetime import datetime
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import re

from scrapers.base_scraper import BaseScraper
from utils.date_utils import convert_posted_date_jobstreet
from utils.tech_extractor import extract_technologies

class JobstreetScraper(BaseScraper):
    """JobStreet job scraper implementation with manual setup"""
    
    def __init__(self):
        super().__init__("JobStreet")
        self.base_url = "https://ph.jobstreet.com"
    
    def scrape_manual(self, max_jobs=500):
        """Scrape JobStreet with manual filter setup"""
        print(f"\nManual JobStreet IT Jobs Scraping")
        
        with self:
            all_job_urls = []
            
            try:
                # Navigate to JobStreet Philippines
                print("Navigating to JobStreet Philippines homepage...")
                self.driver.get(self.base_url)
                time.sleep(random.uniform(3, 5))
                
                # Manual setup instructions
                print("\n" + "="*60)
                print("MANUAL SETUP REQUIRED")
                print("="*60)
                print("Please do the following manually in the browser:")
                print("1. Look for the search filters or advanced search options")
                print("2. Find and click on 'Industry' or 'Job Category' filter")
                print("3. Select 'Information Technology' or 'IT' related categories")
                print("4. You can also set other filters like:")
                print("   - Location (if you want specific cities)")
                print("   - Experience level")
                print("   - Posted date (for freshness)")
                print("5. Click 'Search' or 'Apply Filters'")
                print("6. Wait for the IT job results to load completely")
                print("7. Make sure you can see the job listings")
                print("="*60)
                print("When you're ready for scraping to begin, press ENTER...")
                
                # Wait for user confirmation
                input()
                
                print("Starting automated scraping process...")
                time.sleep(random.uniform(2, 4))
                
                # Collect job URLs with pagination
                page = 1
                consecutive_empty_pages = 0
                
                while len(all_job_urls) < max_jobs:
                    print(f"\nProcessing page {page}...")
                    time.sleep(random.uniform(2, 4))
                    soup = BeautifulSoup(self.driver.page_source, "html.parser")
                    
                    # Extract job links from current page
                    job_links = soup.select('a[data-automation="jobTitle"]')
                    print(f"Found {len(job_links)} job links on page {page}")
                    
                    if not job_links:
                        print(f"No job links found on page {page}. Might have reached the end.")
                        break
                    
                    # Add new unique URLs with posted dates
                    new_urls = []
                    for job_link in job_links:
                        try:
                            href = job_link['href'].split("#")[0]
                            job_url = "https://ph.jobstreet.com" + href
                            
                            # Extract posted date
                            posted_tag = job_link.find_next('span', attrs={"data-automation": "jobListingDate"})
                            raw_posted = posted_tag.text.strip().replace("Posted ", "") if posted_tag else "N/A"
                            posted_date = convert_posted_date_jobstreet(raw_posted)
                            
                            if job_url not in [url for url, _ in all_job_urls]:
                                new_urls.append((job_url, posted_date))
                                all_job_urls.append((job_url, posted_date))
                                
                        except Exception as e:
                            print(f"Error processing job link: {e}")
                            continue
                    
                    print(f"Added {len(new_urls)} new unique job URLs. Total: {len(all_job_urls)}")
                    
                    if len(all_job_urls) >= max_jobs:
                        break
                    
                    # Handle pagination
                    if len(new_urls) == 0:
                        consecutive_empty_pages += 1
                        if consecutive_empty_pages >= 3:
                            print("Found no new jobs for consecutive pages. Reached the end.")
                            break
                    else:
                        consecutive_empty_pages = 0
                    
                    # Try to navigate to next page
                    try:
                        next_button = self.driver.find_element(By.CSS_SELECTOR, 'a[rel="nofollow next"]')
                        if next_button and next_button.is_displayed() and next_button.is_enabled():
                            print(f"Auto-navigating to page {page + 1}...")
                            next_button.click()
                            page += 1
                            time.sleep(random.uniform(3, 5))
                            continue
                        else:
                            print("No more pages found.")
                            break
                    except Exception as e:
                        print(f"Error handling pagination: {e}")
                        break
                
                print(f"Total unique job URLs collected: {len(all_job_urls)}")
                
                # Process individual jobs
                for i, (job_url, posted_date) in enumerate(all_job_urls, 1):
                    print(f"\nProcessing job {i}/{len(all_job_urls)}: {job_url}")
                    self._process_job_detail(job_url, posted_date)
                    
            except Exception as e:
                print(f"Error during JobStreet scraping: {e}")
    
    def _process_job_detail(self, job_url, posted_date):
        """Process individual job detail page"""
        try:
            self.driver.get(job_url)
            time.sleep(random.uniform(4, 6))
            soup = BeautifulSoup(self.driver.page_source, "html.parser")

            # Extract job details
            job_title = soup.select_one('[data-automation="job-detail-title"]').text.strip() if soup.select_one('[data-automation="job-detail-title"]') else "N/A"
            company = soup.select_one('[data-automation="advertiser-name"]').text.strip() if soup.select_one('[data-automation="advertiser-name"]') else "N/A"
            location = soup.select_one('[data-automation="job-detail-location"]').text.strip() if soup.select_one('[data-automation="job-detail-location"]') else "N/A"

            work_type = soup.find('span', attrs={"data-automation": "job-detail-work-type"})
            employment_type = work_type.a.text.strip() if work_type and work_type.a else "N/A"

            # Extract salary
            salary = None
            try:
                salary_elem = soup.select_one('span[data-automation="job-detail-salary"]')
                if salary_elem:
                    salary = salary_elem.text.strip()
                    print(f"Found salary: {salary}")
            except Exception as e:
                print(f"Could not extract salary: {e}")

            # Extract qualifications text
            qualifications_text = ""
            try:
                selectors_to_try = [
                    'div._1lns5ab0.sye2ly0',
                    'div[data-automation="jobAdDetails"]',
                    'div.job-description',
                    'div.FYwKg',
                ]
                
                qualifications_elem = None
                for selector in selectors_to_try:
                    qualifications_elem = soup.select_one(selector)
                    if qualifications_elem:
                        print(f"Found qualifications using selector: {selector}")
                        break
                
                if qualifications_elem:
                    qualifications_text = qualifications_elem.get_text(separator=' ', strip=True)
                    qualifications_text = re.sub(r'\s+', ' ', qualifications_text)
                    print(f"Qualifications extracted: {len(qualifications_text)} characters")
                else:
                    print("No qualifications element found with any selector")
                        
            except Exception as e:
                print(f"Error extracting qualifications: {e}")

            # Extract technologies
            technologies = None
            try:
                combined_text_for_tech = f"{job_title} {qualifications_text}"
                technologies = extract_technologies(combined_text_for_tech)
                if technologies:
                    print(f"Technologies found: {technologies}")
            except Exception as e:
                print(f"Error extracting technologies: {e}")

            # Determine remote option
            location_lower = location.lower()
            text = soup.get_text().lower()
            combined_text = f"{job_title.lower()} {text}"
            
            if any(keyword in location_lower for keyword in ["remote", "wfh", "work from home"]):
                remote_option = "Remote"
            elif "hybrid" in location_lower:
                remote_option = "Hybrid"
            elif any(keyword in location_lower for keyword in ["onsite", "on-site", "office"]):
                remote_option = "On-site"
            elif any(k in combined_text for k in ["remote", "wfh", "work from home"]):
                remote_option = "Remote"
            elif "hybrid" in combined_text:
                remote_option = "Hybrid"
            else:
                remote_option = "On-site"

            # Determine seniority level
            entry_keywords = ["entry-level", "fresh graduate", "fresh grad", "entry level", "new graduate", "junior"]
            
            if self._contains_keyword(combined_text, entry_keywords):
                seniority_level = "Entry Level"
            else:
                seniority_level = "Non-Entry Level"

            # Handle posted date
            if posted_date == "N/A":
                posted_date = None

            # Save job
            self.save_job(
                job_title=job_title,
                company_name=company,
                location=location,
                job_url=job_url,
                employment_type=employment_type,
                remote_option=remote_option,
                posted_date=posted_date,
                platform=self.platform_name,
                keyword="IT and Software",
                seniority_level=seniority_level,
                salary=salary,
                technologies=technologies,
                qualifications=qualifications_text,
                scraped_at=datetime.now()
            )
            
        except Exception as e:
            print(f"Error processing job detail: {e}")

    def _contains_keyword(self, text, keywords):
        """Helper method to check if text contains any of the keywords"""
        import re
        return any(re.search(rf"\b{k}\b", text) for k in keywords)