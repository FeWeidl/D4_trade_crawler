import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def fetch_page(url):
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    logging.info("Fetching page: %s", url)
    driver.get(str(url))
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'flip-card-face'))
        )
        logging.info("Page loaded successfully.")
    except Exception as e:
        logging.error("Error waiting for page to load: %s", e)
    page_content = driver.page_source
    with open("recent_fetch.html", "w", encoding="utf-8") as file:
        file.write(page_content)
    return driver, page_content
