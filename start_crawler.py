import time
import logging
from modules.fetcher import fetch_page
from modules.parser import parse_page
from modules.notifier import send_discord_notification
from modules.database import connect_db, create_table, insert_item, item_exists
from modules.config import Config
from modules.filter import Filters, Filter

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Global variable to control the running state of the crawler
running = False

def start_crawler():
    global running
    running = True

    config = Config('config/config.json')
    filters = Filters(config.filter_file)
    
    db_conn, db_cursor = connect_db('data/items.db')
    create_table(db_cursor)
    
    if not filters.filters_data:
        logging.error("No filters loaded. Exiting.")
        return
    
    while running:
        for filter_data in filters.filters_data:
            if not running:
                break
            filter_config = Filter(filter_data)
            url = filter_config.url
            logging.info(f"Fetching URL: {url}")
            driver, page_content = fetch_page(url)
            if page_content:
                logging.info(f"Page content fetched for URL: {url}")
                interesting_items = parse_page(driver, page_content, filter_config)
                logging.info(f"Parsed items: {interesting_items}")
                for item in interesting_items:
                    logging.info(f"Found item: {item}")
                    if item_exists(db_cursor, item):
                        logging.info(f"Item already in database: {item.get('id')}")
                    else:
                        insert_item(db_cursor, item)
                        db_conn.commit()
                        send_discord_notification(item, config.webhook_url, url)
                        logging.info(f"Item sent to Discord: {item}")
            else:
                logging.error(f"Error fetching page content for URL: {url}")
            driver.quit()
        time.sleep(60)  # Wait for 60 seconds before the next round of fetching

def stop_crawler():
    global running
    running = False
