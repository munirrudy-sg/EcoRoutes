#comment
import math

from GraphFindingAlgos import minheap


def heuristic(lon1, lat1, lon2, lat2):
  #Haversine used as the heuristic
  radius = 6371
  lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])
  dlon = lon2 - lon1
  dlat = lat2 - lat1
  a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
  c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
  distance = radius * c

  return distance

def AStar(graph,start,end):

  co2 = 118
  end_lat = graph.nodes[end]["pos"][0]
  end_lon = graph.nodes[end]["pos"][1]

  heap = minheap.MinHeap()
  visited = set()
  distance_dict={}#Keeps track of the shortest path of vertex from the start node and heuristic cost
  prev_dict={}#Keeps track of the shortest previous node
  prev_dict[start]=None
  for node in graph.nodes:
    if node == start:
      distance_dict[node] = (0,0)
    else:
      distance_dict[node] = (float('inf'),float('inf'))


  heap.insert((start, 0,0))
  while not heap.check_empty():
    current_node, current_distance,est_dist = heap.get_root()

    if current_node == end:  #Reached the target node
      break
    if current_node in visited:
      continue

    visited.add(current_node)

    neighbors = graph.neighbors(current_node)
    for neighbor in neighbors:
      edge_data = graph.get_edge_data(current_node, neighbor)  # Get the edge data between current_node and neighbor
      edge_weight = (edge_data[0].get('length', float('inf')))/1000 #convert m to km.
      if neighbor in visited:
        continue


      node_data = graph.nodes[neighbor]["pos"]
      latitude,longitude=node_data[0],node_data[1]

      heu = heuristic(longitude, latitude, end_lon, end_lat)
      total_distance = distance_dict[current_node][0] + edge_weight + heu

      # Check if the total distance travelled is less than actual distance + heuristic of the neighbour node
      if total_distance < distance_dict[neighbor][0] + distance_dict[neighbor][1]:
        distance_dict[neighbor] = (total_distance-heu, heu)
        prev_dict[neighbor] = current_node
        heap.insert((neighbor, total_distance, heu))

  path = []
  current_node = end
  total_carbon = 0

  while current_node:
    path.append(current_node)
    curr_dist = distance_dict[current_node][0]
    current_node = prev_dict[current_node]
    if current_node is None:
      break
    curr_dist=curr_dist-distance_dict[current_node][0]
    total_carbon+=curr_dist*co2

  path.reverse()
  return (path,round(distance_dict[end][0],5),total_carbon)