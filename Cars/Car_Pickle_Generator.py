import sys
import os
import pickle

# Get the absolute path to the parent directory
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Add the parent directory to the Python path
sys.path.append(parent_dir)

from GraphFindingAlgos import AStar_Car, Dijkstra

import osmnx as ox
from geopy.geocoders import Nominatim

pfile="..\\Data\\Pickle\\car_graph.pickle"

if os.path.exists(pfile):
    with open(pfile, "rb") as f:
        graph = pickle.load(f)
else:
    place_name = "Singapore"
    graph = ox.graph_from_place(place_name, network_type="drive")
    for node, data in graph.nodes(data=True):
        lon, lat = data['x'], data['y']
        graph.nodes[node]['pos'] = (lat, lon)

    with open(pfile, "wb") as f:
        pickle.dump(graph, f)

