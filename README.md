# Sensors + Mosquitto + InfluxDB + Grafana + Docker

## Projects

- `01_bme280_mqtt`: Arduino sketch file for the ESP8266 and the BME280 that publishes sensor data to MQTT
- `02_mijia_ble_mqt`: Python script for the Raspberry Pi 3 that connects to a BTLE MiJia Temperature & Humidity sensor and publishes data to MQTT
- `03-mosquitto`: Mosquitto docker container
- `04-bridge`: Python script that receives MQTT data and persists those to InfluxDB


## Setup

These commands will help setting up everything quickly.


### Host server

You need a computer with Docker installed to host Mosquitto, InfluxDB, and Grafana.  
For the example, a Raspberry Pi 3 B+ with Raspbian will be used.

This machine should be accessible from the `homeserver` domain name (e.g. modifying your DNS rules).  
If you want to access it through a different name or IP address, modify each script to replace `homeserver` with your desired name / IP address.

The Mosquitto username and passwords are `mqttuser` and `mqttpassword`.  
To change these, see the `Credentials` section


### Mosquitto

```sh
$ cd 03-mosquitto
$ mkdir -p /tmp/mosquitto/data /tmp/mosquitto/log
$ chmod o+w /tmp/mosquitto /tmp/mosquitto/data /tmp/mosquitto/log
$ docker run -d -p 1883:1883 -v $PWD/mosquitto.conf:/mosquitto/config/mosquitto.conf -v $PWD/users:/mosquitto/config/users -v /tmp/mosquitto/data:/mosquitto/data -v /tmp/mosquitto/log:/mosquitto/log --name mosquitto eclipse-mosquitto:1.5
$ cd -
```


### InfluxDB

```sh
$ mkdir -p /tmp/influxdb
$ chmod o+w /tmp/influxdb
$ docker run -d -p 8086:8086 -v /tmp/influxdb:/var/lib/influxdb --name influxdb influxdb:1.7
```


### MQTT -> InfluxDB bridge

```sh
$ cd 04-bridge
$ docker build -t nilhcem/mqttbridge .
$ docker run -d --name mqttbridge nilhcem/mqttbridge
$ cd -
```


### ESP8266 BME280

- Update the `WIFI_SSID` and `WIFI_PASSWORD` with your WiFi data
- Flash the `esp8266.ino` file.


### Grafana

```sh
$ mkdir -p /tmp/grafana
$ chmod o+w /tmp/grafana
$ docker run -d -p 3000:3000 -v /tmp/grafana:/var/lib/grafana --name=grafana grafana/grafana:5.4.3
```

- Access Grafana from `http://homeserver:3000`
- Log in with user/password `admin/admin`
- Go to Configuration > Data Sources
- Add data source (InfluxDB)
  - Name: `InfluxDB`
  - URL: `http://homeserver:8086`
  - Database: `home_db`
  - User: `root`
  - Password: `root`
  - Save & Test
- Create a Dashboard
  - Add Graph Panel
  - Edit Panel
  - Data Source: InfluxDB
  - FROM: `[default] [temperature] WHERE [location]=[bme280]`
  - SELECT: `field(value)`
  - FORMAT AS: `Time series`
  - Draw mode: Lines
  - Stacking & Null value: Null value [connected]
  - Left Y
    - Unit: Temperature > Celcius
  - Panel title: Temperature (°C)


### Mijia (optional)

See `02-mijia_ble_mqtt/README.md`.


### Credentials

#### Change your MQTT user / pasword

- Run the following, replacing `[USER]` and `[PASSWORD]`

```sh
$ cd 03-mosquitto
$ echo -n "" > users
$ docker run --rm -v `pwd`/mosquitto.conf:/mosquitto/config/mosquitto.conf -v `pwd`/users:/mosquitto/config/users eclipse-mosquitto:1.5 mosquitto_passwd -b /mosquitto/config/users [USER] [PASSWORD]
$ cd -
```

Update the MQTT_USER and MQTT_PASSWORD constants from all the projects.
