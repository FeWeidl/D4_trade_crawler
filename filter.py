import json
import logging

class Filter:
    def __init__(self, filter_data):
        self.url = filter_data.get("url")
        self.attributes = filter_data.get("attributes", [])
        self.conditions = filter_data.get("conditions", [])
        logging.info("Filter initialized with URL: %s", self.url)

def load_filters(filter_file):
    try:
        with open(filter_file, 'r') as file:
            filters_data = json.load(file)["filters"]
            logging.info("Filters loaded successfully.")
            return filters_data
    except Exception as e:
        logging.error("Error loading filters: %s", e)
        return []
