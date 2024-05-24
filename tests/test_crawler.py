import unittest
from config.config import Config
from filters.filter import Filter, load_filters

class TestCrawler(unittest.TestCase):

    def test_load_config(self):
        config = Config('config/config.json')
        self.assertIsNotNone(config.webhook_url)
        self.assertIsNotNone(config.filter_file)

    def test_load_filters(self):
        filters = load_filters('data/filters.json')
        self.assertGreater(len(filters), 0)

if __name__ == '__main__':
    unittest.main()
