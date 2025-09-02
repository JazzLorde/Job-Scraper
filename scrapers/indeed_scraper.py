"""
Indeed Job Scraper
Scrapes job listings from Indeed Philippines
"""

import time
import random
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import json

from scrapers.base_scraper import BaseScraper
from utils.browser import human_like_scroll
from utils.date_utils import convert_posted_date_indeed

class IndeedScraper(BaseScraper):
    """Indeed job scraper implementation"""
    
    def __init__(self):
        super().__init__("Indeed")
        self.base_url = "https://ph.indeed.com"
    
    def scrape(self, keyword, max_jobs=3):
        """Scrape Indeed for job listings"""
        print(f"\nScraping Indeed for: {keyword}")
        
        with self:  # Use context manager for automatic driver cleanup
            actions = ActionChains(self.driver)
            collected_jobs = []

            # Stage 1: Collect job URLs from search pages
            for page in range(0, 100, 10):  # 10 pages max as safety cap
                if len(collected_jobs) >= max_jobs:
                    break

                search_url = f"{self.base_url}/jobs?q={keyword.replace(' ', '+')}&l=Philippines&start={page}"
                self.driver.get(search_url)
                time.sleep(random.uniform(8, 12))
                human_like_scroll(self.driver)

                job_cards = self.driver.find_elements(By.CLASS_NAME, "job_seen_beacon")

                for card in job_cards:
                    if len(collected_jobs) >= max_jobs:
                        break
                    try:
                        self.driver.execute_script("arguments[0].scrollIntoView(true);", card)
                        actions.move_to_element(card).perform()
                        time.sleep(random.uniform(0.3, 0.7))

                        title_elem = card.find_element(By.CSS_SELECTOR, 'a.jcs-JobTitle')
                        job_title = title_elem.text.strip()
                        job_link = title_elem.get_attribute("href")
                        job_link = job_link if job_link.startswith("http") else self.base_url + job_link

                        try:
                            company = card.find_element(By.CSS_SELECTOR, '[data-testid="company-name"]').text.strip()
                        except:
                            company = "N/A"

                        try:
                            posted_elem = card.find_element(By.XPATH, './/span[contains(@class, "date")]')
                            posted_text = posted_elem.text.strip()
                            posted_date = convert_posted_date_indeed(posted_text)
                        except:
                            posted_date = "N/A"

                        collected_jobs.append((job_title, company, job_link, posted_date))
                    except:
                        continue

                time.sleep(random.uniform(3, 6))

            # Stage 2: Visit individual job pages for detailed information
            for job_title, company, job_url, posted_date in collected_jobs:
                try:
                    self.driver.get(job_url)
                    time.sleep(random.uniform(6, 9))
                    human_like_scroll(self.driver)

                    # Extract location
                    try:
                        location = self.driver.find_element(By.CSS_SELECTOR, '[data-testid="jobsearch-JobInfoHeader-companyLocation"]').text.strip()
                    except:
                        location = "N/A"

                    # Extract job description
                    try:
                        job_description = self.driver.find_element(By.ID, "jobDescriptionText").text.lower()
                    except:
                        job_description = ""

                    # Determine remote option
                    combined_text = f"{job_title.lower()} {job_description}"
                    location_lower = location.lower()

                    if any(k in job_description for k in [
                        "not remote", "not wfh", "not work from home", "not a hybrid role",
                        "must work in office", "in the office full time", "on-site only", "office based", "office base"
                    ]):
                        remote_option = "On-site"
                    elif any(k in location_lower for k in ["remote", "wfh", "work from home"]):
                        remote_option = "Remote"
                    elif "hybrid" in job_description:
                        remote_option = "Hybrid"
                    elif any(k in job_description for k in ["remote", "wfh", "work from home"]):
                        remote_option = "Remote"
                    else:
                        remote_option = "On-site"

                    # Determine employment type
                    employment_type = (
                        "Full-time" if "full-time" in job_description else
                        "Part-time" if "part-time" in job_description else
                        "Contract" if "contract" in job_description else
                        "Not specified"
                    )

                    # Determine seniority level
                    if self._contains_keyword(job_title.lower(), ["manager", "director", "executive", "lead", "head", "officer", "team leader"]):
                        seniority_level = "Mid-Senior level"
                    elif self._contains_keyword(combined_text, ["associate", "specialist", "coordinator", "1 year", "2 years", "3 years"]):
                        seniority_level = "Associate"
                    elif self._contains_keyword(combined_text, ["intern", "internship"]):
                        seniority_level = "Intern"
                    elif self._contains_keyword(combined_text, ["fresh graduate", "entry-level", "assistant", "Bachelor's"]):
                        seniority_level = "Entry-level"
                    else:
                        seniority_level = "Not specified"

                    # Try to get posted_date from JSON-LD in detail page
                    if posted_date == "N/A" or posted_date is None:
                        try:
                            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
                            script_tag = soup.find('script', type='application/ld+json')
                            if script_tag:
                                json_data = json.loads(script_tag.text)
                                posted_raw = json_data.get("datePosted")
                                if posted_raw:
                                    posted_date = posted_raw[:10]  # format: YYYY-MM-DD
                        except Exception as e:
                            print(f"Failed to extract posted date from job detail JSON: {e}")

                    if posted_date == "N/A":
                        posted_date = None

                    # Save job to database
                    self.save_job(
                        job_title=job_title, 
                        company_name=company, 
                        location=location,
                        job_url=job_url, 
                        employment_type=employment_type,
                        remote_option=remote_option, 
                        posted_date=posted_date,
                        platform=self.platform_name, 
                        keyword=keyword, 
                        seniority_level=seniority_level,
                        scraped_at=datetime.now()
                    )
                except Exception as e:
                    print(f"Error scraping Indeed job: {e}")

    def _contains_keyword(self, text, keywords):
        """Helper method to check if text contains any of the keywords"""
        import re
        return any(re.search(rf"\b{k}\b", text) for k in keywords)