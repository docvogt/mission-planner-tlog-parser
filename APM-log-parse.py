# Python script to pull GPS and time from APM log files
#
# Samuel Vanderwaal, 2015
# Northern Embedded Solutions

import csv
import pytz
from datetime import datetime
from sys import argv

# Accepts batches of files by running the command:
# 'python APM-log-parse.py *.csv'
for File in argv[1:]:
    filename = File

    coordArray = []

    # Define global variables for tracking values
    timestamp = 0
    latitude = 0
    longitude = 0
    altitude = 0
    latRef = 'N/A'
    lonRef = 'N/A'
    rel_alt = '0'
    first_position = 0

    # Read input file and create output file
    inFile = open(filename)

    # Create an output file with the same name as input but with "CONVERTED"
    # added at the end
    outFileName = filename[:-4] + '-CONVERTED' + filename[-4:]

    # Open output files for writing

    with open(outFileName, 'w') as csvFile,\
            open(outFileName[0:-4] + '_GPGGA' + '.txt', 'w') as gpggaFile:

        csvwriter = csv.writer(csvFile, delimiter=',')
        gpggawriter = csv.writer(gpggaFile, delimiter=',')

        # Parse every line in the input file
        for line in inFile:
            # Split out the comma separated values into a Python list
            tempList = line.split(',')

            if "mavlink_global_position_int_t" in tempList:
                # Set first position flag so we know we know have data
                # in our variables
                first_position = 1

                # Timestamp is always first value in a line
                timestamp = tempList[0]
                # Get index of 'lat' marker
                j = tempList.index('lat')
                # Latitude value is next value after 'lat' marker
                lat_var = tempList[j+1]
                # Add decimal point to latitude value
                latitude = lat_var[:2] + '.' + lat_var[2:]

                # Get index of 'lon' marker
                k = tempList.index('lon')
                # Longitude value is next value after 'lon' marker
                lon_var = tempList[k+1]
                # Add decimal point to longitude value
                longitude = lon_var[:4] + '.' + lon_var[4:]

                # Get index of 'relative_alt' marker
                l = tempList.index('relative_alt')
                # Relative altitude value is next value after marker
                # Expressed as mm; convert to meters
                relative_alt = float(tempList[l+1]) / 1000.0
                rel_alt = str(relative_alt)

                # Write values everytime we get a "global_position" packet
                csvwriter.writerow([timestamp, latitude, longitude, rel_alt])

            if "mavlink_gps_raw_int_t" in tempList and first_position:
                # Create a local timezone with pytz
                local = pytz.timezone("America/Anchorage")
                # Convert local time stamp to naive datetime object
                naive_dt = datetime.strptime(tempList[0],
                                             "%Y-%m-%dT%H:%M:%S.%f")
                # Create aware local datetime object
                local_dt = local.localize(naive_dt)
                # Convert aware datetime object to UTC timezone
                utc_dt = local_dt.astimezone(pytz.utc)
                # Get the properly formatted time: e.g. 124231.235
                # for 12:42:31.235
                time = utc_dt.time().strftime("%H%M%S.%f")[:-3]

                lat = lat_var[:4] + '.' + lat_var[4:]
                lon = lon_var[:6] + '.' + lon_var[6:]

                if lat[0:1] == '-':
                    latRef = 'S'
                    lat = lat[1:]
                else:
                    latRef = 'N'

                if lon[0:1] == '-':
                    lonRef = 'W'
                    lon = lon[1:]
                else:
                    lonRef = 'E'

                # Get index of 'fix_type' marker
                m = tempList.index('fix_type')
                fix_type = int(tempList[m+1])

                # Mavlink fix is invalid (0-1), 2D (2), and 3D (3)
                # GPGGA fix quality is invalid (0), GPS (1) and RTK (2)
                # We assume only GPS or invalid values
                if fix_type > 1:
                    fixQ = 1
                else:
                    fixQ = 0

                n = tempList.index('satellites_visible')
                nSats = tempList[n+1]

                o = tempList.index('eph')
                HDOP = float(tempList[o+1])/100.0

                # No way currently to get geoid height above WGS84 ellipsoid
                height = ''

                # No need for actual chksum
                chksum = ''

                # Create GPGGA file to allow geotagging with exiftool
                gpggawriter.writerow(["$GPGGA", time, lat, latRef,
                                     lon, lonRef, fixQ, nSats, HDOP,
                                     rel_alt, 'M', height, 'M', chksum])

    # Close file
    inFile.close()
