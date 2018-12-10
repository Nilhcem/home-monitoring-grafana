#!/usr/bin/env python3

"""A MQTT to InfluxDB Bridge

This script receives MQTT data and save those in InfluxDB.

"""

import paho.mqtt.client as mqtt

BROKER_ADDRESS = "test.mosquitto.org"
TOPIC = "oklmzer/home/livingroom/+"  # temperature / humidity / status"


def on_connect(client, userdata, flags, rc):
    """ The callback for when the client receives a CONNACK response from the server."""
    print("Connected with result code " + str(rc))
    client.subscribe(TOPIC)


def on_message(client, userdata, msg):
    """The callback for when a PUBLISH message is received from the server."""
    print(msg.topic + " " + str(msg.payload))


def main():
    client = mqtt.Client("MQTTInfluxDBBridge")
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(BROKER_ADDRESS, 1883, 60)
    client.loop_forever()


if __name__ == "__main__":
    print("MQTT to InfluxDB bridge")
    main()
