import requests
import json
import csv
from datetime import datetime
import re

# Replace with your actual API key
api_key = 'AIzaSyAbW85uWNJtLpqNNxxM1Cu5ruO77DcSJlE'

# API endpoint URL
url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={api_key}'

# Function to clean JSON keys
def clean_json_keys(json_text):
    return re.sub(r'\"(.*?)\:(string|number|date|boolean|array)\"', r'"\1"', json_text)

# Function to save data to CSV
def save_to_csv(data, filename="output.csv"):
    if len(data) > 0:
        keys = data[0].keys()  # Get the keys from the first dictionary as headers
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=keys)
            writer.writeheader()  # Write headers
            writer.writerows(data)  # Write data rows
        print(f"Data saved to {filename}")
    else:
        print("No data to save.")

# Function to process each message through the Gemini API and return structured data
def process_message(message_info):
    # Construct the prompt for each message
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
    active:boolean	
    title:string	(is Aviable)
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

    # Make the POST request to the Gemini API
    response = requests.post(url, headers=headers, data=json.dumps(data))

    # Check if the request was successful
    if response.status_code == 200:
        try:
            result = response.json()
            generated_text = result['candidates'][0]['content']['parts'][0]['text']
            cleaned_message = '{' + generated_text.split('{', 1)[1]
            clean_generated_text = clean_json_keys(cleaned_message.split('}', 1)[0] + '}')

            # Convert the cleaned text to a dictionary
            structured_data = json.loads(clean_generated_text)

            # Add the original message to the structured data
            structured_data['message'] = message_info['message']
            structured_data['author_name'] = message_info['author_name']
            structured_data['date'] = message_info['date']
            structured_data['message_link'] = message_info['message_link']
            structured_data['channel_name'] = message_info['channel_name']
            structured_data['views'] = message_info['views']

            return structured_data
        except Exception as e:
            print(f"Error processing message: {e}")
            return None
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

# Read JSON data from the file
with open('@kvartira_v_almaty_2024-10-07_2024-10-08.json', 'r', encoding='utf-8') as f:
    messages = json.load(f)

# Prepare a list to store structured data results
structured_data_list = []

# Process each message
for message_info in messages:
    structured_data = process_message(message_info)
    if structured_data:
        structured_data_list.append(structured_data)

# Save all structured data to a single CSV file
if structured_data_list:
    save_to_csv(structured_data_list, "output.csv")
else:
    print("No structured data to save.")
