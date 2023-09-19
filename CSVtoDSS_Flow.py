import csv
import os
from datetime import datetime
from pydsstools.heclib.dss import HecDss
from pydsstools.core import TimeSeriesContainer, UNDEFINED

folder_path = "Z:\Amite_Runs_for_Structures\Aug2016_RAS_OWI_ReAn_windLagrangian\CalValModel\BC_Extended\AORC_Data"  # replace with the actual path to the folder containing the csv files

stations = ["J_AMITE_COMITE", "J_UPPERNATALOUTLET", "J_TICKFALLHOLDENOUTLET", "J_CHAPOUTLET"]

for filename in os.listdir(folder_path):
    if filename.endswith(".csv"):
        # Read data from csv file
        with open(os.path.join(folder_path, filename), 'r') as file:
            reader = csv.reader(file)
            next(reader)  # skip header row
            data = [row for row in reader]

        # Create a list of datetime objects for the times at which the values were recorded
        times = [datetime.strptime(row[0], '%m/%d/%Y %H:%M') for row in data]

        # Loop through the 4 columns for tsc_values
        for i, station in enumerate(stations):
            # Extract tsc.values from csv data
            tsc_values = [float(row[173 + i * 4]) for row in data]

            # Update the pathname for each iteration
            date_str = times[0].strftime("%d%b%Y").upper()
            pathname = f"//{station}/FLOW/{date_str}/1HOUR/RUN:NONTC_RANK01/"

            tsc = TimeSeriesContainer()
            tsc.pathname = pathname
            tsc.startDateTime = times[0].strftime("%m/%d/%Y %H:%M")
            tsc.numberValues = len(tsc_values)
            tsc.units = "CFS"  # Assuming the units are cubic feet per second for flow
            tsc.type = "INST-VAL"
            tsc.interval = -1
            tsc.values = tsc_values
            tsc.times = times

            dss_file = filename[:-4] + ".dss"
            fid = HecDss.Open(os.path.join(folder_path, dss_file))
            fid.deletePathname(tsc.pathname)
            fid.put_ts(tsc)
            ts = fid.read_ts(tsc.pathname)
        fid.close()
