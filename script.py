import os
import haversine as hs
from haversine import Unit
import gpxpy
import subprocess
import re
import csv

dir = "gpx_files_sample\\"
# dir = "gpx_files\\"
start_pattern = "<trk>"
end_pattern = "</trk>"
# create rides.gpx if it doesn't exist, clear contents if it does
open('rides.gpx', 'w').close()
# the file being constructed, which will contain <trk> elements from all .gpx files in gpx_files\
output_file = open('rides.gpx', 'w')
first_file = True
ride_count = 0
total_miles = 0.0
current_trail_name_list = []
floatmiles_list = []
# create all_rides.csv if it doesn't exist, clear contents if it does
open('all_rides.csv', 'w').close()

# dictionary of starting coordinates at each trailhead where keys = str, values = tuples, each tuple has 2 floats
trailhead_coordinates = {
			'Lincoln Park Trail': (40.919203, -74.300907),
			'Haverstraw Trail':  (41.182578, -73.951956),
			'Columbia Trail':    (40.817641, -74.724419),
			'Paulinskill Trail': (41.085281, -74.699790),
			'Paulinskill Trail2': (40.992136, -74.910228),
			'Highlands Trail': (40.401271, -73.984361),
			'Cedar Grove Trail': (40.858259, -74.226300),
			'Battlefield Trail': (40.523669, -74.492918),
			'Carol Place Trail': (40.936060, -74.226020),
			'Bluffton Trail': (32.252757, -80.924594),
			'Hilton Head Trail': (32.142620, -80.753349),
			'Mountainside Trail': (40.971169, -74.325388),
			'Franklin Lakes Trail': (40.990281, -74.197101),
			'Monksville Reservoir': (41.136845, -74.306884),
			'Sterling Forest Trail': (41.206681, -74.239067),
			'Cannonball Trail': (41.047944, -74.251842)}

# perform the following actions for each .gpx file in gpx_files\
for file in os.listdir(dir):
	if file.endswith(".gpx"):
		current_file_path = dir + file

		current_file = open(current_file_path, "r")
		lines = current_file.readlines()
		# when building rides.gpx, add the opening elements from the first file
		if (first_file):
			for i in lines[:8]:
				output_file.write(i)
			output_file.write("\n\n")
		first_file = False

		# find the line numbers where <trk> and </trk> are in each .gpx file
		for index, line_value in enumerate(lines):
			if start_pattern in line_value:
				start_line_number = index
			if end_pattern in line_value:
				end_line_number = index + 1
		# print("File: {0}\nStart line: {1}\nEnd line: {2}".format(current_file_path, start_line_number, end_line_number))

		# add the contents between <trk> and </trk> from each file to rides.gpx
		for i in lines[start_line_number:end_line_number]:
			output_file.write(i)
		output_file.write("\n\n")
		current_file.close()

		# get first coordinate from gpx file
		gpx_file = open(current_file_path, "r")
		gpx_data = gpxpy.parse(gpx_file)
		latitude_starting_point = gpx_data.tracks[0].segments[0].points[0].latitude
		longitude_starting_point = gpx_data.tracks[0].segments[0].points[0].longitude
		file_starting_coordinate = latitude_starting_point,longitude_starting_point

		# check distance between first coordinate in gpx file and each trailhead coordinate, return closest trailhead to starting point
		for trail_name, trail_coordinates in trailhead_coordinates.items():
			difference_in_distance = hs.haversine(file_starting_coordinate,trail_coordinates,unit=Unit.FEET)
			if difference_in_distance < 500:
				# print("Trail found in .gpx file is " + trail_name + ".")
				# print("Trail found in gpx file is {0}."format(trail_name))
				# print("First gpx coordinate is " + str(int(difference_in_distance)) + " feet away from " + trail_name + " trailhead.")
				# print("First gpx coordinate is {0} feet away from {1} trailhead."format(difference_in_distance, trail_name))
				ride_count += 1
				# print("Ride number: " + str(ride_count))
				# export trail_name for later use for adding trail name to gpx file <name> element
				current_trail_name = trail_name
		gpx_file.close()

		# edit gpx file <name> to be this format: <name><![CDATA[Lincoln Park Trail - 21.92 miles - Cycling 2-26-21]]></name>
		print(current_trail_name)
		# try:
		# 	lines = output_file.readlines()
		# except:
		# 	print()
		# print(lines[9])

		# add each current_trail_name (iteration) to a list (current_trail_name_list) for adding to csv later
		current_trail_name_list.append(current_trail_name)

		# get distance traveled in miles from gpx file using gpx-cmd-tools
		cmd = "python ..\gpx-cmd-tools\gpxinfo {0} --track --miles".format(current_file_path)
		cmd_output = subprocess.check_output(cmd)
		decoded_output = cmd_output.decode("utf-8")
		# print(decoded_output)
		listmilesline = re.findall('Length 3D.*miles', decoded_output) # return only the line with the amount of miles in it
		strmilesline = listmilesline[0] # convert list item to a str
		strmiles = strmilesline[11:16] # get just the number of miles in xx.xx format
		floatmiles = float(strmiles) # convert str to float
		# roundedfloatmiles = round(floatmiles, 4)
		print("Miles: {0}".format(floatmiles))
		print()
		total_miles = total_miles + floatmiles
		# print(total_miles)

		# add each floatmiles amount (iteration) to a list (floatmiles_list) for adding to csv later
		floatmiles_list.append(floatmiles)

# create csv file of all rides
# print(floatmiles_list)
# print (current_trail_name_list)
print()
print("Generating CSV file...")
for (ride, floatmile_count) in zip(current_trail_name_list, floatmiles_list):
	with open('all_rides.csv', mode='a') as all_rides:
		csv_writer = csv.writer(all_rides, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		csv_writer.writerow([ride, floatmile_count])

# add the closing element to rides.gpx
output_file.write("</gpx>")
output_file.close()

print("Done.")
print()
print("--------------------")
print("Total rides: " + str(ride_count))
print("Total miles: {0}".format(total_miles))