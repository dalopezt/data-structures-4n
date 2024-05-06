from manim import *

class AVLAnimation(Scene):
    def construct(self):
        vertices = []
        edges = []
        root = None

        with open("avl.txt", "r") as f:
            root = eval(f.readline())
            vertices = eval(f.readline())
            edges_str = f.readlines()
            for edge_str in edges_str:
                edges.append(eval(edge_str))
    
        g = Graph(vertices, edges, layout="tree", labels=True, root_vertex=root)
        self.add(g)