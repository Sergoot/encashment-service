from time import time
import networkx as nx
import osmnx as ox
import random
ox.config(use_cache=True, log_console=True)
G = ox.graph_from_place('Moscow, Russia', network_type='drive')
G = ox.add_edge_speeds(G)
G = ox.add_edge_travel_times(G)
start = time()
error_count = 0
for i in range(1000):
    try:
        src = random.choice(list(G))
        dst = random.choice(list(G))
        route = nx.shortest_path(G, src, dst, 'travel_time')
    except:
        print('путь не найден')
        error_count += 1
stop = time()
print('затраченное время: ', stop - start)
print('число ошибок: ', error_count)

route_map = ox.plot_route_folium(G, route)
route_map.save('lol.html')