import os
import time
import pyautogui
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import main
from webdriver_manager.chrome import ChromeDriverManager

# Set the path to your Brave browser executable
brave_path = "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"  # Update with your Brave path

# Create a Service object with Brave path
service = Service(ChromeDriverManager().install())

# Configure Chrome options to use Brave browser
options = webdriver.ChromeOptions()
options.binary_location = brave_path

# Initialize the WebDriver with Brave options
driver = webdriver.Chrome(service=service, options=options)


def take_screenshot(filename):
    time.sleep(2)
    screenshot = pyautogui.screenshot()
    screenshot.save(filename)


def scrape_and_save(url, folder_name, platform):
    driver.get(url)
    time.sleep(3)


    os.makedirs(folder_name, exist_ok=True)


    take_screenshot(os.path.join(folder_name, f'{platform}_profile.png'))


    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)
    soup = BeautifulSoup(driver.page_source, 'html.parser')


    posts = soup.find_all('div', class_='post_class')
    for i, post in enumerate(posts):
        post_text = post.get_text()
        post_file = os.path.join(folder_name, f'post_{i}.txt')
        with open(post_file, 'w', encoding='utf-8') as file:
            file.write(post_text)

        likes = post.find('span', class_='likes_class').get_text()
        comments = post.find('div', class_='comments_class').get_text()
        
        meta_file = os.path.join(folder_name, f'post_{i}_meta.txt')
        with open(meta_file, 'w', encoding='utf-8') as file:
            file.write(f'Likes: {likes}\nComments: {comments}\n')
        

        element = driver.find_element(By.XPATH, 'XPATH_OF_POST')
        element.screenshot(os.path.join(folder_name, f'post_{i}.png'))


def investigate_profile(platform, profile_url):
    folder_name = f"screenshots/{platform}"
    scrape_and_save(profile_url, folder_name, platform)


user=input()
investigate_profile("facebook", "https://www.facebook.com/{d}", user)
investigate_profile("twitter", "https://twitter.com/{d}", user)
investigate_profile("instagram", "https://www.instagram.com/{d}", user)


driver.quit()

main()