import json
import requests
import logging

def send_discord_notification(item, webhook_url, url):
    content = {
        "username": item.get('user'),
        "embeds": [
            {
                "title": item.get('title'),
                "description": "\n".join([f"{attr}: {value}" for attr, value in item.get('attributes', {}).items()]),
                "url": url,
                "color": 7506394
            }
        ]
    }

    response = requests.post(webhook_url, json=content)
    if response.status_code == 204:
        logging.info(f"Notification sent for item: {item.get('title')}")
        item['url'] = url
        item['triggered_attributes'] = {attr: value for attr, value in item.get('attributes', {}).items() if value is not None}
        with open('sent_items.json', 'a') as f:
            f.write(json.dumps(item) + '\n')
    else:
        logging.error(f"Failed to send notification for item: {item.get('title')}, Status code: {response.status_code}")
