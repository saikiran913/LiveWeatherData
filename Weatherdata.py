import requests
import json
import time
from azure.eventhub import EventHubProducerClient, EventData

# Weatherstack parameters
API_KEY = '03ec76e0382abf6b5d63466b032e478c'
BASE_URL = "http://api.weatherstack.com/current"

# Event Hubs parameters
CONNECTION_STR = 'Endpoint=sb://weatherdata.servicebus.windows.net/;SharedAccessKeyName=Testingpolicy;SharedAccessKey=CrT7t/iSt3WHMc0D78cJyy6deu/hg77dn+AEhDN6ABQ=;EntityPath=weatherdata'
EVENTHUB_NAME = 'weatherdata'

def fetch_weather_data(location):
    """Fetches weather data from Weatherstack API."""
    params = {
        'access_key': API_KEY,
        'query': location
    }
    response = requests.get(BASE_URL, params=params)
    return response.json()

def send_data_to_event_hub(data):
    """Sends fetched data to Azure Event Hub."""
    producer = EventHubProducerClient.from_connection_string(conn_str=CONNECTION_STR, eventhub_name=EVENTHUB_NAME)
    with producer:
        event_data_batch = producer.create_batch()
        event_data_batch.add(EventData(json.dumps(data)))
        producer.send_batch(event_data_batch)

if __name__ == "__main__":
    # Example location
    location = 'location'
    while True:
        data = fetch_weather_data(location)
        print("Fetched data:", data)  # Debugging line
        send_data_to_event_hub(data)
        time.sleep(300)  # Fetch data every 5 minutes
