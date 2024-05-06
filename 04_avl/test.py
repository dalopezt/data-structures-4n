from manim import *

class TreeLayout(Scene):
    def construct(self):
        graph = Graph(
            [1, 2, 3, 4, 5, 6, 7],
            [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7)],
            layout="tree",
            root_vertex=1,
            labels=True
        )
        self.add(graph)