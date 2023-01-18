import pandas as pd
import requests

# function to extract peak level
def extract_peak_level(gage, start_date, end_date):
    url = f'https://waterservices.usgs.gov/nwis/iv/?sites={gage}&parameterCd=00065&startDT={start_date}T13:02:48.617-06:00&endDT={end_date}T13:02:48.617-06:00&siteStatus=all&format=rdb'
    data = pd.read_table(url,skiprows=28,names=['agency_cd','site_no','datetime','flow','code'],parse_dates=['datetime'])
    data['flow'] = pd.to_numeric(data['flow'], errors='coerce')
    peak_level = data['flow'].max()
    return peak_level

# gages and durations to extract peak levels
gages = ['07375230', '07375650', '07376300', '07378650', '07378722', '07378745', '07378746', '07378748', '07378810', '07379000', '07379050', '07379075', '07379100', '07379960', '07380101', '07380102', '07380106', '07380120', '07380126', '07380127', '07380200', '07380210', '07380212', '07380215', '073802220', '073802225', '0738022295', '0738022395', '073802245', '073802273', '073802280', '073802282', '073802284', '073802302']
start_dates = ['2002-10-01', '2003-02-02', '2004-04-12', '2009-03-06', '2012-12-21', '2015-10-06', '2016-02-17', '2016-07-18', '2019-04-20']
end_dates = ['2002-11-12', '2003-02-24', '2004-05-04', '2009-04-07', '2013-01-27', '2015-11-12', '2016-03-27', '2016-08-29', '2019-05-17']

# extract peak levels for different gages and durations
for gage in gages:
    for i in range(len(start_dates)):
        peak_level = extract_peak_level(gage, start_dates[i], end_dates[i])
        print(f"Peak level for gage {gage} during {start_dates[i]} to {end_dates[i]}: {peak_level}")
