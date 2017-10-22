import Task2Functions
import pprint

root_path = "./Data"

########################################################################################################################
# Step 1 - Parse contents of stations.xml
########################################################################################################################

step1_path = root_path + '/Stations/stations.xml'
# print(step1_path)
# Get list of stations and assign to a dictionary
dict_stations = Task2Functions.parse_stations_xml(step1_path)
# print("Station Dictionary:\t {}".format(dict_stations))


########################################################################################################################
# Step 2 - Parse contents of JourneyTimes directory
# Step 3 - Process JourneyTimes data into a usable structure
########################################################################################################################


# 2.1 - Get list of .xml files in a directory
step2_path = root_path + "/JourneyTimes/"
list_xml_files = Task2Functions.step2_1_get_list_xml_files(step2_path)

# 2.2 - Get route details for all tube lines, returned as a single dictionary for later processing
# dict_journeytimes = Task2Functions.parse_journeytimes_into_dict(list_xml_files, path) #  !! Function withdrawn !!
# print("JourneyTimes Dictionary:\t {}".format(dict_journeytimes))

dict_all_lines = {}  # Stores a dictionary of lines in format {from: {to: time}
dict_lines_journey_times = {}  # Stores a dictionary of journey times in format {from: {to: time, to: time, ...}}
temp_list_stations = []  # Stores a list of stations on line in route order

for file in list_xml_files:
    file_path = step2_path + file  # Create full path to a .xml file to pass to process_xml_file()
    # print(file_path)
    file = file.split('.')[0]  # Removes the .xml part of the file by splitting on . and keeping first part of file
    file = Task2Functions.format_string(file)
    # Run function and assign result to temp_returned_tuple, then assign the returned values to required dictionaries
    temp_returned_tuple = Task2Functions.step2_2_process_xml_file(file_path)
    dict_all_lines[file] = temp_returned_tuple[0]
    temp_list_stations = temp_returned_tuple[1]
    # print(dict_all_lines[file])
    # print(temp_list_stations)

    # 3.1 - Generate journey times
    dict_lines_journey_times[file] = Task2Functions.step3_generate_journey_times(temp_list_stations
                                                                                 , dict_all_lines[file])
    # print(dict_lines_journey_times[file])
    # break  # used for debugging to stop after the first file
# print(dict_lines_journey_times.keys())
# print(dict_lines_journey_times['Bakerloo'])
# print(dict_all_lines)
# pprint.pprint(dict_lines_journey_times)


########################################################################################################################
# Step 4 - Parse JSON file
########################################################################################################################


step4_path = root_path + '/JSON/'
# Get JSON data using function and place into a list. Format is data will be [{<json hop data>}, {...}]
json_data = Task2Functions.parse_json(step4_path)
# print(json_data)
# pprint.pprint(json_data)


########################################################################################################################
# Step 5 - Enrich data
########################################################################################################################

print("Length of json data: {}".format(json_data.__len__()))

enriched_json_data = Task2Functions.step5_enrich_data(json_data, dict_stations, dict_lines_journey_times)

print("\nLength of json data: {}".format(json_data.__len__()))
print("Length of enriched data: {}".format(enriched_json_data.__len__()))


########################################################################################################################
# Step 6 - Calculate the route of each package
########################################################################################################################


########################################################################################################################
# Step 7 - - Generate the output
########################################################################################################################
