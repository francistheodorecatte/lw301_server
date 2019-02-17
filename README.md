# Emulate cloud server for Oregon Scientific LW301

## Installation

```
python3 setup.py install
```

Requirements: 

* python 3.5+
* tornado 5+

## Usage

```
lw301_server
```

Default config loaded from `/etc/lw301-server/config.conf`.

Config path may be overridden by environment value `LW301_SERVER_CONFIG`.

Available options:

```
lw301_server --help
```

CLI options overrided config options.

### Using Docker image 

#### How to pack

```bash
docker build . -t lw301-server
```

#### How to use

- mkdir /var/log/lw301
- Create and run shell script run_lw301.sh

```bash
#!/bin/sh
docker rm lw301 --force
docker run \
        --name lw301 -d \
      	--restart always \
	    -p __OUTBOUND_IP_ADDR___:80:47265 \
	    -v /var/log/lw301:/log \
	   	--enable-mqtt --mqtt-user=test --mqtt-password=test --mqtt-host=127.0.0.1 \
        lw301-server lw301_server  --address=0.0.0.0 --log_file_prefix=/log/server.log
```


## Triggers

### InfluxDB

Enable by `--enable-influxdb` option. See `--help` for all options.

Trigger send recieved values to influxdb.

Values send as soon as they recieved from the weather station.

Written data:

| Measurement | Tags | Fields |
| --- | --- | --- |
| temperature | mac, channel | celsius (float) |
| humidity | mac, channel | relative (int) |
| pressure | mac | mmhg (int), hpa (int) |


### MQTT

_TODO_

## How to catch LW301 traffic

Summary:

* overwrite DNS for some domains
* proxy :80 to this app

_TODO_: instructions & sample configs.

### DNS

Domains resolved by LW301:

* `static.oregonscientific.com` – some init routines
* `gateway.weather.oregonscientific.com` - sending data
* `blackbox-c.infra.idtcsd.net` - ?


## API

Note: history data lost if app stopped.

### GET /api/history/temperature

```js
{
    "history": [
        {
            "timestamp": 1532271317,
            "utc_datetime": "2018-07-22 17:55:17",
            "value": {
                "celsius": 22.1,
                "channel": 1,
                "mac": "00001234abcd"
            }
        },
        // ...
    ],
    "measurement": "temperature"
}
```

### GET /api/history/humidity

```js
{
    "history": [
        {
            "timestamp": 1532271317,
            "utc_datetime": "2018-07-22 17:55:17",
            "value": {
                "channel": 1,
                "mac": "00001234abcd",
                "relative": 79
            }
        },
        // ...
    ],
    "measurement": "humidity"
}
```


### GET /api/history/pressure

```js
{
    "history": [
        {
            "timestamp": 1532271186,
            "utc_datetime": "2018-07-22 17:53:06",
            "value": {
                "hPa": 982,
                "mac": "00001234abcd",
                "mmHg": 736
            }
        },
        // ...
    ],
    "measurement": "pressure"
}
```


## Licence

Apache License 2.0
