from pydsstools.heclib.dss import HecDss
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime

# First Code
dss_file = "Isaac___Grid___AORC.dss"
pathname1 = "//J_UPPERNATALOUTLET/FLOW/01AUG2012-01SEP2012/1HOUR/RUN:ISAAC - GRID - AORC/"
startDate = "15AUG2012 12:00:00"
endDate = "12SEP2012 12:00:00"

fid = HecDss.Open(dss_file)
ts = fid.read_ts(pathname1, window=(startDate, endDate), trim_missing=True)

times = ts.pytimes
values1 = ts.values * 0.028316847
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
pathname2 = "//J_TICKFALLHOLDENOUTLET/FLOW/01AUG2012-01SEP2012/1HOUR/RUN:ISAAC - GRID - AORC/"

fid = HecDss.Open(dss_file)
ts = fid.read_ts(pathname2, window=(startDate, endDate), trim_missing=True)

values2 = ts.values * 0.028316847
values2[ts.nodata] = -9999
fid.close()


# Third Code
pathname3 = "//J_CHAPOUTLET/FLOW/01AUG2012-01SEP2012/1HOUR/RUN:ISAAC - GRID - AORC/"

fid = HecDss.Open(dss_file)
ts = fid.read_ts(pathname3, window=(startDate, endDate), trim_missing=True)

values3 = ts.values * 0.028316847
values3[ts.nodata] = -9999
fid.close()

# Fourth Code
pathname4 = "//J_AMITE_COMITE/FLOW/01AUG2012-01SEP2012/1HOUR/RUN:ISAAC - GRID - AORC/"

fid = HecDss.Open(dss_file)
ts = fid.read_ts(pathname4, window=(startDate, endDate), trim_missing=True)

values4 = ts.values * 0.028316847
values4[ts.nodata] = -9999
fid.close()

# Merge the four codes into one DataFrame
df = pd.DataFrame({"Time": time_seconds, "Value1": values1[1:], "Value2": values2[1:], "Value3": values3[1:], "Value4": values4[1:]})
df.to_csv('SFINCS_Discharge_Input.csv', index = False, header=False)
np.savetxt("SFINCS_Discharge_Input.txt", df.values, fmt='%.6f', delimiter='\t')

