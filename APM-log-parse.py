# Python script to pull GPS and time from APM log files
#
# Samuel Vanderwaal, 2015
# Northern Embedded Solutions

from sys import argv

# Accepts batches of files by running the command: 'python APM-log-parse.py *.csv'
for File in argv:
	filename = File
	
	coordArray = []

	# Define global variables for tracking values
	global timestamp
	global latitude
	global longitude
	global altitude

	# Read input file and create output file
	inFile = open(filename)

	# Create an output file with the same name as input but with "CONVERTED" added at the end
	outFileName = filename[:-4] + '-CONVERTED' + filename[-4:]

	# Open output file for writing
	outFile = open(outFileName,'w')

	# Parse every line in the input file
	for line in inFile:
		# Split out the comma separated values into a Python list
		tempList = line.split(',')
		
		# Check for 'lat' value
		if 'lat' in tempList:
			timestamp = tempList[0]							# Timestamp is always first value in a line
			j = tempList.index('lat')						# Get index of 'lat' marker
			variable = tempList[j+1]						# Latitude value is next value after 'lat' marker
			latitude = variable[:2] + '.' + variable[2:]	# Add decimal point to latitude value

		# Check for 'lon' value
		if 'lon' in tempList:
			k = tempList.index('lon')						# Get index of 'lon' marker
			variable1 = tempList[k+1]						# Longtidue value is next value after 'lon' marker
			longitude = variable1[:4] + '.' + variable1[4:]	# Add decimal point to longitude value

		# Barometric corrected altitude is in a different line than the lat and lon values
		# Look for 'mavlink_vfr_hud_t' line marker
		# Altitude value is six places away from marker
		if 'mavlink_vfr_hud_t' in tempList:
			l = tempList.index('mavlink_vfr_hud_t')
			altitude = tempList[l+6]

			# Now that we have all our values in global variables write them to the output file
			outFile.write(timestamp + ',' + latitude + ',' + longitude + ',' + altitude + '\n')
	
	# Close files		
	inFile.close()
	outFile.close()



