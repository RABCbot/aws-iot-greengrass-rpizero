# AWS IoT Greengrass on a Raspberry Pi Zero
Goal is to install [AWS IoT Greengrass](https://docs.aws.amazon.com/greengrass/latest/developerguide/quick-start.html) on a headless Raspberry Pi Zero W and deploy a lambda to control Home-assistant locally

## Hardware
* Raspberry Pi Zero W<br/>
* Micro SD Card<br/>
* Micro USB power<br/>

## Raspberry Pi Setup 
Download latest [Raspberry PI OS](https://downloads.raspberrypi.org/raspios_lite_armhf_latest)<br/>
Use [Etcher](https://www.balena.io/etcher/) to flash image to your SD Card<br/>
Browse to your SD card and create an empty file named SSH<br/>
Using a text editor, create a file named wpa_supplicant.conf, enter your WIFI credentials
and copy the file to your SD card<br/>
```
country=US
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
network={
	ssid="<your-ssid>"
	psk="<your wifi-password>"
	key_mgmt=WPA-PSK
}
```
Insert the SD Card in your Rpi Zero and boot<br/>
Find the IP of your Rpi Zero and SSH to it<br/>

Use the Raspberry configuration tool to change the user password, hostname and under advance to expand the filesystem
```
sudo raspi-config
```
Run update and upgrade
```
sudo apt-get update
sudo apt-get upgrade
```
## AWS Greengrass core requirements ([reference](https://docs.aws.amazon.com/greengrass/latest/developerguide/setup-filter.rpi.html))
Add Greengrass core user and group
```
sudo adduser --system ggc_user
sudo addgroup --system ggc_group
```
Edit file 98-rpi.conf
```
cd /etc/sysctl.d
sudo nano 98-rpi.conf
```
Append to end of the file
```
fs.protected_hardlinks = 1
fs.protected_symlinks = 1
```
Reboot
```
sudo reboot
```
Edit cmdline.txt
```
cd /boot/
sudo nano cmdline.txt
```
append to end of the first line (not as a new line)
```
cgroup_enable=memory cgroup_memory=1
```
Reboot
```
sudo reboot
```
## AWS Greengrass setup ([reference](https://docs.aws.amazon.com/greengrass/latest/developerguide/gg-config.html))
Follow AWS console to create greengrass group and greengrass core<br/>
Once you complete the steps, download the security resources as a tar.gz file, these are the certificates that you will need in the next step<br/>
Download the greengrass core software for your architecture, in this case [Raspbian Linuz Armv6l](https://d1onfpft10uf5o.cloudfront.net/greengrass-core/downloads/1.11.0/greengrass-linux-armv6l-1.11.0.tar.gz)<br/>
Use Winscp to copy the certificates tar.gz file and the core software tar.gz to your Rpi Zero

## AWS Greengrass core setup ([reference](https://docs.aws.amazon.com/greengrass/latest/developerguide/gg-device-start.html))
SSH to your RPI Zero and run the commands
```
sudo tar -xzvf greengrass-linux-armv6l-1.11.0.tar.gz /
sudo tar -xzvf xxxxxxx-setup.tar.gz /greengrass
sudo cp ./certs/* ./greengrass/certs
sudo cp .config/* ./greengrass/config
cd greengrass/certs
sudo wget -O root.ca.pem https://www.amazontrust.com/repository/AmazonRootCA1.pem
```

## AWS Greengrass lambda
Create lambda
Configure Greengrass group to use lambda
Configure Greengrass suscription

Winscp copy your lambda (including sdk subfolder) to your Pi /greengrass/core/runtime/python

Start greengrassc

## AWS Greengrass core troubleshooting
```
sudo nano var/log/system/runtime.log
sudo nano var/log/user/us-east-1/114744974534/<your-lambda-name>.log
```




