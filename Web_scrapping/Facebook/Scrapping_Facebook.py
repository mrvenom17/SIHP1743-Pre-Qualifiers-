import requests
from bs4 import BeautifulSoup
import logging
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import tweepy

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Step 1: Scrape Public Profile Using Requests and BeautifulSoup
def scrape_facebook_profile(profile_url):
    try:
        response = requests.get(profile_url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        posts = soup.find_all('div', {'class': 'userContent'})
        
        if posts:
            for post in posts:
                post_text = post.get_text()
                logging.info(f"Post found: {post_text}")
        else:
            logging.warning("No posts found or content is dynamically loaded.")
    except requests.exceptions.RequestException as e:
        logging.error(f"Error retrieving Facebook profile page: {e}")

# Step 2: Scrape Dynamic Content with Selenium
def scrape_facebook_profile_selenium(profile_url):
    try:
        options = Options()
        options.add_argument('--headless')
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        driver.get(profile_url)
        time.sleep(3)  # Wait for the page to load

        posts = driver.find_elements(By.CSS_SELECTOR, 'div[role="article"]')
        for post in posts:
            post_text = post.find_element(By.CSS_SELECTOR, 'div[data-ad-preview="message"]').text
            logging.info(f"Post found: {post_text}")

        driver.quit()
    except Exception as e:
        logging.error(f"Error extracting Facebook posts: {e}")

# Step 3: Using Facebook Graph API
def scrape_facebook_graph_api():
    api_key = 'YOUR_GRAPH_API_KEY'
    user_id = 'TARGET_USER_ID'
    url = f"https://graph.facebook.com/v12.0/{user_id}/feed?access_token={api_key}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()
        for post in data['data']:
            logging.info(f"Post: {post['message']}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching data from Facebook Graph API: {e}")

# Example usage for scraping Facebook profile
if __name__ == "__main__":
    profile_url = 'https://www.facebook.com/some_public_profile'

    # Choose which scraping method to use
    method = input("Choose scraping method (1: BeautifulSoup, 2: Selenium, 3: Graph API): ").strip()

    if method == '1':
        scrape_facebook_profile(profile_url)
    elif method == '2':
        scrape_facebook_profile_selenium(profile_url)
    elif method == '3':
        scrape_facebook_graph_api()
    else:
        logging.warning("Invalid method selected.")
