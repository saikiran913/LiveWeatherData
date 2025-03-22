import requests
import json
import time
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

# Weatherstack parameters
API_KEY = 'YourAPIKey'
BASE_URL = "http://api.weatherstack.com/current"

# Azure Blob Storage parameters
CONNECTION_STRING = 'DefaultEndpointsProtocol=https;AccountName=weatherdatalive;AccountKey=m73i6YRJBD3JDxOl2rNkDA+i1cA3RsSGg7Ghy57AfFnRPktlvXhLZiatNYGr9AdFAWiqcbkbcXuE+ASt8mnJ0A==;EndpointSuffix=core.windows.net'
CONTAINER_NAME = 'weatherdatalive'

def fetch_weather_data(location):
    """Fetches weather data from Weatherstack API."""
    params = {
        'access_key': API_KEY,
        'query': location
    }
    response = requests.get(BASE_URL, params=params)
    return response.json()

def upload_data_to_blob(data, filename):
    """Uploads data to Azure Blob Storage."""
    try:
        # Create the BlobServiceClient object which will be used to create a container client
        blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
        # Create the container if it does not already exist
        container_client = blob_service_client.get_container_client(CONTAINER_NAME)
        container_client.create_container()

        # Create a blob client using the local file name as the name for the blob
        blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=filename)

        # Upload the created file
        blob_client.upload_blob(data, overwrite=True)
        print("Data uploaded to blob successfully.")
    except Exception as e:
        print("Error in uploading to Blob Storage:", e)

if __name__ == "__main__":
    location = 'New York'  # Specify the location for which you want weather data
    while True:
        data = fetch_weather_data(location)
        print("Fetched data:", data)  # Debugging line
        # Convert data to JSON string for uploading
        data_json = json.dumps(data)
        filename = f"weather_{location.replace(' ', '_').lower()}.json"
        upload_data_to_blob(data_json, filename)
        time.sleep(300)  # Fetch data every 5 minutes
