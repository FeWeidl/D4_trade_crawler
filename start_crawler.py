import time
import os
import sqlite3
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from discord_webhook import DiscordWebhook, DiscordEmbed
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Config:
    def __init__(self, config_file):
        self.config_file = config_file
        self.webhook_url = None
        self.filter_file = None
        self.load_config()

    def load_config(self):
        try:
            with open(self.config_file, 'r') as file:
                config = json.load(file)
                self.webhook_url = config.get("webhook_url")
                self.filter_file = config.get("filter_file")
                logging.info("Configuration loaded successfully.")
        except Exception as e:
            logging.error(f"Error loading configuration: {e}")

class Filter:
    def __init__(self, filter_data):
        self.url = filter_data.get("url")
        self.attributes = filter_data.get("attributes", [])
        self.conditions = filter_data.get("conditions", [])
        logging.info(f"Filter initialized with URL: {self.url}")

def fetch_page(url):
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    logging.info(f"Fetching page: {url}")
    driver.get(str(url))
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'flip-card-face'))
        )
        logging.info("Page loaded successfully.")
    except Exception as e:
        logging.error(f"Error waiting for page to load: {e}")
    page_content = driver.page_source
    with open("recent_fetch.html", "w", encoding="utf-8") as file:
        file.write(page_content)
    return driver, page_content

def parse_page(driver, content, filter_config):
    soup = BeautifulSoup(content, 'html.parser')
    items = soup.find_all('div', class_='bg-[#111212] border-2 border-dim-yellow rounded-xl overflow-border-opacity-50 relative flex w-fit flex-1 flex-col gap-1 overflow-x-clip p-2 shadow-[0px_-10px_15px_0px#000a] transition-all duration-75 ui-state-revealed:animate-reveal-appear WTS')
    logging.info(f"Number of items found: {len(items)}")
    results = []
    for index, item in enumerate(items):
        title_element = item.find('div', class_='flex max-w-[250px] flex-wrap items-center gap-0.5 font-diablo text-xs font-bold uppercase sm:text-sm')
        title = title_element.text.strip() if title_element else "N/A"
        logging.info(f'Title: {title}')
        user_element = item.find('button', class_='font-medium uppercase text-xs')
        user = user_element.text.strip() if user_element else "N/A"
        logging.info(f'User: {user}')
        attributes = {}
        for attribute in filter_config.attributes:
            attribute_element = item.find('span', string=lambda text: text and attribute in text)
            attributes[attribute] = attribute_element.text if attribute_element else "N/A"
            logging.info(f'{attribute}: {attributes[attribute]}')
        footer_element = item.find_next('div', class_='bg-white/5 backdrop-blur centered -mb-2 -ml-2 flex w-[calc(100%_+_16px)] flex-col gap-0 rounded-b-lg border-t-2 border-dim-yellow py-2 relative')
        if footer_element:
            exact_price = footer_element.find('h6', string="Exact Price")
            if exact_price:
                price_element = footer_element.find('h4', class_='font-pt-serif text-yellow-200')
                price = price_element.text.strip() if price_element else "N/A"
            else:
                make_offer_element = footer_element.find('h6', string="Taking Offers")
                price = make_offer_element.text.strip() if make_offer_element else "N/A"
        else:
            price = "N/A"
        logging.info(f'Price: {price}')
        logging.info('-' * 40)
        if is_item_relevant(attributes, filter_config.conditions):
            results.append({
                'title': title,
                'user': user,
                'attributes': attributes,
                'price': price
            })
    return results

def is_item_relevant(attributes, conditions):
    for condition_group in conditions:
        match = True
        for condition in condition_group:
            field, operator, value = condition.split(",")
            value = float(value)
            if field in attributes and attributes[field] != "N/A":
                attribute_value = float(attributes[field].split()[0].replace('%', '').replace(',', ''))
                if operator == ">" and not (attribute_value > value):
                    match = False
                elif operator == "<" and not (attribute_value < value):
                    match = False
                elif operator == ">=" and not (attribute_value >= value):
                    match = False
                elif operator == "<=" and not (attribute_value <= value):
                    match = False
                elif operator == "==" and not (attribute_value == value):
                    match = False
                elif operator == "!=" and not (attribute_value != value):
                    match = False
            else:
                match = False
        if match:
            logging.info(f"Item matched conditions: {attributes}")
            return True
    logging.info("Item did not match any conditions.")
    return False

def send_discord_notification(item, webhook_url, url):
    webhook = DiscordWebhook(url=webhook_url)
    embed = DiscordEmbed(
        title=f"**{item['title']}**",
        description=f"**User:** {item['user']}\n\n" + "\n\n".join([f"**{key}:** {value}" for key, value in item['attributes'].items()]) + f"\n\n**Price:** {item['price']}\n\n**URL:** [Link]({url})",
        color=242424
    )
    webhook.add_embed(embed)
    response = webhook.execute()
    logging.info(f"Notification sent for item: {item['title']}")

if __name__ == "__main__":
    config = Config('config.json')
    with open(config.filter_file, 'r') as file:
        filters_data = json.load(file)["filters"]
    db_conn = sqlite3.connect('items.db')
    db_cursor = db_conn.cursor()
    db_cursor.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            user TEXT,
            attributes TEXT,
            price TEXT,
            UNIQUE(title, user, attributes, price)
        )
    ''')
    while True:
        for filter_data in filters_data:
            filter_config = Filter(filter_data)
            url = filter_config.url
            driver, page_content = fetch_page(url)
            if page_content:
                interesting_items = parse_page(driver, page_content, filter_config)
                if interesting_items:
                    for item in interesting_items:
                        try:
                            db_cursor.execute('''
                                INSERT INTO items (title, user, attributes, price) VALUES (?, ?, ?, ?)
                            ''', (item['title'], item['user'], json.dumps(item['attributes']), item['price']))
                            db_conn.commit()
                            send_discord_notification(item, config.webhook_url, url)
                        except sqlite3.IntegrityError:
                            logging.info(f"Item '{item['title']}' by '{item['user']}' already exists in the database.")
            else:
                logging.error("Error fetching page content.")
            driver.quit()
        time.sleep(60)
