import requests
import urllib3
import re
import json
from datetime import datetime
import time
# from pushbullet import Pushbullet
from pushbullet.pushbullet import Pushbullet

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Specify the URL
url = 'https://oap.ind.nl/oap/api/desks/DH/slots?productKey=DOC&persons=1'

# Specify headers
headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'oap-locale': 'en'
}

# Push notification function
def send_push_notification(title, body):
    ACCESS_TOKEN = 'o.rKs9Caxjv8iiz30aIBPQvN9G58mpa7BC'
    # pb = Pushbullet(ACCESS_TOKEN)
    # push = pb.push_note(title, body)
    pb = Pushbullet(api_key=ACCESS_TOKEN)
    device_idn = pb.list_devices()["devices"][0]["iden"]
    # device_idn = "ujBKmhnF0DYsjBLD0k1Uzc"
    pb.bullet_note(device_idn, title, body)

try:
    # Send a GET request with headers and disable SSL verification
    response = requests.get(url, headers=headers, verify=False)

    # Check if the request was successful
    if response.status_code == 200:
        try:
            # Remove non-JSON prefix (e.g., )]}')
            clean_response = re.sub(r'^\)\]\}\',', '', response.text)
            json_data = json.loads(clean_response)

            # Check the first date
            firstDate = json_data["data"][0]["date"]
            print(f"Running..")
            if firstDate.startswith('2024'):
                print('Response:', firstDate)
                send_push_notification('Slot Available', f'A slot is available on {firstDate}.')

        except (ValueError, json.JSONDecodeError) as e:
            print('Failed to parse JSON. Raw content:', response.text)
    else:
        print('Failed to retrieve data. Status code:', response.status_code)

except requests.exceptions.RequestException as e:
    print('An error occurred:', e)

