########################################################################################################################
# Functions that are used for several stages
########################################################################################################################


def format_string(str):
    """Takes in a string and returns a formatted string that has had various elements replaced / modified"""

    str = str.replace("&", "and")
    str = str.replace(" Station", "")
    str = str.replace("Ham and City", "HandC")
    str = str.replace("_", " ")
    str = str.replace("Picadilly", "Piccadilly")
    str = str.strip()

    return str


########################################################################################################################
# Step 1 - Parse contents of stations.xml
########################################################################################################################


def parse_stations_xml_with_desc_field(filepath):
    """
    This function parses the stations.xml file, extracts the station name,
    description (address) and coordinates. The values are placed  into a nested dictionary
    in the format:
        station_dict = {station_name: {'description': '<desc>', 'coordinates': '<coord>}}'
    This function also removes encoded characters and the word "Station" from the station name,
    the completed station_dict is then returned.
    """

    import xml.etree.ElementTree as ET

    station_dict = {}  # A "list" of stations that will be returned

    # Import data from disk and set the root
    #tree = ET.parse('./data/stations.xml')
    tree = ET.parse(filepath)
    root = tree.getroot()[0]  # set root to be the first indent which is the <document> tag
    xml_ns = "{http://www.opengis.net/kml/2.2}"  # set xml namespace for use later
    # print("Root is:", tree.getroot()[0])

    # Iterate through the XML file
    for branch in root:
        station_details = {}  # Details of a single station
        # Filter out the <Placemark> tag im interested in
        if branch.tag == "{}Placemark".format(xml_ns):
            # For each Placemark (station) filter out station name, description (address) and coordinates
            # Items are key:value pairs are placed into a temp dict (station_details) for later processing
            # Items are also stripped of white/tab space and station name as the word "Station" removed
            # Tried using something like element.keys() but always returned blank values
            for item in branch:
                # print(item.tag, ":", item.text) #  print all values for testing
                if item.tag == "{}name".format(xml_ns):
                    # print("Station name:", item.text.strip())
                    # Remove the word Station and the character & then strip white space
                    # Could do with RegEx, will look at changing if time permits
                    station_name = item.text.replace("Station", "").replace("&", "and").strip()
                elif item.tag == "{}description".format(xml_ns):
                    # print("Description:", item.text.strip())
                    station_details["description"] = item.text.strip()
                for leaf in item:
                    # print("Coordinates:", leaf.text.strip())
                    station_details["coordinates"] = leaf.text.strip()
            # print("\n")
            station_dict[station_name] = station_details
            #break  # stop after first Placemark tag
    # print(station_dict)  # Print the dict for testing
    return station_dict


def parse_stations_xml(filepath):
    """
    This function parses the stations.xml file, extracts the station name
    and coordinates. The values are placed  into a nested dictionary
    in the format:
        station_dict = {<station_name>: <coordinates>}'
    This function also removes encoded characters and the word "Station" from the station name,
    the completed station_dict is then returned.
    """

    import xml.etree.ElementTree as ET

    station_dict = {}  # A "list" of stations that will be returned

    # Import data from disk and set the root
    tree = ET.parse(filepath)
    root = tree.getroot()[0]  # set root to be the first indent which is the <document> tag
    xml_ns = "{http://www.opengis.net/kml/2.2}"  # set xml namespace for use later
    # print("Root is:", tree.getroot()[0])

    # Iterate through the XML file
    for branch in root:
        station_name = ""  # Will store the name of a station
        station_coordinates = ""  # Will store the Coordinates for a station
        # Filter out the <Placemark> tag im interested in
        if branch.tag == "{}Placemark".format(xml_ns):
            # For each Placemark (station) filter out station name, description (address) and coordinates
            # Items are key:value pairs are placed into a temp dict (station_details) for later processing
            # Items are also stripped of white/tab space and station name as the word "Station" removed
            # Tried using something like element.keys() but always returned blank values
            for item in branch:
                # print(item.tag, ":", item.text) #  print all values for testing
                if item.tag == "{}name".format(xml_ns):
                    # print("Station name:", item.text.strip())
                    # Remove the word Station and the character & then strip white space
                    # Could do with RegEx, will look at changing if time permits
                    # station_name = item.text.replace("Station", "").replace("&", "and").strip()  # moved into a function for reusabality
                    station_name = format_string(item.text)
                for leaf in item:
                    # print("Coordinates:", leaf.text.strip())
                    station_coordinates = leaf.text.strip()
            # print("\n")
            station_dict[station_coordinates] = station_name
            #break  # stop after first Placemark tag
    # print(station_dict)  # Print the dict for testing
    return station_dict


########################################################################################################################
# Step 2 - Parse contents of JourneyTimes directory
########################################################################################################################


