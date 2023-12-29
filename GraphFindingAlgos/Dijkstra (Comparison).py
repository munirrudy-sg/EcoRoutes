#Template Dijkstra's Algorithm to be used for the comparison between Astar and Dijkstra's call

from GraphFindingAlgos import minheap


def dijkstra (graph,start,end):

  heap = minheap.MinHeap()
  visited = set()
  distance_dict={}#Keeps track of the current shortest distance of all vertices from the start node
  prev_dict={}#Keeps track of the shortest previous node
  prev_dict[start]=None
  for node in graph.nodes:
    if node == start:
      distance_dict[node] = 0
    else:
      distance_dict[node] = float('inf')


  heap.insert((start, 0))
  while not heap.check_empty():
    current_node, current_distance = heap.get_root()

    if current_node == end:  # dest
      break
    if current_node in visited:
      continue

    visited.add(current_node)

    neighbors = graph.neighbors(current_node)
    for neighbor in neighbors:
      edge_data = graph.get_edge_data(current_node, neighbor)  # Get the edge data between current_node and neighbor
      if not edge_data:
        continue

      edge_weight = edge_data.get('length', float('inf'))  # Use a default weight if 'length' attribute is missing
      distance = distance_dict[current_node] + edge_weight
      if distance < distance_dict[neighbor]:
        distance_dict[neighbor] = distance
        prev_dict[neighbor] = current_node
        heap.insert((neighbor, distance))

  path = []
  current_node = end

  while current_node:
    path.append(current_node)
    current_node = prev_dict[current_node]
    if (current_node == None):
      break

  path.reverse()
  return (path,round(distance_dict[end],5
                     ))