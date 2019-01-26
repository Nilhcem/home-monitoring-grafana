# Home sensor data monitoring with MQTT, InfluxDB and Grafana

Blog post: [http://nilhcem.com/iot/home-monitoring-with-mqtt-influxdb-grafana](http://nilhcem.com/iot/home-monitoring-with-mqtt-influxdb-grafana)  


## Projects

- `01-mosquitto`: Mosquitto Docker container configuration files
- `02-bridge`: Python script that receives MQTT data and persists those to InfluxDB
- `03-bme280_mqtt`: Arduino sketch file for the ESP8266 and the BME280 that publishes sensor data to MQTT
- `04-mijia_ble_mqt`: Python script that connects to a BTLE MiJia Temperature & Humidity sensor and publishes data to MQTT
- `05-dht22_mqtt`: Arduino sketch file for the ESP8266 and the DHT22 that publishes sensor data to MQTT


## Setup

### Mosquitto + InfluxDB + Grafana

Make sure you have `docker` and `docker-compose` installed.  
For the example, a Raspberry Pi 3 B+ with Raspbian will be used.

Set the `DATA_DIR` environment variable to the path where will be stored local data (e.g. in `/tmp`):

```sh
export DATA_DIR=/tmp
```

Create data directories with write access:

```sh
mkdir -p ${DATA_DIR}/mosquitto/data ${DATA_DIR}/mosquitto/log ${DATA_DIR}/influxdb ${DATA_DIR}/grafana
sudo chown -R 1883:1883 ${DATA_DIR}/mosquitto
sudo chown -R 472:472 ${DATA_DIR}/grafana
```

Run docker compose:

```sh
$ docker-compose up -d
```

Mosquitto username and passwords are `mqttuser` and `mqttpassword`.
 To change these, see the `Optional: Update mosquitto credentials` section.


## Sensors

Sensors should send data to the mosquitto broker to the following topic:  
`home/{peripheralName}/{temperature|humidity|battery|status}`.  
For example: `home/bme280/temperature`.

Arduino sketches for the ESP8266 are provided to communicate with a BME280 (`03-bme280_mqtt`) and a DHT22 (`05-dht22_mqtt`).  
Before flashing, you need to change the `WIFI_SSID`, `WIFI_PASSWORD`, and `MQTT_SERVER` constants to your WiFi information and MQTT server address.

You can also use a Xiaomi MiJia Temperature & Humidity Sensor.  
For more information, see `04-mijia_ble_mqtt/README.md`.


## Grafana setup

- Access Grafana from `http://<host ip>:3000`
- Log in with user/password `admin/admin`
- Go to Configuration > Data Sources
- Add data source (InfluxDB)
  - Name: `InfluxDB`
  - URL: `http://influxdb:8086`
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


## Optional: Update mosquitto credentials

To change default MQTT username and password, run the following, replacing `[USER]` and `[PASSWORD]`:

```sh
$ cd 01-mosquitto
$ echo -n "" > users
$ docker run --rm -v `pwd`/mosquitto.conf:/mosquitto/config/mosquitto.conf -v `pwd`/users:/mosquitto/config/users eclipse-mosquitto:1.5 mosquitto_passwd -b /mosquitto/config/users [USER] [PASSWORD]
$ cd -
```

Then, update the `MQTT_USER` and `MQTT_PASSWORD` constants in all the subdirectories, and launch docker compose again.


## Alternative: Using docker manually instead of docker compose

```sh
$ cd 01-mosquitto
$ docker run -d -p 1883:1883 -v $PWD/mosquitto.conf:/mosquitto/config/mosquitto.conf -v $PWD/users:/mosquitto/config/users -v $DATA_DIR/mosquitto/data:/mosquitto/data -v $DATA_DIR/mosquitto/log:/mosquitto/log --name mosquitto eclipse-mosquitto:1.5
$ cd -

$ docker run -d -p 8086:8086 -v $DATA_DIR/influxdb:/var/lib/influxdb --name influxdb influxdb:1.7

$ cd 02-bridge
$ docker build -t nilhcem/mqttbridge .
$ docker run -d --name mqttbridge nilhcem/mqttbridge
$ cd -

$ docker run -d -p 3000:3000 -v $DATA_DIR/grafana:/var/lib/grafana --name=grafana grafana/grafana:5.4.3
```
