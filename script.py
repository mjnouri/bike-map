import os

dir = "gpx_files\\"
start_pattern = "<trk>"
end_pattern = "</trk>"
# create rides.gpx if it doesn't exist, clear contents if it does
open('rides.gpx', 'w').close()
# the file being constructed, which will contain <trk> elements from all .gpx files in gpx_files\
output_file = open('rides.gpx', 'a')
first_file = True

#  perform the following actions for each .gpx file in gpx_files\
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
		print(f"File: {current_file_path}\nStart line: {start_line_number}\nEnd line: {end_line_number}\n")
		# add the contents between <trk> and </trk> from each file to rides.gpx
		for i in lines[start_line_number:end_line_number]:
			output_file.write(i)
		output_file.write("\n\n")
		# next step - geolocate first lat/lon point of each .gpx file to get name of trail
			# in a map variable, store each trail name and starting point coordinate
			# store first coordinate in .gpx file to variable
			# if variable coordinate is within 1000' from any starting point in the map variable
			# output matching trail name from map to csv file column

# add the closing element to rides.gpx
output_file.write("</gpx>")
output_file.close()