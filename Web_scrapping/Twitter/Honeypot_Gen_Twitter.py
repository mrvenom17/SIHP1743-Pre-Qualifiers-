import requests
import time
import logging
from faker import Faker
import random
import string
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize Faker for random data generation
fake = Faker()

# List of proxy servers (you can add more or retrieve them from a proxy provider)
proxies_list = [
    "http://proxy1.example.com:8080",
    "http://proxy2.example.com:8080",
    # Add more proxies as needed
]

# Function to get a random proxy
def get_random_proxy():
    return random.choice(proxies_list)

# Step 1: Temporary Email Generation
def get_temp_email(proxy=None):
    try:
        proxies = {"http": proxy, "https": proxy} if proxy else None
        response = requests.get('https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1', proxies=proxies)
        response.raise_for_status()  # Check for HTTP errors
        email = response.json()[0]
        logging.info(f"Generated temporary email: {email}")
        return email
    except requests.exceptions.RequestException as e:
        logging.error(f"Error generating temporary email: {e}")
        raise

# Step 2: Check the Temporary Email Inbox
def check_email_inbox(temp_email, retries=3, delay=10, proxy=None):
    login, domain = temp_email.split('@')
    
    proxies = {"http": proxy, "https": proxy} if proxy else None
    
    for attempt in range(retries):
        try:
            inbox_url = f"https://www.1secmail.com/api/v1/?action=getMessages&login={login}&domain={domain}"
            response = requests.get(inbox_url, proxies=proxies)
            response.raise_for_status()
            
            emails = response.json()
            if emails:
                email_id = emails[0]['id']
                email_details_url = f"https://www.1secmail.com/api/v1/?action=readMessage&login={login}&domain={domain}&id={email_id}"
                email_content = requests.get(email_details_url, proxies=proxies).json()
                logging.info("Email received!")
                return email_content['body']
            else:
                logging.info("No email received yet, retrying...")
        except requests.exceptions.RequestException as e:
            logging.error(f"Error checking email inbox: {e}")
        time.sleep(delay)  # Wait before retrying
    return None

# Step 3: CAPTCHA Solving (2Captcha Integration)
def solve_captcha(captcha_site_key, page_url, proxy=None):
    try:
        proxies = {"http": proxy, "https": proxy} if proxy else None
        captcha_url = f"https://2captcha.com/in.php?key=YOUR_2CAPTCHA_API_KEY&method=userrecaptcha&googlekey={captcha_site_key}&url={page_url}"
        captcha_response = requests.get(captcha_url, proxies=proxies)
        if 'OK|' in captcha_response.text:
            captcha_token = captcha_response.text.split('|')[1]
            logging.info("CAPTCHA solved successfully!")
            return captcha_token
        else:
            logging.error("CAPTCHA solving failed.")
    except requests.exceptions.RequestException as e:
        logging.error(f"Error solving CAPTCHA: {e}")
        raise

# Step 4: Fake Account Creation
def generate_human_username():
    # Generate a human-like username using Faker
    first_name = fake.first_name()
    last_name = fake.last_name()
    random_suffix = ''.join(random.choices(string.digits, k=3))  # E.g., 3 random digits
    username = f"{first_name}_{last_name}{random_suffix}"
    return username

def create_fake_account(platform_url, temp_email, proxy=None):
    human_username = generate_human_username()

    # Data for account creation
    account_data = {
        'email': temp_email,
        'username': human_username,
        'password': fake.password(length=12, special_chars=True, digits=True, upper_case=True, lower_case=True),
        # Other necessary fields for account creation
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    
    proxies = {"http": proxy, "https": proxy} if proxy else None

    try:
        response = requests.post(platform_url + '/register', data=account_data, headers=headers, proxies=proxies)
        if response.status_code == 200:
            logging.info(f"Fake account created with username: {human_username} using {temp_email}")
        else:
            logging.error(f"Account creation failed: {response.content}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Error creating fake account: {e}")

# Step 5: Automating the Full Process (with Selenium)
# Headless browser setup with proxy support (if proxy is enabled)
def automate_fake_account_creation(platform_url, captcha_site_key, use_proxy):
    try:
        proxy = get_random_proxy() if use_proxy else None

        # Generate temp email
        temp_email = get_temp_email(proxy=proxy)

        # Headless browser setup with proxy support (if proxy is enabled)
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        if use_proxy and proxy:
            options.add_argument(f'--proxy-server={proxy}')  # Use proxy if enabled

        # Initialize the WebDriver correctly without passing 'options' twice
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

        # Load the page
        driver.get(platform_url)

        # Solve CAPTCHA and create the fake account
        captcha_token = solve_captcha(captcha_site_key, platform_url, proxy=proxy)
        logging.info(f"CAPTCHA solved: {captcha_token}")
        
        # Use Selenium to fill the signup form dynamically here...
        logging.info("Signing up with temp email and CAPTCHA solved!")

        driver.quit()

    except Exception as e:
        logging.error(f"Error in automation process: {e}")

# Ask the user if they want to use proxies
def ask_for_proxy():
    while True:
        use_proxy_input = input("Do you want to use proxies? (yes/no): ").strip().lower()
        if use_proxy_input in ['yes', 'no']:
            return use_proxy_input == 'yes'
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")

# Example usage for Twitter
if __name__ == "__main__":
    platform_url = 'https://twitter.com'
    captcha_site_key = 'YOUR_CAPTCHA_SITE_KEY'  # Get this from the Twitter signup page source
    
    # Ask user if they want to use proxies
    use_proxy = ask_for_proxy()
    
    # Start the automation
    automate_fake_account_creation(platform_url, captcha_site_key, use_proxy)
