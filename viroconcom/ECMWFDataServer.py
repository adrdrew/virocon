class ECMWFDataServer():



    server = ECMWFDataServer(url="https://api.ecmwf.int/v1",key="5779c25ba27168b4e35275198c308319",email="lbekov@uni-bremen.de")

    # !/usr/bin/env python
    from ecmwfapi import ECMWFDataServer

    server = ECMWFDataServer()

    server.retrieve({
        # Specify the ERA-Interim data archive. Don't change.
        'class': "ei",
        'dataset': "interim",
        'expver': "1",
        'stream': "wave",
        # forecast (type:sfc), from both daily forecast runs (time) with all available forecast steps (step, in hours)
        'type': "sfc",
        'time': "06:00:00",
        'step': "0",
        # all available parameters, for codes see http://apps.ecmwf.int/codes/grib/param-db
        'param': "229.140/232.140",
        # days worth of data
        'date': "2015-06-01/to/2015-06-30",
        # in 0.75 degrees lat/lon
        'grid': "0.75/0.75",
        # optionally restrict area to Europe (in N/W/S/E).
        # "area": "75/-20/10/60",
        # Definition of the format
        'format' : "netcdf",
        # set an output file name
        'target': "output",
        })
