# Python script to pull GPS and time from APM log files
#
# Samuel Vanderwaal, 2015
# Northern Embedded Solutions

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

    # Read input file and create output file
    inFile = open(filename)

    # Create an output file with the same name as input but with "CONVERTED"
    # added at the end
    outFileName = filename[:-4] + '-CONVERTED' + filename[-4:]

    # Open output file for writing
    outFile = open(outFileName, 'w')

    # Parse every line in the input file
    for line in inFile:
        # Split out the comma separated values into a Python list
        tempList = line.split(',')

        if "mavlink_global_position_int_t" in tempList:
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

            # Write values everytime we get a "global_position" packet
            outFile.write(timestamp + ',' + latitude + ',' +
                          longitude + ',' + str(relative_alt) + '\n')

    # Close files
    inFile.close()
    outFile.close()
