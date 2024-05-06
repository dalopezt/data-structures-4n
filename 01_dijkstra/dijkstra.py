import json
import os
from manim import *

INF = 1_000_000 # Extremly high number

def create_grid(rows:int, cols:int) -> list:
    grid = []
    for i in range(rows):
        row = []
        for j in range(cols):
            cell_coords = (j, i)

            # Add generic bounds
            cell_bounds = []

            # Top bounds
            if i > 0:
                cell_bounds.append((j, i-1))
                if j > 0:
                    cell_bounds.append((j-1, i-1))
                if j < cols-1:
                    cell_bounds.append((j+1, i-1))
            
            # Mid bounds
            if j > 0:
                cell_bounds.append((j-1, i))
            if j < cols-1:
                cell_bounds.append((j+1, i))

            # Bottom bounds
            if i < rows-1:
                cell_bounds.append((j, i+1))
                if j > 0:
                    cell_bounds.append((j-1, i+1))
                if j < cols-1:
                    cell_bounds.append((j+1, i+1))

            cell = {
                "coords": cell_coords,
                "bounds": cell_bounds
            }

            row.append(cell)
        grid.append(row)
    return grid

def issubset(subset:list, srcset:list) -> bool:
    for item in subset:
        if item not in srcset:
            return False
    return True

def get_cell(coords:tuple, grid:list) -> dict:
    return grid[coords[1]][coords[0]]

def get_neighbors_coords(coords:tuple, grid:list) -> list: 
    return get_cell(coords, grid)["bounds"]

def get_neighbors_cells(coords:tuple, grid:list) -> list:
    neighbors_coords = get_neighbors_coords(coords, grid)
    return [get_cell(i_coords, grid) for i_coords in neighbors_coords]

def check_dest_neighbors(dest_coords:tuple, grid:list, visited:list) -> bool:
    neighbors_cells = get_neighbors_cells(dest_coords, grid)
    return issubset(neighbors_cells, visited)

def get_entry_for_coords(table:list, coords:tuple) -> dict:
    for entry in table:
        if coords == entry["cell"]["coords"]:
            return entry

def get_path(table:list, dest_coords:tuple) -> list:
    path = []
    current_entry = get_entry_for_coords(table, dest_coords)
    path.append(dest_coords)
    while current_entry["prev_coords"] != None:
        current_entry = get_entry_for_coords(table, current_entry["prev_coords"])
        path.append(current_entry["cell"]["coords"])

    path.reverse()
    return path

def grid_for_frame(grid:list, visited_cells:list, current_cell_coords:tuple, src_cell_coords:tuple, dest_cell_coords:tuple) -> list:
    reduced_grid = []
    for row in grid:
        reduced_row = []
        for cell in row:
            cell_type = "unvisited"
            if cell["coords"] == current_cell_coords:
                cell_type = "current"
            elif cell["coords"] == src_cell_coords:
                cell_type = "src"
            elif cell["coords"] == dest_cell_coords:
                cell_type = "dest"
            elif cell in visited_cells:
                cell_type = "visited"
            elif len(cell["bounds"]) == 0: # wall
                cell_type = "wall"

            reduced_cell = {
                "coords": cell["coords"],
                "type": cell_type
            }

            reduced_row.append(reduced_cell)
        reduced_grid.append(reduced_row)
    return reduced_grid

def read_walls(rows:int, cols:int) -> list:
    walls = []
    nw = int(input("Set the number of walls: "))
    wall_x = -1
    wall_y = -1

    for i in range(nw):
        while wall_x not in range(cols) and wall_y not in range(rows):
            wall_x = int(input(f"Set the x coord of wall {i+1}: "))
            wall_y = int(input(f"Set the y coord of wall {i+1}: "))
        wall = (wall_x, wall_y)
        walls.append(wall)
        wall_x = -1
        wall_y = -1
        
    return walls

def set_walls(grid:list, walls:list) -> list:
    for coords in walls:
        # Remove from neighbors
        wall_neighbors_coords = get_neighbors_coords(coords, grid)

        for wall_neighbor_coords in wall_neighbors_coords:
            if coords in grid[wall_neighbor_coords[1]][wall_neighbor_coords[0]]["bounds"]:
                grid[wall_neighbor_coords[1]][wall_neighbor_coords[0]]["bounds"].remove(coords)

        # Remove itself bounds
        grid[coords[1]][coords[0]]["bounds"] = []
    
    return grid

def read_maze() -> list:
    maze_rows = []
    maze = []
    with open("input.txt", "r") as f:
        maze_rows = f.readlines()
    maze_rows.reverse()
    rows = len(maze_rows)
    cols = 0
    for row in maze_rows:
        cells = row.split()
        maze.append(cells)
        if cols == 0:
            cols = len(cells)
    
    grid = create_grid(rows, cols)
    walls = []
    src = tuple()
    dest = tuple()

    i = 0
    j = 0
    for i in range(rows):
        for j in range(cols):
            if maze[i][j] == "W": # Wall detected
                wall_coords = (j, i)
                walls.append(wall_coords)
            elif maze[i][j] == "S": # Source detected
                src = (j, i)
            elif maze[i][j] == "D": # Destination detected
                dest = (j, i)            
    
    grid = set_walls(grid, walls)
    return { "grid" : grid, "src": src, "dest": dest, "walls": walls }

