import json
import logging
import platform
import sys
import requests
import greengrasssdk

# Setup logging to stdout
logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

# Creating a greengrass core sdk client
client = greengrasssdk.client("iot-data")

# Retrieving platform information to send from Greengrass Core
my_platform = platform.platform()

# Call Home-assistant service
HASS_URL = "http://<your-hass-ip>:8123/api/services/{0}/{1}"
HASS_TOKEN = "Bearer <your-hass-long-lived-token>"
def callservice(domain, service, entity):
    url = HASS_URL.format(domain, service)
    headers = {"Authorization": HASS_TOKEN,
               "Content-type": "application/json"}
    json = {"entity_id": entity}
    response = requests.post(url, headers=headers, json=json)
    response.raise_for_status()

def lambda_handler(event, context):
    try:
      callservice(event['domain'], event['service'], event['entity_id'])
      client.publish(
                topic="home/services/status",
                queueFullPolicy="AllOrException",
                payload=json.dumps(event)
                )
    except Exception as e:
        logger.error("Failed to publish message: " + repr(e))
    return
