server = ECMWFDataServer(url="https://api.ecmwf.int/v1",key="5779c25ba27168b4e35275198c308319",email="lbekov@uni-bremen.de")

from ecmwfapi import ECMWFDataServer
server = ECMWFDataServer()
server.retrieve({
    "class": "ei",
    "dataset": "interim",
    "date": "2015-06-01/to/2015-06-30",
    "expver": "1",
    "grid": "0.75/0.75",
    "levtype": "sfc",
    "param": "229.140/232.140",
    "step": "0",
    "stream": "wave",
    "time": "06:00:00",
    "type": "an",
    "target": "output",
})