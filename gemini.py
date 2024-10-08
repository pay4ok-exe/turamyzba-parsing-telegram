import requests
import json
from datetime import datetime
import re

# Replace with your actual API key
api_key = 'AIzaSyAbW85uWNJtLpqNNxxM1Cu5ruO77DcSJlE'

# API endpoint URL
url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={api_key}'

# Sample message info (this would be passed dynamically based on your data extraction process)
message_info = {
    "date": "2024-10-07 18:50:42",
    "author_name": "kvartira_v_almaty",
    "message": """Мы в поиске прекрасной девушки-соседки, в нашу красивую, чистую, светлую аккуратную квартиру. Нас двое девушек, одна из нас художница, а вторая переводчик английского языка 😁 живём дружно, любим готовить вкусняшки, у нас для этого есть большая кухня и крутая плита! 
    Квартира просторная, двухкомнатная, отдельный санузел (что очень удобно)! Ищем нашу новую милую-соседку в комнату на подселение. 
    Очень хотим уважительного отношения друг к другу, не нарушать личные границы, до конфликтов не доводить - разговаривать. Уметь дружить - мы только рады будем 🫶🏻
    Квартира в доме находится по улице Макатаева (напротив Зелёного Базара, закрытый двор) - Медеуский район. Удобное расположение. Стоимость 120тыс, и возвратный депозит (так как в квартире дорогая бытовая техника) 80тыс - можно разделить на два месяца.
    Мы ждём тебя 🫶🏻🤍 tg: @crausfel WhatsApp: +7 705 422 2116""",
    "media": ["https://t.me/@kvartira_v_almaty/22080"],
    "message_link": "https://t.me/@kvartira_v_almaty/22080",
    "views": 1010,
    "channel_name": "@kvartira_v_almaty"
}

# Construct the prompt with detailed information for the Gemini API
prompt = f"""
Extract structured data from this message for a real estate dataset:
City:string	
district: string	
Адрес:string (All in one sentence)
street:string	
zh_k_name:string (Жилой комплекс)	
photos:string[]	
monthlyExpensePerPerson:number	(Ежемесячная плата)
moveInStart:date	date:date	(Время заселения)
ownername:string	(Имя владельца)
active:boolean	title:string	(is Aviable)
apartmentinfo:string	(Описание комнаты\квартиры, какой этаж)
deposit:number	
overallresidents:number	(How many people live with you)
ownerinfo:string	(Номер\контакты)
roommatepreference:string	(Предпочтение руммейт ex: Muslim)
studentpreference:boolean (Предпочтение if it is student)
workerpreference:boolean (Предпочтение if it is worker)
callpreferences:boolean	(Только звонки: Да/нет)
whatsappnum:number	
whatsapppreference:boolean	(Только вацапп: Да/нет)
selectedgender:string	(Пол сожителя)
streetcomfortable:string	(Плюсы адреса)
nearpoints:string	(Заведения рядом с домом)
nearschool:boolean	
nearuniversity:boolean	
roommateage:number	(От х лет/ от х до у лет)
paymentdate:date	(Дата квартплаты)
petsallow:boolean	(Разрешение на питомца)
havepets:boolean	(Владелец имеет питомца в квартире)
rcame:string	
ufeeseparate:boolean	(Коммуналка раздельно от квартплаты: да/нет)
wifi:boolean 	
tolongterm:boolean	(В долгосрок: Да/нет)
allfurniture:String  (Бытовое техника если да то какие)
withjob:boolean	
ownertg:string	(Telegram)
isStudent:boolen
keyduplicate:boolean	
postviewers:number	
postdate:date	
channelname:string

Message:
Date: {message_info['date']}
Author: {message_info['author_name']}
Message: {message_info['message']}
Message Link: {message_info['message_link']}
Channel Name: {message_info['channel_name']}
Post Views: {message_info['views']}
"""

# Data payload for the API
data = {
    "contents": [
        {
            "parts": [
                {"text": prompt}
            ]
        }
    ]
}

# Headers for the API request
headers = {
    'Content-Type': 'application/json'
}


def clean_json_keys(json_text):
    # Remove anything that comes after a colon in a key, e.g., "Город:string" -> "Город"
    return re.sub(r'\"(.*?)\:(string|number|date|boolean|array)\"', r'"\1"', json_text)


# Function to clean message data by removing null or empty values
def clean_message_data(message):
    cleaned_message = {key: value for key, value in message.items() if value not in (None, "", [], {})}
    return cleaned_message


# Function to save the structured data into a JSON file
def save_to_json(data, channel_name, post_date):
    current_date = datetime.now().strftime("%Y-%m-%d")
    filename = f"{channel_name}_{post_date}_{current_date}.json"

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print(f"Data saved to {filename}")

# Make the POST request to the Gemini API
response = requests.post(url, headers=headers, data=json.dumps(data))

# Check if the request was successful
if response.status_code == 200:
    result = response.json()
    generated_text = result['candidates'][0]['content']['parts'][0]['text']
    cleaned_message = '{' + generated_text.split('{', 1)[1]
    clean_generated_text = clean_json_keys(cleaned_message.split('}', 1)[0] + '}')
    print(clean_generated_text)

    structured_data = json.loads(clean_generated_text)
    structured_data['message'] = message_info['message']

    # Save the structured data to a JSON file
    save_to_json(structured_data, message_info['channel_name'], message_info['date'].split(' ')[0])
else:
    print(f"Error: {response.status_code}, {response.text}")