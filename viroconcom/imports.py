

# !/usr/bin/env python
from ecmwfapi import ECMWFDataServer







def _getECMWF():
    server = ECMWFDataServer(url="https://api.ecmwf.int/v1", key='5779c25ba27168b4e35275198c308319',
                             email='lbekov@uni-bremen.de')

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


from cfgrib import Dataset

def _cfgrib():
    test = Dataset.variables\
        ('_mars-atls05-70e05f9f8ba4e9d19932f1c45a7be8d8-eZjCl5.grib')
    print(test)

_cfgrib()