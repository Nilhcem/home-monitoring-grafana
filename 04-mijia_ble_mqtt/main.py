#!/usr/bin/env python3

"""MiJia GATT to MQTT"""

import re
import time

import paho.mqtt.client as mqtt
from bluepy import btle

MQTT_TOPIC_HUMIDITY = 'home/mijia/humidity'
MQTT_TOPIC_TEMPERATURE = 'home/mijia/temperature'
MQTT_TOPIC_BATTERY = 'home/mijia/battery'
MQTT_TOPIC_STATE = 'home/mijia/status'

MQTT_PUBLISH_DELAY = 60
MQTT_CLIENT_ID = 'mijia'

MQTT_SERVER = 'homeserver'
MQTT_USER = 'mqttuser'
MQTT_PASSWORD = 'mqttpassword'

MIJIA_BTLE_ADDRESS = '4c:65:a8:d7:fb:36'

MIJIA_BATTERY_SERVICE_UUID = btle.UUID('180f')
MIJIA_BATTERY_CHARACTERISTIC_UUID = btle.UUID('2a19')

MIJIA_DATA_SERVICE_UUID = btle.UUID('226c0000-6476-4566-7562-66734470666d')
MIJIA_DATA_CHARACTERISTIC_UUID = btle.UUID('226caa55-6476-4566-7562-66734470666d')
MIJIA_DATA_CHARACTERISTIC_HANDLE = 0x0010

BTLE_SUBSCRIBE_VALUE = bytes([0x01, 0x00])
BTLE_UNSUBSCRIBE_VALUE = bytes([0x00, 0x00])

battery = None
temperature = None
humidity = None


def on_connect(client, userdata, flags, rc):
    client.publish(MQTT_TOPIC_STATE, 'connected', 1, True)


class MyDelegate(btle.DefaultDelegate):
    def __init__(self):
        btle.DefaultDelegate.__init__(self)

    def handleNotification(self, cHandle, data):
        fetch_sensor_data(bytearray(data).decode('utf-8'))


def main():
    mqttc = mqtt.Client(MQTT_CLIENT_ID)
    mqttc.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    mqttc.will_set(MQTT_TOPIC_STATE, 'disconnected', 1, True)
    mqttc.on_connect = on_connect

    mqttc.connect(MQTT_SERVER, 1883, 60)
    mqttc.loop_start()

    last_msg_time = time.time()

    while True:
        try:
            print('Connecting to ' + MIJIA_BTLE_ADDRESS)
            dev = btle.Peripheral(MIJIA_BTLE_ADDRESS)
            print('Set delegate')
            dev.setDelegate(MyDelegate())

            # Get battery level
            if battery is None:
                fetch_battery_level(dev)
                print('Battery level: ' + str(battery))

            # Subscribe to data characteristic
            if temperature is None or humidity is None:
                dev.writeCharacteristic(MIJIA_DATA_CHARACTERISTIC_HANDLE, BTLE_SUBSCRIBE_VALUE, True)
                while True:
                    if dev.waitForNotifications(1.0):
                        print('Temperature: ' + temperature)
                        print('Humidity: ' + humidity)
                        dev.writeCharacteristic(MIJIA_DATA_CHARACTERISTIC_HANDLE, BTLE_UNSUBSCRIBE_VALUE, True)
                        dev.disconnect()
                        break

        except (btle.BTLEDisconnectError, IOError):
            print("Disconnected :)")

        if battery is not None and temperature is not None and humidity is not None:
            delay_gap = time.time() - last_msg_time
            if delay_gap < MQTT_PUBLISH_DELAY:
                time.sleep(MQTT_PUBLISH_DELAY - delay_gap)

            publish_sensor_data(mqttc)
            last_msg_time = time.time()
            reset_variables()


def reset_variables():
    global battery
    global temperature
    global humidity

    battery = None
    temperature = None
    humidity = None


def fetch_battery_level(dev):
    global battery

    battery_service = dev.getServiceByUUID(MIJIA_BATTERY_SERVICE_UUID)
    battery_characteristic = battery_service.getCharacteristics(MIJIA_BATTERY_CHARACTERISTIC_UUID)[0]
    battery = ord(battery_characteristic.read())


def fetch_sensor_data(temp_hum):
    global temperature
    global humidity

    pattern = re.compile('T=([\d.-]+) H=([\d.-]+)')
    match = re.match(pattern, temp_hum)
    if match:
        temperature = match.group(1)
        humidity = match.group(2)


def publish_sensor_data(mqttc):
    mqttc.publish(MQTT_TOPIC_TEMPERATURE, temperature, 1, True)
    mqttc.publish(MQTT_TOPIC_HUMIDITY, humidity, 1, True)
    mqttc.publish(MQTT_TOPIC_BATTERY, battery, 1, True)


if __name__ == '__main__':
    print('Starting MiJia GATT client')
    main()
