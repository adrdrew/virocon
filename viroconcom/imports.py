

# !/usr/bin/env python
from ecmwfapi import ECMWFDataServer

server = ECMWFDataServer(url="https://api.ecmwf.int/v1",key='5779c25ba27168b4e35275198c308319',email='lbekov@uni-bremen.de')



server.retrieve({
    "class": "ei",
    "dataset": "interim",
    "date": "2001-06-01/to/2001-06-30",
    "expver": "1",
    "grid": "0.75/0.75",
    "levtype": "sfc",
    "param": "229.140/232.140",
    "step": "0",
    "stream": "wave",
    "time": "00:00:00/06:00:00/12:00:00/18:00:00",
    "type": "an",
    "target": "output",
})