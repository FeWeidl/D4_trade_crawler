import time
import json
import logging
from fetcher import fetch_page
from parser import parse_page
from notifier import send_discord_notification
from database import connect_db, create_table, insert_item

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
            logging.error("Error loading configuration: %s", e)

class Filter:
    def __init__(self, filter_data):
        self.url = filter_data.get("url")
        self.attributes = filter_data.get("attributes", [])
        self.conditions = filter_data.get("conditions", [])
        logging.info("Filter initialized with URL: %s", self.url)

if __name__ == "__main__":
    config = Config('config.json')
    with open(config.filter_file, 'r') as file:
        filters_data = json.load(file)["filters"]
    
    db_conn, db_cursor = connect_db('items.db')
    create_table(db_cursor)
    
    while True:
        for filter_data in filters_data:
            filter_config = Filter(filter_data)
            url = filter_config.url
            driver, page_content = fetch_page(url)
            if page_content:
                interesting_items = parse_page(driver, page_content, filter_config)
                if interesting_items:
                    for item in interesting_items:
                        insert_item(db_cursor, item)
                        db_conn.commit()
                        send_discord_notification(item, config.webhook_url, url)
            else:
                logging.error("Error fetching page content.")
            driver.quit()
        time.sleep(60)
