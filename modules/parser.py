import logging
from bs4 import BeautifulSoup

def parse_page(driver, content, filter_config):
    soup = BeautifulSoup(content, 'html.parser')
    items = soup.find_all('div', class_='bg-[#111212] border-2 border-dim-yellow rounded-xl overflow-border-opacity-50 relative flex w-fit flex-1 flex-col gap-1 overflow-x-clip p-2 shadow-[0px_-10px_15px_0px#000a] transition-all duration-75 ui-state-revealed:animate-reveal-appear WTS')
    logging.info("Number of items found: %d", len(items))
    results = []
    for index, item in enumerate(items):
        title_element = item.find('div', class_='flex max-w-[250px] flex-wrap items-center gap-0.5 font-diablo text-xs font-bold uppercase sm:text-sm')
        title = title_element.text.strip() if title_element else "N/A"
        logging.info('Title: %s', title)
        user_element = item.find('button', class_='font-medium uppercase text-xs')
        user = user_element.text.strip() if user_element else "N/A"
        logging.info('User: %s', user)
        attributes = {}
        for attribute in filter_config.attributes:
            attribute_element = item.find('span', string=lambda text: text and attribute in text)
            attributes[attribute] = attribute_element.text if attribute_element else "N/A"
            logging.info('%s: %s', attribute, attributes[attribute])
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
        logging.info('Price: %s', price)
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
            logging.info("Item matched conditions: %s", attributes)
            return True
    logging.info("Item did not match any conditions.")
    return False
