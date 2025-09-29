Job Listing Scraper
A comprehensive web scraping system that aggregates IT job listings from multiple platforms across the Philippines

Overview
This automated scraper collects, processes, and standardizes job data from six major job platforms in the Philippines:
- JobStreet 
- Indeed 
- LinkedIn 
- Kalibrr 
- Foundit 
- Glassdoor 

Tech Stack
- Python
- Selenium & Undetected ChromeDriver
- BeautifulSoup4
- PostgreSQL


Data Flow

Platform-Specific Scraping Workflows
Each platform requires different setup steps based on available filters. 

1. LinkedIn
  - Runs: 3 times (once per industry filter) | Limit: 5,000 jobs per run
  - Setup Steps:
  a. Browser opens LinkedIn Jobs (Philippines location)
  b. You manually select filters:
    Industry and Job Function
    Industry: Choose ONE option (run separately for each):
    Technology, Information and Internet
    IT Services and Consulting
    Job Function: Information Technology
  

  c. Press ENTER to start scraping
    What Happens:  
  d. Automatically scrolls down to load more jobs
  e. Collects job URLs from cards
  f. Visits each job page individually
  g. Extracts all data fields
  h. Saves to database 

2. JobStreet
  Runs: 1 time | Limit: 5,000 jobs per run
  Setup Steps:
  Browser opens JobStreet Philippines
  You manually select filter:
  Check: "Information and Communication Technology"
  Press ENTER to start scraping
  
  What Happens:
  Automatically clicks "Next page" buttons
  Collects all job URLs from every page
  Then visits each job URL one by one
  Extracts all data fields
  Saves to database 

4. Indeed
Runs: Multiple times (once per job category) | Limit: 500 jobs per run
Setup Steps:
Browser opens Indeed Philippines
You manually search by specific IT job category:
Examples: "Software Developer", "Data Analyst", "IT Support", "Network Engineer"
Set location to "Philippines"
Type the search keyword you used (the category)
Press ENTER to start scraping

What Happens:
Stage 1: Collects job URLs from all search result pages
Stage 2: Visits each URL individually and extracts data
Saves to database 
You repeat this entire process for the next IT category


4. Glassdoor
Glassdoor
Runs: Multiple times (once per job category) | Limit: 500 jobs per run
Setup Steps:
Browser opens Glassdoor
You manually search by specific IT job category:
Examples: "Software Engineer", "DevOps Engineer", "Database Administrator"
Set location to "Philippines"
Type the search keyword you used (the category)
Press ENTER to start scraping

What Happens:
Stage 1: Collects job URLs from all search result pages
Stage 2: Visits each URL individually and extracts data
Saves to database 
You repeat this entire process for the next IT category

5. Kalibrr
Runs: 1 time | Limit: 5,000 jobs per run
Setup Steps:
Browser opens Kalibrr
You manually select filter:
Click "Filter" button
Open "Job Function" dropdown
Check: "IT and Software"
Click "Search"
Press ENTER to start scraping

What Happens:
Collects job URLs from the page
Visits each job page individually
Extracts all data fields
Saves to database 

6. Foundit
Runs: 2 times (once per filter) | Limit: 2,000 jobs per run
Setup Steps (Run 1):
Browser opens Foundit Philippines
You manually set filters:
- Job Function: IT
- Industry: IT
Press ENTER to start scraping

What Happens:
Goes through each page of results
Clicks each job card (opens in new tab)
Extracts data from the detail page
Closes tab and returns to listings
Moves to next page
Saves to database 






