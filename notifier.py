import logging
from discord_webhook import DiscordWebhook, DiscordEmbed

def send_discord_notification(item, webhook_url, url):
    webhook = DiscordWebhook(url=webhook_url)
    embed = DiscordEmbed(
        title=f"**{item['title']}**",
        description=f"**User:** {item['user']}\n\n" + "\n\n".join([f"**{key}:** {value}" for key, value in item['attributes'].items()]) + f"\n\n**Price:** {item['price']}\n\n**URL:** [Link]({url})",
        color=242424
    )
    webhook.add_embed(embed)
    response = webhook.execute()
    logging.info("Notification sent for item: %s", item['title'])
