import os
import time

from config import Config
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common import ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# setting driver headless via chrome.Options
chrome_options = Options()
chrome_options.add_argument("--headless=new")  # for Chrome >= 109

os.environ['PATH'] += 'Driver'
# driver = webdriver.Chrome(options=chrome_options)
driver = webdriver.Remote("http://127.0.0.1:4444/wd/hub", options=webdriver.ChromeOptions())

''' better alternative I found in StackOverFlow which helps to run chrome webdriver docker images headless
    Reason? website crawlers and robots.txt might block that client(browser) req due to its --headless tag but,
    here client is docker server which runs the driver via selenium     '''


def user_signin(user=Config.USER, email=Config.EMAIL, password=Config.PASSWORD):
    driver.get(f'https://x.com/{user}/')
    username = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, 'r-30o5oe'))
    )
    username.send_keys(user, Keys.ENTER)

    try:
        email_element = WebDriverWait(driver, 4).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'r-30o5oe'))
        )
        email_element.send_keys(email)
        email_element.send_keys(Keys.ENTER)
    except ElementNotInteractableException:
        # Email field not found, proceed without entering email
        pass

    # Find the password field and enter the password
    password_element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.NAME, 'password'))
    )

    password_element.send_keys(password, Keys.ENTER)

    # Wait for the tweets to load
    time.sleep(6)

    # Get the page source
    page_source = driver.page_source
    driver.quit()

    return page_source


def parse_data(source):
    soup = BeautifulSoup(source, 'html.parser')
    # Find all tweet articles
    tweet_articles = soup.find_all('article', {'role': 'article'})
    parsed_tweets = []
    tweet_count = 0

    # Extract information from each tweet article
    for tweet in tweet_articles:
        if tweet_count > 3:
            break
        tweet_count += 1
        # Try to find the tweet text
        tweet_text_div = tweet.find('div', {'data-testid': 'tweetText'})
        tweet_text_parts = []
        if tweet_text_div:
            for element in tweet_text_div.find_all(['span', 'img'], recursive=True):
                if element.name == 'span':
                    tweet_text_parts.append(element.get_text())
                elif element.name == 'img':
                    alt_text = element.get('alt', '')
                    tweet_text_parts.append(alt_text)
            tweet_text = ' '.join(tweet_text_parts)
        else:
            tweet_text = 'No tweet text found'

        # Try to find the tweet's timestamp
        time_tag = tweet.find('time')
        if time_tag:
            timestamp = time_tag['datetime']
            # Parse and format the timestamp
            parsed_timestamp = datetime.fromisoformat(timestamp)
            formatted_timestamp = parsed_timestamp.strftime('%d/%m/%Y')
        else:
            formatted_timestamp = 'No timestamp found'

        parsed_tweets.append({'time': formatted_timestamp, 'text': tweet_text})

    return parsed_tweets


def output_data(tweets):
    tweet = []
    for item in tweets:
        # Print tweet text and timestamp
        timestamp = item["time"]
        data = item["text"]
        tweet.append({f'Tweet: {data} timestamp: {timestamp}'})
    return tweet


'''Just for testing purpose'''