def step2_1_get_list_xml_files(directory):
    """
    This function will take in a directory path and return in a list xml file names
    found in the directory.
    Function is called from parse_journeytimes.
    """
    import os

    lst_xml_files = []

    # Iterate through the directory, if .xml file is found append to list then return the list
    for file in os.listdir(directory):
        if file.endswith(".xml"):
            lst_xml_files.append(file)
    return lst_xml_files


# def parse_journeytimes_into_dict(list_xml_files, path):
#     """
#     #######################################################################################################
#     FUNCTION WITHDRAWN AS NOT REALLY NEEDED, CODE MOVED INTO TASK2MAIN.PY INSTEAD BUT KEPT HERE FOR HISTORY
#     PURPOSES
#     #######################################################################################################
#
#     This function will take in the list of xml files and a directory path. Each XML file in the list
#     will then be passed to the function process_xml_file_dict() for separate processing. Returned value from
#     process_xml_file_dict() is then added to the dict_lines dictionary. After each file has been processed the
#     the dictionary dict_lines is returned.
#     """
#
#     dict_lines = {}  # Used to store the returned dicts from process_xml_file_dict()
#
#     for file in list_xml_files:
#         file_path = path + file
#         # print(file_path)
#         # add to dict_routes the returned dictionary from process_xml_file. file.split() is being used
#         # to split the file string on '.' to remove the .xml file extension
#         return_tuple = process_xml_file_into_dict(file_path)
#         # dict_lines[file.split('.')[0]] = process_xml_file_into_dict(file_path)  # Original calling line
#
#         break  # used for debugging to stop after only the first file
#     return dict_lines


def step2_2_process_xml_file(filename):
    """
    This function takes the full filename for a .XML file and parses it, placing all elements in a dictionary
    and then returning the dictionary to the calling function parse_journeytimes_dict()
    """
    import xml.etree.ElementTree as ET

    # Create empty dict and list for later use
    dict_station = {}  # Will store all parsed data in the format {from: {to: time}}
    list_station = []  # Will store only station names in order of the route, will act as an index list later on

    # Import data from disk and set the root
    tree = ET.parse(filename)
    root = tree.getroot()[1][0]  # set root to be the third indent which is the <Route id=...> tag
    # print(tree.getroot()[1][0])

    # Iterate through XML file from root to get contents of each element
    for element in root:
        # Format the element values using a function and assign to variables
        var_from = format_string(element[0].text)  # from station field
        var_to = format_string(element[1].text)  # to station field
        var_time = element[2].text  # journey time field

        dict_station[var_from] = {var_to: var_time}  # Format as nested dictionary
        #dict_station[var_from] = (var_to, var_time)  # Format as tuple in a dictionary

        list_station.append(var_from)
        list_station.append(var_to)

    # Remove duplicate station entries from the list
    for station in list_station:
        if list_station.count(station) != 1:  # count number of times station appears in the list, if not equal to 1
            list_station.remove(station)  # remove the station from the list

    # print(dict_station)
    # print(list_station)
    return dict_station, list_station


########################################################################################################################
# Step 3 - Process JourneyTimes data into a usable structure
########################################################################################################################


def step3_generate_journey_times(list_stations, dict_line):
    """
    Generates the journey times for a particular line and returns a dictionary of the results

    :param list_stations: A list of the stations on the line
    :param dict_line: A dictionary in the format of {from: {to: time}, ...}
    :return: A dictionary in the format {from: {to: time, ...} from: ...}
    """
    journey_complete = {}

    for from_station in list_stations:
        journey_complete[from_station] = {}
        for to_station in list_stations:
            # print("\n\nFrom Station: {}\nTo Station: {}".format(from_station, to_station))
            if list_stations.index(from_station) < list_stations.index(to_station):
                current_station = from_station
                total_time = 0
                # print("\t", dict_line.items())
                while current_station != to_station:
                    for key, val in dict_line[current_station].items():
                        current_station = key
                        interval_time = int(val)
                    # current_station, interval_time = dict_line[current_station]
                    # interval_time = int(interval_time)
                    #     print("\t[*] Calling at {} which is {} minute(s) from last stop".format(key, val))

                    total_time = total_time + interval_time
                # print("\t\tTotal Time: {}".format(total_time))

                journey_complete[from_station][to_station] = total_time
            else:
                # print("\t[!] NOT MATCHED - Skipped")
                pass

    for from_station in list_stations:
        for to_station in list_stations:
            if list_stations.index(from_station) > list_stations.index(to_station):
                journey_complete[from_station][to_station] = journey_complete[to_station][from_station]

    return journey_complete


########################################################################################################################
# Step 4 - Parse JSON file
########################################################################################################################


