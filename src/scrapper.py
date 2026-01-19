"""
LinkedIn Job Scraper (Portfolio Implementation)
Author: Dinesh Kumaralingam
Description: 
    A robust Selenium-based scraper designed to harvest job postings for specific roles.
    Includes anti-blocking measures (randomized delays, user-agent rotation) and 
    data parsing via BeautifulSoup.

    Note: This script is designed for research purposes.
"""

import time
import random
import logging
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler("scraper.log"), logging.StreamHandler()]
)

class LinkedInScraper:
    def __init__(self, headless=True):
        """Initialize the scraper with browser options and anti-detection settings."""
        self.options = Options()
        if headless:
            self.options.add_argument("--headless")
        
        # Anti-Blocking: Spoof User-Agent to look like a real user
        self.options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")
        self.options.add_argument("--disable-blink-features=AutomationControlled")
        self.options.add_argument("--window-size=1920,1080")
        
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.options)
        self.data = []

    def random_sleep(self, min_seconds=2, max_seconds=5):
        """Simulate human behavior with randomized delays."""
        sleep_time = random.uniform(min_seconds, max_seconds)
        time.sleep(sleep_time)

    def search_jobs(self, role, location="United States", num_pages=5):
        """Navigates to the job search page and iterates through results."""
        base_url = f"https://www.linkedin.com/jobs/search?keywords={role}&location={location}"
        logging.info(f"Starting scrape for role: {role} in {location}")
        
        self.driver.get(base_url)
        self.random_sleep(3, 6)

        for page in range(num_pages):
            logging.info(f"Scraping page {page + 1} for {role}...")
            self.parse_current_page(role)
            
            # Pagination Logic (Scroll & Click Next)
            try:
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                self.random_sleep()
                
                # Note: Selector for 'Next' button varies; using a generic xpath approach
                next_button = self.driver.find_element(By.XPATH, "//button[@aria-label='Next']")
                next_button.click()
                self.random_sleep(4, 7)
            except Exception as e:
                logging.warning(f"Pagination ended or failed: {e}")
                break

    def parse_current_page(self, role):
        """Parses the current list of job cards."""
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        job_cards = soup.find_all("div", class_="base-card") # Common LinkedIn card class

        for card in job_cards:
            try:
                title = card.find("h3", class_="base-search-card__title").text.strip()
                company = card.find("h4", class_="base-search-card__subtitle").text.strip()
                location = card.find("span", class_="job-search-card__location").text.strip()
                link = card.find("a", class_="base-card__full-link")["href"]
                
                # Append raw data
                self.data.append({
                    "job_title": title,
                    "company": company,
                    "location": location,
                    "job_link": link,
                    "role_category": role,
                    "scraped_date": pd.Timestamp.now()
                })
            except AttributeError:
                continue

    def extract_full_descriptions(self):
        """
        Optional: Visits each link to get full text. 
        Note: Separated to minimize API calls/blocking risk during initial pass.
        """
        logging.info(f"Extracting full descriptions for {len(self.data)} jobs...")
        
        for i, job in enumerate(self.data):
            try:
                self.driver.get(job['job_link'])
                self.random_sleep(2, 4)
                
                desc_soup = BeautifulSoup(self.driver.page_source, "html.parser")
                # Common selector for description container
                desc_box = desc_soup.find("div", class_="show-more-less-html__markup")
                
                if desc_box:
                    self.data[i]['description'] = desc_box.text.strip()
                else:
                    self.data[i]['description'] = None
                    
            except Exception as e:
                logging.error(f"Failed to extract description for {job['job_title']}: {e}")

    def save_data(self, filename="data/raw_linkedin_jobs.csv"):
        """Saves the harvested data to CSV."""
        df = pd.DataFrame(self.data)
        df.to_csv(filename, index=False)
        logging.info(f"Data saved to {filename}. Total records: {len(df)}")

    def close(self):
        self.driver.quit()

# --- Execution Entry Point ---
if __name__ == "__main__":
    scraper = LinkedInScraper(headless=True)
    
    target_roles = [
        "Data Analyst", 
        "Data Scientist", 
        "Consultant", 
        "Supply Chain Analyst", 
        "Marketing Analyst"
    ]
    
    try:
        for role in target_roles:
            scraper.search_jobs(role, num_pages=2) # Kept low for demo purposes
        
        # Uncomment below for deep extraction (slower)
        # scraper.extract_full_descriptions()
        
        scraper.save_data()
        
    except Exception as e:
        logging.critical(f"Scraper failed: {e}")
    finally:
        scraper.close()