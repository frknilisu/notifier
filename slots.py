import os
import requests
import urllib3
import re
import json

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Pushbullet API credentials
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
PUSHBULLET_URL = 'https://api.pushbullet.com/v2/pushes'

# Specify the URL
TARGET_URL = 'https://oap.ind.nl/oap/api/desks/DH/slots?productKey=DOC&persons=1'

# Specify headers
TARGET_HEADERS = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'oap-locale': 'en'
}


def send_notification(title, body):
    headers = {
        'Access-Token': ACCESS_TOKEN,
        'Content-Type': 'application/json'
    }
    payload = {
        'type': 'note',
        'title': title,
        'body': body
    }
    response = requests.post(PUSHBULLET_URL, json=payload, headers=headers)
    if response.status_code == 200:
        print("Notification sent successfully!")
    else:
        print("Failed to send notification:", response.text)


def retrieve_first_date():
    try:
        response = requests.get(TARGET_URL, headers=TARGET_HEADERS, verify=False)

        if response.status_code == 200:
            try:
                clean_response = re.sub(r'^\)\]\}\',', '', response.text) # Remove non-JSON prefix (e.g., )]}')
                json_data = json.loads(clean_response)
                firstDate = json_data["data"][0]["date"]
                return firstDate
            except (ValueError, json.JSONDecodeError) as e:
                print('Failed to parse JSON. Raw content:', response.text)
        else:
            print('Failed to retrieve data. Status code:', response.status_code)

        return ""
    
    except requests.exceptions.RequestException as e:
        print('An error occurred:', e)


def test():
    title = "Test Notification"
    body = "This is a test message from Pushbullet API."
    send_notification(title, body)


def main():
    print("Running...")
    first_date = retrieve_first_date()
    if first_date.startswith('2025'):
        print('Response:', first_date)
        title = "Slot Available"
        body = f'A slot is available on {first_date}.'
        send_notification(title, body)

main()
