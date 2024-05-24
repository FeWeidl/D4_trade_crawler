# D4_trade_crawler
allows to automate searching for trade results at https://diablo.trade/listings/items

fill the config file with your information and rename it config

Make sure Python ans PIP is installed. Please refer to the official documentation on how to install.

Prerequesites:
```
python --version
pip --version
```

possibly a chromedriver needs to be installed
´refer to https://googlechromelabs.github.io/chrome-for-testing/
```
chromedriver --version
```

# D4 Trade Crawler

This project automates the search for trade results on Diablo.trade and sends notifications for interesting trades to a Discord channel.

## Project Structure

```
D4_trade_crawler/
├── config/
│   ├── config.json
│   ├── filters.json
├── modules/
│   ├── config.py
│   ├── filter.py
│   ├── fetcher.py
│   ├── parser.py
│   ├── notifier.py
│   └── database.py
├── data/
│   └── items.db  # This will be generated and should not be pushed to the repo.
├── tests/
│   └── test_crawler.py
├── start_crawler.py
└── README.md
```

## Configuration

### `config/config.json`

```json
{
    "webhook_url": "https://discord.com/api/webhooks/your_webhook_url",
    "filter_file": "config/filters.json"
}
```

### `config/filters.json`

Define your filters in this file. Example:

```json
{
    "filters": [
        {
            "url": "https://diablo.trade/listings/items",
            "attributes": ["Attribute1", "Attribute2"],
            "conditions": [
                // Condition group 1: Both Attribute1 and Attribute2 criteria must be met
                ["Attribute1,>,10", "Attribute2,==,20"]
            ]
        },
        {
            "url": "https://diablo.trade/listings/items",
            "attributes": ["Attribute3", "Attribute4"],
            "conditions": [
                // Condition group 1: Both Attribute3 and Attribute4 criteria must be met
                ["Attribute3,<,5", "Attribute4,>=,15"],
                // Condition group 2: Both Attribute3 and Attribute4 criteria must be met
                ["Attribute3,==,2", "Attribute4,!=,7"]
            ]
        },
        {
            "url": "https://diablo.trade/listings/items",
            "attributes": ["Attribute5", "Attribute6"],
            "conditions": [
                // Condition group 1: Both Attribute5 and Attribute6 criteria must be met
                ["Attribute5,<=,30", "Attribute6,!=,0"],
                // Condition group 2: Both Attribute5 and Attribute6 criteria must be met
                ["Attribute5,>,15", "Attribute6,==,10"]
            ]
        }
    ]
}
```

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/FeWeidl/D4_trade_crawler.git
    cd D4_trade_crawler
    ```
  

2. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Running the Crawler

1. Ensure `config/config.json` and `config/filters.json` are correctly configured.
2. Run the crawler:
    ```bash
    python start_crawler.py
    or
    py start_crawler.py
    ```

## Testing

1. To run the tests:
    ```bash
    python -m unittest discover tests
    ```

## Project Modules

### `modules/config.py`
Handles loading configuration settings from `config/config.json`.

### `modules/filter.py`
Loads and processes filter settings from `config/filters.json`.

### `modules/fetcher.py`
Fetches web pages using Selenium.

### `modules/parser.py`
Parses HTML content to extract trade data.

### `modules/notifier.py`
Sends notifications to Discord.

### `modules/database.py`
Manages database operations, such as creating tables and inserting items.

