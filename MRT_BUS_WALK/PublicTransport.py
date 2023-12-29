import networkx as nx
from geopy.geocoders import Nominatim
import osmnx as ox
import pickle
import os
import math
import sys
import time

# Get the absolute path to the parent directory
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Add the parent directory to the Python path
sys.path.append(parent_dir)

from GraphFindingAlgos import AStar_Eco
from GUI import Map as GUI

mrtGraph= "Data\\Pickle\\MRT_Graph.pickle"
buswalkGraph="Data\\Pickle\\Bus_Walk.pickle"
combinedGraph="Data\\Pickle\\Combined_Graph.pickle"
WALKING_SPEED=5


# This Function reduces the float values to 3 decimal places (Rounded down)
def round_coordinates(coord, precision=3):
    factor = 10 ** precision
    lat = math.floor(coord[0] * factor) / factor
    lon = math.floor(coord[1] * factor) / factor
    return lat, lon

def haversine(lon1, lat1, lon2, lat2):
    #Haversine used as the heuristic
    radius = 6371
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = radius * c

    return distance

# Reads the pickle files to get the graph, if pickle graph does not exist, it will create a new pickle graph.
if os.path.exists(combinedGraph):
    with open(combinedGraph, "rb") as f:
        combined_G = pickle.load(f)
    with open(buswalkGraph, "rb") as f:
        buswalk_G = pickle.load(f)
    with open(mrtGraph, "rb") as f:
            mrt_G = pickle.load(f)

else:
    #Create combined graph if does not exist
    if os.path.exists(mrtGraph) and os.path.exists(buswalkGraph):
        with open(mrtGraph, "rb") as f:
            mrt_G = pickle.load(f)
        with open(buswalkGraph, "rb") as f:
            buswalk_G = pickle.load(f)
        combined_G = nx.compose(mrt_G, buswalk_G)

    for node in mrt_G.nodes():
        if "STATION" in node:
            print(node)
            # MRT NODE
            lat, lon = mrt_G.nodes[node]['pos']
            nearest_walk_bus_node = ox.distance.nearest_nodes(buswalk_G, lon, lat)
            target_node = buswalk_G.nodes[nearest_walk_bus_node]
            target_lat, target_lon = target_node['y'], target_node['x']
            dist = haversine(lon, lat, target_lon, target_lat)
            time_needed = (dist / WALKING_SPEED) * 60
            combined_G.add_edge(node, nearest_walk_bus_node, key=f"walk_{node}_{nearest_walk_bus_node}",
                                duration=time_needed)
            combined_G.add_edge(nearest_walk_bus_node,node,key=f"walk_{nearest_walk_bus_node}_{node}", duration=time_needed)
            for n in combined_G.neighbors(node):
                print(n)

    bus_stops_dict = {}
    for nodes in combined_G.nodes():
        if isinstance(nodes, tuple):
            walking, busstop = nodes[:2]
            if (walking, busstop) not in bus_stops_dict:
                bus_stops_dict[(walking, busstop)] = []
                bus_stops_dict[(walking, busstop)].append(nodes)
            else:
                bus_stops_dict[(walking, busstop)].append(nodes)

    for key, values in bus_stops_dict.items():
        for i in range(len(values)):
            bus_node_A = values[i]
            for j in range(i + 1, len(values)):
                bus_node_B = values[j]
                combined_G.add_edge(bus_node_A, bus_node_B, key=f"walk_{bus_node_A}_{bus_node_B}", duration=0)
                combined_G.add_edge(bus_node_B, bus_node_A, key=f"walk_{bus_node_B}_{bus_node_A}", duration=0)

    with open(combinedGraph, "wb") as f:
        pickle.dump(combined_G, f)

    with open(combinedGraph, "wb") as f:
        pickle.dump(combined_G, f)



