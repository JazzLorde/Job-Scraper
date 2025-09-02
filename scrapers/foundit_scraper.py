"""
Foundit Job Scraper
Scrapes IT job listings from Foundit with click-based navigation
Improved version with job tracking and DOM refresh handling
"""

import time
import random
import hashlib
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from bs4 import BeautifulSoup
import re

from scrapers.base_scraper import BaseScraper
from utils.tech_extractor import extract_technologies
from utils.date_utils import convert_posted_date_foundit


class FounditScraper(BaseScraper):
    """Foundit job scraper implementation with click-based navigation"""
    
    def __init__(self):
        super().__init__("Foundit")
        self.base_url = "https://www.foundit.com.ph"
        self.scraped_jobs = set()  # Track scraped jobs by hash
        self.scraped_urls = set()  # Track scraped URLs
    
    def scrape_manual(self, max_jobs=20):
        """Scrape Foundit with manual filter setup"""
        print(f"\nManual Foundit IT Jobs Scraping")
        
        with self:
            jobs_processed = 0
            
            try:
                # Navigate to Foundit homepage
                print("Navigating to Foundit...")
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
                print("   - Experience level")
                print("   - Company type")
                print("   - Salary range")
                print("   - Date posted")
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
                input()
                
                print("Starting automated scraping process...")
                
                # Process jobs page by page
                page = 1
                consecutive_empty_pages = 0
                
                while jobs_processed < max_jobs:
                    print(f"\n=== Processing page {page} ===")
                    time.sleep(random.uniform(2, 4))
                    
                    # Get all job card info on this page at once
                    job_cards_info = self._get_all_job_cards_info_fast()
                    print(f"Found {len(job_cards_info)} job cards on page {page}")
                    
                    if not job_cards_info:
                        consecutive_empty_pages += 1
                        if consecutive_empty_pages >= 3:
                            print("No job cards found for multiple pages. Ending scraping.")
                            break
                        
                        # Try to go to next page
                        if not self._go_to_next_page():
                            break
                        page += 1
                        continue
                    else:
                        consecutive_empty_pages = 0
                    
                    # Process each job card efficiently
                    jobs_processed_this_page = 0
                    
                    for i, job_info in enumerate(job_cards_info):
                        if jobs_processed >= max_jobs:
                            break
                        
                        # Skip if we've already processed this job
                        if job_info['hash'] in self.scraped_jobs:
                            print(f"Skipping already processed: {job_info['title']}")
                            continue
                        
                        print(f"\nJob {jobs_processed + 1}/{max_jobs} (Page {page}, Card {i+1})")
                        print(f"Processing: {job_info['title']} at {job_info['company']}")
                        
                        # Process this specific job card efficiently
                        if self._process_job_card_fast(i, job_info):
                            jobs_processed += 1
                            jobs_processed_this_page += 1
                            self.scraped_jobs.add(job_info['hash'])
                        
                        # Short delay between jobs
                        time.sleep(random.uniform(0.5, 1.5))
                    
                    print(f"Page {page} completed: {jobs_processed_this_page} new jobs processed")
                    
                    # Move to next page
                    if not self._go_to_next_page():
                        print("No more pages available")
                        break
                    page += 1
                    
            except Exception as e:
                print(f"Error during Foundit scraping: {e}")
                import traceback
                traceback.print_exc()
            
            print(f"\nFoundit scraping completed!")
            print(f"Total jobs processed: {jobs_processed}")
    
    def _get_all_job_cards_info_fast(self):
        """Get all job card info quickly without detailed clicking analysis"""
        try:
            # Wait for job cards
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".flex.flex-col.gap-4.rounded-2xl")))
            
            job_cards = self.driver.find_elements(By.CSS_SELECTOR, ".flex.flex-col.gap-4.rounded-2xl")
            cards_info = []
            
            for i, card in enumerate(job_cards):
                try:
                    title = self._extract_card_title_fast(card, i)
                    company = self._extract_card_company_fast(card, i)
                    
                    job_hash = hashlib.md5(f"{title}|{company}".encode()).hexdigest()
                    
                    cards_info.append({
                        'index': i,
                        'title': title,
                        'company': company,
                        'hash': job_hash
                    })
                    
                except Exception as e:
                    print(f"Error extracting info for card {i}: {e}")
                    cards_info.append({
                        'index': i,
                        'title': f"Job {i}",
                        'company': f"Company {i}",
                        'hash': f"fallback_{i}_{int(time.time())}"
                    })
            
            return cards_info
            
        except Exception as e:
            print(f"Error getting job cards info: {e}")
            return []
    
    def _extract_card_title_fast(self, card, index):
        """Fast title extraction"""
        try:
            elem = card.find_element(By.TAG_NAME, "h3")
            return elem.text.strip() if elem.text.strip() else f"Job {index}"
        except:
            return f"Job {index}"
    
    def _extract_card_company_fast(self, card, index):
        """Fast company extraction"""
        try:
            # Look for company link first
            company_elem = card.find_element(By.CSS_SELECTOR, "a[href*='company'], a[href*='jobs-career']")
            if company_elem and company_elem.text.strip():
                return company_elem.text.strip()
        except:
            pass
        
        try:
            # Fallback: look for any link that might be company
            links = card.find_elements(By.TAG_NAME, "a")
            for link in links[1:]:  # Skip first link (usually job title)
                text = link.text.strip()
                if text and len(text) < 50:
                    return text
        except:
            pass
        
        return f"Company {index}"
    
    def _process_job_card_fast(self, card_index, job_info):
        """Process a job card with new tab handling"""
        try:
            # Store the original tab and URL
            original_tab = self.driver.current_window_handle
            original_tabs = set(self.driver.window_handles)
            original_url = self.driver.current_url
            
            # Get the fresh job card element
            job_cards = self.driver.find_elements(By.CSS_SELECTOR, ".flex.flex-col.gap-4.rounded-2xl")
            
            if card_index >= len(job_cards):
                print(f"Card index {card_index} out of range")
                return False
            
            card = job_cards[card_index]
            
            # Click the job card
            click_success = self._quick_click_job_card(card)
            
            if not click_success:
                print("Failed to click job card")
                return False
            
            # Wait briefly for new tab or navigation
            time.sleep(2)
            
            # Check if a new tab was opened
            new_tabs = set(self.driver.window_handles)
            
            if len(new_tabs) > len(original_tabs):
                # New tab was opened
                new_tab = list(new_tabs - original_tabs)[0]
                print(f"New tab opened, switching to it")
                
                try:
                    # Switch to the new tab
                    self.driver.switch_to.window(new_tab)
                    time.sleep(1)
                    
                    # Check if we're on a job page
                    job_url = self.driver.current_url
                    print(f"Job tab URL: {job_url}")
                    
                    if 'search' not in job_url.lower() and job_url != original_url:
                        # Process the job page
                        job_processed = self._process_current_job_page()
                        
                        # Close the job tab and return to original
                        self.driver.close()
                        self.driver.switch_to.window(original_tab)
                        time.sleep(1)
                        
                        return job_processed
                    else:
                        print("New tab is not a job detail page")
                        # Close the tab and return to original
                        self.driver.close()
                        self.driver.switch_to.window(original_tab)
                        return False
                        
                except Exception as e:
                    print(f"Error processing new tab: {e}")
                    # Make sure we close any extra tabs and return to original
                    try:
                        current_tabs = self.driver.window_handles
                        for tab in current_tabs:
                            if tab != original_tab:
                                self.driver.switch_to.window(tab)
                                self.driver.close()
                        self.driver.switch_to.window(original_tab)
                    except:
                        pass
                    return False
            
            else:
                # Check if navigation happened in current tab
                new_url = self.driver.current_url
                if new_url != original_url and 'search' not in new_url.lower():
                    print(f"Navigated in current tab to: {new_url}")
                    # Process the job page
                    job_processed = self._process_current_job_page()
                    
                    # Return to listings
                    self.driver.get(original_url)
                    time.sleep(1.5)
                    
                    return job_processed
                else:
                    print("Click didn't open job page in current tab either")
                    return False
                
        except Exception as e:
            print(f"Error processing job card: {e}")
            # Ensure we're back on the original tab
            try:
                self.driver.switch_to.window(original_tab)
            except:
                pass
            return False
    
    def _quick_click_job_card(self, card):
        """Quick and efficient job card clicking"""
        try:
            # Strategy 1: Click the h3 title (most common clickable element)
            try:
                title_elem = card.find_element(By.TAG_NAME, "h3")
                if title_elem.is_displayed():
                    title_elem.click()
                    return True
            except:
                pass
            
            # Strategy 2: Click any job-related link
            try:
                links = card.find_elements(By.TAG_NAME, "a")
                for link in links:
                    href = link.get_attribute('href') or ''
                    # Skip company profile links
                    if 'company' not in href.lower() and link.is_displayed():
                        link.click()
                        return True
            except:
                pass
            
            # Strategy 3: JavaScript click on the card itself
            try:
                self.driver.execute_script("arguments[0].click();", card)
                return True
            except:
                pass
            
            # Strategy 4: Regular click on card
            try:
                card.click()
                return True
            except:
                pass
            
            return False
            
        except Exception as e:
            print(f"Error in quick click: {e}")
            return False
    
    def _process_current_job_page(self):
        """Process the current job detail page"""
        try:
            # Wait for page to load
            time.sleep(random.uniform(3, 5))
            current_url = self.driver.current_url
            
            print(f"Processing job page: {current_url}")
            
            # Additional check: if URL contains search terms, we're not on a job detail page
            search_indicators = ['search', 'results', 'find', 'browse']
            if any(indicator in current_url.lower() for indicator in search_indicators):
                print(f"URL indicates search page, not job detail: {current_url}")
                return False
            
            # Skip if this URL was already processed
            if current_url in self.scraped_urls:
                print(f"Skipping already processed URL: {current_url}")
                return False
            
            soup = BeautifulSoup(self.driver.page_source, "html.parser")
            
            # Skip if this is from an external platform we already scrape
            external_platforms = ['indeed.com', 'kalibrr.com', 'linkedin.com', 'jobstreet.com']
            if any(platform in current_url.lower() for platform in external_platforms):
                print(f"Skipping external job from: {current_url}")
                return False
            
            # Extract job details
            job_title = self._extract_job_title(soup)
            company_name = self._extract_company_name(soup)
            location = self._extract_location(soup)
            posted_date = self._extract_posted_date(soup)
            seniority_level = self._extract_seniority_level(soup)
            employment_type = self._extract_employment_type(soup)
            salary = self._extract_salary(soup)
            qualifications_text = self._extract_qualifications(soup)
            
            # Debug output
            print(f"Extracted data:")
            print(f"  Title: {job_title}")
            print(f"  Company: {company_name}")
            print(f"  Location: {location}")
            print(f"  Qualifications length: {len(qualifications_text)}")
            
            technologies = self._extract_technologies_from_text(job_title, qualifications_text)
            remote_option = self._determine_remote_option(job_title, location, qualifications_text)
            
            # More strict validation
            if (job_title == "N/A" or 
                any(bad_word in job_title.lower() for bad_word in ['showing', 'results', 'search', 'found']) or
                len(qualifications_text) < 20):
                print("Could not extract valid job info - skipping")
                print(f"Title: {job_title}")
                print(f"Qualifications length: {len(qualifications_text)}")
                return False
            
            # Create a unique identifier for this job
            job_hash = hashlib.md5(f"{job_title}|{company_name}|{qualifications_text[:100]}".encode()).hexdigest()
            
            if job_hash in self.scraped_jobs:
                print("Job already processed (duplicate content) - skipping")
                return False
            
            # Use the captured keyword, with fallback
            keyword_to_use = getattr(self, 'current_keyword', 'Manual Search')
            
            # Save job to database
            self.save_job(
                job_title=job_title,
                company_name=company_name,
                location=location,
                job_url=current_url,
                employment_type=employment_type,
                remote_option=remote_option,
                posted_date=posted_date,
                platform=self.platform_name,
                keyword=keyword_to_use,  # Use the captured keyword here
                seniority_level=seniority_level,
                salary=salary,
                technologies=technologies,
                qualifications=qualifications_text,
                scraped_at=datetime.now()
            )
            
            # Track this job as processed
            self.scraped_jobs.add(job_hash)
            self.scraped_urls.add(current_url)
            
            print(f"Successfully processed: {job_title} at {company_name}")
            return True
            
        except Exception as e:
            print(f"Error processing job detail: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def _extract_job_title(self, soup):
        """Extract job title from the page"""
        # Debug: Print page title and URL to understand what page we're on
        page_title = soup.find('title')
        if page_title:
            print(f"Page title: {page_title.get_text()}")
        
        current_url = self.driver.current_url
        print(f"Current URL: {current_url}")
        
        # If we're still on search results page, return early
        if any(term in current_url.lower() for term in ['search', 'results', 'find']):
            print("Warning: Still on search results page, not job detail page")
            return "N/A"
        
        selectors = [
            'h1',
            'h1.text-2xl',
            'h1.font-bold',
            '.job-title',
            'h3.text-darkKnight-700',
            '[data-testid="job-title"]',
            '.title',
            '*[class*="job-title"]',
            '*[class*="title"]'
        ]
        
        for selector in selectors:
            try:
                elem = soup.select_one(selector)
                if elem and elem.get_text().strip():
                    title = elem.get_text().strip()
                    # Filter out obvious non-job-titles
                    if not any(bad_word in title.lower() for bad_word in ['showing', 'results', 'search', 'found']):
                        print(f"Found job title: {title}")
                        return title
            except:
                continue
        
        # If no good title found, try to extract from page content
        print("No job title found with selectors, trying text analysis...")
        
        # Look for patterns that might be job titles
        text_content = soup.get_text()
        lines = [line.strip() for line in text_content.split('\n') if line.strip()]
        
        for line in lines[:10]:  # Check first 10 lines
            if (len(line) > 10 and len(line) < 100 and 
                not any(bad_word in line.lower() for bad_word in ['showing', 'results', 'search', 'found', 'filter', 'sort']) and
                any(job_word in line.lower() for job_word in ['developer', 'engineer', 'analyst', 'manager', 'specialist', 'coordinator'])):
                print(f"Found potential job title in text: {line}")
                return line
        
        return "N/A"
    
    def _extract_company_name(self, soup):
        """Extract company name from the page"""
        selectors = [
            'a.line-clamp-2',
            '[data-testid="company-name"]',
            '.company-name',
            'a[href*="jobs-career"]',
            'a[href*="company"]'
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
        """Extract location from job page - improved to handle multiple location parts"""
        try:
            locations = []
            
            # Method 1: Look for location links with the specific pattern
            location_links = soup.find_all('a', href=lambda x: x and '/search/jobs-in-' in x)
            
            for link in location_links:
                location_text = link.get_text().strip()
                # Clean up the text - remove trailing comma, whitespace, and other punctuation
                location_text = location_text.rstrip(', ').strip()
                
                # Skip empty or very short location names
                if location_text and len(location_text) > 1 and location_text not in locations:
                    locations.append(location_text)
            
            # Method 2: If no links found, look for location spans or divs near location indicators
            if not locations:
                # Look for elements that might contain location info
                location_indicators = [
                    'location', 'place', 'city', 'area', 'region'
                ]
                
                # Search for spans/divs that might contain location
                all_elements = soup.find_all(['span', 'div', 'p'])
                for elem in all_elements:
                    elem_text = elem.get_text().strip()
                    elem_class = ' '.join(elem.get('class', []))
                    
                    # Check if element seems location-related
                    if (any(indicator in elem_class.lower() for indicator in location_indicators) or
                        any(indicator in elem_text.lower() for indicator in ['philippines', 'manila', 'cebu', 'davao', 'metro'])):
                        
                        # Clean the text
                        clean_text = elem_text.strip().rstrip(', ')
                        if clean_text and len(clean_text) > 1 and clean_text not in locations:
                            locations.append(clean_text)
            
            # Method 3: Look for comma-separated locations in a single element
            if not locations:
                # Sometimes locations are in a single element separated by commas
                location_selectors = [
                    '[data-testid="location"]',
                    '.location',
                    'span[title*="location"]',
                    'div[class*="location"]',
                    '.job-location',
                    '[class*="job-location"]'
                ]
                
                for selector in location_selectors:
                    elem = soup.select_one(selector)
                    if elem and elem.get_text().strip():
                        location_text = elem.get_text().strip()
                        
                        # Check if it contains multiple locations separated by comma
                        if ',' in location_text:
                            parts = [part.strip() for part in location_text.split(',')]
                            for part in parts:
                                if part and part not in locations:
                                    locations.append(part)
                        else:
                            if location_text not in locations:
                                locations.append(location_text)
            
            # Method 4: Advanced text parsing for location patterns
            if not locations:
                page_text = soup.get_text()
                
                # Look for common Philippines location patterns
                import re
                location_patterns = [
                    r'(?:Metro\s+)?Manila(?:\s*,\s*Philippines)?',
                    r'(?:Quezon\s+City|QC)(?:\s*,\s*Philippines)?',
                    r'Makati(?:\s*City)?(?:\s*,\s*Philippines)?',
                    r'Taguig(?:\s*City)?(?:\s*,\s*Philippines)?',
                    r'Pasig(?:\s*City)?(?:\s*,\s*Philippines)?',
                    r'Ortigas(?:\s*Center)?(?:\s*,\s*Philippines)?',
                    r'BGC|Bonifacio\s+Global\s+City',
                    r'Cebu(?:\s*City)?(?:\s*,\s*Philippines)?',
                    r'Davao(?:\s*City)?(?:\s*,\s*Philippines)?',
                    r'Iloilo(?:\s*City)?(?:\s*,\s*Philippines)?',
                    r'Philippines',
                    r'Remote\s*-\s*Philippines',
                    r'Work\s+from\s+Home\s*-\s*Philippines'
                ]
                
                found_locations = set()
                for pattern in location_patterns:
                    matches = re.findall(pattern, page_text, re.IGNORECASE)
                    for match in matches:
                        clean_match = match.strip()
                        if clean_match and clean_match not in found_locations:
                            found_locations.add(clean_match)
                            locations.append(clean_match)
            
            # Clean up and deduplicate locations
            final_locations = []
            seen = set()
            
            for loc in locations:
                # Additional cleanup
                clean_loc = loc.strip().rstrip(',.!?;')
                
                # Skip if too short or already seen
                if len(clean_loc) <= 1 or clean_loc.lower() in seen:
                    continue
                    
                # Skip obvious non-location text
                skip_terms = ['apply', 'job', 'search', 'filter', 'sort', 'view', 'more', 'less', 'show']
                if any(term in clean_loc.lower() for term in skip_terms):
                    continue
                    
                seen.add(clean_loc.lower())
                final_locations.append(clean_loc)
            
            # Return the result
            if final_locations:
                # Join multiple locations with comma and space
                result = ', '.join(final_locations)
                print(f"Extracted location(s): {result}")
                return result
            else:
                print("No location found, using default")
                return "Not specified"
                
        except Exception as e:
            print(f"Error extracting location: {e}")
            import traceback
            traceback.print_exc()
            return "Not specified"
    
    def _extract_posted_date(self, soup):
        """Extract posted date from the page and convert to actual date"""
        try:
            # Method 1: Look for the specific span with "Posted X days ago" pattern
            posted_spans = soup.find_all('span', string=lambda x: x and 'posted' in x.lower() and 'ago' in x.lower())
            
            for span in posted_spans:
                posted_text = span.get_text().strip()
                print(f"Found posted date text: {posted_text}")
                return convert_posted_date_foundit(posted_text)
            
            # Method 2: Look for spans with class that might contain posted date
            all_spans = soup.find_all('span', class_=lambda x: x and 'ml-' in str(x))
            
            for span in all_spans:
                span_text = span.get_text().strip()
                if 'posted' in span_text.lower() and 'ago' in span_text.lower():
                    print(f"Found posted date in span: {span_text}")
                    return convert_posted_date_foundit(span_text)
            
            # Method 3: Look for any element containing "Posted X ago" pattern anywhere on page
            import re
            page_text = soup.get_text()
            
            posted_patterns = [
                r'Posted\s+\d+\s+(?:days?|hours?|weeks?|months?)\s+ago',
                r'Posted\s+(?:today|yesterday)',
                r'\d+\s+(?:days?|hours?|weeks?)\s+ago'
            ]
            
            for pattern in posted_patterns:
                matches = re.findall(pattern, page_text, re.IGNORECASE)
                if matches:
                    print(f"Found date pattern: {matches[0]}")
                    return convert_posted_date_foundit(matches[0])
            
            print("No posted date found")
            return None
            
        except Exception as e:
            print(f"Error extracting posted date: {e}")
            return None
    
    def _extract_seniority_level(self, soup):
        """Extract seniority level from the page with strict priority logic"""
        try:
            print("=== SENIORITY LEVEL EXTRACTION DEBUG ===")
            
            # Get job description and title for analysis using existing method
            job_desc_text = self._extract_qualifications(soup)
            job_title = self._extract_job_title(soup)
            combined_text = f"{job_title.lower()} {job_desc_text.lower()}"
            
            print(f"Job title: {job_title}")
            
            # PRIORITY 1: Check for "internship" anywhere (highest priority)
            if any(term in combined_text for term in ['internship']):
                print("FOUND INTERNSHIP - Returning 'Internship'")
                return "Internship"
            
            # PRIORITY 2: Look for EXACT <span>Fresher</span> element ONLY
            print("Searching for EXACT Fresher span...")
            spans = soup.find_all('span')
            print(f"Found {len(spans)} span elements to check")
            
            fresher_found = False
            for i, span in enumerate(spans):
                span_text = span.get_text().strip()
                if span_text:
                    print(f"Span {i+1}: '{span_text}'")
                    
                    # VERY STRICT: Only exact match for "Fresher" - nothing else
                    if span_text.strip().lower() == 'fresher':
                        print(f"EXACT FRESHER MATCH FOUND in span: '{span_text}' - Returning 'Entry Level'")
                        fresher_found = True
                        return "Entry Level"
            
            if not fresher_found:
                print("No exact 'Fresher' span found")
            
            # PRIORITY 3: Check for experience requirements (this should override fresher if present)
            print("Checking for experience requirements...")
            import re
            
            # Look for experience patterns in the visible text
            page_text = soup.get_text()
            experience_patterns = [
                r'(\d+)-(\d+)\s*(?:years?|yrs?)',  # "5-15 Years"
                r'(\d+)\+\s*(?:years?|yrs?)',      # "5+ Years"  
                r'(\d+)\s*to\s*(\d+)\s*(?:years?|yrs?)',  # "5 to 10 years"
                r'minimum\s*(\d+)\s*(?:years?|yrs?)',     # "minimum 3 years"
                r'at\s*least\s*(\d+)\s*(?:years?|yrs?)'   # "at least 2 years"
            ]
            
            for pattern in experience_patterns:
                matches = re.findall(pattern, page_text, re.IGNORECASE)
                if matches:
                    print(f"Found experience pattern: {pattern} -> {matches}")
                    
                    # Extract minimum years from the match
                    if isinstance(matches[0], tuple):
                        # For patterns like "5-15 years", get the first number
                        min_years = int(matches[0][0]) if matches[0][0].isdigit() else 0
                    else:
                        min_years = int(matches[0]) if matches[0].isdigit() else 0
                    
                    print(f"Minimum experience required: {min_years} years")
                    
                    if min_years >= 2:
                        print(f"Experience requirement {min_years}+ years - Returning 'Non-Entry Level'")
                        return "Non-Entry Level"
                    elif min_years <= 1:
                        print(f"Experience requirement {min_years} year(s) - Returning 'Entry Level'")
                        return "Entry Level"
            
            # PRIORITY 4: Check for senior level indicators in title and description
            senior_indicators = ['senior', 'lead', 'principal', 'manager', 'supervisor', 'head of', 'director', 'architect']
            for indicator in senior_indicators:
                if indicator in combined_text:
                    print(f"FOUND senior indicator '{indicator}' - Returning 'Non-Entry Level'")
                    return "Non-Entry Level"
            
            # PRIORITY 5: Check for other entry level indicators ONLY in job description
            entry_indicators = ['fresh graduate', 'new graduate', 'entry level', 'junior developer', 'junior engineer']
            for indicator in entry_indicators:
                if indicator in combined_text:
                    print(f"FOUND entry level indicator '{indicator}' - Returning 'Entry Level'")
                    return "Entry Level"
            
            # DEFAULT: If no specific indicators found, return Non-Entry Level
            print("NO SPECIFIC INDICATORS FOUND - Returning 'Non-Entry Level'")
            return "Non-Entry Level"
            
        except Exception as e:
            print(f"ERROR extracting seniority level: {e}")
            import traceback
            traceback.print_exc()
            return "Non-Entry Level"

    
    def _extract_employment_type(self, soup):
        """Extract employment type from the page"""
        # Look for employment type indicators in the page
        page_text = soup.get_text().lower()
        
        if 'full time' in page_text or 'full-time' in page_text:
            return "Full-time"
        elif 'part time' in page_text or 'part-time' in page_text:
            return "Part-time"
        elif 'contract' in page_text:
            return "Contract"
        elif 'freelance' in page_text:
            return "Freelance"
        elif 'internship' in page_text:
            return "Internship"
        
        return "Not specified"
    
    def _extract_salary(self, soup):
        """Extract salary from the page"""
        # Look for salary patterns in the page text
        page_text = soup.get_text()
        salary_patterns = [
            r'₱[\d,]+(?:\s*-\s*₱[\d,]+)?',
            r'PHP\s*[\d,]+(?:\s*-\s*PHP\s*[\d,]+)?',
            r'\$[\d,]+(?:\s*-\s*\$[\d,]+)?'
        ]
        
        for pattern in salary_patterns:
            matches = re.findall(pattern, page_text, re.IGNORECASE)
            if matches:
                return matches[0]
        return None
    
    def _extract_qualifications(self, soup):
        """Extract qualifications text from the page"""
        selectors = [
            'div.break-words',
            '.job-description',
            '.qualifications',
            '[data-testid="job-description"]',
            '.job-details',
            '.description'
        ]
        
        for selector in selectors:
            try:
                elem = soup.select_one(selector)
                if elem:
                    text = elem.get_text(separator=' ', strip=True)
                    text = re.sub(r'\s+', ' ', text)
                    if len(text) > 50:  # Only return if we got substantial text
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
        
        if "hybrid" in combined_text:
            return "Hybrid"
        elif any(k in combined_text for k in ["remote", "wfh", "work from home"]):
            return "Remote"
        
        elif "onsite" in combined_text:
            return "Onsite"
        else:
            return "Not Specified"
    
    def _go_to_next_page(self):
        """Try to navigate to the next page"""
        try:
            # Try common pagination selectors
            next_selectors = [
                "a[aria-label='Next page']",
                "button[aria-label='Next page']",
                ".pagination .next a",
                "a[rel='next']",
                "button[rel='next']",
                "//a[contains(text(), 'Next')]",
                "//button[contains(text(), 'Next')]",
                "//a[contains(@aria-label, 'next')]",
                "//button[contains(@aria-label, 'next')]"
            ]
            
            for selector in next_selectors:
                try:
                    if selector.startswith("//"):
                        next_button = self.driver.find_element(By.XPATH, selector)
                    else:
                        next_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                    
                    if next_button and next_button.is_displayed() and next_button.is_enabled():
                        # Check if button is actually clickable (not disabled)
                        classes = next_button.get_attribute('class') or ''
                        if 'disabled' not in classes.lower():
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