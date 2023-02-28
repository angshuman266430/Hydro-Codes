from pydsstools.heclib.dss import HecDss
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime

# First Code
dss_file = "ADCIRC_WL_Isaac_SegMean.dss"
pathname1 = "/IRREGULAR/TIMESERIES/STAGE/01Jan2012/IR-Year/Station_0001/"
startDate = "17AUG2012 00:20:00"
endDate = "15SEP2012 24:00:00"

fid = HecDss.Open(dss_file)
ts = fid.read_ts(pathname1, window=(startDate, endDate), trim_missing=True)

times = ts.pytimes
values1 = ts.values * 0.3048
values1[ts.nodata] = -9999
fid.close()

# Calculate difference in time
time_diffs = [j-i for i, j in zip(times[:-1], times[1:])]

# Start time from 0 and add difference for all next outputs for time to previous timestep output
time_sum = [datetime.timedelta(0)]
for i in range(1, len(time_diffs)):
    time_sum.append(time_sum[i-1] + time_diffs[i-1])

# Convert time to seconds
time_seconds = [time.total_seconds() for time in time_sum]

# Second Code
pathname2 = "/IRREGULAR/TIMESERIES/STAGE/01Jan2012/IR-Year/Station_0002/"

fid = HecDss.Open(dss_file)
ts = fid.read_ts(pathname2, window=(startDate, endDate), trim_missing=True)

values2 = ts.values * 0.3048
values2[ts.nodata] = -9999
fid.close()


# Third Code
pathname3 = "/IRREGULAR/TIMESERIES/STAGE/01Jan2012/IR-Year/Station_0003/"

fid = HecDss.Open(dss_file)
ts = fid.read_ts(pathname3, window=(startDate, endDate), trim_missing=True)

values3 = ts.values * 0.3048
values3[ts.nodata] = -9999
fid.close()

# Fourth Code
pathname4 = "/IRREGULAR/TIMESERIES/STAGE/01Jan2012/IR-Year/Station_0004/"

fid = HecDss.Open(dss_file)
ts = fid.read_ts(pathname4, window=(startDate, endDate), trim_missing=True)

values4 = ts.values * 0.3048
values4[ts.nodata] = -9999
fid.close()

# Fifth Code
pathname5 = "/IRREGULAR/TIMESERIES/STAGE/01Jan2012/IR-Year/Station_0005/"

fid = HecDss.Open(dss_file)
ts = fid.read_ts(pathname5, window=(startDate, endDate), trim_missing=True)

values5 = ts.values * 0.3048
values5[ts.nodata] = -9999
fid.close()

# Sixth Code
pathname6 = "/IRREGULAR/TIMESERIES/STAGE/01Jan2012/IR-Year/Station_0006/"

fid = HecDss.Open(dss_file)
ts = fid.read_ts(pathname6, window=(startDate, endDate), trim_missing=True)

values6 = ts.values * 0.3048
values6[ts.nodata] = -9999
fid.close()

# Seventh Code
pathname7 = "/IRREGULAR/TIMESERIES/STAGE/01Jan2012/IR-Year/Station_0007/"

fid = HecDss.Open(dss_file)
ts = fid.read_ts(pathname7, window=(startDate, endDate), trim_missing=True)

values7 = ts.values * 0.3048
values7[ts.nodata] = -9999
fid.close()

# Eighth Code
pathname8 = "/IRREGULAR/TIMESERIES/STAGE/01Jan2012/IR-Year/Station_0008/"

fid = HecDss.Open(dss_file)
ts = fid.read_ts(pathname8, window=(startDate, endDate), trim_missing=True)

values8 = ts.values * 0.3048
values8[ts.nodata] = -9999
fid.close()

# Merge the four codes into one DataFrame
df = pd.DataFrame({"Time": time_seconds, "Value1": values1[1:], "Value2": values2[1:], "Value3": values3[1:], "Value4": values4[1:], "Value5": values5[1:], "Value6": values6[1:], "Value7": values7[1:], "Value8": values8[1:]})
df.to_csv('SFINCS_WL_Input.csv', index = False, header=False)
np.savetxt("SFINCS_WL_Input.txt", df.values, fmt='%.6f', delimiter='\t')

