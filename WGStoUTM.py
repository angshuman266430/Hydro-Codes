import csv
import pyproj

def wgs84_to_utm15n(lat, lon):
    utm_crs = pyproj.Proj(proj='utm', zone=15, datum='WGS84')
    wgs84 = pyproj.Proj(proj='latlong', datum='WGS84')
    x, y = pyproj.transform(wgs84, utm_crs, lon, lat)
    return x, y

with open('coordinate.csv', 'r') as input_file:
    reader = csv.reader(input_file)
    header = next(reader)
    lat_index = header.index("latitude")
    lon_index = header.index("longitude")
    data = [row for row in reader]

output_data = []
for row in data:
    lat = float(row[lat_index])
    lon = float(row[lon_index])
    x, y = wgs84_to_utm15n(lat, lon)
    row.extend([x, y])
    output_data.append(row)

header.extend(["UTM_X", "UTM_Y"])
with open('output_coordinate.csv', 'w', newline='') as output_file:
    writer = csv.writer(output_file)
    writer.writerow(header)
    writer.writerows(output_data)