def get_path_frame(grid:list, path:list, iteration:int, last_frame:list) -> list:
    reduced_grid = []
    for row in grid:
        reduced_row = []
        for cell in row:
            coords = cell["coords"]
            cell_type = last_frame[coords[1]][coords[0]]["type"]
            if cell_type == "current":
                cell_type = "visited"
            if coords in path and path.index(coords) <= iteration:
                cell_type = "path"
            reduced_cell = {
                "coords": coords,
                "type": cell_type
            }

            reduced_row.append(reduced_cell)
        reduced_grid.append(reduced_row)
    return reduced_grid

def generate_frames():
    # Frames and data table
    frames = []
    table = []

    # Create simple grid
    data = read_maze()

    grid = data["grid"]
    src_coords = data["src"]
    dest_coords = data["dest"]
    walls = data["walls"]
    dest_cell = get_cell(dest_coords, grid)

    # Get all unvisited cells with inf distance
    unvisited_cells = []
    for row in grid:
        for cell in row:
            if cell["coords"] in walls:
                continue
            unvisited_cells.append(cell)
            table.append({
                "cell" : cell,
                "min_weight": INF,
                "prev_coords": None
            })

    # Get none visited cells
    visited_cells = []
    current_cell = get_cell(src_coords, grid)
    
    for entry in table:
        if current_cell == entry["cell"]:
            entry["min_weight"] = 0

    # Execution while there're still nodes
    # while len(unvisited_cells) > 0:
    while not check_dest_neighbors(dest_coords, grid, visited_cells) or dest_cell in unvisited_cells:
        reduced_grid = grid_for_frame(grid, visited_cells, current_cell["coords"], src_coords, dest_coords)
        frames.append(reduced_grid)
        unvisited_cells.remove(current_cell)
        visited_cells.append(current_cell)

        # Get bounds
        cell_neighbors = get_neighbors_cells(current_cell["coords"], grid)

        # Remove visited nodes from options
        for cell_neighbor in cell_neighbors:
            if cell_neighbor in visited_cells:
                cell_neighbors.remove(cell_neighbor)
        
        # Get distance from src to current node
        partial_distance = 0
        for entry in table:
            if current_cell == entry["cell"]:
                partial_distance = entry["min_weight"]
                break

        # Explode valid bounds to see if there's something to update
        for cell_neighbor in cell_neighbors:
            distance = partial_distance + 1
            for entry in table:
                if entry["cell"] == cell_neighbor:
                    # If the new distance is less that the previous one, update
                    if distance < entry["min_weight"]:
                        entry["min_weight"] = distance
                        entry["prev_coords"] = current_cell["coords"]
        
        # Select the new node to be explored
        min_distance = INF
        new_cell = current_cell
        for entry in table:
            if entry["cell"] in visited_cells:
                continue
            if entry["min_weight"] < min_distance:
                min_distance = entry["min_weight"]
                new_cell = entry["cell"]
        current_cell = new_cell

    # Get path
    path = get_path(table, dest_coords)
    print("Path: ", path)

    # Generate path highlighting frames
    last_frame = frames[-1]
    for i in range(len(path)):
        frames.append(get_path_frame(grid, path, i, last_frame))

    with open("frames.json", "w") as f:
        f.write(json.dumps(frames))

class DijkstraAnimation(Scene):
    def get_color(self, cell_type):
        if cell_type == "src":
            return GREEN_C
        elif cell_type == "dest":
            return RED_C
        elif cell_type == "wall":
            return DARKER_GRAY
        elif cell_type == "unvisited":
            return GRAY
        elif cell_type == "visited":
            return PINK
        elif cell_type == "current":
            return YELLOW_C
        elif cell_type == "path":
            return BLUE_E

    def construct(self):
        frames = []
        with open("frames.json", "r") as f:
            frames = json.load(f)
        
        manim_frames = []
        for frame in frames:
            # Create a 10x10 grid of squares
            squares = VGroup()
            i = 0
            j = 0
            for row in frame:
                for cell in row:
                    square = Square(side_length=0.6, fill_color=self.get_color(cell["type"]), fill_opacity=1)
                    square.move_to(np.array([3*j/5.0 - 2.4, 3*i/5.0 - 2.4, 0]))
                    squares.add(square)
                    j += 1
                i += 1
                j = 0
            manim_frames.append(squares)
        
        manim_frame = manim_frames[0]
        self.add(manim_frame)
        for i in range(len(manim_frames)-1):
            if i == 0:
                continue
            self.wait(0.2)
            self.play(Transform(manim_frame, manim_frames[i+1]), run_time=0.2)
        self.wait(5)

if __name__ == "__main__":
    generate_frames()
    os.system("manim -pqh dijkstra.py DijkstraAnimation")