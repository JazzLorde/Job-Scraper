"""
Indeed Job Scraper
Scrapes job listings from Indeed Philippines with manual setup and full data extraction
"""

import time
import random
import hashlib
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import json
import re

from scrapers.base_scraper import BaseScraper
from utils.date_utils import convert_posted_date_indeed
from utils.tech_extractor import extract_technologies

class IndeedScraper(BaseScraper):
    """Indeed job scraper implementation with manual setup"""
    
    def __init__(self):
        super().__init__("Indeed")
        self.base_url = "https://ph.indeed.com"
        self.scraped_jobs = set()  # Track scraped jobs by hash
        self.scraped_urls = set()  # Track scraped URLs
    
    def scrape_manual(self, max_jobs=500):
        """Scrape Indeed with manual filter setup"""
        print(f"\nManual Indeed IT Jobs Scraping")
        
        with self:
            all_job_urls = []
            
            try:
                # Navigate to Indeed homepage
                print("Navigating to Indeed...")
                self.driver.get(self.base_url)
                time.sleep(random.uniform(3, 5))
                
                # Manual setup instructions
                print("\n" + "="*60)
                print("MANUAL SETUP REQUIRED")
                print("="*60)
                print("Please do the following manually in the browser:")
                print("1. Enter IT-related search terms (e.g., 'software developer', 'data analyst')")
                print("2. Set Location to 'Philippines' if not already set")
                print("3. Use any additional filters you want:")
                print("   - Date posted")
                print("   - Salary estimate")
                print("   - Job type (Full-time, Part-time, etc.)")
                print("   - Experience level")
                print("   - Remote options")
                print("4. Click 'Find jobs' and wait for results to load")
                print("5. Make sure you can see job listings")
                print("="*60)
                
                # Capture the search keyword from user
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
                
                # First stage: Collect job URLs from all pages
                page = 0
                consecutive_empty_pages = 0
                max_pages = 100  # Safety limit
                
                while len(all_job_urls) < max_jobs and page < max_pages:
                    print(f"\n=== Collecting URLs from page {page + 1} ===")
                    time.sleep(random.uniform(2, 4))
                    
                    # Get job URLs from current page
                    new_urls = self._collect_job_urls_from_page()
                    print(f"Found {len(new_urls)} job URLs on page {page + 1}")
                    
                    if not new_urls:
                        consecutive_empty_pages += 1
                        if consecutive_empty_pages >= 3:
                            print("No job URLs found for multiple pages. Ending collection.")
                            break
                    else:
                        consecutive_empty_pages = 0
                        # Add new unique URLs
                        for url in new_urls:
                            if url not in all_job_urls:
                                all_job_urls.append(url)
                    
                    print(f"Total unique job URLs collected: {len(all_job_urls)}")
                    
                    if len(all_job_urls) >= max_jobs:
                        print(f"Target reached! Collected {len(all_job_urls)} URLs (target: {max_jobs})")
                        break
                    
                    # Try to go to next page
                    if not self._go_to_next_page():
                        print("No more pages available")
                        break
                    page += 1
                
                print(f"\nTotal unique job URLs collected: {len(all_job_urls)}")
                
                # Limit to max_jobs
                if len(all_job_urls) > max_jobs:
                    all_job_urls = all_job_urls[:max_jobs]
                    print(f"Limited to first {max_jobs} URLs")
                
            except Exception as e:
                print(f"Error during URL collection: {e}")
                import traceback
                traceback.print_exc()
                return
            
            # Second stage: Process individual job pages
            if not all_job_urls:
                print("No job URLs collected. Please check the manual setup and try again.")
                return
            
            print(f"\nStarting detailed job information extraction...")
            jobs_processed = 0
            
            for i, job_url in enumerate(all_job_urls, 1):
                print(f"\nProcessing job {i}/{len(all_job_urls)}: {job_url}")
                
                if self._process_job_detail(job_url):
                    jobs_processed += 1
                
                # Short delay between jobs
                time.sleep(random.uniform(2, 4))
            
            print(f"\nIndeed scraping completed!")
            print(f"Total jobs processed: {jobs_processed}")
    
    def _collect_job_urls_from_page(self):
        """Collect all job URLs from the current page"""
        job_urls = []
        
        try:
            # Wait for job cards to load
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".job_seen_beacon, .slider_container .slider_item, [data-jk]")))
            
            # Try multiple selectors for job cards
            job_cards = self.driver.find_elements(By.CSS_SELECTOR, ".job_seen_beacon")
            if not job_cards:
                job_cards = self.driver.find_elements(By.CSS_SELECTOR, ".slider_container .slider_item")
            if not job_cards:
                job_cards = self.driver.find_elements(By.CSS_SELECTOR, "[data-jk]")
            
            print(f"Found {len(job_cards)} job cards on current page")
            
            for card in job_cards:
                try:
                    # Try multiple selectors for job links
                    job_link = None
                    
                    # Strategy 1: Direct job title link
                    try:
                        link_elem = card.find_element(By.CSS_SELECTOR, 'a.jcs-JobTitle')
                        job_link = link_elem.get_attribute('href')
                    except:
                        pass
                    
                    # Strategy 2: Other job title selectors
                    if not job_link:
                        selectors = [
                            '[data-testid="job-title"] a',
                            'h2 a',
                            '.jobTitle a',
                            'a[data-jk]',
                            'a[href*="/viewjob"]'
                        ]
                        
                        for selector in selectors:
                            try:
                                link_elem = card.find_element(By.CSS_SELECTOR, selector)
                                job_link = link_elem.get_attribute('href')
                                if job_link:
                                    break
                            except:
                                continue
                    
                    if job_link:
                        # Clean and validate URL
                        if not job_link.startswith('http'):
                            job_link = self.base_url + job_link
                        
                        # Keep the URL as-is, including redirect URLs since they work
                        job_urls.append(job_link)
                        
                except Exception as e:
                    print(f"Error extracting URL from job card: {e}")
                    continue
            
            print(f"Successfully extracted {len(job_urls)} job URLs")
            return job_urls
            
        except Exception as e:
            print(f"Error collecting job URLs from page: {e}")
            return []
    
    def _process_job_detail(self, job_url):
        """Process individual job detail page"""
        try:
            # Navigate to job page
            self.driver.get(job_url)
            time.sleep(random.uniform(4, 6))
            
            # Skip if this URL was already processed
            if job_url in self.scraped_urls:
                print(f"Skipping already processed URL: {job_url}")
                return False
            
            soup = BeautifulSoup(self.driver.page_source, "html.parser")
            
            # Extract job details
            job_title = self._extract_job_title(soup)
            company_name = self._extract_company_name(soup)
            location = self._extract_location(soup)
            posted_date = self._extract_posted_date(soup)
            employment_type = self._extract_employment_type(soup)
            salary = self._extract_salary(soup)
            qualifications_text = self._extract_qualifications(soup)
            
            # Debug output
            print(f"Extracted data:")
            print(f"  Title: {job_title}")
            print(f"  Company: {company_name}")
            print(f"  Location: {location}")
            print(f"  Qualifications length: {len(qualifications_text)}")
            
            # Extract technologies from job description
            technologies = self._extract_technologies_from_text(job_title, qualifications_text)
            
            # Determine remote option
            remote_option = self._determine_remote_option(job_title, location, qualifications_text)
            
            # Extract and normalize seniority level
            seniority_level = self._extract_seniority_level(job_title, qualifications_text)
            normalized_seniority = self._normalize_seniority_level(seniority_level)
            
            # Validation
            if (job_title == "N/A" or 
                len(qualifications_text) < 20):
                print("Could not extract valid job info - skipping")
                return False
            
            # Create a unique identifier for this job
            job_hash = hashlib.md5(f"{job_title}|{company_name}|{qualifications_text[:100]}".encode()).hexdigest()
            
            if job_hash in self.scraped_jobs:
                print("Job already processed (duplicate content) - skipping")
                return False
            
            # Use the captured keyword
            keyword_to_use = getattr(self, 'current_keyword', 'Manual Search')
            
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
                keyword=keyword_to_use,
                seniority_level=normalized_seniority,
                salary=salary,
                technologies=technologies,
                qualifications=qualifications_text,
                scraped_at=datetime.now()
            )
            
            # Track this job as processed
            self.scraped_jobs.add(job_hash)
            self.scraped_urls.add(job_url)
            
            print(f"Successfully processed: {job_title} at {company_name}")
            return True
            
        except Exception as e:
            print(f"Error processing job detail: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def _extract_job_title(self, soup):
        """Extract job title from the page"""
        selectors = [
            'h1[data-testid="jobsearch-JobInfoHeader-title"]',
            'h1.jobsearch-JobInfoHeader-title',
            '.jobsearch-JobInfoHeader-title',
            'h1'
        ]
        
        for selector in selectors:
            try:
                elem = soup.select_one(selector)
                if elem and elem.get_text().strip():
                    return elem.get_text().strip()
            except:
                continue
        return "N/A"
    
    def _extract_company_name(self, soup):
        """Extract company name from the page"""
        selectors = [
            '[data-testid="inlineHeader-companyName"]',
            '.jobsearch-JobInfoHeader-subtitle a',
            '.jobsearch-JobInfoHeader-subtitle',
            '.jobsearch-CompanyInfoContainer a'
        ]
        
        for selector in selectors:
            try:
                elem = soup.select_one(selector)
                if elem and elem.get_text().strip():
                    return elem.get_text().strip()
            except:
                continue
        return "N/A"
    
    def _extract_location(self, soup):
        """Extract location from the page"""
        selectors = [
            '[data-testid="jobsearch-JobInfoHeader-companyLocation"]',
            '.jobsearch-JobInfoHeader-subtitle div',
            '[data-testid="job-location"]'
        ]
        
        for selector in selectors:
            try:
                elem = soup.select_one(selector)
                if elem and elem.get_text().strip():
                    return elem.get_text().strip()
            except:
                continue
        return "N/A"
    
    def _extract_posted_date(self, soup):
        """Extract posted date from the page"""
        try:
            # Try JSON-LD first
            script_tag = soup.find('script', type='application/ld+json')
            if script_tag:
                json_data = json.loads(script_tag.text)
                posted_raw = json_data.get("datePosted")
                if posted_raw:
                    return posted_raw[:10]  # format: YYYY-MM-DD
        except:
            pass
        
        # Try text-based extraction
        try:
            posted_elem = soup.find('span', string=lambda x: x and 'ago' in x.lower())
            if posted_elem:
                posted_text = posted_elem.get_text().strip()
                return convert_posted_date_indeed(posted_text)
        except:
            pass
        
        return None
    
    def _extract_employment_type(self, soup):
        """Extract employment type from job description"""
        try:
            job_desc_text = self._extract_qualifications(soup).lower()
            
            if any(term in job_desc_text for term in ['full-time', 'full time', 'fulltime']):
                return "Full-time"
            elif any(term in job_desc_text for term in ['part-time', 'part time', 'parttime']):
                return "Part-time"
            elif any(term in job_desc_text for term in ['contract', 'contractor', 'contractual']):
                return "Contract"
            elif any(term in job_desc_text for term in ['freelance', 'freelancer']):
                return "Freelance"
            elif any(term in job_desc_text for term in ['internship', 'intern', 'trainee']):
                return "Internship"
            elif any(term in job_desc_text for term in ['temporary', 'temp']):
                return "Temporary"
            
            return "Not specified"
        except:
            return "Not specified"
    
    def _extract_salary(self, soup):
        """Extract salary from the page"""
        try:
            # Look for salary patterns in the page text
            page_text = soup.get_text()
            salary_patterns = [
                r'₱[\d,]+(?:\s*-\s*₱[\d,]+)?(?:\s*(?:per\s*month|/month|monthly))?',
                r'PHP\s*[\d,]+(?:\s*-\s*PHP\s*[\d,]+)?(?:\s*(?:per\s*month|/month|monthly))?',
                r'\$[\d,]+(?:\s*-\s*\$[\d,]+)?(?:\s*(?:per\s*year|/year|annually))?',
                r'[\d,]+\s*-\s*[\d,]+\s*(?:PHP|₱)'
            ]
            
            for pattern in salary_patterns:
                matches = re.findall(pattern, page_text, re.IGNORECASE)
                if matches:
                    return matches[0]
            
            return None
        except:
            return None
    
    def _extract_qualifications(self, soup):
        """Extract qualifications text from job description"""
        selectors = [
            '#jobDescriptionText',
            '[data-testid="jobsearch-jobDescriptionText"]',
            '.jobsearch-jobDescriptionText',
            '.jobsearch-JobComponent-description'
        ]
        
        for selector in selectors:
            try:
                elem = soup.select_one(selector)
                if elem:
                    text = elem.get_text(separator=' ', strip=True)
                    text = re.sub(r'\s+', ' ', text)
                    return text
            except:
                continue
        return ""
    
    def _extract_technologies_from_text(self, job_title, qualifications_text):
        """Extract technologies using the tech extractor"""
        try:
            combined_text = f"{job_title} {qualifications_text}"
            return extract_technologies(combined_text)
        except:
            return None
    
    def _determine_remote_option(self, job_title, location, qualifications_text):
        """Determine remote work option"""
        combined_text = f"{job_title.lower()} {location.lower()} {qualifications_text.lower()}"
        
        # Check for explicit "not remote" indicators first
        if any(term in combined_text for term in [
            "not remote", "not wfh", "not work from home", "not a hybrid role",
            "must work in office", "in the office full time", "on-site only", 
            "office based", "office base"
        ]):
            return "On-site"
        elif "hybrid" in combined_text:
            return "Hybrid"
        elif any(term in combined_text for term in ["remote", "wfh", "work from home"]):
            return "Remote"
        else:
            return "On-site"
    
    def _extract_seniority_level(self, job_title, qualifications_text):
        """Extract seniority level from job content"""
        try:
            combined_text = f"{job_title.lower()} {qualifications_text.lower()}"
            
            if any(term in combined_text for term in ['internship', 'intern', 'trainee']):
                return "Internship"
            elif any(term in combined_text for term in ['manager', 'director', 'lead', 'senior', 'head', 'executive', 'principal']):
                return "Non-Entry Level"
            elif any(term in combined_text for term in ['entry', 'junior', 'associate', 'fresh graduate', 'assistant']):
                return "Entry Level"
            else:
                return "Non-Entry Level"
        except:
            return "Non-Entry Level"
    
    def _normalize_seniority_level(self, seniority_level):
        """Normalize seniority level to standard categories"""
        seniority_lower = seniority_level.lower()
        
        if 'internship' in seniority_lower or 'intern' in seniority_lower:
            return "Internship"
        elif any(indicator in seniority_lower for indicator in ['entry', 'junior', 'associate', 'fresh']):
            return "Entry Level"
        else:
            return "Non-Entry Level"
    
    def _go_to_next_page(self):
        """Try to navigate to the next page"""
        try:
            # Look for next page link
            next_selectors = [
                'a[aria-label="Next Page"]',
                'a[aria-label="Next"]',
                '.pn a[aria-label="Next"]',
                '.np:last-child a'
            ]
            
            for selector in next_selectors:
                try:
                    next_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if next_button and next_button.is_displayed() and next_button.is_enabled():
                        next_button.click()
                        time.sleep(random.uniform(3, 5))
                        return True
                except:
                    continue
            
            print("No working next page button found")
            return False
            
        except Exception as e:
            print(f"Error navigating to next page: {e}")
            return False
