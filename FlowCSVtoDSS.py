import pandas as pd
from pydsstools.heclib.dss import HecDss
from pydsstools.core import TimeSeriesContainer
from datetime import datetime

csv_path = 'Z:\\LWI2023-24\\LWI_FLOW_GAGES\\CSVtoDSS\\Gage_time_series_laura.csv'
dss_output_path = 'Z:\\LWI2023-24\\LWI_FLOW_GAGES\\CSVtoDSS\\Gage_time_series_laura.dss'

df = pd.read_csv(csv_path)
df['datetime'] = pd.to_datetime(df['datetime'], format='%m/%d/%Y %H:%M')

fid = HecDss.Open(dss_output_path, mode='w')

for column in df.columns[1:]:
    station = column.split('_')[0]
    gage_identifier = column.split('_')[1]

    tsc = TimeSeriesContainer()
    # If your data are indeed at a fixed interval, specify it here. For example, 15 minutes.
    # Note: The exact method to set the interval in pydsstools may vary. Adjust as per documentation.
    tsc.interval = 15  # Assuming a fixed interval can be set directly.
    tsc.values = df[column].tolist()
    tsc.times = df['datetime'].tolist()
    tsc.startDateTime = tsc.times[0].strftime("%d%b%Y:%H%M").upper()
    tsc.numberValues = len(tsc.values)
    tsc.units = "CFS"
    tsc.type = "INST-VAL"
    # Adjust the pathname to include a valid interval indication, such as "15MIN" for 15-minute data
    tsc.pathname = f"/{station}/{gage_identifier}/FLOW//15MIN/Laura/"

    fid.put_ts(tsc)

