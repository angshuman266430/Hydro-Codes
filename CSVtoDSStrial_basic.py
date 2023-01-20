from datetime import datetime
from pydsstools.heclib.dss import HecDss
from pydsstools.core import TimeSeriesContainer, UNDEFINED

dss_file = "example.dss"
pathname = "/IRREGULAR/TIMESERIES/STAGE//IR-YEAR/Station_0001/"
tsc = TimeSeriesContainer()
tsc.pathname = pathname
tsc.startDateTime = "15JUL2019 19:00:00" #change the format to "15JUL2019 19:00:00"
tsc.numberValues = 7
tsc.units = "ft"
tsc.type = "INST"
tsc.interval = -1
tsc.values = [100, UNDEFINED, 500, 5000, 10000, 24.1, 25]

# Create a list of datetime objects for the times at which the values were recorded
times = [datetime(2019, 7, 15, 19, 0, 0),
         datetime(2019, 7, 15, 20, 0, 0),
         datetime(2019, 7, 15, 21, 0, 0),
         datetime(2019, 7, 15, 22, 0, 0),
         datetime(2019, 7, 15, 23, 0, 0),
         datetime(2019, 7, 16, 0, 0, 0),
         datetime(2019, 7, 16, 1, 0, 0)]

tsc.times = times

fid = HecDss.Open(dss_file)
fid.deletePathname(tsc.pathname)
fid.put_ts(tsc)
ts = fid.read_ts(pathname)
fid.close()
