# UDP version of Open Pixel Control 🎛💡

[![Build Status](https://travis-ci.com/felddy/opcu.svg?branch=develop)](https://travis-ci.com/felddy/opcu)
[![Coverage Status](https://coveralls.io/repos/github/felddy/opcu/badge.svg?branch=develop)](https://coveralls.io/github/felddy/opcu?branch=develop)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/felddy/opcu.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/felddy/opcu/alerts/)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/felddy/opcu.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/felddy/opcu/context:python)

Consuming raw or undercooked meats, poultry, seafood, shellfish or eggs may
increase your risk of foodborne illness.

## Installing spidev

`sudo apt-get install python3-spidev`

## Running server at boot.  Add to /etc/rc.local

On arcade box:
`/home/pi/opcu.py apa102 &> /dev/null &`

On shelves:
`/home/pi/opcu.py lpd8806 &> /dev/null &`

docker-compose run opc

## Building Feather firmware

1. Make a copy of the wifi_secrets.h.template file and name it wifi_secrets.h
1. Edit the wifi_secrets.h file to include the WiFi credentials
1. Install the [WiFi101 library by Arduino](https://www.arduino.cc/en/Reference/WiFi101)
for the WINC1500 module using the IDE Library Manager.
1. [Manually install](https://www.arduino.cc/en/Guide/Libraries#toc5)
the [Adafruit_ZeroDMA](https://github.com/adafruit/Adafruit_ZeroDMA/archive/master.zip)
library.
1. Add the [Adafruit boards index](https://adafruit.github.io/arduino-board-index/package_adafruit_index.json)
to the IDE's preferences, under "Additional Boards Manager URLs".
1. Select the "Adafruit Feather M0" under the Tools menu.
1. Compile and Upload to the Feather over USB.

For more information about using the IDE with the Feather [see here](https://learn.adafruit.com/adafruit-feather-m0-basic-proto/using-with-arduino-ide).

This project is based on [Adafruit Lightship](https://github.com/adafruit/Adafruit_Lightship/)

## Contributing

We welcome contributions!  Please see [here](CONTRIBUTING.md) for
details.