# This Function takes a start string and end string and will put in our A* algorithmn,
# to get a list of nodes in order. Then these nodes will be converted into [lattitude, longitude],
# which will then be put into our draw_map function to get our <iframe>.
def Route(start, end, mode):
    # Starts the time to calculate how fast our algorithm takes to compute.
    start_time = time.time()

    value1 = start
    value2 = end

    # If the start or end node is a Bus Stop which is in a tuple format,
    # it will just get the node id instead of the whole tuple.
    for nodes in combined_G.nodes():
        if isinstance(nodes,tuple):
            value = nodes[1]
            if value == value1:
                start = nodes
            elif value == value2:
                end = nodes

    print("Start is " + str(start))
    print("End is " + str(end))

    # This will push the nodes to our A* algorithmn to get the path.
    Eco=AStar_Eco.AStar(combined_G,start, end, mode)


    geolocator = Nominatim(user_agent="ecoroutes_test")
    coordinates = []
    mode_list = []
    location_list = []

    # Reduced coordinates and mode_list
    reduced_coordinates = []
    reduced_mode_list = []
    reduced_locations = []

    # Once the path_list is out, this section here will change the Node Id to,
    # [latitude, longitude] format.
    for node in Eco[0]:
        node_data = combined_G.nodes[node]

        if 'pos' in node_data:
            node_data['y'], node_data['x'] = node_data['pos']  # Extract 'pos' key and rename it as 'y' and 'x'

        if isinstance(node, tuple):
            node_data['mode'] = 'Bus'
        elif isinstance(node, str):
            node_data['mode'] = 'Train'
        elif isinstance(node, int):
            node_data['mode'] = 'Walk'

        latitude, longitude, mode = node_data['y'], node_data['x'], node_data['mode']
        location = geolocator.reverse((latitude, longitude), exactly_one=True)

        coordinates.append((latitude, longitude))
        location_list.append(location)
        mode_list.append(mode)

    print(type(location_list))
    print(type(location_list[0][0]))
    print(type(location_list[0][1]))

    # Extracting only the string portion from each tuple
    location_list = [location[0] for location in location_list]

    # Printing the list of location names
    print("LOCATION NAMES" + str(location_list))

    # Initialize variables to keep track of the previous mode and rounded coordinates
    prev_mode = None
    prev_rounded_coords = None

    # Manually iterating through the lists using indices
    for i in range(len(coordinates)):
        coord = coordinates[i]
        mode = mode_list[i]
        location = location_list[i]
        
        # Check if the mode is "Walk" and the next mode is also "Walk"
        if mode == "Walk" and (prev_mode == "Walk" or i == len(coordinates) - 1):
            # Round the coordinates down to 3 decimal places
            rounded_coords = round_coordinates(coord)
            
            # Check if the rounded coordinates are the same as the previous rounded coordinates
            if rounded_coords == prev_rounded_coords:
                # Skip adding the coordinate to the reduced list
                continue
            
            # Add the unique walking coordinate to the reduced list
            reduced_coordinates.append(coord)
            reduced_mode_list.append(mode)
            reduced_locations.append(location)
            
            # Update the previous mode and rounded coordinates
            prev_mode = mode
            prev_rounded_coords = rounded_coords
            
        else:
            # Add the non-walking coordinate to the reduced list
            reduced_coordinates.append(coord)
            reduced_mode_list.append(mode)
            reduced_locations.append(location)
            
            # Update the previous mode and rounded coordinates
            prev_mode = mode
            prev_rounded_coords = round_coordinates(coord)

    # Print the reduced lists
    # print(reduced_coordinates)
    # print(reduced_mode_list)

    print("REDUCED LOCATIONS" + str(reduced_locations))

    # Calculation of Computing Time.
    end_time = time.time()
    execution_time = end_time - start_time
    
    return (Eco[1], Eco[2], GUI.draw_map(reduced_coordinates, reduced_mode_list, reduced_locations), execution_time, reduced_locations)
