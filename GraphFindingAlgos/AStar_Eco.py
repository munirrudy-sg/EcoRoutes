import math

from GraphFindingAlgos import minheap
"""This functions calculates the fastest path to the given destination from the given source, it is calculated
using the A* algorithm which uses an additional heuristic in the consideration of the 'best' node to use next"""

def eco_friendliness(time,transportation,mode="Eco"):
  eco_dict = {"MRT": 18.05, "bus": 36.5,"walk":0}#Carbon emission per minute
  if mode=="Fastest":
    i1=1.0
    i2=0
  elif mode=="Balanced":
    i1=0.8
    i2=0.2
  elif mode=="Eco":
    i1=0.5
    i2=0.5
  result=i1*time+i2*(time*eco_dict[transportation])
  return result

def est_time(lon1, lat1, lon2, lat2, transportation):
  #Haversine used as the heuristic to calculate straight line distance divided by travelling speed to get an overestimate
  speed={"walk":5,"MRT":83.33,"bus":30}
  radius = 6371
  lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])
  dlon = lon2 - lon1
  dlat = lat2 - lat1
  a = math.sin(dlat / 2)**  2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
  c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
  distance = radius * c

  time_taken=(distance/speed[transportation])*60
  return time_taken

def AStar(graph,start,end,mode):
  eco_dict = {"MRT": 18.05, "bus": 36.5,"walk":0}  # Carbon emission per minute
  end_values=graph.nodes[end]

  if "pos" in end_values:
    node_data = end_values["pos"]
    end_lat, end_lon = node_data[0], node_data[1]
  else:
    end_lat, end_lon = end_values['y'], end_values['x']


  heap = minheap.MinHeap()
  visited = set()
  time_dict={}
  prev_dict={}
  prev_dict[start]=None
  #time_dict will contain the time taken to get to one place, the type of transportation, eco friendly+time calculation
  for node in graph.nodes:
    if node == start:
      time_dict[node] = (0,"Null",0)
    else:
      time_dict[node] = (float('inf'),"Null",float('inf'))

  #heap will have node no,eco friendly+time calculation,only time
  heap.insert((start,0,0))
  while not heap.check_empty():
    current_node = heap.get_root()[0]
    if current_node=="HAW PAR VILLA MRT STATION":
      print("ASD")
    if current_node == end:  #Reached the target node
      break
    if current_node in visited:
      continue
    visited.add(current_node)

    neighbors = graph.neighbors(current_node)

    for neighbor in neighbors:
      if neighbor in visited:
        continue

      edge_data = graph.get_edge_data(current_node, neighbor)  # Get the edge data between current_node and neighbor
      if 0 in edge_data:

        temp=edge_data[0]

        if "key" in temp:
          #means mrt
          edge_weight = temp.get('duration', float('inf'))
          edge_transportation = temp.get('key', '')[:3]
        else:
          temp_list=list(temp)
          if len(temp_list)==1:
            #bus edge
            edge_key=list(edge_data.keys())[-1]
            edge_transportation=edge_key[:3]
            edge_weight=edge_data[edge_key]['duration']
          else:
            #walking edge
            edge_transportation="walk"
            edge_weight=temp['duration']
      else:
        #Walking to MRT edge
        edge_key=next(iter(edge_data))
        edge_transportation=edge_key[:4]
        edge_weight=edge_data[edge_key]['duration']


      # total_time = time_dict[current_node][0] + edge_weight
      # neighbour_time=time_dict[neighbor][0]
      #heu = heuristic(edge_weight, edge_transportation,mode=mode)

      #total_value = time_dict[current_node][0]+edge_weight+heu
      node_values=graph.nodes[neighbor]
      if "pos" in node_values:
        node_data = graph.nodes[neighbor]["pos"]
        latitude, longitude = node_data[0], node_data[1]
      else:
        latitude,longitude=node_values['y'],node_values['x']

      heu2 = est_time(longitude, latitude, end_lon, end_lat, edge_transportation)
      heu = eco_friendliness(edge_weight+heu2, edge_transportation, mode=mode)

      total_value=time_dict[current_node][0]+edge_weight+heu2+heu
      neighbor_value = time_dict[neighbor][2]
      if edge_transportation=="bus":
        total_value-=15 #Change edge transportation from
      if total_value < neighbor_value:
        time_dict[neighbor] = (total_value-heu2-heu, edge_transportation, total_value)
        prev_dict[neighbor] = current_node
        heap.insert((neighbor, total_value, edge_weight))

  path = []
  current_node = end
  total_carbon=0

  while current_node:
    path.append(current_node)
    curr_time=time_dict[current_node][0]
    curr_transportation=time_dict[current_node][1]
    current_node = prev_dict[current_node]
    if current_node is None:
      break
    curr_time=curr_time-time_dict[current_node][0]
    total_carbon+=curr_time*eco_dict[curr_transportation]


  path.reverse()
  return (path,round(time_dict[end][0],5),total_carbon)
