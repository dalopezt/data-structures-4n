import json
import os
import math
from manim import *

def read_graph():
    data = []
    adj_matrix = []
    with open("input.txt", "r") as f:
        data = f.readlines()
    for row in data:
        cells = row.split()
        adj_row = []
        for cell in cells:
            adj_row.append(int(cell))
        adj_matrix.append(adj_row)
    return adj_matrix

def find_root(parent, i):
    if parent[i] == i:
        return i
    return find_root(parent, parent[i])

def apply_union(parent, rank, node_a, node_b):
    node_a_root = find_root(parent, node_a)
    node_b_root = find_root(parent, node_b)
    if rank[node_a_root] < rank[node_b_root]:
        parent[node_a_root] = node_b_root
    elif rank[node_a_root] > rank[node_b_root]:
        parent[node_b_root] = node_a_root
    else:
        parent[node_b_root] = node_a_root
        rank[node_a_root] += 1

def get_edges_sorted(adj_matrix):
    w_edges = []
    for i in range(len(adj_matrix)):
        for j in range(len(adj_matrix)):
            if j < i:
                continue
            if adj_matrix[i][j] == 0:
                continue
            else:
                coords = (i, j)
                w_edges.append({"coords": coords, "weight": adj_matrix[i][j]})
    return sorted(w_edges, key = lambda item: item["weight"])
                

if __name__ == "__main__":
    adj_matrix = read_graph()
    n = len(adj_matrix)
    w_edges = get_edges_sorted(adj_matrix) 
    rank = []
    parent = []
    mst = []

    data = {}
    data["graph"] = adj_matrix
    data["dim"] = n
    
    i, e = 0, 0
    for node in range(n):
        parent.append(node)
        rank.append(0)

    while e < n - 1:
        w_edge = w_edges[i]
        i += 1
        node_a_root = find_root(parent, w_edge["coords"][0])
        node_b_root = find_root(parent, w_edge["coords"][1])
        if node_a_root != node_b_root:
            e += 1
            mst.append(w_edge["coords"])
            apply_union(parent, rank, node_a_root, node_b_root)

    data["mst"] = mst
    with open("frame.json", "w") as f:
        f.write(json.dumps(data))

    os.system("manim -pqh kruskal.py KruskalAnimation")

class KruskalAnimation(Scene):
    def construct(self):
        data = {}
        with open("frame.json", "r") as f:
            data = json.load(f)
        
        vertices = [i for i in range(data["dim"])]
        edges = set()
        i = 0
        j = 0
        for row in data["graph"]:
            for cell in row:
                if i < j:
                    j += 1
                    continue
                if cell == 0:
                    j += 1
                    continue
                coords = (i, j)
                edges.add(coords)
                j += 1
            i += 1
            j = 0
        
        mst = data["mst"]
        mst_edges = {tuple(pair):{"stroke_color": RED} for pair in mst}
        
        # Create the graph with labels
        g = Graph(vertices, edges, layout="circular", layout_scale=3, 
                  labels=True, edge_config=mst_edges)
        
        # Add graph to scene
        self.add(g)

        g.vertices[0].get_x()

        # Create a dictionary to store labels for each edge
        for edge in g.edges:
            weight = data["graph"][edge[0]][edge[1]]
            if [edge[0], edge[1]] in mst or [edge[1], edge[0]] in mst:
                label = Tex(str(weight), font_size=40, color=RED, stroke_width=1)
            else:
                label = Tex(str(weight), font_size=40, color=WHITE, stroke_width=1)
            edge_coords = self.calculate_label_coords(edge, g)
            label.move_to(np.array([edge_coords[0], edge_coords[1], 0]))
            self.add(label)

    def calculate_label_coords(self, edge, g):
        start_x = g.vertices[edge[0]].get_x()
        start_y = g.vertices[edge[0]].get_y()

        end_x = g.vertices[edge[1]].get_x()
        end_y = g.vertices[edge[1]].get_y()

        mid_x = (start_x+end_x)/2
        mid_y = (start_y+end_y)/2

        m_1 = (end_y - start_y)/(end_x - start_x)
        if m_1 == 0:
            return (mid_x, mid_y + 0.3)    
        m_2 = -1/m_1

        cos_theta = 1/math.sqrt(m_2*m_2 + 1)
        sin_theta = m_2/math.sqrt(m_2*m_2 + 1)

        label_x = mid_x + 0.3*cos_theta
        label_y = mid_y + 0.3*sin_theta
        return (label_x, label_y)
        