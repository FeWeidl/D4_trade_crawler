import json
import logging

class Filters:
    def __init__(self, filter_file):
        self.filter_file = filter_file
        self.filters_data = None
        self.load_filters()

    def load_filters(self):
        try:
            with open(self.filter_file, 'r') as file:
                self.filters_data = json.load(file)["filters"]
                logging.info("Filters loaded successfully.")
        except Exception as e:
            logging.error("Error loading filters: %s", e)

class Filter:
    def __init__(self, filter_data):
        self.url = filter_data.get("url")
        self.attributes = filter_data.get("attributes", [])
        self.conditions = filter_data.get("conditions", [])
        logging.info("Filter initialized with URL: %s", self.url)
