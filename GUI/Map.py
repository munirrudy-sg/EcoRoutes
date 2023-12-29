import folium
import os

# Get the directory path of the script
script_directory = os.path.dirname(os.path.abspath(__file__))
# Construct the absolute file path to the CSV file
mrt_csv = os.path.join(script_directory,'..', 'Data', 'MRT Stations.csv')

# This function has to take in a list of coordinates in path order following this format [lat, long].
# It also takes in a list of 'mode' to differentiate between the modes of transport.
# The modes of transport are 'Car' and 'Train' and 'Bus'
# Afterwards, it will return a <iframe> tag back
def draw_map(path_list, mode_list, location_list):

    # Creating a Folium Map of Singapore
    m = folium.Map(location=[1.3521, 103.8198], zoom_start=12)

    # Creating a list for path coordinates in order.
    path_coordinates = []
    path_coordinates = path_list.copy()

    # Differentiating the modes of transport and Icons
    icon_list = []
    for mode in mode_list:
        if mode == 'Car':
            icon_list.append('car')
        elif mode == 'Train':
            icon_list.append('train')
        elif mode == 'Bus':
            icon_list.append('bus')
        else:
            icon_list.append('person-walking')

    # Adding Markers into folium map
    for position in range(len(path_coordinates)):

        # Creating a special marker for the first and last station
        if position == 0:
            folium.Marker(
                location = path_coordinates[position],
                popup = location_list[position],
                icon = folium.Icon(color='green', icon = icon_list[position] , prefix='fa'),
                tooltip="Start!",
                ).add_to(m)
        elif position == len(path_coordinates) - 1:
            folium.Marker(
                location = path_coordinates[position],
                popup = location_list[position],
                icon = folium.Icon(color='red', icon = icon_list[position] , prefix='fa'),
                tooltip="End!",
                ).add_to(m)
        else:
            folium.Marker(
                location = path_coordinates[position],
                popup = location_list[position],
                icon = folium.Icon(color='blue', icon = icon_list[position], prefix='fa'),
                ).add_to(m)

    if path_coordinates:        
        # Adding a line to connect the markers
        folium.PolyLine(
            locations = path_coordinates,
            dash_array = '5', 
            color = "blue", 
            weight = 2.5, 
            opacity = 1).add_to(m)

    # Render m
    m.get_root().render()

    # Get the iframe of m
    iframe = m.get_root()._repr_html_()

    return iframe
