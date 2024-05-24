import json
import logging

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
