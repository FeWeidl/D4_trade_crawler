from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging

def fetch_page(url):
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(options=options)
        driver.get(url)

        # Wait for the page to load by checking for the presence of the element with id="search-top"
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "search-top"))
        )
        logging.info(f"Page loaded successfully: {url}")
        return driver, driver.page_source
    except Exception as e:
        logging.error(f"Error waiting for page to load: {e}")
        return None, None
