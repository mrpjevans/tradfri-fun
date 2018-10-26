from pytradfri import Gateway
from pytradfri.api.libcoap_api import APIFactory
from pytradfri.util import load_json, save_json
from time import sleep

IP_ADDRESS = '192.168.0.158'
CONFIG_FILE = 'tradfri_standalone_psk.conf'
conf = load_json(CONFIG_FILE)

identity = conf[IP_ADDRESS].get('identity')
psk = conf[IP_ADDRESS].get('key')
api_factory = APIFactory(host=IP_ADDRESS, psk_id=identity, psk=psk)

api = api_factory.request
gateway = Gateway()
devices_command = gateway.get_devices()
devices_commands = api(devices_command)
devices = api(devices_commands)

lights = [dev for dev in devices if dev.has_light_control]

for brightness in range(0, 255, 5):
    api(lights[0].light_control.set_dimmer(brightness))
    sleep(0.1)
