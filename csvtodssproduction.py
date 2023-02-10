import os
import pandas as pd
from datetime import datetime
from pydsstools.core import TimeSeriesContainer, UNDEFINED
from pydsstools.heclib.dss import HecDss

folder_path = '.'
for filename in os.listdir(folder_path):
    if filename.endswith(".csv"):
        data = pd.read_csv(filename)

        times = data.datetime
        times_dt = pd.to_datetime(times, yearfirst=True)
        data['ConvertedDate'] = times_dt.dt.strftime("%d%b%Y %H:%M:%S").astype(str)
        startDate = data['ConvertedDate'][0]
        timesList = data['ConvertedDate'].values.tolist()
        valuesList = data.total_wl.values.tolist()

        pathname = '///STAGE//1HOUR//'
        tsc = TimeSeriesContainer()
        tsc.pathname = pathname
        tsc.startDateTime = timesList[0]
        tsc.numberValues = len(valuesList)
        tsc.units = "FEET"
        tsc.type = "INST-VAL"
        tsc.interval = -1
        tsc.values = valuesList
        tsc.times = timesList

        dss_file = filename[:-4]+".dss"
        with HecDss.Open(dss_file) as fid:
            status = fid.put_ts(tsc)