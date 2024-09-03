import os
import time
import pyautogui
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

# Initialize WebDriver (Chrome browser in this case)
driver = webdriver.Chrome()  # Ensure ChromeDriver is in your PATH

# Function to take screenshots
def take_screenshot(filename):
    time.sleep(2)  # Wait for the page to load completely
    screenshot = pyautogui.screenshot()
    screenshot.save(filename)

# Function to scrape and save posts, likes, and comments
def scrape_and_save(url, folder_name, platform):
    driver.get(url)
    time.sleep(5)  # Wait for the page to load

    # Create folder to save screenshots and data
    os.makedirs(folder_name, exist_ok=True)

    # Take a screenshot of the profile page
    take_screenshot(os.path.join(folder_name, f'{platform}_profile.png'))

    # Scroll down to load more content (if applicable)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)  # Adjust time as needed

    # Parse page content with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Example: Locate posts, likes, and comments (adjust selectors based on platform)
    posts = soup.find_all('div', class_='post_class')  # Replace 'post_class' with actual class for posts
    for i, post in enumerate(posts):
        post_text = post.get_text()
        post_file = os.path.join(folder_name, f'post_{i}.txt')
        with open(post_file, 'w', encoding='utf-8') as file:
            file.write(post_text)
        
        # Example: Extract likes and comments (adjust selectors based on platform)
        likes = post.find('span', class_='likes_class').get_text()  # Replace with actual class for likes
        comments = post.find('div', class_='comments_class').get_text()  # Replace with actual class for comments
        
        meta_file = os.path.join(folder_name, f'post_{i}_meta.txt')
        with open(meta_file, 'w', encoding='utf-8') as file:
            file.write(f'Likes: {likes}\nComments: {comments}\n')
        
        # Capture screenshot of the post
        element = driver.find_element(By.XPATH, 'XPATH_OF_POST')  # Replace with actual XPath for post
        element.screenshot(os.path.join(folder_name, f'post_{i}.png'))

# Investigate suspect's profile for each platform
def investigate_profile(platform, profile_url):
    folder_name = f"screenshots/{platform}"
    scrape_and_save(profile_url, folder_name, platform)

# Usage Example
investigate_profile("facebook", "https://www.facebook.com/suspect_profile")
investigate_profile("twitter", "https://twitter.com/suspect_profile")
investigate_profile("instagram", "https://www.instagram.com/suspect_profile")

# Close the WebDriver after investigation
driver.quit()

