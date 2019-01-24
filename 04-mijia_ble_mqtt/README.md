# Bluetooth LE to MQTT bridge for the Xiaomi Mijia Temperature & Humidity sensor

## Update constants in main.py

- Update the `MQTT_SERVER` constant with the address of the MQTT server.
- Update the `MIJIA_BTLE_ADDRESS` constant with the BLE address of your Mijia device.


## Install dependencies

You'll need to install bluez and python3. Then you'll need pip3 to install bluepy.

Example on a Raspberry Pi 3:
```sh
$ sudo apt-get install python-pip libglib2.0-dev
$ sudo pip3 install -r requirements.txt
```


## Run

```sh
$ ./main.py
```
