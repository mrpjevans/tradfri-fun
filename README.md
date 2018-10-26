# tradfri-fun
Code for controlling Trådfri lights to accompany the article in MagPI issue 76.

## Requirements

- Trådfri gateway
- Trådfri colour-changing light
- Raspberry Pi (Raspian Stretch)

These instructions will also work on other Linux distributions and macOS, although package management will differ.

## Installation

Run the following commands:

```bash
$ cd
$ sudo apt install git automake libtool python3-pi
$ git clone --depth 1 --recursive -b dtls https://github.com/home-assistant/libcoap.git
$ cd libcoap
$ ./autogen.sh
$ ./configure --disable-documentation --disable-shared --without-debug CFLAGS="-DCOAP_DEBUG_FD=stderr"
$ make
$ make install
$ cd
$ pip3 install pytradfri
```
You can safely remove the ~/libcoap directory at this point.

Run the test script to check communication with the gateway:

```bash
$ python3 -i -m pytradfri IP-Address
```
N.B. Replace IP-Address with the IP address of your gateway.

Enter the security code printed on the base of your gateway. This creates a .conf file containing your unique password that must be present in the same directory as the following scripts.

## The Scripts

These are simple Python 3 scripts intended to be a starting point for more adventurous projects. They all asssume a single smart light with colour capability.

These scripts will not run without modification. Please see the notes in each one for instructions.
 
### brighten.py

A test of Pi -> gateway -> light. Slowly brightens the light from 0 to 254 (maximum brightness).

### watch_light.py

Displays event information. Run the script then control the light with a normal remote. You will see data on the console as changes occur.

### cheerlights.py

Set the colour of the smart light to the current Cheerlights value. See cheerlights.com for more on this project.

### webhook.py

An example of how to trigger an IFTTT webhook when a Trådfri light is switched on.
