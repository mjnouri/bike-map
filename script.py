import os

dir = "gpx_files\\"
start_pattern = "<trk>"
end_pattern = "</trk>"
# create rides.gpx if it doesn't exist, clear contents if it does
open('rides.gpx', 'w').close()
output_file = open('rides.gpx', 'a')
first_file = True

for file in os.listdir(dir):
	if file.endswith(".gpx"):
		current_file_path = dir + file
		current_file = open(current_file_path, "r")
		lines = current_file.readlines()
		if (first_file):
			for i in lines[:8]:
				output_file.write(i)
			output_file.write("\n\n")
		first_file = False
		for index, line_value in enumerate(lines):
			if start_pattern in line_value:
				start_line_number = index
			if end_pattern in line_value:
				end_line_number = index + 1
		print(f"File: {current_file_path}\nStart line: {start_line_number}\nEnd line: {end_line_number}\n")
		for i in lines[start_line_number:end_line_number]:
			output_file.write(i)
		output_file.write("\n\n")

output_file.write("</gpx>")
output_file.close()