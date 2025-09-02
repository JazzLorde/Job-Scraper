"""
LinkedIn Job Scraper
Scrapes IT job listings from LinkedIn with manual setup
"""

import time
import random
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re

from scrapers.base_scraper import BaseScraper
from utils.date_utils import linkedin_format_posted_date
from utils.tech_extractor import extract_technologies

class LinkedinScraper(BaseScraper):
    """LinkedIn job scraper implementation with manual setup"""
    
    def __init__(self):
        super().__init__("LinkedIn")
        self.base_url = "https://www.linkedin.com"
    
    def scrape_manual(self, max_jobs=20):
        """Scrape LinkedIn with manual filter setup"""
        print(f"\nManual LinkedIn IT Jobs Scraping")
        
        with self:
            all_job_urls = []
            
            try:
                # Navigate to LinkedIn Jobs
                print("Navigating to LinkedIn Jobs...")
                self.driver.get("https://www.linkedin.com/jobs/search/?location=Philippines")
                time.sleep(random.uniform(3, 5))
                
                # Manual setup instructions
                print("\n" + "="*60)
                print("MANUAL SETUP REQUIRED")
                print("="*60)
                print("Please do the following manually in the browser:")
                print("1. Enter IT-related search terms (e.g., 'software developer', 'IT')")
                print("2. Set Location to 'Philippines' if not already set")
                print("3. Use any additional filters you want:")
                print("   - Experience level")
                print("   - Company size")
                print("   - Date posted")
                print("   - Remote work options")
                print("4. Click 'Search' and wait for results to load")
                print("5. Make sure you can see job listings")
                print("="*60)
                
                # NEW: Capture the search keyword from user
                search_keyword = input("Please enter the search terms you used (this will be stored in the keyword column): ").strip()
                if not search_keyword:
                    search_keyword = "Manual Search"
                
                # Store the keyword in the instance for use during scraping
                self.current_keyword = search_keyword
                print(f"Using keyword: '{search_keyword}'")
                
                print("When you're ready for scraping to begin, press ENTER...")
                
                # Wait for user confirmation
                input()
                
                print("Starting automated scraping process...")
                time.sleep(random.uniform(2, 4))
                
                # Dismiss any modal that might appear
                try:
                    WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "section[role='dialog']")))
                    self.driver.execute_script("""
                        const rect = document.querySelector("section[role='dialog']").getBoundingClientRect();
                        const clickX = rect.left - 10;
                        const clickY = rect.top - 10;
                        document.elementFromPoint(clickX, clickY).click();
                    """)
                    print("Modal dismissed.")
                    time.sleep(2)
                except:
                    print("No modal to dismiss")
                
                # Collect job URLs by scrolling
                consecutive_no_new_jobs = 0
                max_scrolls = 20
                scroll_count = 0
                
                while len(all_job_urls) < max_jobs and scroll_count < max_scrolls:
                    # Scroll to load more jobs
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(random.uniform(2, 4))
                    scroll_count += 1
                    
                    # Get current job cards
                    job_cards = self.driver.find_elements(By.CLASS_NAME, 'base-card')
                    print(f"Found {len(job_cards)} total job cards after scroll {scroll_count}")
                    
                    # Extract job URLs
                    new_urls = []
                    for card in job_cards:
                        try:
                            job_link_elem = card.find_element(By.TAG_NAME, 'a')
                            job_url = job_link_elem.get_attribute('href')
                            
                            # Clean URL
                            if '?' in job_url:
                                job_url = job_url.split('?')[0]
                            
                            if job_url not in all_job_urls:
                                new_urls.append(job_url)
                                all_job_urls.append(job_url)
                                
                        except Exception as e:
                            continue
                    
                    print(f"Added {len(new_urls)} new unique job URLs. Total: {len(all_job_urls)}")
                    
                    if len(all_job_urls) >= max_jobs:
                        break
                    
                    if len(new_urls) == 0:
                        consecutive_no_new_jobs += 1
                        if consecutive_no_new_jobs >= 5:
                            break
                    else:
                        consecutive_no_new_jobs = 0
                
                print(f"Total unique job URLs collected: {len(all_job_urls)}")
                
                # Process individual jobs
                for i, job_url in enumerate(all_job_urls, 1):
                    print(f"\nProcessing job {i}/{len(all_job_urls)}: {job_url}")
                    self._process_job_detail(job_url)
                    
            except Exception as e:
                print(f"Error during LinkedIn scraping: {e}")
    
    def _normalize_seniority_level(self, seniority_level):
        """Normalize seniority level to Entry Level, Non-Entry Level, or Internship"""
        
        seniority_lower = seniority_level.lower()
        
        # Keep Internship as is
        if 'internship' in seniority_lower:
            return "Internship"
        
        # Check if current seniority level indicates entry level
        entry_level_indicators = [
            'entry level', 'entry-level'
        ]
        
        # If any entry level indicator is found, return Entry Level
        if any(indicator in seniority_lower for indicator in entry_level_indicators):
            return "Entry Level"
        
        # Everything else becomes Non-Entry Level
        return "Non-Entry Level"

    # Replace your _process_job_detail method with this corrected version:
    def _process_job_detail(self, job_url):
        """Process individual job detail page"""
        try:
            self.driver.get(job_url)
            time.sleep(random.uniform(4, 6))
            soup = BeautifulSoup(self.driver.page_source, "html.parser")
            
            # Extract job title
            title_elem = soup.find('h1', class_='top-card-layout__title')
            if not title_elem:
                title_elem = soup.select_one('h1[data-automation="job-detail-title"]')
            job_title = title_elem.get_text().strip() if title_elem else "N/A"
            
            # Extract company name
            company_elem = soup.find('a', class_='topcard__org-name-link')
            if not company_elem:
                company_elem = soup.find('h4', class_='base-search-card__subtitle')
            company_name = company_elem.get_text().strip() if company_elem else "N/A"
            
            # Extract location
            location_elem = soup.find('span', class_='topcard__flavor--bullet')
            if not location_elem:
                location_elem = soup.select_one('[data-automation="job-detail-location"]')
            location = location_elem.get_text().strip() if location_elem else "N/A"
            
            # Extract employment type and seniority level
            employment_type = "Not specified"
            seniority_level = "Not specified"
            
            try:
                criteria_items = soup.find_all('li', class_='description__job-criteria-item')
                for item in criteria_items:
                    header = item.find('h3', class_='description__job-criteria-subheader')
                    if header:
                        header_text = header.get_text().lower()
                        criteria_text_elem = item.find('span', class_='description__job-criteria-text')
                        
                        if criteria_text_elem:
                            criteria_text = criteria_text_elem.get_text().strip()
                            
                            if 'employment type' in header_text:
                                employment_type = criteria_text
                            elif 'seniority level' in header_text:
                                seniority_level = criteria_text
            except Exception as e:
                print(f"Error extracting employment details: {e}")
            
            # Extract posted date
            posted_date = None
            try:
                posted_elem = soup.find('span', class_='posted-time-ago__text')
                if posted_elem:
                    posted_text = posted_elem.get_text().strip()
                    posted_date = linkedin_format_posted_date(posted_text)
            except Exception as e:
                print(f"Could not extract posted date: {e}")
            
            # Extract salary
            salary = None
            try:
                criteria_items = soup.find_all('li', class_='description__job-criteria-item')
                for item in criteria_items:
                    header = item.find('h3', class_='description__job-criteria-subheader')
                    if header and any(word in header.get_text().lower() for word in ['salary', 'compensation']):
                        salary_elem = item.find('span', class_='description__job-criteria-text')
                        if salary_elem:
                            salary = salary_elem.get_text().strip()
                            print(f"Found salary: {salary}")
                            break
            except Exception as e:
                print(f"Could not extract salary: {e}")
            
            # Extract qualifications text
            qualifications_text = ""
            try:
                # Try to expand job description first
                try:
                    show_more_btn = self.driver.find_element(By.CSS_SELECTOR, '.show-more-less-html__button--more')
                    if show_more_btn.is_displayed():
                        show_more_btn.click()
                        time.sleep(2)
                except:
                    pass
                
                # Extract job description
                description_elem = soup.find('div', class_='description__text')
                if description_elem:
                    qualifications_text = description_elem.get_text(separator=' ', strip=True)
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
                        
            except Exception as e:
                print(f"Error extracting technologies: {e}")
            
            # Determine remote option
            combined_text = f"{job_title.lower()} {location.lower()} {qualifications_text.lower()}"
            
            if "hybrid" in combined_text:
                remote_option = "Hybrid"
            elif any(k in combined_text for k in ["remote", "wfh", "work from home"]):
                remote_option = "Remote"
            else:
                remote_option = "On-site"
            
            # Handle posted date
            if posted_date == "N/A":
                posted_date = None
            
            # Use the captured keyword, with fallback
            keyword_to_use = getattr(self, 'current_keyword', 'Manual Search')
            
            # Normalize seniority level
            normalized_seniority = self._normalize_seniority_level(seniority_level)
            
            # Save job
            self.save_job(
                job_title=job_title,
                company_name=company_name,
                location=location,
                job_url=job_url,
                employment_type=employment_type,
                remote_option=remote_option,
                posted_date=posted_date,
                platform=self.platform_name,
                keyword=keyword_to_use,
                seniority_level=normalized_seniority,
                salary=salary,
                technologies=technologies,
                qualifications=qualifications_text,
                scraped_at=datetime.now()
            )
            
        except Exception as e:
            print(f"Error processing job detail: {e}")