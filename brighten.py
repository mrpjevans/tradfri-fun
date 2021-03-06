'''
brighten.py
pj@mrpjevans.com

Based in part on code from: https://github.com/ggravlingen/pytradfri/

Simply sets you light to minimum dimness then slowly brightens to max.

Make you you update the IP address to match your gateway's and
run $ python3 -i -m pytradfri IP to (re)create your
tradfri_standalone_psk.conf (Credentials file)
'''

from pytradfri import Gateway
from pytradfri.api.libcoap_api import APIFactory
from pytradfri.util import load_json, save_json
from time import sleep

# Change this IP address to your gateway
IP_ADDRESS = '192.168.0.158'

# Make sure you're in the same directory as this file
CONFIG_FILE = 'tradfri_standalone_psk.conf'

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

# Brightness ranges from 0 to 254, so lets set the light in stages of 5
for brightness in range(0, 255, 5):

    # Set the first light to 'brightness' and then pause for a moment
    api(lights[0].light_control.set_dimmer(brightness))
    sleep(0.1)
