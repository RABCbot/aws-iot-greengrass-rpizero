# AWS IoT Greengrass on a Raspberry Pi Zero
Goal is to install [AWS IoT Greengrass](https://docs.aws.amazon.com/greengrass/latest/developerguide/quick-start.html) on a headless Raspberry Pi Zero W and deploy a lambda to control Home-assistant locally

## Hardware
* Raspberry Pi Zero W<br/>
* Micro SD Card<br/>
* Micro USB power<br/>

## Raspberry Pi Setup 
Download latest Raspberry PI OS https://downloads.raspberrypi.org/raspios_lite_armhf_latest<br/>
Use [Etcher](https://www.balena.io/etcher/) to flash image to your SD Card<br/>
Create empty SSH file and create wpa_supplicant.conf file with your WIFI credentials<br/>
Boot your Rpi Zero>br/>
SSH to your Rpi Zero<br/>

Use the Raspberry configuration tool to change the user password, hostname and under advance to expand the filesystem
```
sudo raspi-config
```
Run update and upgrade
```
sudo apt-get update
sudo apt-get upgrade
```
Setup Rpi for Greengrass
```
sudo adduser --system ggc_user
sudo addgroup --system ggc_group
cd /etc/sysctl.d
sudo nano 98-rpi.conf
```
Append to end of the file
```
fs.protected_hardlinks = 1
fs.protected_symlinks = 1
sudo reboot
```

```
cd /boot/
sudo nano cmdline.txt
append to end of the first line:
cgroup_enable=memory cgroup_memory=1
```
Reboot
```
sudo reboot
```

AWS Console
Create greengrass group and core
Download certificates
Download core installer for your pi (6l for zero)
Winscp to copy both files to your pi

sudo tar -xzvf greengrass-linux-armv6l-1.11.0.tar.gz /
sudo tar -xzvf edgewater-setup.tar.gz /greengrass

sudo cp ./certs/* ./greengrass/certs
sudo cp .config/* ./greengrass/config

cd greengrass/certs
sudo wget -O root.ca.pem https://www.amazontrust.com/repository/AmazonRootCA1.pem

AWS console
Create lambda
Configure Greengrass group to use lambda
Configure Greengrass suscription

Winscp copy your lambda (including sdk subfolder) to your Pi
/greengrass/core/runtime/python

Start greengrassc

**
** LAMBDA FOR THE PI
** 
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
def callservice(host, token, service, entity):
    url = "http://{0}/api/services/{1}".format(host, service)
    headers = {"Authorization": token,
               "Content-type": "application/json"}
    json = {"entity_id": entity}
    response = requests.post(url, headers=headers, json=json)
    response.raise_for_status()

def lambda_handler(event, context):
    try:
      callservice(
          "192.168.101.113:8123",
          "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiI0MDkwMmVkZmY1YjI0ODQwODBlZDE3NDRkYWJlNGUyMCIsImlhdCI6MTU1MTgwMjI1NywiZXhwIjoxODY3MTYyMjU3fQ.Es9y4-HDsOv8FxHkI_amHZArlyqGixEx8Exv3JBRjUI",
          "light/turn_on",
          "light.office_light")
      client.publish(
                topic="home/services/status",
                queueFullPolicy="AllOrException",
                payload=json.dumps({"message": "turn_on"})
                )
    except Exception as e:
        logger.error("Failed to publish message: " + repr(e))
    return


**
** LAMBDA TESTER
**
import boto3
import json

client = boto3.client('iot-data', region_name='us-east-1')

def lambda_handler(event, context):
    response = client.publish(
        topic='home/services/trigger',
        qos=0,
        payload=json.dumps(event)
    )
    return {
        'statusCode': 200,
        'body': json.dumps('OK')
    }

Add inline policy:
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": "iot:Publish",
            "Resource": "arn:aws:iot:us-east-1:114744974534:topic/home/services/trigger"
        }
    ]
}

**
** TROUBLESHOOTING CORE
**
sudo nano var/log/system/runtime.log
sudo nano var/log/user/us-east-1/114744974534/<your-lambda-name>.log




