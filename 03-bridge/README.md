# MQTT to InfluxDB Bridge

## Build

```sh
$ docker build -t nilhcem/mqttbridge .
```


## Run

```sh
$ docker run -d --name mqttbridge nilhcem/mqttbridge
```


## Dev

```sh
$ docker run -it --rm -v `pwd`:/app --name python python:3.7-alpine sh
```
