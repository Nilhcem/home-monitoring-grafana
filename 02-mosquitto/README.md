# Mosquitto (Docker)

```sh
$ docker run -it -p 1883:1883 -v `pwd`/mosquitto.conf:/mosquitto/config/mosquitto.conf eclipse-mosquitto:1.5
```


### Mount Points

A docker mount point has been created in the image to be used for configuration.
```
/mosquitto/config
```

Two docker volumes have been created in the image to be used for persistent storage and logs.
```
/mosquitto/data
/mosquitto/log
```


### Configuration

When creating a container from the image, the default configuration values are used.
To use a custom configuration file, mount a **local** configuration file to `/mosquitto/config/mosquitto.conf`
```sh
$ docker run -it -p 1883:1883 -v <absolute-path-to-configuration-file>:/mosquitto/config/mosquitto.conf nilhcem/mosquitto
```

### Persistence

Configuration can be changed to:

* persist data to `/mosquitto/data`
* log to `/mosquitto/log/mosquitto.log`

i.e. add the following to `mosquitto.conf`:
```
persistence true
persistence_location /mosquitto/data/

log_dest file /mosquitto/log/mosquitto.log
```

**Note**: For any volume used, the data will be persistent between containers.
