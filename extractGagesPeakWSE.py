import pandas as pd
import requests

# function to extract peak level
def extract_peak_level(gage, start_date, end_date):
    url = f'https://waterservices.usgs.gov/nwis/iv/?sites={gage}&parameterCd=00065&startDT={start_date}T13:02:48.617-06:00&endDT={end_date}T13:02:48.617-06:00&siteStatus=all&format=rdb'
    data = pd.read_table(url,skiprows=28,names=['agency_cd','site_no','datetime','flow','code'],parse_dates=['datetime'])
    peak_level = data['flow'].max()
    return peak_level

# gages and durations to extract peak levels
gages = ['07380120', '07380102', '07380101']
start_dates = ['2020-10-23', '2021-08-25', '2023-01-10']
end_dates = ['2020-11-09', '2021-09-08', '2023-01-12']

# extract peak levels for different gages and durations
for gage in gages:
    for i in range(len(start_dates)):
        peak_level = extract_peak_level(gage, start_dates[i], end_dates[i])
        print(f"Peak level for gage {gage} during {start_dates[i]} to {end_dates[i]}: {peak_level}")
