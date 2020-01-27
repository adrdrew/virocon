class ECMWFDataServer():



    server = ECMWFDataServer(url="https://api.ecmwf.int/v1",key="5779c25ba27168b4e35275198c308319",email="lbekov@uni-bremen.de")

    # !/usr/bin/env python
    from ecmwfapi import ECMWFDataServer

    server = ECMWFDataServer()

    # This script downloads ERA-Interim forecasts, on pressure levels.
    # Adapt the script to your requirements.
    # The data volume for all pressure level data is about 5GB per day, and all pressure level data for more than a single day will exceed the WebAPI limit of 600.000 fields. Thus please restrict the download to what you really need.
    # It is likely you need to split your request, this is best done by time periods, ie. first download for month 1, then for month 2, etc.

    server.retrieve({
        # Specify the ERA-Interim data archive. Don't change.
        "class": "ei",
        "dataset": "interim",
        "expver": "1",
        "stream": "oper",
        # pressure levels (levtype:pl), all available levels (levelist)
        "levtype": "pl",
        "levelist": "1/2/3/5/7/10/20/30/50/70/100/125/150/175/200/225/250/300/350/400/450/500/550/600/650/700/750/775/800/825/850/875/900/925/950/975/1000",
        # forecast (type:fc), from both daily forecast runs (time) with all available forecast steps (step, in hours)
        "type": "fc",
        "time": "00:00:00/12:00:00",
        "step": "3/6/9/12/15/18/21/24/30/36/42/48/60/72/84/96/108/120/132/144/156/168/180/192/204/216/228/240",
        # all available parameters, for codes see http://apps.ecmwf.int/codes/grib/param-db
        "param": "60.128/129.128/130.128/131.128/132.128/133.128/135.128/138.128/155.128/157.128/203.128/246.128/247.128/248.128",
        # two days worth of data
        "date": "2016-01-01/to/2016-01-02",
        # in 0.75 degrees lat/lon
        "grid": "0.75/0.75",
        # optionally restrict area to Europe (in N/W/S/E).
        # "area": "75/-20/10/60",
        # Optionally get output in NetCDF format. However, for NetCDF timestamps (time+step) must not overlap, so use e.g. "time":"00:00:00/12:00:00","step":"12"
        # "format" : "netcdf",
        # set an output file name
        "target": "CHANGEME",
        })