import os, re

dir = "gpx_files\\"
# dir = "..\\runkeeper_data\\"

start_pattern = "<trk>"
end_pattern = "</trk>"
output_file = open('output_file.txt', 'a')

for file in os.listdir(dir):
	if file.endswith(".gpx"):
		file_path = dir + file
		opened_file = open(file_path, "r")
		lines = opened_file.readlines()
		for count, value in enumerate(lines):
			if start_pattern in value:
				start_line_number = count + 1
			if end_pattern in value:
				end_line_number = count + 1
		print(f"File: {file_path}\nStart line: {start_line_number}\nEnd line: {end_line_number}")
		# output_file.write(opened_file[opened_file.index(start_line_number):opened_file.index(end_line_number)])
		# output_file.write(str(opened_file))
		print(opened_file)
		opened_file.close()
		print()
