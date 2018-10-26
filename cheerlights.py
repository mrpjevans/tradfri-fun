'''
cheerlights.py
pj@mrpjevans.com

Based in part on code from: https://github.com/ggravlingen/pytradfri/

This script will poll the Cheerlights API once a minute and
switch the first smart light in your devices to the current Cheerlights
colour.

Make you you update the IP address to match your gateway's and
run $ python3 -i -m pytradfri IP to (re)create your
tradfri_standalone_psk.conf (Credentials file)
'''

from pytradfri import Gateway
from pytradfri.api.libcoap_api import APIFactory
from pytradfri.util import load_json, save_json
from time import sleep
import urllib.request
import json

# Change this IP address to your gateway
IP_ADDRESS = '192.168.0.158'

# Make sure you're in the same directory as this file
CONFIG_FILE = 'tradfri_standalone_psk.conf'

CHEERLIGHTS_URL = 'http://api.thingspeak.com/channels/1417/field/1/last.json'

# Load in the file, get our password for the gateway and create an API
conf = load_json(CONFIG_FILE)
identity = conf[IP_ADDRESS].get('identity')
psk = conf[IP_ADDRESS].get('key')
api_factory = APIFactory(host=IP_ADDRESS, psk_id=identity, psk=psk)

# This section connects to the gateway and gets information on devices
api = api_factory.request
gateway = Gateway()
devices_command = gateway.get_devices()
devices_commands = api(devices_command)
devices = api(devices_commands)

# Create an array of objects that are lights
lights = [dev for dev in devices if dev.has_light_control]

# The gateway contains predefined colour names, we can map these to Cheerlights
colourConvertor = {
    'red': 'Saturated Red',
    'green': 'Lime',
    'blue': 'Blue',
    'cyan': 'Light Blue',
    'white': 'Cool white',
    'oldlace': 'Warm white',
    'purple': 'Saturated Purple',
    'magenta': 'Light Purple',
    'yellow': 'Yellow',
    'orange': 'Warm Amber',
    'pink': 'Pink'
}

# Loop-de-loop
while(True):

    # Get the latest colour from Cheerlights
    with urllib.request.urlopen(CHEERLIGHTS_URL) as url:
        data = json.loads(url.read().decode())
        colour = data['field1']
    print('Cheerlights colour is ' + colour)

    # Send it to the light
    api(lights[0].light_control.set_predefined_color(colourConvertor[colour]))

    sleep(60)