def parse_json(directory):
    import os
    import json
    import pprint

    list_json_files = []
    all_json_data = []

    # Get a list of JSON files in the specified directory and add to a list
    for file in os.listdir(directory):
        if file.endswith(".json"):
            list_json_files.append(file)
    # print(list_json_files)

    # For each file in list open the JOSN file and append the data to a list
    for file in list_json_files:
        with open("{}/{}".format(directory, file)) as json_data:
            data = json.load(json_data)
            for hop in data:
                all_json_data.append(hop)

    # pprint.pprint(all_json_files)
    # Sort the data in the list by order of arr_time
    all_json_data = sorted(all_json_data, key=lambda k: k['arr_time'])  # Lambda from google lol

    return all_json_data


########################################################################################################################
# Step 5 - Enrich data
########################################################################################################################


def step5_enrich_data(json_data, dict_stations, journey_times):
    import datetime  # Used for calculating the dep_time
    import pprint  # Used in debugging to make output easier to read

    enriched_json_data = []

    # print("Length of json data: {}".format(json_data.__len__()))

    for hop in json_data:
        # try:
        # Get values from hop and assign to variables
        arr_time = hop['arr_time']
        arr_time = datetime.datetime.strptime(arr_time, '%H:%M')  # <class 'datetime.datetime'>
        courier = hop['courier']
        from_coords = hop['from_coords']
        line = format_string(hop['line'])  # Run through format_string() to change & to and
        to_coords = hop['to_coords']
        # Calculate or look up additional information
        from_station = dict_stations[from_coords]
        to_station = dict_stations[to_coords]
        # Try to calculate journey and departure times using function, handle any errors in except
        try:
            enriched_json_data.append(step5_1_return_dep_journey_time(journey_times, line, from_station
                                                                      , to_station, arr_time, courier, from_coords
                                                                      , to_coords))
        # Handle any errors from the try that have a KeyError using various if/elif statements to correct
        # station names. Assumes the line is always correct
        except KeyError as e:
            # Change Edgware to Edgware Road if you are NOT on the Northern line
            if to_station == "Edgware":
                if line != "Northern":
                    to_station = "Edgware Road"
            elif from_station == "Edgware":
                if line != "Northern":
                    from_station = "Edgware Road"

            # Change White City to Wood Lane as both stations are in the same place
            elif to_station == "White City":
                to_station = "Wood Lane"
            elif from_station == "White City":
                from_station = "Wood Lane"

            # Correct name of station for Shepherds Bush on the H&C line
            elif to_station == "Shepherd's Bush Hammersmith and City":
                to_station = "Shepherd's Bush Market"
            elif from_station == "Shepherd's Bush Hammersmith and City":
                from_station = "Shepherd's Bush Market"

            # Correct name of Paddington on H&C line
            elif from_station == "Paddington":
                from_station = "Paddington (HandC Line)"

            # If everything above fails print error message and exit gracefully with error code 10
            else:
                print("\n[!] ERROR: KeyError on: {}"
                      "\n\tJSON DATA: {}"
                      "\n\tENRICHED DATA: From Station: {} | To Station: {}"
                      .format(e, hop, from_station, to_station))
                exit(10)

            # Using changed data from the above except, if, elif run the function to generate journey and dep times
            enriched_json_data.append(step5_1_return_dep_journey_time(journey_times, line, from_station
                                                                      , to_station, arr_time, courier
                                                                      , from_coords, to_coords))


    # pprint.pprint(enriched_json_data)
    # print("Length of enriched data: {}".format(enriched_json_data.__len__()))
    return enriched_json_data


def step5_1_return_dep_journey_time(journey_times, line, from_station, to_station
                                     , arr_time, courier, from_coords, to_coords):
    import datetime

    enriched_hop_data = {}

    journey_time = journey_times[line][from_station][to_station]
    dep_time = arr_time - datetime.timedelta(minutes=journey_time)
    # Print all the info nice and pretty like
    print("\n[*] New hop:\n\tArr Time: {}\n\tCourier: {}\n\tFrom Coords: {}\n\tLine: {}\n\tTo Coords: {}"
          "\n\t[*] Enriched data:\n\t\tFrom Station: {}\n\t\tTo Station: {}\n\t\tJourney Time: {}\n\t\tDep Time: {}"
          .format(arr_time, courier, from_coords, line, to_coords, from_station, to_station
                  , journey_time, dep_time))

    enriched_hop_data = {'arr_time': arr_time, 'courier': courier, 'from_coords': from_coords, 'line': line
                            , 'to_coords': to_coords, 'from_station': from_station, 'to_station': to_station
                            , 'journey_time': journey_time, 'dep_time': dep_time}

    return enriched_hop_data


########################################################################################################################
# Step 6 - Calculate the route of each package
########################################################################################################################


########################################################################################################################
# Step 7 - - Generate the output
########################################################################################################################
