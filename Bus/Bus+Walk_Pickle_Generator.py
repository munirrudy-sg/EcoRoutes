import osmnx as ox
import networkx as nx
import folium
import pandas as pd
from geopy.distance import geodesic
import requests
import itertools
import pickle
import os

picklename="..\\Data\\Bus_Walk.pickle"
if os.path.exists(picklename):
    with open(picklename, "rb") as f:
        G_combined = pickle.load(f)
else:

    print("Setting up...")

    # Define the API endpoints
    bus_stops_url = "http://datamall2.mytransport.sg/ltaodataservice/BusStops"
    bus_routes_url = "http://datamall2.mytransport.sg/ltaodataservice/BusRoutes"

    # Define the headers for the API request
    headers = {
        "AccountKey": "nDR1RKXtRtOhzKfgXjcIyQ==",  # replace with your account key
        "accept": "application/json"
    }

    # Function to handle paginated responses
    def fetch_data(url):
        offset = 0
        records = []

        while True:
            print(f"Fetching data from {url} with offset = {offset}...")
            response = requests.get(f"{url}?$skip={offset}", headers=headers)
            data = response.json()

            records.extend(data['value'])

            if len(data['value']) < 500:
                break

            offset += 500

        return records

    print("Fetching data from APIs...")
    bus_stops_data = fetch_data(bus_stops_url)
    bus_routes_data = fetch_data(bus_routes_url)

    print("Processing data...")

    # Convert JSON to pandas DataFrame
    bus_stops = pd.json_normalize(bus_stops_data).set_index('BusStopCode')
    bus_routes = pd.json_normalize(bus_routes_data)

    # Check if bus stop exists in bus stop data
    bus_routes = bus_routes[bus_routes['BusStopCode'].isin(bus_stops.index)]

    # Add latitude and longitude to bus_routes from bus_stops
    bus_routes = bus_routes.join(bus_stops[['Latitude', 'Longitude']], on='BusStopCode')

    # Define your places
    place = "Singapore"

    WALKING_SPEED = 5
    BUS_SPEED = 30
    TRANSFER_PENALTY = 8  # Changed to 15 minutes to better reflect actual transfer times

    print("Building walking graph...")
    # Construct a graph for the walking paths
    G_walk = ox.graph_from_place(place, network_type='walk', simplify=False)
    G_walk = nx.MultiDiGraph(G_walk)

    # Convert walking time to walking distance for edges
    for u, v, k, data in G_walk.edges(data=True, keys=True):
        data['duration'] = data['length'] / (WALKING_SPEED * 1000 / 60)  # in minutes

    print("Adding bus stop nodes to the walking graph...")
    # Add nodes for the bus stops to the walking graph and save the OSMnx node ids
    bus_stop_node_ids = {}
    for index, stop in bus_stops.iterrows():
        node_id = ox.distance.nearest_nodes(G_walk, stop['Longitude'], stop['Latitude'])
        G_walk.add_node(node_id, y=stop['Latitude'], x=stop['Longitude'])
        bus_stop_node_ids[index] = node_id

    print("Building bus routes graph...")
    # Construct a graph for the bus routes
    G_bus = nx.MultiDiGraph()

    # Add nodes and edges to the bus graph
    for index, stop in bus_routes.iterrows():
        if stop['BusStopCode'] in bus_stop_node_ids:
            node_id = bus_stop_node_ids[stop['BusStopCode']]
            G_bus.add_node(node_id, y=stop['Latitude'], x=stop['Longitude'])

    for service in bus_routes['ServiceNo'].unique():
        for direction in [1, 2]:
            service_stops = bus_routes[
                (bus_routes['ServiceNo'] == service) & (bus_routes['Direction'] == direction)].sort_values('StopSequence')
            for (_, stop1), (_, stop2) in zip(service_stops.iterrows(), service_stops.iloc[1:].iterrows()):
                if stop1['BusStopCode'] in bus_stop_node_ids and stop2['BusStopCode'] in bus_stop_node_ids:
                    node1 = bus_stop_node_ids[stop1['BusStopCode']]
                    node2 = bus_stop_node_ids[stop2['BusStopCode']]
                    distance = stop2['Distance'] - stop1['Distance']  # Use the difference in the 'Distance' fields
                    time = distance / (BUS_SPEED * 1000 / 60)  # in minutes
                    G_bus.add_edge(node1, node2, duration=time)
    print(G_bus.nodes)

    print("Combining graphs...")
    # Construct a combined graph
    G_combined = nx.compose(G_walk, G_bus)

    # Add edges for getting on/off the bus
    for node in G_combined.nodes():
        if isinstance(node, tuple) and G_walk.has_node(node[0]):
            for neighbor in G_walk.neighbors(node[0]):
                G_combined.add_edge(node, neighbor, key=f"walk_{node}_{neighbor}",
                                    duration=G_walk[node[0]][neighbor][0]['duration'])
            for neighbor in G_bus.neighbors(node):
                G_combined.add_edge(node, neighbor, key=f"bus_{node}_{neighbor}",
                                    duration=G_bus[node][neighbor]['duration'] + TRANSFER_PENALTY)

    print("Intersection of walking and bus nodes:")
    intersection = set(G_walk.nodes()).intersection(set(G_bus.nodes()))
    print(intersection)

    with open(picklename, "wb") as f:
        pickle.dump(G_combined, f)



# Define your start and end coordinates
start_coord = (1.41738337,103.8329799)  # My house
end_coord = (1.350838988,103.848144)  # Bukit Timah Hill

# Find the nearest nodes
print("Finding nearest nodes...")
start_node = ox.distance.nearest_nodes(G_combined, start_coord[1], start_coord[0])
end_node = ox.distance.nearest_nodes(G_combined, end_coord[1], end_coord[0])

# Find the shortest path
print("Finding shortest path...")
shortest_path = nx.shortest_path(G_combined, start_node, end_node, weight='duration')

# Print a description of the route
print("Start at node", shortest_path[0])
for i in range(len(shortest_path) - 1):
    node1 = shortest_path[i]
    node2 = shortest_path[i + 1]
    edge_data = G_combined.get_edge_data(node1, node2)

    # Get the mode of transport for each edge
    modes = [str(k).split("_")[0] if isinstance(k, str) else "unknown" for k in edge_data.keys()]

    if 'bus' in modes:
        print(f"Take the bus from node {node1} to node {node2}")
    elif 'walk' in modes:
        print(f"Walk from node {node1} to node {node2}")
print("Arrive at node", shortest_path[-1])

# Convert the nodes into Lat and Long coordinates
shortest_path_coords = []
for node in shortest_path:
    point = G_combined.nodes[node]
    shortest_path_coords.append([point['y'], point['x']])

# Create a Map centered around the start point
print("Creating map...")
m = folium.Map(location=start_coord, zoom_start=14)

# Add a line to the map
folium.PolyLine(shortest_path_coords, color="red", weight=2.5, opacity=1).add_to(m)

# Save the map
print("Saving map...")
m.save("map.html")
print("Done.")