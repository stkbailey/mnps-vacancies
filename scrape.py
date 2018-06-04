import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import json
import time


jobs = []
total = 0
    
def scrape(website_url):
    """Prepare a website url and scrape all pages"""
    # Scrape all pages
    start = time.time()

    try:
        parse(website_url)
    except TimeoutException:
        browser.quit()
        print('All data successfully scraped!')
        end = time.time()
        print('Time: {} minutes \n'.format(round((end - start) / 60), 1))
        
    # Store all jobs and total count
    data = {
        'total': total,
        'jobs': jobs
    }
    return json.dumps(data)

def parse(jobs_page):
    """Parse main jobs page and get all jobs URLs"""
    global jobs
    global total

    # Open first URL
    browser.get(jobs_page)

    # Wait or sleep until all page data loaded
    WebDriverWait(browser, 20).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'postingsList'))
    )

    body = browser.page_source

    # Parse page html to extract jobs info
    soup = BeautifulSoup(body, 'html.parser')
    jobs_content = soup.select('ul.postingsList')

    # Store the count of jobs located in this page
    total += len(jobs_content)
    
    # Get all jobs links (URLs) form jobs info (jobs_content variable)
    for job in jobs_content:
        job_dict = {}

        job_id_str = job.select_one('span.title2').text
        job_dict['job_id'] = job_id_str.split(':')[-1].strip()
        job_dict['title'] = (job.select_one('li.title').text
                                 .replace(job_id_str, '')
                                 .strip() )

        list_items = job.select('li')
        fields = ['Position Type', 'Date Posted', 'Location', 
                  'Date Available', 'Closing Date'] 

        for f in fields: 
            job_dict[f] = None
            for li in list_items:
                if f in li.text:
                    key = f.replace(' ', '_').lower()
                    job_dict[f] = li.select_one('span.normal').text
        
        jobs.append(job_dict)        
    
if __name__ == '__main__':
    print('Start scraping all MNPS jobs ...')
  
    print('Please, Do not close chrome driver. '
          'It will be closed automatically after finished.')
    print('This process may take several minutes')

    # Set chrome options
    chrome_options = webdriver.ChromeOptions()
    path_to_chrome = 'C:\\Users\\stkba\\Documents\\GitHub\\chromedriver.exe'
     # chrome_options.add_argument('headless')
    
    # Creates and open a new instance of the chrome driver
    browser = webdriver.Chrome(path_to_chrome, chrome_options=chrome_options)

    url = 'https://www.applitrack.com/mnps/OnlineApp/default.aspx?all=1'
    data_json = scrape(url)
    print(data_json)
