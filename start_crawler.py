import time
import logging
from utils.fetcher import fetch_page
from utils.parser import parse_page
from utils.notifier import send_discord_notification
from utils.database import connect_db, create_table, insert_item
from config.config import Config
from filters.filter import Filters, Filter

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

if __name__ == "__main__":
    config = Config('config/config.json')
    filters = Filters(config.filter_file)
    
    db_conn, db_cursor = connect_db('data/items.db')
    create_table(db_cursor)
    
    while True:
        for filter_data in filters.filters_data:
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
