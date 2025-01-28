import time
import traceback
import re
import sys
import multiprocessing as mp
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from tqdm import tqdm
import numpy as np

# Chrome Driver Options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--disable-extensions")
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("window-size=2100,700")

# Chrome Driver Service using WebDriver Manager
chrome_service = Service(ChromeDriverManager().install())

def __scrape_job(job, wd):
    try:
        title = job.find_element(By.CLASS_NAME, 'base-search-card__title').text
        print(f"Job Title: {title}")

        for _ in range(3):
            try:
                job.find_element(By.CSS_SELECTOR, 'a').click()
                break
            except:
                wd.execute_script("window.scrollBy(0,500);")
                continue

        full_url = job.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
        match = re.search(r'https:\/\/www.linkedin.com\/jobs\/view\/.+\?', full_url)
        if match:
            full_url = match.group(0)
        else:
            full_url = full_url

        company = job.find_element(By.CLASS_NAME, 'base-search-card__subtitle').text
        company_url = job.find_element(By.CSS_SELECTOR, 'h4>a').get_attribute('href')
        location = job.find_element(By.CLASS_NAME, 'job-search-card__location').text
    except Exception as e:
        print(f"Error scraping job: {e}")
        traceback.print_exc()
        full_url = np.nan
        company = np.nan
        company_url = np.nan
        location = np.nan

    time.sleep(3)

    try:
        description = wd.find_element(By.CLASS_NAME, 'show-more-less-html__markup').get_attribute('innerHTML')
        description = str(description)
    except:
        description = np.nan
    try:
        seniority_level = wd.find_element(By.XPATH, '/html/body/div[1]/div/section/div[2]/div/section[1]/div/ul/li[1]/span').text
    except:
        seniority_level = 'Not Assigned'
    try:
        employment_type = wd.find_element(By.XPATH, '/html/body/div[1]/div/section/div[2]/div/section[1]/div/ul/li[2]/span').text
    except:
        employment_type = 'Not Assigned'
    try:
        job_function = wd.find_element(By.XPATH, '/html/body/div[1]/div/section/div[2]/div/section[1]/div/ul/li[3]/span').text
        job_function = job_function.replace(', and ', ', ')
    except:
        job_function = 'Not Assigned'
    try:
        industries = wd.find_element(By.XPATH, '/html/body/div[1]/div/section/div[2]/div/section[1]/div/ul/li[4]/span').text
        industries = industries.replace(', and ', ', ')
    except:
        industries = 'Not Assigned'

    job_data = pd.DataFrame({
        'title': [title],
        'full_url': [full_url],
        'company': [company],
        'company_url': [company_url],
        'location': [location],
        'description': [description],
        'seniority_level': [seniority_level],
        'employment_type': [employment_type],
        'job_function': [job_function],
        'industries': [industries],
    })
    return job_data

def __scrape(url, bar_position=0):
    wd = webdriver.Chrome(service=chrome_service, options=chrome_options)
    wd.get(url)
    time.sleep(2.5)

    try:
        num_of_jobs = wd.find_element(By.XPATH, '/html/body/div[1]/div/main/div/h1/span[1]').text
        num_of_jobs = int(num_of_jobs.replace('+', '').replace(',', '').strip())
    except:
        num_of_jobs = 1000  # Default value if unable to fetch

    jobs_data = []
    last_scraped_job = 0
    height = wd.execute_script("return document.documentElement.scrollHeight")
    same_position = 0
    pbar = tqdm(desc='Scraping...', total=num_of_jobs, position=bar_position)
    while True:
        try:
            xpath = f'//*[@id="main-content"]/section[2]/ul/li[{last_scraped_job + 1}]'
            next_job = wd.find_elements(By.XPATH, xpath)
            if not next_job:
                print(f"No more jobs found at index {last_scraped_job + 1}")
                break
            jobs_data.append(__scrape_job(next_job[0], wd))
            last_scraped_job += 1
            pbar.update(1)
        except Exception as e:
            print(f"Error in main loop: {e}")
            traceback.print_exc()
            same_position += 1
            if same_position >= 5:
                print('LinkedIn error not allowing the showing of more jobs')
                break
            continue
        same_position = 0  # Reset counter if no exception

        try:
            wd.find_element(By.CLASS_NAME, 'two-pane-serp-page__results-list').find_element(By.CSS_SELECTOR, 'button').click()
            time.sleep(2.5)
            if height == wd.execute_script("return document.documentElement.scrollHeight"):
                same_position += 1
                continue
            else:
                same_position = 0
                height = wd.execute_script("return document.documentElement.scrollHeight")
        except Exception as e:
            print(f"Error clicking 'see more jobs': {e}")
            traceback.print_exc()
            same_position += 1
            if same_position >= 5:
                break
            continue

    wd.quit()
    return pd.concat(jobs_data)

def __get_jobs(q, url, position):
    q.put(__scrape(url, position))

def get_listings_from(urls: list) -> pd.DataFrame:
    processes = []
    q = mp.Queue()
    jobs = []
    position = 0
    for url in urls:
        p = mp.Process(target=__get_jobs, args=(q, url, position))
        position += 1
        p.start()
        processes.append(p)

    for p in processes:
        jobs.append(q.get())

    for p in processes:
        p.join()

    print('\nDone Scraping!\n')
    return pd.concat(jobs)

urls = [
    'https://www.linkedin.com/jobs/search?keywords=Data&location=United%20States',
]

if __name__ == '__main__':
    df = get_listings_from(urls).dropna(axis=0, subset='full_url')
    df.drop_duplicates(subset='full_url', inplace=True)
    if len(df) == 0:
        print("No job listings found.")
    else:
        df.to_csv('linkedin-job-data2.csv', mode='w', index=False)