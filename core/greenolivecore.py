import json
import logging
import requests

logger = logging.getLogger(__name__)

def lambda_handler(request, context):
  logger.info(json.dumps(request))
  cfg = read_config("/local/hass.config")
  call_hass(cfg["url"],
            cfg["bearer_token"],
            request)

def call_hass(url, token, request):
  try:
    headers = {"Authorization": "Bearer {}".format(token),
               "Content-Type'": "Application/Json"}
    response = requests.request("POST", url, headers=headers, json=request)
    response.raise_for_status()
  except Exception as err:
    logger.info("Home-assistant call failed, because %s", str(err))

def read_config(filename):
  try:
    with open(filename, "r") as f:
      return json.load(f)
  except IOError as ex:
    logger.error("Failed to read configuration file, because %s", ex)

def write_config(filename, config):
  try:
    with open(filename, "w") as f:
      json.dump(config, f)
  except IOError as ex:
    logger.error("Failed to write configuration file, because %s", ex)

