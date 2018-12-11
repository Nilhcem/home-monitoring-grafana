#!/usr/bin/env python3

"""A MQTT to InfluxDB Bridge

This script receives MQTT data and save those in InfluxDB.

"""

import re
from typing import NamedTuple

import paho.mqtt.client as mqtt
from influxdb import InfluxDBClient

INFLUXDB_ADDRESS = '192.168.1.37'
MQTT_ADDRESS = 'test.mosquitto.org'
MQTT_TOPIC = 'oklmzer/home/+/+'  # [inside|outside][temperature|humidity|status]

influxdb_client = InfluxDBClient(INFLUXDB_ADDRESS, 8086)


class SensorData(NamedTuple):
    location: str
    measurement: str
    value: float


def on_connect(client, userdata, flags, rc):
    """ The callback for when the client receives a CONNACK response from the server."""
    print('Connected with result code ' + str(rc))
    client.subscribe(MQTT_TOPIC)


def on_message(client, userdata, msg):
    """The callback for when a PUBLISH message is received from the server."""
    print(msg.topic + ' ' + str(msg.payload))
    sensor_data = _parse_mqtt_message(msg.topic, msg.payload.decode('utf-8'))
    if (sensor_data is not None):
        _send_sensor_data_to_influxdb(sensor_data)


def _parse_mqtt_message(topic, payload):
    matchObj = re.match('oklmzer/home/([^/]+)/([^/]+)', topic)
    if matchObj:
        location = matchObj.group(1)
        measurement = matchObj.group(2)
        if (measurement == 'status'):
            return None
        return SensorData(location, measurement, float(payload))
    else:
        return None


def _send_sensor_data_to_influxdb(sensor_data):
    json_body = [
        {
            'measurement': sensor_data.measurement,
            'tags': {
                'location': sensor_data.location
            },
            'fields': {
                'value': sensor_data.value
            }
        }
    ]
    influxdb_client.write_points(json_body)


def main():
    influxdb_client.switch_database('influx_db')

    mqtt_client = mqtt.Client('MQTTInfluxDBBridge')
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message

    mqtt_client.connect(MQTT_ADDRESS, 1883)
    mqtt_client.loop_forever()


if __name__ == '__main__':
    print('MQTT to InfluxDB bridge')
    main()
