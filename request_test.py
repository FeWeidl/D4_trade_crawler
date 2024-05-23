import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from discord_webhook import DiscordWebhook, DiscordEmbed

class Config:
    def __init__(self, config_file):
        self.config_file = config_file
        self.webhook_url = None
        self.load_config()

    def load_config(self):
        with open(self.config_file, 'r') as file:
            for line in file:
                key, value = line.strip().split(':', 1)
                setattr(self, key, value.strip())

def fetch_page(url):
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    driver.get(url)
    
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'flip-card-face'))
        )
    except Exception as e:
        print(f"Fehler beim Warten auf die Seite: {e}")
    
    page_content = driver.page_source

    with open("recent_fetch.html", "w", encoding="utf-8") as file:
        file.write(page_content)
    
    return page_content

def parse_page(content):
    soup = BeautifulSoup(content, 'html.parser')
    items = soup.find_all('div', class_='bg-[#111212] border-2 border-dim-yellow rounded-xl overflow-border-opacity-50 relative flex w-fit flex-1 flex-col gap-1 overflow-x-clip p-2 shadow-[0px_-10px_15px_0px#000a] transition-all duration-75 ui-state-revealed:animate-reveal-appear WTS')
    print(f"Anzahl der gefundenen Elemente: {len(items)}")
    
    results = []

    for item in items:
        title_element = item.find('div', class_='flex max-w-[250px] flex-wrap items-center gap-0.5 font-diablo text-xs font-bold uppercase sm:text-sm')
        title = title_element.text.strip() if title_element else "N/A"
        print(f'Title: {title}')
        
        movement_speed_element = item.find('span', string=lambda text: text and "Movement Speed" in text)
        movement_speed = movement_speed_element.text if movement_speed_element else "N/A"
        print(f'Movement Speed: {movement_speed}')
        
        damage_reduction_element = item.find('span', string=lambda text: text and "Damage Reduction from Close Enemies" in text)
        damage_reduction = damage_reduction_element.text if damage_reduction_element else "N/A"
        print(f'Damage Reduction from Close Enemies: {damage_reduction}')
        
        footer_element = item.find_next('div', class_='bg-white/5 backdrop-blur centered -mb-2 -ml-2 flex w-[calc(100%_+_16px)] flex-col gap-0 rounded-b-lg border-t-2 border-dim-yellow py-2 relative')
        if footer_element:
            exact_price = footer_element.find('h6', string="Exact Price")
            if exact_price:
                price_element = footer_element.find('h4', class_='font-pt-serif text-yellow-200')
                price = price_element.text.strip() if price_element else "N/A"
            else:
                make_offer_element = footer_element.find('h4', string="Make an offer!")
                price = make_offer_element.text.strip() if make_offer_element else "N/A"
        else:
            price = "N/A"
        
        print(f'Price: {price}')
        
        print('-' * 40)
        
        if price != "N/A":
            results.append({
                'title': title,
                'movement_speed': movement_speed,
                'damage_reduction': damage_reduction,
                'price': price
            })

    return results

def send_discord_notification(item, webhook_url):
    webhook = DiscordWebhook(url=webhook_url)
    embed = DiscordEmbed(
        title=f"**{item['title']}**",
        description=f"**Movement Speed:** {item['movement_speed']}\n**Damage Reduction:** {item['damage_reduction']}\n**Price:** {item['price']}",
        color=242424
    )
    webhook.add_embed(embed)
    response = webhook.execute()

if __name__ == "__main__":
    config = Config('config')
    url = "https://diablo.trade/listings/items?cursor=21&group1=&rarity=unique&uniqueItem=yens-blessing"
    
    while True:
        page_content = fetch_page(url)
        if page_content:
            interesting_items = parse_page(page_content)
            if interesting_items:
                for item in interesting_items:
                    send_discord_notification(item, config.webhook_url)
        else:
            print("Fehler beim Abrufen der Seite")
        
        time.sleep(60)
