import requests
from bs4 import BeautifulSoup
import logging
import tweepy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# URL of the Twitter profile (Public profile scraping)
url = 'https://twitter.com/suspect_profile'
response = requests.get(url)

# Ensure the request was successful
if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')

    # Twitter uses dynamic content loading
    tweets = soup.find_all('div', {'class': 'tweet'})

    # Check if we found any tweets
    if tweets:
        for tweet in tweets:
            tweet_text = tweet.find('p', {'class': 'tweet-text'}).text
            logging.info(f"Tweet found: {tweet_text}")
    else:
        logging.warning("No tweets found, Twitter may be using dynamic content loading.")
else:
    logging.error(f"Failed to retrieve the page. Status code: {response.status_code}")


# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize the Chrome WebDriver with options
chrome_options = Options()
chrome_options.add_argument('--headless')  # Run in headless mode to speed up
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Twitter profile URL
url = 'https://twitter.com/suspect_profile'
driver.get(url)

# Wait for tweets to load (Implementing WebDriverWait for better handling)
time.sleep(3)  # Can replace with WebDriverWait for dynamic wait

try:
    tweets = driver.find_elements(By.CSS_SELECTOR, 'article[role="article"]')
    for tweet in tweets:
        tweet_text = tweet.find_element(By.CSS_SELECTOR, 'div[data-testid="tweetText"]').text
        logging.info(f"Tweet found: {tweet_text}")
except Exception as e:
    logging.error(f"Error extracting tweet text: {e}")
finally:
    driver.quit()  # Ensure driver quits after scraping


# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Twitter Developer credentials (fetch these securely from environment variables)
api_key = 'YOUR_API_KEY'
api_key_secret = 'YOUR_API_KEY_SECRET'
access_token = 'YOUR_ACCESS_TOKEN'
access_token_secret = 'YOUR_ACCESS_TOKEN_SECRET'

# Authenticate with Twitter API
auth = tweepy.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Fetch tweets from a suspect’s account
suspect_username = "suspect_profile"
try:
    tweets = api.user_timeline(screen_name=suspect_username, count=100, tweet_mode="extended")
    
    # Log each tweet
    for tweet in tweets:
        logging.info(f"Tweet: {tweet.full_text}")
except tweepy.TweepError as e:
    logging.error(f"Error fetching tweets: {e}")


# # Importing the Tweet model and session from Data_Model_Twitter
# from Data_Storage.DB_Model_Twitter import Tweet, session

# # Assuming you have a list of tweets (e.g., from Tweepy or Selenium scraping)
# tweets_data = [
#     {"username": "user1", "tweet_text": "This is tweet 1", "tweet_date": "2024-09-15"},
#     {"username": "user2", "tweet_text": "This is tweet 2", "tweet_date": "2024-09-14"},
# ]

# # Save the scraped tweets to the database
# def save_tweets_to_db(tweets):
#     for tweet_data in tweets:
#         new_tweet = Tweet(
#             username=tweet_data['username'],
#             tweet_text=tweet_data['tweet_text'],
#             tweet_date=tweet_data['tweet_date']
#         )
#         session.add(new_tweet)
#     session.commit()
#     print("Tweets saved to the database")

# # Call the function to save tweets
# save_tweets_to_db(tweets_data)
