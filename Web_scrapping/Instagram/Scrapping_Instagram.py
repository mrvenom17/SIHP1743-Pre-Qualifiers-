import requests
from bs4 import BeautifulSoup
import logging
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# URL of the Instagram profile (Public profile scraping)
url = 'https://www.instagram.com/suspect_profile/?__a=1'
response = requests.get(url)

# Ensure the request was successful
if response.status_code == 200:
    profile_data = response.json()
    
    # Extract posts
    posts = profile_data['graphql']['user']['edge_owner_to_timeline_media']['edges']
    
    if posts:
        for post in posts:
            post_caption = post['node']['edge_media_to_caption']['edges'][0]['node']['text']
            logging.info(f"Post found: {post_caption}")
    else:
        logging.warning("No posts found.")
else:
    logging.error(f"Failed to retrieve the page. Status code: {response.status_code}")


# Selenium approach for scraping dynamic content
logging.basicConfig(level=logging.INFO)

# Initialize the Chrome WebDriver with options
chrome_options = Options()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

url = 'https://www.instagram.com/suspect_profile/'
driver.get(url)

time.sleep(3)  # Wait for the page to load

try:
    posts = driver.find_elements_by_class_name('v1Nh3')
    for post in posts:
        post_caption = post.text
        logging.info(f"Post found: {post_caption}")
except Exception as e:
    logging.error(f"Error extracting post text: {e}")
finally:
    driver.quit()
