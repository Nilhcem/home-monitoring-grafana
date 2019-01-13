 # Sensors + Mosquitto + InfluxDB + Grafana + Docker

 ## Projects
 - `01_bme280_mqtt`: Arduino sketch file for the ESP8266 and the BME280 that publishes sensor data to MQTT
 - `02_mijia_ble_mqt`: Python script for the Raspberry Pi 3 that connects to a BTLE MiJia Temperature & Humidity sensor and publishes data to MQTT
 - `03-mosquitto`: Mosquitto docker container
 - `04-bridge`: Python script that receives MQTT data and persists those to InfluxDB

## Build everything manually

- Deploy mosquitto
