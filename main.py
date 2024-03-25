import networkx as nx
import matplotlib.pyplot as plt
from collections import namedtuple
from networkx.drawing.nx_agraph import write_dot, graphviz_layout
import string
def convert_node_id_to_name(id, max_room):
    name=""
    if id==max_room+1: return 'Goal'
    for i in range(int((id-1)/26)+1):
        name=name+list(string.ascii_uppercase)[(id-1)%26]
        id=id-26
    return name
condition=namedtuple("State","R L")
primary_graph = DAG_of_states= nx.DiGraph()
file = open("input.txt")
nodes, edges = file.readline().replace("\n", "").replace("\r", "").split(" ")
colors = file.readline().replace("\n", "").replace("\r", "").split(" ")
rooms_no = len(colors)
for i in range(rooms_no): primary_graph.add_node(i, color=colors[i])
primary_graph.add_node(rooms_no, color='Orange')
Rocket_start_node, Lucky_start_node = file.readline().replace("\n", "").replace("\r", "").split(" ")
Rocket_start_node = int(Rocket_start_node) - 1
Lucky_start_node = int(Lucky_start_node) - 1
for i in range(int(edges)):
    edge = file.readline().replace("\n", "").replace("\r", "").split(" ")
    edge_start=int(edge[0]) - 1
    edge_end=int(edge[1]) - 1
    edge_color=str(edge[2])
    primary_graph.add_edge(edge_start, edge_end, color=edge_color)
check_room=[[0 for i in range(rooms_no + 1)] for j in range(rooms_no + 1)]
def DAG(instant_condition):
    if check_room[instant_condition[0]][instant_condition[1]]!=0:
        return
    check_room[instant_condition[0]][instant_condition[1]]=instant_condition
    for left in list(primary_graph.adj.items())[instant_condition[0]][1]:
        if primary_graph.edges()[(instant_condition[0], left)]['color'] == primary_graph.nodes()[instant_condition[1]]['color']:
            next_condition = condition(left, instant_condition[1])
            DAG_of_states.add_node(next_condition)
            if check_room[next_condition[0]][next_condition[1]] == 0:
                DAG_of_states.add_edge(instant_condition, next_condition)
            DAG(next_condition)
    for right in list(primary_graph.adj.items())[instant_condition[1]][1]:
        if primary_graph.edges()[(instant_condition[1], right)]['color']==primary_graph.nodes()[instant_condition[0]]['color']:
            next_condition=condition(instant_condition[0],right)
            DAG_of_states.add_node(next_condition)
            if check_room[next_condition[0]][next_condition[1]]==0:
                DAG_of_states.add_edge(instant_condition, next_condition)
            DAG(next_condition)
DAG(condition(0,1))
tree=list(nx.bfs_predecessors(DAG_of_states, condition(R=0, L=1)))
def moving_turn(state_list,s):
    if state_list[0][0]==state_list[1][0]:
        return('L ' + str(state_list[0][1]+1) +'\t// Lucky moves to ' + convert_node_id_to_name(state_list[0][1] + 1, s))
    else:
        return('R ' + str(state_list[0][0]+1) +'\t// Rocket moves to ' + convert_node_id_to_name(state_list[0][0] + 1, s))
solve = "No"
path = []
for i in range(len(tree)):
    if solve=="No" and tree[-i - 1][0][0] or tree[-i - 1][0][1] == rooms_no:
        solve = "Yes"
        path.append(moving_turn(tree[-i - 1], rooms_no))
        index = i
    if solve == "Yes" and tree[-i - 1][0] == tree[-index - 1][1]:
        index = i
        path.append(moving_turn(tree[-i - 1], rooms_no))
if solve=="Yes":
    for i in range(len(path)):
        print(path[-i - 1])
else:
    print("There isn't any solution for this problem")

