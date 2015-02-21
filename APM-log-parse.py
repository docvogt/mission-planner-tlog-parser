# Python script to pull GPS and time from APM log files
#
# Samuel Vanderwaal, 2015
#

from sys import argv

# Assign the argument vectors ('script' is title of the program and 'filename' will be the name of the file you want to open
for File in argv:
	filename = File
	
	coordArray = []

	global timestamp
	global latitude
	global longitude
	global altitude

	# Read input file and create output file
	inFile = open(filename)

	outFileName = filename[:-4] + '-CONVERTED' + filename[-4:]


	outFile = open(outFileName,'w')

	for line in inFile:
		tempList = line.split(',')
		
		if 'lat' in tempList:
			timestamp = tempList[0]
			j = tempList.index('lat')
			variable = tempList[j+1]
			latitude = variable[:2] + '.' + variable[2:]	# Add decimal point to latitude value

		if 'lon' in tempList:
			k = tempList.index('lon')
			variable1 = tempList[k+1]
			longitude = variable1[:4] + '.' + variable1[4:]	# Add decimal point to longitude value

		if 'mavlink_vfr_hud_t' in tempList:
			l = tempList.index('mavlink_vfr_hud_t')
			altitude = tempList[l+6]

			outFile.write(timestamp + ',' + latitude + ',' + longitude + ',' + altitude + '\n')
			
	inFile.close()
	outFile.close()



