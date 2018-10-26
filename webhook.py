'''
webhook.py
pj@mrpjevans.com

Create a WebHook at ifttt.com to do, well, whatever you want! Maybe send
an email to begin with. You'll give it a trigger name which is used to
create a URL something like the following:

https://maker.ifttt.com/trigger/{trigger_name}/with/key/{your_key}

Replace those two values in {} and got to the URL to check it's working.
Once you're happy, change WEBHOOK below to match. Run the script. Every time
the light is switched on, your WebHook is called.

Make you you update the IP address to match your gateway's and
run $ python3 -i -m pytradfri IP to (re)create your
tradfri_standalone_psk.conf (Credentials file)
'''

from pytradfri import Gateway
from pytradfri.api.libcoap_api import APIFactory
from pytradfri.util import load_json, save_json
from time import sleep
import urllib.request
import threading

# Change this IP address to your gateway
IP_ADDRESS = '192.168.0.158'

# Make sure you're in the same directory as this file
CONFIG_FILE = 'tradfri_standalone_psk.conf'

WEBHOOK = 'https://maker.ifttt.com/trigger/{trigger_name}/with/key/{your_key}'

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


def observe(api, device):
    def callback(updated_device):
        light = updated_device.light_control.lights[0]
        if (light.state):
            # Light has been switched on
            print('Light on! Calling WebHook...')
            urllib.request.urlopen(WEBHOOK)
        else:
            print('Light off')

    def err_callback(err):
        print(err)

    def worker():
        api(device.observe(callback, err_callback, duration=120))

    threading.Thread(target=worker, daemon=True).start()
    print('Sleeping to start observation task')
    sleep(1)

observe(api, lights[0])

while(True):
    sleep(0.01)
