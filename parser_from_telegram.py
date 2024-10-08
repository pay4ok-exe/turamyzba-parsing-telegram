from telethon.sync import TelegramClient
from datetime import datetime
import json

from telethon.tl.types import DocumentAttributeVideo, DocumentAttributeFilename, MessageMediaPhoto

# Get your api_id, api_hash from my.telegram.org
api_id = '27472979'
api_hash = '188a70ed821fb3c97a7d244bc4d11fe5'

def get_chat_link():
    print("Enter the chat username or ID: ")
    return input()

async def get_chat_history(client, chat_link, start_date, end_date):
    messages = []
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")

    async for message in client.iter_messages(chat_link):
        # Convert message.date to naive datetime by removing timezone info
        message_date = message.date.replace(tzinfo=None)

        if start_date <= message_date <= end_date and (message.text or message.media):
            # Construct the message link using chat link and message ID
            message_link = f"https://t.me/{chat_link}/{message.id}"

            media_urls = []
            if message.media:
                if isinstance(message.media, MessageMediaPhoto):
                    media_urls.append(message_link)  # Placeholder for actual photo URL extraction
                elif message.document:
                    media_urls.append(message_link)  # Placeholder for actual document URL extraction

            views_count = getattr(message, 'views', 0)  # Get views count if available

            message_info = {
                "date": message.date.strftime("%Y-%m-%d %H:%M:%S"),
                "author_name": getattr(message.sender, 'username', None) or getattr(message.sender, 'first_name', None),
                "message": message.text if message.text else "",
                "media": media_urls,
                "message_link": message_link,
                "views": views_count,
                "channel_name": chat_link
            }

            messages.append(message_info)

    return messages


def save_chat_history(messages, chat_link, start_date, end_date):
    # Filter messages to exclude those with empty 'message' or empty 'media' fields
    filtered_messages = [msg for msg in messages if msg['message'].strip()]

    # Only save non-empty messages
    if filtered_messages:
        filename = f"{chat_link}_{start_date}_{end_date}.json"
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(filtered_messages, file, ensure_ascii=False, indent=4)
            print(f"Filtered chat history saved successfully as {filename}.")
    else:
        print("No non-empty messages to save.")



async def main():
    chat_link = get_chat_link()
    start_date = input("Enter start date (YYYY-MM-DD): ")
    end_date = input("Enter end date (YYYY-MM-DD): ")

    async with TelegramClient('session_name', api_id, api_hash) as client:
        messages = await get_chat_history(client, chat_link, start_date, end_date)
        save_chat_history(messages, chat_link, start_date, end_date)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
