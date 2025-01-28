from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Chrome Driver Options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--disable-extensions")
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("window-size=2100,700")

# Chrome Driver Service using WebDriver Manager
chrome_service = Service(ChromeDriverManager().install())

# Initialize WebDriver
wd = webdriver.Chrome(service=chrome_service, options=chrome_options)
wd.get('https://www.linkedin.com/jobs/search?keywords=Data&location=Vietnam')

# Get page source
vietnam_page_source = wd.page_source
with open('vietnam_linkedin_jobs2.txt', 'w', encoding='utf-8') as f:
    f.write(vietnam_page_source)

wd.quit()